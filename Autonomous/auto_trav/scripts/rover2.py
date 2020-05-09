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
latitude=longitude=heading=0
gps_obtained=imu_obtained=False
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
#endlat=float(input())
#endlong=float(input())
endlat=13.348009
endlong=74.792166
###############################Initialization ends################################################

def straight():
    stm_send='m3x4999y0000z'
    print ('Going straight')
    ser.write(stm_send.encode())
    ser.write(stm_send.encode())
def anticlockwise():
    stm_send='m4x0000y4999z'
    print('Rotating anticlockwise')
    ser.write(stm_send.encode())
    ser.write(stm_send.encode())
def clockwise():
    stm_send='m4x9999y4999z'
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
def callback(data):
    global latitude,longitude,gps_obtained
    latitude,longitude=data.data.split(',')
    if not(gps_obtained):
    	gps_obtained=True
    print(latitude,longitude)
def callback1(data):
    global heading,imu_obtained 
    heading=data.data
    if not(imu_obtained):
    	imu_obtained=True
    print(heading)  
def get_heading():
    global latitude,longitude,endlat,endlong
    startlat,startlong=latitude,longitude
    (az12, az21, dist) = g.inv(startlong, startlat, endlong, endlat)
    if az12<0:
       az12=az12+360
    return az12,dist   
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
##############################################Main###############################################                
# def main():

#     global latitude,longitude
#     rospy.init_node('rover',anonymous=True,disable_signals=True)  
#     rospy.Subscriber("coordinates",String,callback)
#     rospy.Subscriber("heading",String,callback1)
#     print('a')
#     print('b')
  
##############################################Main ends#################################################                     


if __name__=='__main__':
	try:
		rospy.init_node('rover',anonymous=True,disable_signals=True)  
		rospy.Subscriber("heading",String,callback1)
		rospy.Subscriber("coordinates",String,callback)
		while True:
			if ((not imu_obtained) or (not gps_obtained)):
				print('Not Enough Data')
			else:	
				match_head()	
				waypoint_heading,waypoint_dist=get_heading()
		        	if waypoint_dist>5:
					print("Distance Remaining",waypoint_dist)
		            		straight()
		        	else:
		            		brute_stop()
		            		print('Reached')
		            		break
	except KeyboardInterrupt:
		brute_stop()
		print('Here')
		pass

