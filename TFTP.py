#-*- coding: utf-8 -*-
import socket
import os
import sys
from pathlib import Path, PurePosixPath
from threading import Thread

BLOCK_SIZE = 512
BUFFER = 65536
CLIENT_ACP_PORT = 1512
SERVER_REC_PORT = 1600
SERVER_ADDR = 0.0.0.0
SERVER_PORT = 69
ACC_NUM = 10

# TFTP操作符
class TFTPOpcode:
    RRQ = b'\x00\x01'
    WRQ = b'\x00\x02'
    DATA = b'\x00\x03'
    ACK = b'\x00\x04'
    ERROR = b'\x00\x05'
    RACK = b'\x00\x06'

# TFTP错误代码
class TFTPError_code:
    FILE_NOT_FOUND = 0
    ACESS_DENY = 1
    DISK_FULL = 2
    FILE_EXIST = 3
    UNKNOW_OP = 4

    __MESSAGES = {
        FILE_NOT_FOUND: 'File not found',
        ACCESS_DENY: 'Access deny',
        DISK_FULL: 'Disk full or allocation exceeded',
        FILE_EXISTS: 'File already exists',
        UNKNOW_OP:'Invalid operation(Unknow)'
    }
    
    @classmethod
    def get_message(self, error_code: int) -> str:
    '''return error message with errorcode'''
        return self.__MESSAGES[error_code]

# TFTP初始化
class TFTP_Server:
    # def __init__(self, addr, port):
    #     self.socks = socket(AF_INET, SOCK_DGRAM)
    #     self.ADDR = addr
    #     self.PORT = port
    def server_init(self, addr=SERVER_ADDR, port=SERVER_PORT):
        ssocks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # socket closed重启服务
        webserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_bind(ssocks, ACC_NUM)
        print('*'* 5 + 'tftp server start up!!!' + '*'* 5)
        print('Waiting client to connect')
        while True:
            data, clientinfo = ssocks.recvfrom(1024)
            Opcode = data[0:2]
            file_name = data[2:-7]
            mode = data[-6:-1]
            if mode == b'octet'
            # 
                if Opcode == TFTPOpcode.WRQ:
                    pass

                elif Opcode == TFTPOpcode.ACK:
                    pass

                elif Opcode == TFTPOpcode.RRQ:
                    pass

                elif Opcode == TFTPOpcode.DATA:
                    pass
                
                elif Opcode == TFTPOpcode.ERROR:
                    pass
        ssocks.close()

        
        
        









def socks_bind(s, ACC_NUM):
    try:
        s.bind((addr, port))
        s.listen(ACC_NUM)
        print("Socket Bind Connected!!!")
    except socket.error as e:
        print("Socket Bind Error At %s:%s " %(url, port))
        sys.exit()