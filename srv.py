#receive header
######################################################
#  -----------------------------------------------   #
# | receiver | len of incoming message | message |   #
# ------------------------------------------------   #
######################################################

#send header
######################################################
#  -----------------------------------------------   #
# | sender | len of outgoing message | message   |   #
# ------------------------------------------------   #
######################################################

import socket
import threading
import time
import logging


HOST = ''
PORT = 4224
LEN_OF_IP = 15

established_connections = []
packets = []



logging.basicConfig(filename='logg.txt',filemode='a',format='%(asctime)s - %(levelname)s - %(message)s',level=logging.DEBUG)



sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    sock.bind((HOST, PORT))
    sock.listen()
except Exception as e:
    logging.error(str(e))
    logging.info('some error occured during creating socket.\nquiting...')
    quit()
    


#this function is used by threat for receiving messages from client
def receive_messages(conn):
    while(True):
        #first header of packet (receiver IP)
        receiver = conn.recv(LEN_OF_IP).decode('utf-8')
        receiver = receiver.replace('*','')

        #second header of packet (len of incomming message)
        len_of_incoming_message = conn.recv(2).decode('utf-8')
        len_of_incoming_message = len_of_incoming_message.replace('*','')

        #third header of packet (message itself)
        message = conn.recv(int(len_of_incoming_message)).decode('utf-8')


        sender = conn.getpeername()[0]

        package = sender + "|" + receiver + "|" + message + "\n"

        packets.append(package)
        logging.debug('packets are --> ' + str(packets))

    

#192.168.6.15  ===> 192.168.6.15***
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
        return str(leng) + '*'

    return str(leng)



def send_messages():
    while(True):

        time.sleep(1)

        if(established_connections):
            for packet in packets:
                headers = packet.split('|', 3)

                for established_connection in established_connections:
                    if(established_connection.getpeername()[0] == headers[1] and packets):

                        #IP address of sender (first header of packet)
                        established_connection.sendall(format_IP(headers[0]).encode('utf-8'))   
 
                        #send len of message (second header of packet)
                        established_connection.sendall(format_len(headers[2]).encode('utf-8'))

                        #send message (third header of message)
                        established_connection.sendall(headers[2].encode('utf-8'))

                        packets.remove(packet)
                            


def main():
    t_send = threading.Thread(target=send_messages)
    t_send.start()

    while(True):
        conn, addr = sock.accept()
        established_connections.append(conn)
        logging.debug('established connections are: --> ' + str(established_connections))

        t1 = threading.Thread(target=receive_messages, args=(conn,))
        t1.start()



if(__name__ == '__main__'):
    main()
