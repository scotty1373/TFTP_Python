#-*- coding: utf-8 -*-
import sys
import os
import socket
import TFTP

server_ip = sys.argv[1]
file_path = sys.argv[2]
mode = sys.argv[3]

def client_get(server_ip: str, file_path: str):
    # get模式，第一次发送数据初始化
    rrq_data = TFTP.TFTPOpcode.RRQ + file_path.encode(encoding='utf-8') + b'0' + b'octet' + b'0'
    socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 初始连接服务器，端口69
    # socket自动绑定一个接收端口，可以不bind固定端口
    socks.sendto(rrq_data, (server_ip, TFTP.SERVER_PORT))   
        
    # 文件序号
    fileNum = 0
    last_block = False
    downloadFlag = True
    
    file_name = file_path.split('\\')[-1]
    fp = open(file_name, 'wb')
    fp.seek(0,0)
    
    while True:
        # maximal 516 byte 
        recv_data, serverinfo = socks.recvfrom(1024)
        print('server port:' + serverinfo[1])
        
        Opcode = recv_data[0:2]
        Block_Num = recv_data[2:4].decode(encoding='utf-8')
        data = recv_data[2].decode(encoding='utf-8')
        
        if Opcode == TFTP.TFTPOpcode.DATA and fileNum == Block_Num:
            fileNum += 1
            
            if fileNum == 65536:
                fileNum = 0
    
            # 下载检测，文件是否存在
            downloadFlag = True
            # final block check
            if len(data) != 512:
                last_block = True
                fp.write(data)
                socks.sendto((TFTP.TFTPOpcode.ACK + fileNum.encode(encoding='utf-8')), (server_ip, serverinfo[1]))
                print('File written successfully!')
                print('Bytes upload: %d' %((Block_Num*512) + len(data)))
                break
            
            fp.write(data)
            # client ack
            socks.sendto((TFTP.TFTPOpcode.ACK + fileNum.encode(encoding='utf-8')), (server_ip, serverinfo[1]))
            
        elif Opcode == TFTP.TFTPOpcode.ERROR:
            print(TFTP.TFTPError_code.get(Opcode))
            print('file get error, check server file path and try again')
            downloadFlag = False
            break
        
        # 接收文件块错误，请求重传
        elif fileNum != Block_Num:
            socks.sendto((TFTP.TFTPOpcode.RACK + fileNum.encode(encoding='utf-8')), (server_ip, serverinfo[1]))

    if downloadFlag:
        fp.close()
    else:
        os.unlink(file_name)
        sys.exit()
        

def client_put(server_ip: str, file_path: str):
    # WRQ require C2S
    wrq_data = TFTP.TFTPOpcode.WRQ + file_path.encode(encoding='utf-8') + b'0' + b'octet' + b'0'
    socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 初始连接服务器，端口69
    # socket自动绑定一个接收端口，可以不bind固定端口
    socks.sendto(send_data, (server_ip, TFTP.SERVER_PORT))   
        
    # 文件序号
    fileNum = 0
    last_block = False
    downloadFlag = True
    
    file_name = file_path.split('\\')[-1]
    fp = open(file_path, 'rb')
    # seerve ack receive
    ack_recv, remoteinfo = socks.recvfrom(1024)
    print('remote data transmission port: ' + remoteinfo[1])
    
    ts_Port = remoteinfo[1]
    Opcode = ack_recv[:2]
    Block_Num = ack_recv[2:4].decode(encoding='utf-8')
    
    if Opcode == TFTP.TFTPOpcode.ERROR:
        print('tftp server eerror')
        sys.exit()
    
    while True:
        file_buff = fp.read(512)
        transmit_buffer = TFTP.TFTPOpcode.DATA + fileNum.encode(encoding='utf-8') + file_buff

        if fileNum == 65536:
            fileNum = 0
        # maximal 516 byte 
        socks.sendto(transmit_buffer, (server_ip, ts_Port))
        
        ack_recv_iter, remoteinfo = socks.recvfrom(1024)
             
        Opcode = ack_recv_iter[0:2]
        Block_Num = ack_recv_iter[2:4].decode(encoding='utf-8')
        
        if Opcode == TFTP.TFTPOpcode.ERROR:
            print('Data upload error')  
            sys.exit()
        
        if len(file_buff) < 512 or fileNum != Block_Num:
            print('File:%s upload successfully!!!' %file_name)
            print('Bytes upload: %d' %((Block_Num-1)*512 + len(file_buff)))
            break
   
        fileNum += 1
        
    if downloadFlag:
        fp.close()
    else:
        os.unlink(file_name)


if __name__ == "__main__":
    if mode == '1':
        client_get(server_ip, file_path)
               
    elif mode == '2':
        client_put(server_ip, file_path)

        
            
                
                
                
            
            
            
            