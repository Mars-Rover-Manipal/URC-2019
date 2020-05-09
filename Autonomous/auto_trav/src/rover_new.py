#!/usr/bin/env python
import rospy 
from std_msgs.msg import String 
import signal
import serial
import time
from gps3 import gps3
from math import radians, cos, sin, asin, sqrt
from geopy import distance
import pyproj
import socket
import sys
###############################Initialization#####################################################
g = pyproj.Geod(ellps='WGS84')
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
ser = serial.Serial(port='/dev/ttyTHS2',baudrate = 38400)
endlat=13.348009
endlong=74.792203

###############################Initialization ends################################################

class Trav:
    def __init__(self):
        self.latitude = None
        self.longitude = None
        self.imu = None

    def gps_callback(self, msg):
        self.latitude, self.longitude = str(msg.data).split(',')
	print(self.latitude, self.longitude)

    def heading_callback(self, msg):
        self.imu_val = msg.data

    def straight(self):
        stm_send='m3x4999y0000z'
        print ('Going straight')
        ser.write(stm_send.encode())
        ser.write(stm_send.encode())
    def anticlockwise(self):
        stm_send='m4x0000y4999z'
        print('Rotating anticlockwise')
        ser.write(stm_send.encode())
        ser.write(stm_send.encode())
    def clockwise(self):
        stm_send='m4x9999y4999z'
        print('Rotating clockwise')
        ser.write(stm_send.encode())
        ser.write(stm_send.encode())
    def backward(self):
        stm_send='m4x4999y9999z'    
        print('Going backward')
        ser.write(stm_send.encode())
        ser.write(stm_send.encode())
    def brute_stop(self):
        stm_send='m2x4999y4999z'
        print('Brute Stop')
        ser.write(stm_send.encode())
        ser.write(stm_send.encode())
    def get_heading(self):
	print(self.longitude,self.latitude)
        (az12, az21, dist) = g.inv(self.longitude, self.latitude, endlong, endlat)
        if az12<0:
            az12=az12+360
        return az12, dist

    def match_head(self):
        waypoint_heading,dist=self.get_heading()
        while True:
            heading_diff=self.imu_val-waypoint_heading
            print(self.imu_val,waypoint_heading,heading_diff)

            if self.imu_val < waypoint_heading+5 and self.imu_val>waypoint_heading-5:
                    #brute_stop()
                    break
            if heading_diff >=-180:
                    if heading_diff<=0:
                            self.clockwise()
            if heading_diff <-180:
                    self.anticlockwise()
            if heading_diff>=0:
                    if heading_diff<180:
                            self.turn = 2 
                            anticlockwise()             
            if heading_diff >= 180:
                    turn = 1
                    self.clockwise()

    def match_dist(self):
        self.match_head()
        waypoint_heading,waypoint_dist=self.get_heading()
        if waypoint_dist>5:
            self.straight()
        else:
            self.brute_stop()
            print('Reached')

##############################################Class ends#################################################                     

def exit_gracefully(sig, frame):
    t = Trav()
    t.brute_stop()
    rospy.signal_shutdown("Stop")

if __name__=='__main__':
    rospy.init_node('rover', disable_signals=True,)  
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)
    trav = Trav()
    rospy.Subscriber("coordinates",String,trav.gps_callback)
    rospy.Subscriber("heading",String,trav.heading_callback)
    trav.match_dist()
    rospy.spin()
