#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import socket
import threading

class ListenerThread(threading.Thread):
	def __init__(self, client_socket, allclients):
		threading.Thread.__init__(self)

		self.client_socket = client_socket
		self.allclients = allclients

	def run(self):
		while True:
			msg = self.client_socket.recv(1024).decode('ascii')
			print('Client ' + str(self.client_socket) + ' says: ' + msg)
			self.broadcast(msg)

	def broadcast(self, message):
		print('Broadcasting to all clients: ' + message)

		message = message.encode('ascii')
		for client in self.allclients:
			if client != self.client_socket:
				client.send(message)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999

server_socket.bind((host, port))
server_socket.listen()

print('Server set up, waiting for connections')
allclients = []

while True:
	client_socket, client_address = server_socket.accept()
	allclients.append(client_socket)
	print('Received a connection from: ' + str(client_address))
	ListenerThread(client_socket, allclients).start()