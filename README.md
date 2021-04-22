# TFTP 服务器python简单实现

### 脚本简介

通过socket库实现TFTP客户端文件上传下载，支持多用户同时上传下载

### 启用服务端

> Linux服务端用sudo运行，Linux在1024以下端口调用需要权限
>

调用多线程库_thread, 必须使用python3

`sudo python3 server.py`

### 本地上传（PUT）

`python client.py <--server_ip> <--local_file_path> <2 --mode>`

### 本地下载（GET）

`python client.py <--server_ip> <--server_file_path> <1 --mode>`

> Windows下路径需要将反斜线转成正斜线，Unix和Linux可识别
>

`path = path.replace('\\', '/')`