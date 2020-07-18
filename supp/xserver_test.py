#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import pygame
import socket

print('hi')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999

server_socket.bind((host, port))

server_socket.listen(1)

while True:
	cliest_socket, client_address = server_socket.accept()
	msg = 'Hello ' + str(client_address)

	cliest_socket.send(msg.encode('ascii'))

	print('Connected to: ' + str(client_address))

