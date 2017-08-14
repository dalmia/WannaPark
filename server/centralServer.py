import socket 
import time

MAGIC = "face600d"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.43.20'
port = 45788

server_socket.bind((host, port))

park_details = {}

#waiting for connection 
server_socket.listen(5)
while True:
	c, addr = server_socket.accept()
	print 'Got connection from ', addr
	data = c.recv(1024)
	lot_info = data.split("::")
	magic = lot_info[0].split("=")[1]
	if (magic == MAGIC):
		identity = lot_info[1].split("=")[1]
		total = lot_info[2].split("=")[1]
		available = lot_info[3].split("=")[1]
		detail  = lot_info[4].split("=")[1]
		info = {"identity":identity,"total":total, "available":available, "detail":detail}
		park_details[identity] = info
	else:
		continue

	print park_details
	time.sleep(5)
	c.close()

