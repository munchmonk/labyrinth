#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import socket
import threading

class ListenerThread(threading.Thread):
	def __init__(self, client_socket, client_address, peers):
		threading.Thread.__init__(self)

		self.client_socket = client_socket
		self.client_address = client_address
		self.peers = peers

	def run(self):
		while True:
			msg = self.client_socket.recv(1024).decode('ascii')
			print(str(self.client_address) + ' says: ' + msg)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999

server_socket.bind((host, port))
server_socket.listen()

mythreads = []

while True:
	client_socket, client_address = server_socket.accept()

	peers = [thread.client_socket for thread in mythreads]
	
	new_thread = ListenerThread(client_socket, client_address, peers)
	mythreads.append(new_thread)
	new_thread.start()

