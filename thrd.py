import socket

HOST='localhost'
PORT=5000

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((HOST,PORT))

dst=input("enter destination:")
if(len(dst)<15):
    while(len(dst)<15):
        dst=dst + '*'

s.sendall(dst.encode('utf-8'))

while(True):
    msg=input()
    lenght=len(msg)
    if(lenght<=99):
        if(lenght<10):
            len_as_str='0' + str(lenght)
        else:
            len_as_str=str(lenght)    
    s.sendall(len_as_str.encode('utf-8'))
    s.sendall(msg.encode('utf-8'))

