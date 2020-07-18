#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import pygame
import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999

client_socket.connect((host, port))

print('Connected to server!')
msg = client_socket.recv(1024).decode('ascii')
print('Server says: ' + msg)
start = time.time()

while time.time() - start < 30:
	pass

client_socket.close()

