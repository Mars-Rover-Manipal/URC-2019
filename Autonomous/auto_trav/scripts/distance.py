#!/usr/bin/env python
import numpy as np
import cv2
import rospy
greenLower = (20,75,104)
greenUpper = (43,158,255)
camera = cv2.VideoCapture(1)

while True:
	(grabbed, frame) = camera.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
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
 		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
camera.release()
cv2.destroyAllWindows()
