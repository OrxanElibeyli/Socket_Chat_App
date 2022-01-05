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


clients = []

HOST = ''
PORT = 4224
LEN_OF_IP = 15

established_connections = []
packets = []



sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    sock.bind((HOST, PORT))
except Exception as e:
    print('this exception occured ---->', e)
    print('exiting...')
    quit()
    
sock.listen()








#this function is used by threat for receiving messages from client
def receive_messages(conn):
    while(True):
        #first header of packet
        receiver = conn.recv(LEN_OF_IP).decode('utf-8')
        receiver = receiver.replace('*','')


        #second header of packet
        len_of_incoming_message = conn.recv(2).decode('utf-8')
        len_of_incoming_message = len_of_incoming_message.replace('*','')

        #third header of packet
        message = conn.recv(int(len_of_incoming_message)).decode('utf-8')

        sender = conn.getpeername()[0]

        package = sender + "|" + receiver + "|" + message + "\n"

        packets.append(package)



        print(packets)

        # message_file = open("messages.txt","a")
        # message_file.write(package)
        # message_file.close()
    


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
    print('\n send function called \n')

    for packet in packets:
        print('packet --> ',packet)
    
    print('\n')
    
    while(True):
        time.sleep(1)
        if(established_connections):
            for packet in packets:
                headers = packet.split('|', 3)
                print("!!!!!!!! ----> ", packets)
                print('packet -- >', packet)
                for established_connection in established_connections:
                    print('ec -->',established_connection)
                    #print("getpeername - ->", established_connection.getpeername[0])
                    if(established_connection.getpeername()[0] == headers[1] and packets):
                        
                        #print('-------',format_IP(headers[0]))

                        #IP address of sender (first header of packet)
                        established_connection.sendall(format_IP(headers[0]).encode('utf-8'))   
 
                        #print('-!-------',format_len(headers[2]))
                        #send len of message (second header of packet)
                        established_connection.sendall(format_len(headers[2]).encode('utf-8'))

                        #print('--------|',headers[2],'|')
                        #send message (third header of message)
                        established_connection.sendall(headers[2].encode('utf-8'))


                        #delete message which was sent
                        print('packets before -- >',packets)
                        packets.remove(packet)
                        print('packets after -- >',packets)
                            

t_send = threading.Thread(target=send_messages)
t_send.start()

while(True):
    conn, addr = sock.accept()
    established_connections.append(conn)
    #print('established connections ---->', established_connections)

    for connnection in established_connections:
        print('established connection --> ', connnection)

    print('\n')

    t1 = threading.Thread(target=receive_messages, args=(conn,))
    t1.start()





#   NOTE
# there is a bug. when a client connect to server 2 times, message from its peer come two times and an exception occurs
