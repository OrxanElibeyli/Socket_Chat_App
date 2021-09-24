import socket
import threading
import time

HOST=''
PORT=5000

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen()

messages=[]

connected_clients=[]

len_as_str=''
def check_message_len(lenght):
    global len_as_str
    if(lenght<=99):                         #calculate length of message which will be send
        if(lenght<10):                      #this must be 2 byte. So if len<10 add '0' to end of len
            len_as_str='0' + str(lenght)
        else:
            len_as_str=str(lenght)




def remove_stars(dst):
    index=dst.decode('utf-8').find('*')
    return dst[0:index]
        


def receive_message(conn,addr):
    while(True):
        dst=conn.recv(24)                                   #accept destination ip
        print('dst: ',dst)
        msg_len=conn.recv(2)                                #accept incoming message length
        print('msg: ',msg_len)

        msg=conn.recv(int(msg_len.decode('utf-8')))
        print(f'{msg} from {addr}')

        destination=remove_stars(dst)

        messages.append((destination,msg.decode('utf-8')))

        print("msgs :",messages)



def send_messages():
    while(True):
        print('messages  :',messages)
        print("trying to send message...")
        time.sleep(2)
        if(messages):
            print('------------- success ---------------')
            for message in messages:
                for connected_client in connected_clients:
                    print('------------- success22 ---------------')
                    print('str(message[0]) :', str(message[0].decode('utf-8')))
                    if(str(connected_client).find(str(message[0].decode('utf-8')))!=-1):
                        #print("msg[0] :",messages[0])
                        #print('msg[1] :', message[1])
                        check_message_len(len(message[1]))
                        connected_client.sendall(len_as_str.encode('utf-8'))   #send length of data
                        connected_client.sendall(message[1].encode('utf-8'))        #send data
                        print('message send...')

                        messages.remove(message)

                        #remove sended message







t0=threading.Thread(target=send_messages)
t0.start()

while(True):
    conn, addr = s.accept()
    connected_clients.append(conn)

    print('connected clients  :',connected_clients)

    

    t=threading.Thread(target=receive_message, args=(conn,addr))
    t.start()

