import socket
import threading

HOST='192.168.3.71'
PORT=5000

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((HOST,PORT))

dst=input("enter destination:")
if(len(dst)<15):
    while(len(dst)<15):
        dst=dst + '*'

custom_dst="raddr=('" + dst + "'"

len_as_str=''
def check_message_len(lenght):
    global len_as_str
    if(lenght<=99):                         #calculate length of message which will be send
        if(lenght<10):                      #this must be 2 byte. So if len<10 add '0' to end of len
            len_as_str='0' + str(lenght)
        else:
            len_as_str=str(lenght)


def receive_messages():
    while(True):
        msg_len=s.recv(2)                                #accept incoming message length

        msg=s.recv(int(msg_len.decode('utf-8')))


        

        print('\n ========> ',msg)    



t=threading.Thread(target=receive_messages)
t.start()

while(True):



    s.sendall(custom_dst.encode('utf-8'))

    msg=input('enter message  :')
    lenght=len(msg)

    # if(lenght<=99):                         #calculate length of message which will be send
    #     if(lenght<10):                      #this must be 2 byte. So if len<10 add '0' to end of len
    #         len_as_str='0' + str(lenght)
    #     else:
    #         len_as_str=str(lenght)    
    check_message_len(lenght)

    s.sendall(len_as_str.encode('utf-8'))   #send length of message
    s.sendall(msg.encode('utf-8'))          #send message itself