#!/usr/bin/env python
import rospy 
from std_msgs.msg import String 

def rewrite():
	pub=rospy.Publisher("rw",String, queue_size=1)
	rospy.init_node("rewrite",anonymous=True)
	rate=rospy.Rate(100)
	
	while not rospy.is_shutdown():
		str1=raw_input()
		print(type(str1)) 	
		pub.publish(str(str1))
		#rospy.loginfo('Sent %s'%str1)

if __name__=='__main__':
	try:
		rewrite()
	except rospy.ROSInterruptException:
		pass		
