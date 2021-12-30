#send header
######################################################
#  -----------------------------------------------   #
# | receiver | len of outgoing message | message |   #
# ------------------------------------------------   #
######################################################

#receive header
######################################################
#  -----------------------------------------------   #
# | sender | len of outgoing message | message   |   #
# ------------------------------------------------   #
######################################################

import socket
import threading
import ipaddress



SERVER = '192.168.3.71'
PORT = 4224
LEN_OF_IP = 15


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((SERVER,PORT))
    print('connected to the server')
except Exception as e:
    print('this exception occured: -- >', e)
    print('something went wrong while connecting to the server. Probably server is not up')
    print('exiting...')
    quit()
        


def validate_ip_addresses(ip_address):
    try:
        ipaddress.ip_address(ip_address)
        return True
    except:
        pass

    return False



#192.168.6.15  ===> 192.168.6.15***
def format_IP(str):
    IP = str

    if(len(str)<15):
        while(len(str)<15):
            str = str + '*'

        IP = str

    return IP

#9  ===> 9*
def format_len(message):
    leng = len(message)
    if(leng<10):
        return str(leng) + '*'

    return str(leng)
        




def show_messages_to_user(sender, message_from_client):
    file_name = str(sender) + '.txt'

    try:
        message_file = open(file_name, 'a')
        try:
            message_file.write("message from peer ---------> " + message_from_client)
        except Exception as e:
            print('this exception occured while writing to file: --->', e)
        finally:
            message_file.close()
    except Exception as e:
            print('this exception occured while opening file: --->', e)


def receive_messages():
    while(True):
        #first header of packet
        sender = sock.recv(LEN_OF_IP).decode('utf-8')
        sender = sender.replace('*','')
        #print('sender-->',sender)

        #second header of packet
        len_of_incoming_message = sock.recv(2).decode('utf-8')
        len_of_incoming_message = len_of_incoming_message.replace('*','')

        #third header of packet
        message_from_client = sock.recv(int(len_of_incoming_message)).decode('utf-8')

        show_messages_to_user(sender, message_from_client)

    


t_receive = threading.Thread(target=receive_messages)
t_receive.start()



while(True):
    dst = input("enter destination:")
    if(validate_ip_addresses(dst) == True):
        dst = format_IP(dst)
        break
    else:
        print('Your IP address format is wrong')



while(True):

    message_to_client= input('enter message:') 

    #send first header (destination)
    sock.sendall(dst.encode('utf-8')) 

    #send second header (len of outgoing message)
    sock.sendall(format_len(message_to_client).encode('utf-8'))  

    #send third header (message itself)
    sock.sendall(message_to_client.encode('utf-8')) 


    destination = str(dst).replace('*','') + '.txt'
    message_file = open(destination, 'a')
    message_file.write("your message == > " + message_to_client + '\n')
    message_file.close()
