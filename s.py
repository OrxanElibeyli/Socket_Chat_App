import socket

HOST='localhost'
PORT=5000

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen()


while(True):
    conn, addr = s.accept()
    dst=conn.recv(15)
    print('dst: ',dst)
    msg_len=conn.recv(2)
    print('msg: ',msg_len)

    msg=conn.recv(int(msg_len.decode('utf-8')))
    print(msg)


    # while(True):    
    #     msg=conn.recv(2)
    #     if not msg:
    #         break

    #     print(msg)