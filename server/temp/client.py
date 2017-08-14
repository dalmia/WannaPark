import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = "192.168.43.20"			# Get local machine name
port = 4000           # Reserve a port for your service.

s.connect((host, port))
s.send("LOT_QUERY")
print s.recv(1024)
s.close
