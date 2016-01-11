# Echo client program
import socket

HOST = 'localhost'    # The remote host
PORT = 60007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket object
s.connect((HOST, PORT)) # Connect to a particualr port
"""
Send data to the server localhost on port 60007
If the port is not listening then it will raise an exception
"""
s.send(b'Hello, world')                     
data = s.recv(1024) # recieve response from the server
s.close()
print('Received', repr(data))