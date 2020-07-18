#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import pygame
import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999

client_socket.connect((host, port))

print('Connected to server!')


while True:
	msg = input('Enter message: ')
	client_socket.send(msg.encode('ascii'))



client_socket.close()

