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
    # WRQ SERVER RESPONSE
    @staticmethod
    def server_recv(addr: str, port: str, path: str) -> None:
        server_local_file_name = str(path).split('\\')[-1]
        fp_recv = open(server_local_file_name, 'wb')
        local_Block_num = 0
        s2c_socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s2c_ack = TFTPOpcode.ACK + str(local_Block_num).zfill(5).encode(encoding='utf-8')
        s2c_socks.sendto(s2c_ack, (addr, port))
        # recv block num match

        while True:
            c2s_data, clientinfo = s2c_socks.recvfrom(1024)
            opcode = c2s_data[:2]
            Block_Num = c2s_data[2:7].decode(encoding='utf-8').lstrip('0')
            recv_buffer = c2s_data[7:]

            local_Block_num += 1
            if local_Block_num == 65536:
                local_Block_num = 1

            if opcode == TFTPOpcode.DATA and str(local_Block_num) == Block_Num:
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
                s2c_ack = TFTPOpcode.ACK + str(local_Block_num).encode(encoding='utf-8')
                s2c_socks.sendto(s2c_ack, clientinfo)

            elif local_Block_num != Block_Num:
                s2c_ack = TFTPOpcode.ERROR + str(local_Block_num).encode(encoding='utf-8')
                s2c_socks.sendto(s2c_ack, clientinfo)
                print('Block missing!!!')
                os.unlink(server_local_file_name)
                s2c_socks.close()
                sys.exit()

    @staticmethod
    def server_upload(addr: str, port: str, path: str) -> None:
        with open(path, 'rb') as fp_upload:
            local_Block_num = 1
            s2c_socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            upload_buffer = fp_upload.read(512)
            upload_mess = TFTPOpcode.DATA + str(local_Block_num).zfill(5).encode(encoding='utf-8') + upload_buffer
            s2c_socks.sendto(upload_mess, (addr, port))

            c2s_data, clieninfo = s2c_socks.recvfrom(1024)
            # client ack receive
            opcode = c2s_data[:2]
            Block_Num = c2s_data[2:4].decode(encoding='utf-8').lstrip('0')

            while True:
                upload_buffer = fp_upload.read(512)

                local_Block_num += 1
                if local_Block_num == 65536:
                    local_Block_num = 1

                upload_mess = TFTPOpcode.DATA + str(local_Block_num).zfill(5).encode(encoding='utf-8') + upload_buffer
                s2c_socks.sendto(upload_mess, (addr, port))
                if opcode == TFTPOpcode.ACK:

                    if len(upload_buffer) < 512:
                        print('File upload completed!')
                        print('Bytes uploaded: %d' % ((local_Block_num - 1) * 512 + len(upload_buffer)))
                        # fp_recv.seek(0, 2)
                        # bytes_Total = fp_recv.tell()
                        # if bytes_Total == (int(Block_Num) - 1) * 512 + len(recv_buffer)):
                        #     print('Bytes receive matched')
                        fp_upload.close()
                        s2c_socks.close()
                        sys.exit()

                elif local_Block_num != Block_Num:
                    s2c_error_send = TFTPOpcode.ERROR + local_Block_num.encode(encoding='utf-8')
                    s2c_socks.sendto(s2c_error_send, clieninfo)
                    print('Block missing!!!')
                    s2c_socks.close()
                    sys.exit()

                c2s_data, clieninfo = s2c_socks.recvfrom(1024)
                # client ack receive
                opcode = c2s_data[:2]
                Block_Num = c2s_data[2:7].decode(encoding='utf-8').lstrip('0')

    def toup(self):
        pass













            
            
        
        

