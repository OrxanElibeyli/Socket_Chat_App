######################################################
#  -----------------------------------------------   #
# | dst addr | len of outgoing message | message |   #
# ------------------------------------------------   #
######################################################

import socket
import pdb





SERVER = '192.168.3.71'
PORT = 4224

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER,PORT))

print('*connected to the server')


#000.000.000.000  15
#192.168.0.1

def format_IP(str):
    IP = str

    if(len(str)<15):
        while(len(str)<15):
            str = str + '*'

        IP = str

    return IP

def format_len(message):
    leng = len(message)
    if(leng<10):
        leng = leng + '*'

    return leng
        


dst = input("enter destination:")
dst = format_IP(dst)

while(True):

    message = input('enter message:') 

    sock.sendall(dst.encode('utf-8')) #send first header (destination)
    sock.sendall(format_len(message).encode('utf-8'))  #send second header (len of outgoing message)
    sock.sendall(message.encode('utf-8')) #send third header (message itself)
