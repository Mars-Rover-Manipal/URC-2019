import socket
import time
import random
TCP_IP   = '127.0.0.1'
TCP_PORT = 5008
transmit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transmit.connect((TCP_IP, TCP_PORT))
a=['s','a','c','p','b']
while True:
	transmit.send(random.choice(a).encode())
	time.sleep(0.5)