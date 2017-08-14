import socket
import time

sm2_host = "192.168.43.110"
sm2_port = 10005

sm2_socket = socket.socket()
sm2_socket.bind((sm2_host, sm2_port))
sm2_socket.listen(10)
c,addr = sm2_socket.accept()
while True:	
	print "connection received from secure camera"
	data = c.recv(1024)
	print data
c.close()
sm2_socket.close()
