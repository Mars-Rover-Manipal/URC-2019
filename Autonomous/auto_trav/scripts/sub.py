#!/usr/bin/env python
import rospy
from vision_msgs.msg import Classification2D
from std_msgs.msg import String
count = 0
def callback(data):	
   global count 	
   conv_res=str((data.results)[0]).split() 
   rospy.init_node("ball",anonymous=True)
   pubball=rospy.Publisher("/ball_flag",String, queue_size=1)	
   if conv_res[1]=='0' and float(conv_res[3])>0.98:
	count=count+1
   else:
	count = 0
	pubball.publish('0')
	print('No Ball:',conv_res[3])
   if count >= 4 :
	pubball.publish('1')
	print('Ball:',conv_res[3])
		

def listener():
    rospy.init_node('ball', anonymous=True)
    rospy.Subscriber("/imagenet/classification", Classification2D, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
