import socket
import threading
import time


HOST='localhost'
PORT=5000

s=None
clients=[]
messages_to_clients=[]
data=[]
connectted_client_addresses=[]


def create_socket(host,port):
    global s
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(2)


def remove_tags(msg):
    index1=msg.find('</dst>')
    dst=msg[0 : index1]
    index2=msg.find('</msg>')
    message=msg[index1+11 : index2]
    packet=[dst,message]
    messages_to_clients.append(packet)
    print("message to clients  : ",messages_to_clients)
    return


def accept_message(conn):
    print('function called')
    message=''
    #clients.append(addr)
    while(True):
        msg=conn.recv(20)
        if not msg:
            break
        #print(msg)
        
        message=message+msg.decode('utf-8')
        print(message)
        #remove_tags(message)
        if(msg.decode('utf-8').find('<end>')!=-1):
            remove_tags(message)
            message=''
            #break

    #remove_tags(message)
    
            
            
        
        
        


    #print(clients)

    return
    #print(data)


def send_message():
    while(True):
        print("trying to send messages")
        for packet in messages_to_clients:
            for client in connectted_client_addresses:
                if(client[0]==packet[0]):
                    s.sendto(packet[1].encode('utf-8'),client)
                else:
                    time.sleep(5)


    #if client is not online write message to temporary file

if __name__ == '__main__':
    create_socket(HOST,PORT)

    t0=threading.Thread(target=send_message)
    t0.start()
    while(True):
        conn, addr = s.accept()
        connectted_client_addresses.append(addr)
        print('connection accepted')
        print(connectted_client_addresses)

        t=threading.Thread(target=accept_message, args=[conn])
        t.start()


        
    accept_connections()