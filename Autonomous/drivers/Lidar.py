import socket
import time 
TCP_IP1   = '127.0.0.1'
TCP_PORT1 = 5007
TCP_PORT2 = 5006
s2=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.bind((TCP_IP1,TCP_PORT1))
s2.listen(1)
conn1,addr1=s2.accept()
s1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((TCP_IP1,TCP_PORT2))
s1.listen(1)
conn,addr=s1.accept()
"""TCP_IP   = '127.0.0.1'
TCP_PORT = 5008
transmit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transmit.connect((TCP_IP, TCP_PORT))"""
try:

	while True:

		l1=float(conn1.recv(20))
		l2=float(conn1.recv(20))
		print(l1,l2)
		if l1>100 and l2>100:
			print("Forward")
			val='s'
		elif l1<100 and l2>100:
			print("Clockwise")
			val='c'
		elif l1>100 and l2<100:
			print("Anticlockwise")
			val='a'
		elif l1<100 and l2<100:
			print("Stop")
			val='p'	
			#transmit.send(val.encode())
			start=time.time()
			while time.time()-start<4:
				val='b'
				#transmit.send(val.encode())
except:
	s1.close()
	s2.close()				