import socket
import time
import threading

MAGIC = "face600d"
park_details = {}
spot_details = {}

def id_interface(host, port):
	self.host = host
	self.port = port
	self.id_socket = socket.socket()
	id_socket.bind((host,port))
	id_socket.listen(5)
	
	while True:	
		c, addr = id_socket.accept()
		print "Connection from parking lot received."	
		data = c.recv(1024)
		lot_info = data.split("::")
		magic = lot_info[0].split("=")[1]
		if (magic == MAGIC):
			identity = lot_info[1].split("=")[1]
			total = lot_info[2].split("=")[1]
			available = lot_info[3].split("=")[1]
			detail  = lot_info[4].split("=")[1]
			info = {"identity":identity,"total":total, "available":available}
			park_details[identity] = info

			i = 0
			detial_dict = {}
			for i in range(0,total):
				if detail[i]=='0':
					temp_dict = {"state":0, "book_time":""}
				else:
					temp_dict = {"state":1, "book_time":""}

				detial_dict[i+1] = temp_dict
			spot_details[identity]=detial_dict
		else:
			continue

		print park_details
		time.sleep(1)

	c.close()

def es_interface(host, port1, port2):
	self.host = host
	self.port1 = port1
	self.es_socket = socket.socket()
	es_socket.bind((host,port1))
	es_socket.listen(5)
	
	while True:
		c, addr = es_socket.accept()
		data = c.recv(1024)
		es_info = data.split("::")
		magic = es_info[0].split("=")[1]
		if (magic == MAGIC):
			name = es_info[1].split("=")[1]
			name_by_user = es_info[2].split("=")[1]
			if name != name_by_user:
				print "Wrong Parking Lot"
			else:
				if name in park_details:
					if (park_details[name][available] - num_book[name])>0:
						num_book[name]+=1

						total_spot = park_details[name][total]
						for j in range(0, total_spot):
							if(spot_details[name][i][state]==0):
								spot_details[name][i][state]=2
								spot_details[name][i][book_time] = time.time()
								break
						es_socket.send("AVAILABLE")
					else:
						es_socket.send("NOT_AVAILABLE")
				else:
					print "No parking lot with such name available"

def 				


		