######################################################
#  -----------------------------------------------   #
# | dst addr | len of incoming message | message |   #
# ------------------------------------------------   #
######################################################

import socket
import threading


clients = []

HOST = ''
PORT = 4224

LEN_OF_IP = 15



sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()


#this function is used by threat for receiving messages from client
def receive_mesages(conn):
    while(True):
        #first header of TCP
        dest_addr = conn.recv(LEN_OF_IP)

        #second header of TCP
        len_of_incoming_message = conn.recv(2)

        #third header of TCP
        message = conn.recv(len_of_incoming_message)

        package = conn + " | " + dest_addr + " | " + message


        message_file = open("messages.txt","w+")
        message_file.write(package)
        message_file.close()
    

while(True):
    conn, addr = sock.accept()
    print('connection ---> ', conn)
    print('address --->',addr)

    t1 = threading.Thread(target=receive_mesages, args=(conn,))
    t1.start()
    

