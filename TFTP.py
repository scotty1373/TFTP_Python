# -*- coding: utf-8 -*-
import socket
import os
import sys
from pathlib import Path, PurePosixPath
from threading import Thread

BLOCK_SIZE = 512
BUFFER = 65536
CLIENT_ACP_PORT = 1512
SERVER_REC_PORT = 1600
SERVER_ADDR = '0.0.0.0'
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
    ACCESS_DENY = 1
    DISK_FULL = 2
    FILE_EXISTS = 3
    UNKNOWN_OP = 4

    __MESSAGES = {
        FILE_NOT_FOUND: 'File not found',
        ACCESS_DENY: 'Access deny',
        DISK_FULL: 'Disk full or allocation exceeded',
        FILE_EXISTS: 'File already exists',
        UNKNOWN_OP: 'Invalid operation(Unknow)'
    }

    # return error message with errorcode
    @classmethod
    def get_message(self, error_code: int) -> str:
        return self.__MESSAGES[error_code]

def socks_bind(s, ACC_NUM: int, addr: str, port: int) -> None:
    try:
        s.bind((addr, port))
        s.listen(ACC_NUM)
        print("Socket Bind Connected!!!")
    except socket.error as e:
        print("Socket Bind Error At %s:%s " % (addr, port))
        sys.exit()


# TFTP初始化
class TFTP_Server:
    # def __init__(self, addr, port):
    #     self.socks = socket(AF_INET, SOCK_DGRAM)
    #     self.ADDR = addr
    #     self.PORT = port
    def server_init(self, addr=SERVER_ADDR, port=SERVER_PORT):
        s_socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # socket closed重启服务
        s_socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s_socks.bind((addr, port))
            s_socks.listen(ACC_NUM)
            print("Server Socket Bind Successfully!!!")
        except socket.error as e:
            print("Socket Bind Error At %s:%s " % (addr, port))
            print(e)
            sys.exit()

        print('*' * 5 + 'TFTP Server Start Up!!!' + '*' * 5)
        print('Waiting client to connect')
        while True:
            data, clientinfo = s_socks.recvfrom(1024)
            print('Receive remote client require ')
            opcode = data[0:2]
            file_name = data[2:-7]
            mode = data[-6:-1]

            client_port = clientinfo[1]

            if mode == b'octet':
                #
                if opcode == TFTPOpcode.WRQ:
                    pass

                elif opcode == TFTPOpcode.ACK:
                    pass


        s_socks.close()

