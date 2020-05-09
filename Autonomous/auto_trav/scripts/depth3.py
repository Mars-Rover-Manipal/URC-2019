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
v_head=0
s_head=0

class image_converter:

  def __init__(self):
    self.bridge = CvBridge()

    self.image_sub = rospy.Subscriber("/camera/depth/image_rect_raw",Image,self.callback)
  def callback(self,data):
    try:
      data.encoding = 'bgr8'
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    median = cv2.medianBlur(cv_image,15)
    cv2.imshow("Image window", cv_image)
    cv2.imshow("Image ", median)

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
