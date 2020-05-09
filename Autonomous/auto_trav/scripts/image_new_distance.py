#!/usr/bin/env python
from __future__ import print_function

import roslib
roslib.load_manifest('auto_trav')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

greenLower = (22, 68, 77)
greenUpper = (36, 235, 255)
 
class image_converter:

	def __init__(self):

		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/camera/rgb/image_color",Image,self.callback)
		self.distpub=rospy.Publisher("distance",String,queue_size=1)

	def callback(self,data):
		global greenUpper,greenLower
		try:
			data.encoding = 'bgr8'
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)
		hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, greenLower, greenUpper)
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
                center = None
                if len(cnts) > 0:
                        c = max(cnts, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        rect = cv2.minAreaRect(c)
                        rect = rect[1][0]*rect[1][1]
                        cir = 3.14*radius*radius
                        if rect + 100> cir and cir>350:
                                M = cv2.moments(c)
                                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                                cv2.circle(frame, (int(x), int(y)), int(radius),
                                           (0, 255, 255), 2)
                                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                                dist = (60*100)/(radius*2)
                                print ("Distance: ",dist-2)
				self.distpub.publish(str(dist-2))
			else:
				self.distpub.publish('3000')
		cv2.imshow("Image window", cv_image)
		cv2.waitKey(3)
		
	#try:
	  #self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "mono8"))
	#except CvBridgeError as e:
	  #print(e)

def main(args):
	ic = image_converter()
	rospy.init_node('image_converter', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
		cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv)
