#send header
############################################################
#  ------------------------------------------------------- #
# | quit | receiver | len of outgoing message | message  | #
# -------------------------------------------------------- #
############################################################

#receive header
############################################################
#  -----------------------------------------------------   #
# | quit | sender | len of outgoing message | message  |   #
# ------------------------------------------------------   #
############################################################

import socket
import threading
import ipaddress
import logging
from my_protocol import MY_PROTOCOL

logging.basicConfig(filename='client_logs.txt',filemode='a',format='%(asctime)s - %(levelname)s - %(message)s',level=logging.DEBUG)


SERVER = '192.168.3.71'
PORT = 4224
LEN_OF_IP = 15

mp = MY_PROTOCOL()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((SERVER,PORT))
    logging.info(f'connected to the server: {SERVER}')
except Exception as e:
    logging.error(str(e))
    logging.info('some error ocurred during connection to server.')
    logging.info('quiting...')
    quit()
        


def validate_ip_addresses(ip_address):
    try:
        ipaddress.ip_address(ip_address)
        return True
    except:
        pass

    return False


def show_messages_to_user(sender, message_from_client):
    file_name = str(sender) + '.txt'

    try:
        message_file = open(file_name, 'a')
        try:
            message_file.write("message from peer ---------> " + message_from_client)
        except Exception as e:
            logging.error('thi error occured while writing to the file:' + str(e))
        finally:
            message_file.close()
    except Exception as e:
            logging.error('thi error occured while opening file:' + str(e))


def receive_messages():
    while(True):
        packet = mp.receive_message(sock)
        show_messages_to_user(packet.pop('src'), packet.pop('message'))

    
t_receive = threading.Thread(target=receive_messages)
t_receive.start()

print('enter quit() for quiting.')

while(True):
    dst = input("enter destination:")
    if(validate_ip_addresses(dst) == True):
        break
    else:
        print('Your IP address format is wrong')



while(True):

    message_to_client= input('enter message:') 

    mp.send_message(conn = sock, src = sock.getsockname()[0], dst = dst, message = message_to_client)

    destination = str(dst).replace('*','') + '.txt'
    message_file = open(destination, 'a')
    message_file.write("your message == > " + message_to_client + '\n')
    message_file.close()
