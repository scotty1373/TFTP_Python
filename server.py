# -*- coding: utf-8 -*-
import sys
import os
import socket
import threading
import TFTP




if __name__ == '__main__':
    s_socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # socket closed重启服务
    s_socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s_socks.bind((TFTP.SERVER_ADDR, TFTP.SERVER_PORT))
        # s_socks.listen(TFTP.ACC_NUM)
        print("Server Socket Bind Successfully!!!")
    except socket.error as e:
        print("Socket Bind Error At %s:%s " % (TFTP.SERVER_ADDR, TFTP.SERVER_PORT))
        print(e)
        sys.exit()

    print('*' * 5 + 'TFTP Server Start Up!!!' + '*' * 5)
    print('Waiting client to connect')
    while True:
        # First time receive from client
        data, clientinfo = s_socks.recvfrom(1024)
        print('Receive remote client require ')
        opcode = data[0:2]
        file_name = data[2:-7]
        mode = data[-6:-1]
        # Remote client port & ip ------- next stage communication
        client_port = clientinfo[1]
        client_ip = clientinfo[0]
        # Confirm tftp transmit mode
        if mode == b'octet':
            if opcode == TFTPOpcode.WRQ:
                threading._start_new_thread(TFTP.TFTP_Server.server_recv, (client_ip, client_port, file_name, ))

            elif opcode == TFTPOpcode.RRQ:
                threading.start_new_thread(TFTP.TFTP_Server.server_upload, (client_ip, client_port, file_name, )
                
    s_socks.close()
