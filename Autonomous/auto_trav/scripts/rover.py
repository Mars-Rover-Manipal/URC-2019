#!/usr/bin/env python
import rospy 
from std_msgs.msg import String 
import serial
import time
from gps3 import gps3
from math import radians, cos, sin, asin, sqrt
from geopy import distance
import pyproj
import socket
import sys
import threading,os
latitude=longitude=heading=ball=opencv_count=0
gps_obtained=imu_obtained=kinect_obtained=ball_obtained=dist_obtained=False
kinect = 'straight'
distance = 3000
flag=0
###############################Initialization#####################################################
g = pyproj.Geod(ellps='WGS84')
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
ser = serial.Serial(port='/dev/ttyTHS2',baudrate = 38400)
def pos_update():
    while True:
        for new_data in gps_socket:
            if new_data:
                data_stream.unpack(new_data)
                global latitude,longitude
                latitude =  data_stream.TPV['lat']
                longitude =  data_stream.TPV['lon']
                if type(longitude) is type('sdas') or type(latitude) is type('sdas'):
                    continue                 
                #print(latitude,longitude)
                return latitude,longitude
        break          

#endlat=13.347678
#endlong=74.792668
###############################Initialization ends################################################

def straight():
    stm_send='m5x4999y0000z'
    print ('Going straight')
    ser.write(stm_send.encode())
    ser.write(stm_send.encode())
def straight_slow(gear):
    stm_send='m'+str(gear)+'x4999y0000z'
    print ('Going straight')
    ser.write(stm_send.encode())
    ser.write(stm_send.encode())
def anticlockwise():
    stm_send='m5x0000y4999z'
    print('Rotating anticlockwise')
    ser.write(stm_send.encode())
    ser.write(stm_send.encode())
def clockwise():
    stm_send='m5x9999y4999z'
    print('Rotating clockwise')
    ser.write(stm_send.encode())
    ser.write(stm_send.encode())
def backward():
    stm_send='m4x4999y9999z'    
    print('Going backward')
    ser.write(stm_send.encode())
    ser.write(stm_send.encode())
def brute_stop():
    stm_send='m2x4999y4999z'
    print('Brute Stop')
    ser.write(stm_send.encode())
    ser.write(stm_send.encode())
def mast_cam():
    stm_send='m2x4999y4999a'
    print('Visual Marker')
    ser.write(stm_send.encode())
    ser.write(stm_send.encode())
def gps_callback(data):
    global latitude,longitude,gps_obtained
    latitude,longitude=data.data.split(',')
    latitude=float(latitude)
    longitude=float(longitude)
    if not(gps_obtained):
    	gps_obtained=True
    #print(latitude,longitude)
def imu_callback(data):
    global heading,imu_obtained 
    heading=float(data.data)
    if not(imu_obtained):
    	imu_obtained=True
    #print(heading)  
def kinect_callback(data):
    global kinect,kinect_obtained 
    kinect=data.data
    if not(kinect_obtained):
    	kinect_obtained=True
def ball_callback(data):
    global ball,ball_obtained 
    ball=data.data
    if not(ball_obtained):
    	ball_obtained=True
    #print(heading)  
def dist_callback(data):
    global distance,dist_obtained 
    distance=float(data.data)
    if not(dist_obtained):
    	dist_obtained=True
def get_heading():
    global latitude,longitude,endlat,endlong
    startlat,startlong=latitude,longitude
    (az12, az21, dist) = g.inv(startlong, startlat, endlong, endlat)
    if az12<0:
       az12=az12+360
    return az12,dist  
def avoid():
    while True:
	print('Obstacle Detected')
	if kinect=='left':
		for i in range(400):
			anticlockwise()
	elif kinect=='right':
		for i in range(5):
			clockwise()
	else:
		for i in range(500):
			if kinect!='straight':
				avoid()
			else:
				straight_slow(5)
		break
def match_head():
    waypoint_heading,dist=get_heading()
    while True:
        #waypoint_heading_opp=waypoint_heading+180
        imu_heading=int(heading)
        heading_diff=imu_heading-waypoint_heading
        print(imu_heading,waypoint_heading,heading_diff)

        if imu_heading < waypoint_heading+5 and imu_heading>waypoint_heading-5:
                #brute_stop()
                break
        if heading_diff >=-180:
                if heading_diff<=0:
                        clockwise()
        if heading_diff <-180:
                anticlockwise()
        if heading_diff>=0:
                if heading_diff<180:
                        turn = 2 
                        anticlockwise()             
        if heading_diff >= 180:
                turn = 1
                clockwise()

def match_head_bd():
    waypoint_heading,dist=get_heading()
    while True:
        imu_heading=int(heading)
        heading_diff=imu_heading-waypoint_heading
        print(imu_heading,waypoint_heading,heading_diff)
	if int(ball) == 1:
		detect()
		break
		rospy.logwarn('BHEEEEEEEEEEEEEEEEEEEENCHOOOOOOOOOOOOOOOOOOOD')
        if imu_heading < waypoint_heading+5 and imu_heading>waypoint_heading-5:
                #brute_stop()
                break
        if heading_diff >=-180:
                if heading_diff<=0:
                        clockwise()
        if heading_diff <-180:
                anticlockwise()
        if heading_diff>=0:
                if heading_diff<180:
                        turn = 2 
                        anticlockwise()             
        if heading_diff >= 180:
                turn = 1
                clockwise()

def detect():
	global flag, ball
	#if int(ball)==1:
	#	flag = 1
	rospy.logwarn("Ball Detected BHEEENCCHHOODDDDD!!!!!!!!!!!!!!")
	brute_stop()
	if int(ball)==1:
		flag = 1
		for i in range(400):
			straight()
		for i in range(400):
			mast_cam()		
		brute_stop()
	else:
		while int(ball) !=1:
			clockwise()
		flag = 1
		for i in range(400):
			straight()
		brute_stop()
		mast_cam()
		brute_stop()

def clock_turn():
	global heading,flag,ball
        h=heading
        z=0
        while z-h <90:
                n=heading
                if n<h:
                        z=360+n
                else:
                        z=n
                if int(ball) == 1:
			detect()
			break
		elif int(flag) == 0:
			clockwise()
		else:
			rospy.logwarn('IM AM OUT BITCHES')
			break

def ball_search():
    global endlat,endlong,flag,ball,kinect
    x,y = latitude, longitude 
    way = []
    r = 6
    for i in range(2):
    	for i in range(0, 361, 60):
    		cx = cos(radians(i))*r/111035 + x
    		cy = sin(radians(i))*r/111035 + y
    		a = []
    		a.append(cx)
    		a.append(cy)
    		way.append(a)
		#time.sleep(1)
    	for i in range(len(way)):
		print(i+1, "REACHED!!!!!!")
		for j in range(4):
			if flag==0:
				clock_turn()
			else:
				break
		if flag == 1 :
			brute_stop()
			break
    		endlat = way[i][0]
    		endlong = way[i][1]
		while not flag == 1:
			if ((not imu_obtained) or (not gps_obtained)):
				print('Not Enough Data')
			else:	
				match_head_bd()	
				waypoint_heading,waypoint_dist=get_heading()
			        if waypoint_dist>2:
					if kinect=="straight":
						print(waypoint_dist)
				            	straight_slow(6)
						if int(ball) == 1:
							detect()
							break
			        else:
			            	brute_stop()
					break
	if flag == 1:
		break
	r = r+4
#endlat=13.3499018
#endlong=74.7916073
#endlat=13.3502110
#endlong=74.7913515
endlat=13.3502658
endlong=74.7917116
#endlat=13.3504280
#endlong=74.7916891
if __name__=='__main__':
	try:
		rospy.init_node('rover',anonymous=True,disable_signals=True)  
		rospy.Subscriber("heading",String,imu_callback)
		rospy.Subscriber("coordinates",String,gps_callback)
		rospy.Subscriber("/kinect_data",String,kinect_callback)
		rospy.Subscriber("/ball_flag",String,ball_callback)
		while flag!=1:
			if ((not imu_obtained) or (not gps_obtained)):
				print('Not Enough Data')
			else:	
				match_head()	
				waypoint_heading,waypoint_dist=get_heading()
		        	if waypoint_dist>6:
					if kinect=="straight":
						print(waypoint_dist)
			            		straight_slow(7)
					else:
						avoid()
		        	else:
		            		brute_stop()
		            		print('Reached')
					print("Starting Ball Search...")
					ball_search()
		            		break
	except KeyboardInterrupt:
		brute_stop()
		rospy.logwarn('Rover killed by the user')
		pass

