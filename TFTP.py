#-*- coding: utf-8 -*-
import socket
import os
import sys
from pathlib import Path, PurePosixPath
from threading import Thread

BLOCK_SIZE = 512
BUFFER = 65536
SERVER_PORT = 69
CLIENT_ACP_PORT = 1512
SERVER_REC_PORT = 1600

# TFTP操作符
class TFTPOpcode:
    RRQ = b'\x00\x01'
    WRQ = b'\x00\x02'
    DATA = b'\x00\x03'
    ACK = b'\x00\x04'
    ERROR = b'\x00\x05'

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
class TFTP:
    def __init__(self, addr, port):
        self.socks = socket(AF_INET, SOCK_DGRAM)
        self.ADDR = addr
        self.PORT = port

