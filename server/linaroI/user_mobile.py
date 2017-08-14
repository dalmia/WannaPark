import socket
import time
from random import randint

MAGIC = "face600d"
lot_iden_map = {1:"lot_a", 2:"lot_b", 3:"lot_c"}

server_socket = socket.socket()         # Create a socket object
server_host = "192.168.43.20"			# Get local machine name
server_port = 4000            	# Reserve a port for your service.

server_socket.connect((server_host, server_port))
random_selection = 0


server_socket.send("LOT_QUERY")
lot_result = server_socket.recv(1024)

if lot_result != "":
	lot_result = lot_result.split("::")
	num_lot = int(lot_result[0])
	if num_lot > 0:
		random_selection = randint(1,num_lot)
		server_socket.send("BOOK::"+lot_iden_map[random_selection])
		booking_status = server_socket.recv(1024)
		print booking_status
	else:
		print "NO parking spot available"
else:
	exit()
server_socket.close()



ue_host = "192.168.43.20"
ue_port = 6000
ue_socket = socket.socket()
ue_socket.bind((server_host, ue_port))


es_host = "192.168.43.20"
es_port = 7000
es_data = lot_iden_map[random_selection]+"::"+ue_host+"::"+str(ue_port)
es_socket = socket.socket()
es_socket.connect((es_host, es_port))
print "Sending QR info to entry_scanner"
es_socket.send(es_data)
es_socket.close()



ue_socket.listen(5)
print "Waiting for spot response from server"
c,addr = ue_socket.accept()
spot_data = c.recv(1024)
if spot_data != "":
	if spot_data != "WRONG_LOT":
		assigned_spot = int(spot_data.split("=")[1])
		print "You are assigned to ",assigned_spot
		c.close()
	else:
		print "You arrived at the wrong lot."
ue_socket.close()