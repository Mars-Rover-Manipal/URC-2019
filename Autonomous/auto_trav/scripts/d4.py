#!/usr/bin/env python
from __future__ import print_function
from collections import defaultdict
import roslib
roslib.load_manifest('auto_trav')
import sys
import rospy
import cv2
import numpy as np
import time
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String
r=l=0
class image_converter:

  def __init__(self):
    self.pubdist=rospy.Publisher("/kinect_data",String, queue_size=1)

    self.bridge = CvBridge()

    self.image_sub = rospy.Subscriber("/camera/depth/image_rect_raw",Image,self.callback)

  def callback(self,data):
    global r,l
    try:
      data.encoding = 'bgr8'
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    
    #print(cv_image.shape)
    lower_blue = np.array([0,0,0])
    upper_blue = np.array([40,255,255])
    cv_image=cv_image[70:320,0:640]
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((5,5),np.uint8)
    kernel2 = np.ones((5,5),np.uint8)
    #opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    res = cv2.bitwise_and(cv_image, cv_image, mask= mask)
    rgb = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
    res = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(res,50,255,cv2.THRESH_BINARY)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel2)
    cv2.imshow("Res",thresh)
    areadict=defaultdict(lambda:0)
    _,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    CX =list()
    CY = list()
    area = list()
    max_area = 0
    for i in range(len(contours)):
      cnt = contours[i]
      M = cv2.moments(cnt)
      if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
      else:
        # set values as what you need in the situation
        cx=int(0)
        cy=int(0) 
      CY.append(int(cy))  
      CX.append(int(cx))
      area.append(cv2.contourArea(cnt))	
    print(CX)
    print(CY)
    print(area)	
    if len(area)>0:
    	max_area = max(area)
    	ind=area.index(max_area) 
    	if CX[ind]<320 and area[ind]>200:
            r=r+1
	    if r>9:
	        print('Right')
      		self.pubdist.publish('right')
    	elif CX[ind]>320 and area[ind]>200: 
    	    l=l+1
	    if l>9:
	        print("Left")
      		self.pubdist.publish('left')
	    
    	else:
      	    print('Straight')
	    r=l=0
      	    self.pubdist.publish('straight')  
    else:
	r=l=0
	print('Straight')
      	self.pubdist.publish('straight')
    cv2.imshow("Image window", hsv)
    cv2.imshow("Image window2", cv_image)
    cv2.waitKey(3)
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
