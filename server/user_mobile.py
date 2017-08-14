import socket
import time
from random import randint, choice
from string import digits, ascii_uppercase, ascii_lowercase

MAGIC = "face600d"
lot_iden_map = {1:"lot_a", 2:"lot_b", 3:"lot_c"}

server_socket = socket.socket()         # Create a socket object
server_host = "192.168.43.20"			# Get local machine name
server_port = 4000            	# Reserve a port for your service.

server_socket.connect((server_host, server_port))
random_selection = 0


server_socket.send("LOT_QUERY")
lot_result = server_socket.recv(1024)
print "lot_result received ", lot_result

if lot_result != "":
	lot_result = lot_result.split("::")
	num_lot = int(lot_result[0])
	if num_lot > 0:
		random_selection = 1#randint(1,num_lot)
		server_socket.send("BOOK::"+lot_iden_map[random_selection])
		booking_status = server_socket.recv(1024)
		print booking_status
	else:
		print "NO parking spot available"
else:
	exit()
server_socket.close()

print "so far so good"

ue_host = "192.168.43.20"
ue_port = 6000
ue_socket = socket.socket()
ue_socket.bind((ue_host, ue_port))


es_host = "192.168.43.20"
es_port = 7000

#generating session key to handle 
session_key = ''.join(choice(ascii_lowercase + ascii_uppercase + digits) for i in range(15))
estimated_time = randint(50,140)
es_data = lot_iden_map[random_selection]+"::"+ue_host+"::"+str(ue_port)+"::"+session_key+"::"+str(time.time() + 5.5*60*60 + estimated_time+60)
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

time.sleep(5)

exits_host = "192.168.43.20"
exits_port = 10003

exitue_host = "192.168.43.20"
exitue_port = 10004
exitue_socket = socket.socket()
exitue_socket.bind((exitue_host, exitue_port))

exits_socket = socket.socket()
exits_socket.connect((exits_host, exits_port))
print "sending exit code to secure_camera"
data = "TAKE_EXIT_IMAGE::"+session_key+"::"+exitue_host+"::"+str(exitue_port)
exits_socket.send(data)
exits_socket.close()

exitue_socket.listen(5)
c,addr = exitue_socket.accept()
received_data = c.recv(1024)
if received_data == "EXIT_SECURITY_PASS":
	print "Exit security passed. Thank you for visiting"
else:
	print "Man, we got you. Have a great time in jail"
c.close()
exitue_socket.close()

