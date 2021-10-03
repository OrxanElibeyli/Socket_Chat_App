#                packet format
#   | destination | length of message |   message   |
#   |   24 byte   |      2 byte       |  0-99 byte  |




import socket
import threading
import time
import sys
from logging1 import Logging1

HOST=''                                                 #all network interfaces can be used for connection
PORT=5000                                               #port which server listen

logger=Logging1()

data_packets=[]                                          #destination and message to destination
connected_clients=[]                                     #socket addresses of connnected clients


try:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen()
except Exception as e:
    print('Something went wrong while creating socket. For more information see log file')
    logger.log('error',str(e))
    print('exiting...')
    sys.exit()





def close(conn):
    conn.sendall('4'.encode('utf-8'))
    conn.sendall('quit'.encode('utf-8'))
    conn.close()
    
    if(connected_clients):
        connected_clients.remove(conn)


def check_message_len(lenght):
    '''customize length of outgoing message. If len<10 add '0' to end of len'''
    len_as_str=''
    if(lenght<=99):
        if(lenght<10):
            len_as_str='0' + str(lenght)
        else:
            len_as_str=str(lenght)
    return len_as_str


def remove_stars(dst):
    '''  raddr=('192.168.4.181** ===> raddr=('192.168.4.181  '''
    index=dst.find('*')
    return dst[0:index]


def receive_message(conn,addr):
    '''receive messages from each client'''
    while(True):
        dst=(conn.recv(24)).decode('utf-8')                           #accept destination ip

        logger.log('info', 'message destination is: ' + dst)

        msg_len=(conn.recv(2)).decode('utf-8')                        #accept incoming message length
        msg=(conn.recv(int(msg_len))).decode('utf-8')

        #if client request to end chat then close connection
        if(msg == 'quit'):
            close(conn)
            logger.log('info', f'chat closed by {addr}')
            break

        logger.log('info', f'{msg} from {addr} to {dst}')

        dst=remove_stars(dst)
        data_packets.append((dst,msg))

        logger.log('info', 'data packets is : ' + str(data_packets))




def send_messages():
    ''' check message destination and connected clients. Then send messages'''
    global command
    
    while(True):
        #print('command ', command)
        #if(command == 'close'):
            #break
        time.sleep(2)
        if(data_packets):
            for packet in data_packets:
                for connected_client in connected_clients:
                    if(str(connected_client).find(packet[0])!=-1):
                        len_as_str=check_message_len(len(packet[1]))
                        connected_client.sendall(len_as_str.encode('utf-8'))       #send length of data
                        connected_client.sendall(packet[1].encode('utf-8'))        #send data
                        data_packets.remove(packet)
                        logger.log('info', f'message sent: {packet}')
                        logger.log('info', 'data packets after last send is : ' + str(data_packets))

                        


def main():
    ''' program begin from here '''
    global send_thread
        

    send_thread=threading.Thread(target=send_messages)
    send_thread.start()

    while(True):
        #print('cmnd: ',command)
        #if(command == 'close'):
            #break

        print('accepting')
        conn, addr = s.accept()
        connected_clients.append(conn)

        log_line='connected clients: ' + str(connected_clients)
        logger.log('info',log_line)

        #print('connected clients  :',connected_clients)


        receive_thread=threading.Thread(target=receive_message, args=(conn,addr))
        receive_thread.start()
        print(receive_thread)


if(__name__ == '__main__'):
    main()
