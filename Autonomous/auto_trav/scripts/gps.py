#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import threading
import time
from gps3 import gps3
latitude=0
longitude=0
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
def pos_update():
    while True:
        global latitude,longitude
        print('here1')
        for new_data in gps_socket:
            if new_data:
                data_stream.unpack(new_data)
                global latitude,longitude
                latitude =  data_stream.TPV['lat']
                longitude =  data_stream.TPV['lon']
                if type(longitude) is type('sdas') or type(latitude) is type('sdas'):
                    continue
                else:
                    return latitude,longitude
def gpub():
    pubcor=rospy.Publisher("coordinates",String, queue_size=1)
    #publong=rospy.Publisher("longitude",String, queue_size=1)
    rospy.init_node("GPS",anonymous=True)
    rate=rospy.Rate(10)
    while not rospy.is_shutdown():
        latitude,longitude=pos_update()
        pubcor.publish(str(latitude)+','+str(longitude))
        rate.sleep()


if __name__=='__main__':
    try:
        gpub()
    except rospy.ROSInterruptException:
        pass    
