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

sc_host = "192.168.43.20"
sc_port = 10002



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
			server_socket.connect((server_host, server_port))
			sc_socket = socket.socket()
			sc_socket.connect((sc_host, sc_port))		
			data = lot_name+"::"+ scanned_value
			session_key = scanned_value.split("::")[3]			
			server_socket.send(data)			
			sc_data = "TAKE_ENTRY_IMAGE::"+session_key
			sc_socket.send(sc_data)
			value_read = False
			sc_socket.close()
			server_socket.close()

if __name__ == "__main__":
	Main()