#!coding=utf-8
 
import socket
import os
import sys
import struct

def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('140.113.24.2', 9001))
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    print (s.recv(1024))

    #輸入檔案路徑
    filepath = input('please input file path: ')
    # 判斷是否為檔案
    if os.path.isfile(filepath):
        # 定義檔案訊息。128s表示檔案名為128bytes長，l表示一個int或log文件類型，在此為檔案大小
        fileinfo_size = struct.calcsize('128sl')
        # 定義檔案head訊息，包含檔案名稱和檔案大小
        fhead = struct.pack('128sl', os.path.basename(filepath).encode('utf-8'), os.stat(filepath).st_size)
        # 送出檔案名稱與檔案大小
        s.send(fhead)

        # 將傳送檔案以二進位的形式分多次上傳至伺服器
        fp = open(filepath, 'rb')
        while 1:
            data = fp.read(1024)
            if not data:
                print ('{0} file send over...'.format(os.path.basename(filepath)))
                break
            s.send(data)
        # 關閉目前套接字對象
        s.close()
        
if __name__ == '__main__':
    socket_client()