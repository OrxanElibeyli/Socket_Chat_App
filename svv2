#receive header
############################################################
#  ------------------------------------------------------- #
# | quit | receiver | len of outgoing message | message  | #
# -------------------------------------------------------- #
############################################################

#send header
############################################################
#  -----------------------------------------------------   #
# | quit | sender | len of outgoing message | message  |   #
# ------------------------------------------------------   #
############################################################

import socket
import threading
import time
import logging

from my_protocol import MY_PROTOCOL


HOST = ''
PORT = 4224
LEN_OF_IP = 15

established_connections = []
packets = []



logging.basicConfig(filename='server_logs.txt',filemode='a',format='%(asctime)s - %(levelname)s - %(message)s',level=logging.DEBUG)

mp = MY_PROTOCOL()

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
        package = mp.receive_message(conn)
        packets.append(package)
        logging.debug('packets are --> ' + str(packets))
    

def send_messages():
    while(True):

        time.sleep(1)

        if(established_connections):
            for packet in packets:

                for established_connection in established_connections:
 
                    if(established_connection.getpeername()[0] == packet['dst'] and packets):

                        mp.send_message(conn = established_connection, src = packet['src'], dst = packet['dst'], message = packet['message'])
                        
                        packets.remove(packet)
                        logging.debug('packet deleted ')
                            

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
