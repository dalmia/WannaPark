import socket
import time
import threading

MAGIC = "face600d"
host = "192.168.43.20"
sr_port = 4000
id_port = 5000
es_port = 5001


eu_port = 6000

sr_socket = socket.socket()
sr_socket.bind((host, sr_port))

id_socket = socket.socket()
id_socket.bind((host, id_port))

es_socket = socket.socket()
es_socket.bind((host, es_port))

sm_host = "192.168.43.20"
sm_port = 5002
sm_socket = socket.socket()
sm_socket.connect((sm_host, sm_port))


park_details = {}
spot_details = {}

def id_interface():
	# print "id_interface is running"
	id_socket.listen(5)	
	while True:	
		c, addr = id_socket.accept()
		# print "Connection from parking lot received."	
		data = c.recv(1024)
		lot_info = data.split("::")
		magic = lot_info[0].split("=")[1]
		if (magic == MAGIC):
			identity = lot_info[1].split("=")[1]
			total = lot_info[2].split("=")[1]
			available = lot_info[3].split("=")[1]
			detail  = lot_info[4].split("=")[1]
			info = {"total":int(total), "available":int(available)}
			park_details[identity] = info

			detial_dict = {}
			for i in range(0,int(total)):
				if detail[i]=='0':
					temp_dict = {"state":0, "book_time":""}
				else:
					temp_dict = {"state":1, "book_time":""}

				detial_dict[i+1] = temp_dict
			spot_details[identity]=detial_dict
		c.close()


def Mobile_init(name, eu_socket):
	# self.eu_socket = eu_socket
	data = eu_socket.recv(1024)
	if data == "LOT_QUERY":
		num_avail = 0
		message = ""
		for key,value in park_details.iteritems():
			print value
			if value["available"]>0:
				num_avail+=1
				message = message+"::"+key
		message = str(num_avail)+message
		eu_socket.send(message)

		user_response = eu_socket.recv(1024)
		print user_response
		if user_response != "":
			parsed_user_response = user_response.split("::")
			status = parsed_user_response[0]
			if status == "BOOK":
				lot_name = parsed_user_response[1]
				if park_details[lot_name]["available"] > 0:
					park_details[lot_name]["available"]-=1
					eu_socket.send("BOOKING_CONFIRMED")
				else:
					eu_socket.send("UNABLE_TO_BOOK_PLEASE_TRY_LATER")
	eu_socket.close()

def es_interface():
	es_socket.listen(5)
	while True:
		c, addr = es_socket.accept()
		data = c.recv(1024)
		print "es_interface data -> "+data
		if data != "":
			parsed_data = data.split("::")
			lot_name = parsed_data[0]
			user_lot_name = parsed_data[1]
			user_host = parsed_data[2]
			user_port = int(parsed_data[3])

			user_socket = socket.socket()
			user_socket.connect((user_host,user_port))
			if lot_name == user_lot_name:				
				sm_socket.send("OPEN")
				user_socket.send("ASSIGNED_SPOT=1")	
				# 
				user_socket.close()			
			else:
				sm_socket.send("CLOSE")
				user_socket.send("WRONG_LOT")
				user_socket.close()
		c.close()
	es_socket.close()

def Main():
	id_thread = threading.Thread(target=id_interface)
	id_thread.start()

	es_thread = threading.Thread(target=es_interface)
	es_thread.start()

	sr_socket.listen(5)
	i = 0
	while True:
		c, addr = sr_socket.accept()
		print 'Got connection from ', addr
		t = threading.Thread(target=Mobile_init, args=("thread_"+str(i), c))
		t.start()
		i+=1
	
	sr_socket.close()

if __name__ == "__main__":
	Main()