import socket
import os

socket_path = '/tmp/my_socket'

# send data to unix socket
client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect(socket_path)
client.sendall(b'Hello from the client!')
response = client.recv(1024)
print('Received from server:', response.decode())
client.close()