import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.43.20'
port = 4000

server_socket.bind((host, port))  
server_socket.listen(50)
print "socket created"

while True:
	c, addr = server_socket.accept()
	print "connnection received from ", addr
	data = c.recv(1024*16)
	print data
	send_data = "hello aman2"
	# json_data = demjson.encode(data)

	c.send(send_data)
	c.close()
