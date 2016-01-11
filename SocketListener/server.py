# Echo server program
import socket

HOST = 'localhost'
PORT = 60007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
s.bind((HOST, PORT)) # Connect to localhost for a particular port
s.listen(5) # Starts a TCP listener with queued connections as 5

connection, address = s.accept() # starts accepting connections
print('connected by', address)
while True:
	data = connection.recv(1024) # recieve data from client
	if not data: break
	connection.send(data) # send recieved data to the client
connection.close() # close the connection