import socket

HOST='localhost'
PORT=5000
destination='127.0.0.1'

tags=['</dst>','<msg>','</msg>','<end>']

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))


def add_tags_to_message(msg):
    return destination +tags[0] + tags[1] +msg + tags[2] + tags[3]


while(True):
    msg=input()
    s.sendall(add_tags_to_message(msg).encode('utf-8'))


