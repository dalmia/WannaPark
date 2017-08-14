import socket
import time

MAGIC = "face600d"

server_socket = socket.socket()
server_host = '192.168.43.20'
server_port = 5002
server_socket.bind((server_host, server_port))
server_socket.listen(5)
c,addr = server_socket.accept()
while True:	
	scanner_data = c.recv(1024)
	print scanner_data
c.close()
server_socket.close()


