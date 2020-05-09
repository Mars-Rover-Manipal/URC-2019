'''
################################################################################################
Multiplexer code for the rover which accepts lidar and gps values at a time and gives one output
Author: Ved Chitnis
Date: Jan 28th 2019
Time of last change: 00:06 Tuesday, 29.01.2019
Last change: Added safety for broken data link
################################################################################################
'''
import socket
from traversal_functions import straight,anticlockwise,clockwise,brute_stop,backward
try:
	while True:
		data=get_lidar()
		data2=get_gps()
		print(data,data2)
		if data =="'" or data2=="'":
			break
		if data == "s":
			if data2 == "a":
				#print("Anticlockwise")
				anticlockwise()
			elif data2 == "c":
				#print("Clockwise")
				clockwise()
			elif data2 == "p":
				#print("Stop")
				brute_stop()
			elif data2== "b":
				#print("Backward")			 
				backward()
			else:
				#print("Straight")			
				straight()
		else:
			if data == "a":
				#print("Anticlockwise")
				anticlockwise()
			elif data == "c":
				#print("Clockwise")
				clockwise()
			elif data == "p":
				#print("Stop")
				brute_stop()
			elif data=="b":
				#print("Backward")			 	
				backward()
			else:
				#print("Straight")	
				straight()
	print("Data link broken, Rover Stopped")			
except:
	s1.close()
	s2.close()				