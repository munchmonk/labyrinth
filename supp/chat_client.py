#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import socket
import threading


class ListenerThread(threading.Thread):
	def __init__(self, client_socket):
		threading.Thread.__init__(self)

		self.client_socket = client_socket

	def run(self):
		while True:
			msg = self.client_socket.recv(1024).decode('ascii')
			print('Server says: ' + msg)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999

client_socket.connect((host, port))

print('Connected to server: ' + str(host))

ListenerThread(client_socket).start()

while True:
	msg = input('Enter message: ')
	client_socket.send(msg.encode('ascii'))

