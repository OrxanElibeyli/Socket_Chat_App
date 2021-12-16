import socket
import threading


clients = []

HOST = ''
PORT = 4224


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()



def receive_mesages(conn):
    while(True):
        message = conn.recv(10)
        print(message)
    

while(True):
    conn, addr = sock.accept()
    print('connection ---> ', conn)
    print('address --->',addr)

    t1 = threading.Thread(target=receive_mesages, args=(conn,))
    t1.start()
    

