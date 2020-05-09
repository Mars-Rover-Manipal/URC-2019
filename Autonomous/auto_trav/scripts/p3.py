#!/usr/bin/env python
import pyrealsense2 as rs
import rospy
from std_msgs.msg import String
lsum=0
rsum=0
val="Straight"
def distfunc():
	global rsum,lsum,val
	try:
	    pipeline = rs.pipeline()
	    pipeline.start()

	    while True:
	        frames = pipeline.wait_for_frames()
	        depth = frames.get_depth_frame()
	        if not depth: continue
	        distmat = [[0 for x in range(480)] for y in range(640)]
	        for y in range(480):
	            for x in range(640):
	                dist = depth.get_distance(x, y)
	                if 0 < dist and dist < 2:
	                    distmat[x][y]=1
	        for y in range(480):
	        	for x in range(320):
	        		lsum=lsum+distmat[x][y]
	        for y in range(480):
	        	for x in range(321,640):
	        		rsum=rsum+distmat[x][y]	        
	        print(lsum,rsum)
	        if lsum>rsum+1000:
	        	pubdist.publish("right")
			val="Right"
	        elif rsum>lsum+1000:
	        	pubdist.publish("left")
			val="Left"
	        else:
	        	pubdist.publish("straight")
			val="Straight"
		print(val)

	        lsum=0
	        rsum=0
	except Exception as e:
		print(e)
		pass

if __name__=='__main__':
	pubdist=rospy.Publisher("/kinect_data",String, queue_size=1)
	rospy.init_node("Obstacle_avoidance_node",anonymous=True)
	try:
		distfunc()
	except rospy.ROSInterruptException:
		pass    
