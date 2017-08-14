simport socket               # Import socket module
import time

MAGIC = "face600d"

#format of input file
	# magic::dGaVaDsD
	# identity::lot_a
	# total::8
	# avaiable::3
	# detail::01001111


while(1):
	with open("lot_details.txt") as lot_details:
		lines = lot_details.read().splitlines()
	lot_details.close()

	magic = lines[0].split("=")[1]
	identity = lines[1].split("=")[1]
	total = lines[2].split("=")[1]
	avaiable = lines[3].split("=")[1]
	detail = lines[4].split("=")[1]

	print magic

	if (magic==MAGIC):
		data = "magic="+magic+"::identity="+identity+"::total="+total+"::available="+avaiable+"::detail="+detail
		print data

		server_socket = socket.socket()         # Create a socket object
		server_host = "192.168.43.20"			# Get local machine name
		server_port = 5000           	# Reserve a port for your service.

		server_socket.connect((server_host, server_port))
		server_socket.send(data)
		server_socket.close()
		time.sleep(5)

