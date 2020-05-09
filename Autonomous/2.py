import socket
import time
import random
TCP_IP   = '127.0.0.1'
TCP_PORT = 5009
transmit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transmit.connect((TCP_IP, TCP_PORT))
b=['s','c','a','p','b']
while True:
	transmit.send(random.choice(b).encode())
	time.sleep(1)