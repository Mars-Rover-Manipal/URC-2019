#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def base_station():
	pub=rospy.Publisher("Travtop",String, queue_size=1)
	rospy.init_node("base_station",anonymous=True)
	rate=rospy.Rate(10)
	a=0000
	b=0000
	while not rospy.is_shutdown():
		str1="m4x"+str(a).zfill(4)+"y"+str(b).zfill(4)
		pub.publish(str1)
		#rospy.loginfo('Sent %s'%str1)
		print(str1) 
		rate.sleep()
		a=a+1
		b=b+1
		if a>=9999:
			a=a-9999
		if b>=9999:
			b=b-9999	
	pub.publish(str1)

if __name__=='__main__':
	try:
		base_station()
	except rospy.ROSInterruptException:
		pass		
