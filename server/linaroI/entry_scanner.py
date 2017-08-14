import socket               # Import socket module
import time
import threading

MAGIC = "face600d"
lot_name = "lot_a"
server_host = "192.168.43.20"
server_port = 5001

ue_host = "192.168.43.20"
ue_port = 7000
ue_socket = socket.socket()
ue_socket.bind((ue_host, ue_port))


value_read = False
scanned_value = ""

def read_value():
	global value_read
	global scanned_value
	ue_socket.listen(5)
	while True:
		c, addr = ue_socket.accept()
		scanned_value = c.recv(1024)
		if scanned_value != "":
			time.sleep(1)
			value_read = True
		c.close()
	ue_socket.close()


def Main():
	global value_read
	t1 = threading.Thread(target=read_value)
	t1.start()

	while(1):	
		if value_read:
			server_socket = socket.socket()
			data = lot_name+"::"+ scanned_value
			server_socket.connect((server_host, server_port))
			server_socket.send(data)
			value_read = False
			server_socket.close()

if __name__ == "__main__":
	Main()