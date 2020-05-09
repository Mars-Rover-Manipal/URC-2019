#!/usr/bin/env python
import rospy 
from std_msgs.msg import String 
import serial 
ser=serial.Serial('/dev/ttyTHS2',baudrate=38400)
pubult=rospy.Publisher("/kinect_data",String,queue_size=1)
val='s'
count=0
def ultpub():
	global val,count
	while True:
		a=ser.read()
		print(a)
		if a==val:
			count+=1
		else:
			count=0
			val=a
		if count >=3:
			if a == 's':
				pubult.publish("straight")
			elif a == 'l':
				pubult.publish("left")
			elif a == 'r':
				pubult.publish("right")
			elif a == 'b':
				pubult.publish("backward")
		else:
			pubult.publish("straight")		

if __name__=='__main__':
	try:
		rospy.init_node("Ultrasonic",anonymous=True)
		ultpub()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		exit()
		
