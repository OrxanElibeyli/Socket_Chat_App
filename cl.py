import socket
import pdb


print('*client was started...')
print('*trying to connect server...')


SERVER = '192.168.3.71'
PORT = 4224

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER,PORT))

print('*connected to the server')
while(True):
    message = input('enter something:')

    sock.sendall(message.encode())
