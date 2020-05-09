import socket
import time
import random
TCP_IP   = '127.0.0.1'
TCP_PORT = 40010
transmit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transmit.connect((TCP_IP, TCP_PORT))
TCP_PORT1 = 40000
transmit1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transmit1.connect((TCP_IP, TCP_PORT1))
while True:
	transmit.send(random.randint(0,5000).encode())
	transmit1.send(random.randint(0,5000).encode())
	time.sleep(0.5)