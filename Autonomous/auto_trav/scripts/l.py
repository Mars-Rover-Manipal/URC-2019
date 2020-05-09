#!/usr/bin/env python
import time
import pygame
from pygame import joystick
import math
from time import sleep
import os
import rospy
from std_msgs.msg import String
  
def map1(x,in_min,in_max,out_min,out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def base_station():
	pub=rospy.Publisher("Travtop",String, queue_size=1)
	rospy.init_node("base_station",anonymous=True)
	rate=rospy.Rate(10)
	while True:
		pygame.event.pump()
		x1=j.get_axis(0)
		y1=j.get_axis(1)
		gear=j.get_axis(3)
		hat=j.get_hat(0)
		
		gear=int(map1(gear,-1.0,1.0,9,0))
		x=map1(x1,-1.0,1.0,0.0,9999)
		y=map1(y1,-1.0,1.0,0.0,9999)

		zero=j.get_axis(2)

		if(zero>0.7):
			x=9999
			y=4999
		elif(zero<-0.7):
			x=0
			y=4999

		if hat[1]==1:
			y=0
		elif hat[1]==-1:
			y=9999
		if hat[0]==1:
			x=9999
		elif hat[0]==-1:
			x=0
		

		x=str(int(x)).zfill(4)
		y=str(int(y)).zfill(4)
		val="m"+str(gear)+"x"+str(x)+"y"+str(y)
		clear = lambda : os.system('tput reset')
		#clear()
		pub.publish(val)


if __name__=='__main__':
	try:	
		joystick.init()
		pygame.display.init()
		if pygame.joystick.get_count() == 0:
		    print("No joystick detected")
		    exit(0)
		j=joystick.Joystick(0)
		j.init()			
		adx='a'
		ady='b'
		switch=True
		active=True
		pygame.event.pump()

		base_station()
	except rospy.ROSInterruptException:
		pass		

