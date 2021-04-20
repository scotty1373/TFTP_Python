# -*- coding: utf-8 -*-
import socket
import os
import sys
from pathlib import Path, PurePosixPath


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

    # Return error message with errorcode
    @classmethod
    def get_message(self, error_code: int) -> str:
        return self.__MESSAGES[error_code]


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
                    pass

                elif opcode == TFTPOpcode.RRQ:
                    pass
        s_socks.close()
    
    # WRQ SERVER RESPONSE
    def server_recv(self, addr: str, port: int, path: str) -> None:
        fp_recv = open(path, 'wb')
        local_Block_num = 0
        s2c_socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s2c_ack = TFTPOpcode.ACK + local_Block_num.encode(encoding='utf-8')
        s2c_socks.sendto(s2c_ack, (addr, port))
        while True:
            c2s_data, clientinfo = s2c_socks.recvfrom(1024)
            opcode = c2s_data[:2]
            Block_Num = c2s_data[2:4].decode(encoding='utf-8')
            recv_buffer = c2s_data[4:]

            if opcode == TFTPOpcode.DATA and local_Block_num == Block_Num:
                fp_recv.write(recv_buffer)
                if len(recv_buffer) < 512:
                    print('File receive completed!')
                    print('Bytes receive: %d' % ((int(Block_Num) - 1) * 512 + len(recv_buffer)))
                    # fp_recv.seek(0, 2)
                    # bytes_Total = fp_recv.tell()
                    # if bytes_Total == (int(Block_Num) - 1) * 512 + len(recv_buffer)):
                    #     print('Bytes receive matched')
                    fp_recv.close()
                    s2c_socks.close()
                    sys.exit()
                local_Block_num += 1
                if local_Block_num == 65536:
                    local_Block_num = 0
                s2c_ack = TFTPOpcode.ACK + local_Block_num.encode(encoding='utf-8')
            elif local_Block_num != Block_Num:
                s2c_ack = TFTPOpcode.ERROR + local_Block_num.encode(encoding='utf-8')
                print('Block missing!!!')
                os.unlink(path)
                s2c_socks.close()
                sys.exit()

    def server_upload(self, addr: str, port: str, path: str) -> None:
        fp_recv = open(path, 'rb')
        local_Block_num = 0
        s2c_socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            c2s_data, clientinfo = s2c_socks.recvfrom(1024)
            opcode = c2s_data[:2]
            Block_Num = c2s_data[2:4].decode(encoding='utf-8')
            recv_buffer = c2s_data[4:]

            if opcode == TFTPOpcode.DATA and local_Block_num == Block_Num:
                fp_recv.read(BLOCK_SIZE)
                if len(recv_buffer) < 512:
                    print('File receive completed!')
                    print('Bytes receive: %d' % ((int(Block_Num) - 1) * 512 + len(recv_buffer)))
                    # fp_recv.seek(0, 2)
                    # bytes_Total = fp_recv.tell()
                    # if bytes_Total == (int(Block_Num) - 1) * 512 + len(recv_buffer)):
                    #     print('Bytes receive matched')
                    fp_recv.close()
                    s2c_socks.close()
                    sys.exit()
                local_Block_num += 1
                if local_Block_num == 65536:
                    local_Block_num = 0
                s2c_ack = TFTPOpcode.ACK + local_Block_num.encode(encoding='utf-8')
            elif local_Block_num != Block_Num:
                s2c_ack = TFTPOpcode.ERROR + local_Block_num.encode(encoding='utf-8')
                print('Block missing!!!')
                os.unlink(path)
                s2c_socks.close()
                sys.exit()
    def init(self):
        pass













            
            
        
        

