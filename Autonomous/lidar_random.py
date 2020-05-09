import socket
import time
import random
TCP_IP1  = '127.0.0.1'
TCP_PORT1 = 5007
transmit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transmit.connect((TCP_IP1, TCP_PORT1))
TCP_PORT2 = 5006
transmit2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transmit2.connect((TCP_IP1, TCP_PORT2))
while True:
	transmit.send(str(random.randint(0,5000)).encode())
	transmit2.send(random.randint(0,5000).encode())
	time.sleep(0.5)