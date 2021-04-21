# -*- coding: utf-8 -*-
import sys
import os
import socket
import time

import TFTP

server_ip = sys.argv[1]
file_path = sys.argv[2]
mode = sys.argv[3]
# server_ip = '127.0.0.1'
# file_path = 'C:\\Users\\spsim\\Desktop\\data_proc\\train_data.csv'
# mode = '2'
# mode = '1' receive file from remote server
# mode = '2' upload file from remote server


def client_get(server_ip: str, file_path: str):
    # get模式，第一次发送数据初始化
    print('File Receive initializing!')
    rrq_data = TFTP.TFTPOpcode.RRQ + file_path.encode(encoding='utf-8') + b'0' + b'octet' + b'0'
    socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 初始连接服务器，端口69
    # socket自动绑定一个接收端口，可以不bind固定端口
    socks.sendto(rrq_data, (server_ip, TFTP.SERVER_PORT))
    print('RRQ request sending! Waiting for response', end='')
    for i in range(3): time.sleep(1); print('.', end='', flush=True)
    print('')
    # 文件序号
    fileNum = 0
    last_block = False

    file_name = file_path.split('\\')[-1]
    fp = open(file_name, 'wb')
    fp.seek(0, 0)
    print('*' * 5 + 'Connection established!!!' + '*' * 5)
    while True:
        # maximal 516 byte
        # 接受远端服务器udp端口 
        recv_data, serverinfo = socks.recvfrom(1024)

        Opcode = recv_data[0:2]
        Block_Num = recv_data[2:7].decode(encoding='utf-8').lstrip('0')
        data = recv_data[7:]

        fileNum += 1
        if fileNum == 65536:
            fileNum = 1

        fp.write(data)

        if Opcode == TFTP.TFTPOpcode.DATA and str(fileNum) == Block_Num:
            if len(data) < 512:
                socks.sendto((TFTP.TFTPOpcode.ACK + str(fileNum).zfill(5).encode(encoding='utf-8')),
                             (server_ip, serverinfo[1]))
                print('File written successfully!')
                print('Bytes received: %d' % (((fileNum - 1) * 512) + len(data)))
                socks.close()
                sys.exit()
            socks.sendto((TFTP.TFTPOpcode.ACK + str(fileNum).zfill(5).encode(encoding='utf-8')),
                         (server_ip, serverinfo[1]))

        elif Opcode == TFTP.TFTPOpcode.ERROR:
            print(TFTP.TFTPError_code.get_message(Opcode))
            print('file get error, check server file path and try again')
            socks.close()
            sys.exit()

        # 接收文件块错误，请求重传
        elif fileNum != Block_Num:
            socks.sendto((TFTP.TFTPOpcode.ERROR + fileNum.encode(encoding='utf-8')),
                         (server_ip, serverinfo[1]))
            print('Block missing!!!')
            print('*' * 5 + 'Socket closed' + '*' * 5)


def client_put(server_ip: str, file_path: str):
    # WRQ require C2S
    wrq_data = TFTP.TFTPOpcode.WRQ + file_path.encode(encoding='utf-8') + b'0' + b'octet' + b'0'
    socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 初始连接服务器，端口69
    # socket自动绑定一个接收端口，可以不bind固定端口
    socks.sendto(wrq_data, (server_ip, TFTP.SERVER_PORT))

    # 文件序号
    fileNum = 1
    last_block = False
    downloadFlag = True

    file_name = file_path.split('\\')[-1]

    fp = open(file_path, 'rb')
    print('Require send %s to server' % file_name)
    print('WRQ request sending! Waiting for response', end='')
    for i in range(3): time.sleep(1); print('.', end='', flush=True)

    # server ack receive
    ack_recv, remoteinfo = socks.recvfrom(1024)
    print('*' * 5 + 'Connection established' + '*' * 5)
    print('remote data transmission port: ' + str(remoteinfo[1]))
    # remote port to transmit data
    ts_Port = remoteinfo[1]
    Opcode = ack_recv[:2]
    Block_Num = ack_recv[2:].decode(encoding='utf-8').lstrip('0')

    while True:
        file_buff = fp.read(512)

        transmit_buffer = TFTP.TFTPOpcode.DATA + str(fileNum).zfill(5).encode(encoding='utf-8') + file_buff

        # maximal 516 byte 
        socks.sendto(transmit_buffer, (server_ip, ts_Port))

        fileNum += 1
        if fileNum == 65536:
            fileNum = 1

        if Opcode == TFTP.TFTPOpcode.ERROR:
            print('Block missing, check your network env, keep connection stable!')
            sys.exit()

        if len(file_buff) < 512:
            print('File:%s upload successfully!!!' % file_name)
            print('Bytes upload: %d' % ((int(Block_Num) - 1) * 512 + len(file_buff)))
            print('client: %s, port: %s ' % (remoteinfo[0], remoteinfo[1]), end='')
            print('Terminate socket connection')
            socks.close()
            sys.exit()
        # 接收放在最后，不然传完后会一直等待远程响应
        ack_recv_iter, remoteinfo = socks.recvfrom(1024)

        Opcode = ack_recv_iter[0:2]
        Block_Num = ack_recv_iter[2:].decode(encoding='utf-8').lstrip('0')


if __name__ == "__main__":
    if mode == '1':
        client_get(server_ip, file_path)

    elif mode == '2':
        client_put(server_ip, file_path)
