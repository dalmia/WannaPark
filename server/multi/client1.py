# Python TCP Client A
import socket 
 
host = socket.gethostname() 
port = 2004
BUFFER_SIZE = 2000 
MESSAGE = raw_input("tcpClientA: Enter message/ Enter exit:") 
 
tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientA.connect((host, port))
 
while MESSAGE != 'exit':
    tcpClientA.send(MESSAGE)     
    data = tcpClientA.recv(BUFFER_SIZE)
    print " Client2 received data:", data
    MESSAGE = raw_input("tcpClientA: Enter message to continue/ Enter exit:")
 
tcpClientA.close() 