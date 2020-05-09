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



for i in range(5):
	straight()
