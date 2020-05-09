#!/usr/bin/env python
import rospy 
from std_msgs.msg import String 
def callback(data):
	print("Recieved ",data.data)

def re():
	rospy.init_node('re',anonymous=True)
	rospy.Subscriber("rw",String,callback)
	rospy.spin()

if __name__=='__main__':
	re()
