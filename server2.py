#                packet format
#   | destination | length of message |   message   |
#   |   15 byte   |      2 byte       |  0-99 byte  |



import socket
import threading

SERVER='192.168.43.181'                                    #chat server
PORT=5000                                                  #port for this application

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((SERVER,PORT))


def customize_destination(dst):
    '''costumize acording max ip length, dots (15) and conn object (conn, add = s.accept())'''

    if(len(dst)<15):
        while(len(dst)<15):
            dst=dst + '*'

    dst="raddr=('" + dst + "'"
    return dst


def check_message_len(lenght):
    '''customize length of outgoing message. If len<10 add '0' to end of len'''

    len_as_str =''
    if(lenght<=99):
        if(lenght<10):
            len_as_str='0' + str(lenght)
        else:
            len_as_str=str(lenght)

    return len_as_str


def receive_messages():
    '''receive message from chat partner via chat server'''

    while(True):
        msg_len=s.recv(2)                                #accept incoming message length
        msg=s.recv(int(msg_len.decode('utf-8')))

        print('\n ========> ',msg)
        print('\n')


def main():
    '''program start from here'''

    receive_messages_thread=threading.Thread(target=receive_messages)
    receive_messages_thread.start()


    dst=input("enter destination:")                         #where client want to send message
    dst=customize_destination(dst)


    while(True):
        s.sendall(dst.encode('utf-8'))                      #send destination (first packet)

        msg=input('enter message  :')
        lenght=len(msg)
        len_as_str=check_message_len(lenght)                #length of outgoing message. for example, 89,45,56,07,04
                

        s.sendall(len_as_str.encode('utf-8'))               #send length of message (second packet)
        s.sendall(msg.encode('utf-8'))                      #send message itself (thrid packet)


if(__name__ == '__main__'):
    main()
