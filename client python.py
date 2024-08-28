import socket
import struct

def client_program():
    # 創建 UDP 客戶端套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = b"hello,Server"
    message1 = b"new word"
    dirct = 2
    hour = 5
    min_ = 10
    second = 2.03
    count = 2
    lat = [20,30]
    long = [100,125]
    byte = struct.pack("!IIIfI",dirct,hour,min_,second,count)
    for i in range(count):
        byte = byte + struct.pack("!dd",lat[i],long[i])        

    server_address = ('127.0.0.1', 10005)
    client_address = ('127.0.0.1',10006)
    client_socket.bind(client_address)
    client_socket.sendto(message,server_address)
    data, server = client_socket.recvfrom(1024)
    print(f"data:{data.decode()} from {server}")
    client_socket.sendto(byte,server_address)
if __name__ == "__main__":
    client_program()
