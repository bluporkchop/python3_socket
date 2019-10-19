#!coding=utf-8

import threading
import socket
import struct

def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # port設為9001
        s.bind(('140.113.24.2', 9001))
        # 設置監聽數量
        s.listen(10)
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    print ('Waiting connection...')
 
    while 1:
        # 等待請求並接受(程式會停留在這一旦收到連線請求即開啟接受數據的線程)
        conn, addr = s.accept()
        # 接收數據
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()
 
def deal_data(conn, addr):
    print ('Accept new connection from {0}'.format(addr))
    # conn.settimeout(500)
    # 收到請求後的回覆
    conn.send('Hi, Welcome to the server!'.encode('utf-8'))
 
    while 1:
        # 申請相同大小的空間存放發送來的文件名與文件大小信息
        fileinfo_size = struct.calcsize('128sl')
        # 接收檔案名稱與檔案大小信息
        buf = conn.recv(fileinfo_size)
        # 判斷是否接收到檔案標頭信息
        if buf:
            # 獲取檔案名和檔案大小
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.strip(b'\00')
            fn = fn.decode()
            print ('file new name is {0}, filesize if {1}'.format(str(fn),filesize))
 
            recvd_size = 0  # 定義已接收檔案的大小
            # 儲存在該腳本所在目錄下面
            fp = open('./' + str(fn), 'wb')
            print ('start receiving...')
            
            # 將批次傳輸的二進位流依次寫入到檔案
            while not recvd_size == filesize:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                    fp.write(data)
            fp.close()
            print ('end receive...')
        # 傳輸結束斷開連線
        conn.close()
        break
        
if __name__ == "__main__":
    socket_service()
    