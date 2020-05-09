from drivers.Gps import current_pos
from drivers.Imu import get_heading,match_head
from drivers.traversal_functions import straight,anticlockwise,clockwise,backward,brute_stop,clock_turn,anti_turn
from drivers.magneto import get_imu_head
from drivers.LidarClient import getlidar
from drivers.ballDetectClient import getball
from coordinate_file import get_coordinates
####List of coordinates###
endlat,endlot=get_coordinates()
TCP_IP1= '192.168.1.7'
TCP_PORT1 = 5008
BUFFER_SIZE1 = 1024
transmit1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transmit1.connect((TCP_IP1, TCP_PORT1))
TCP_IP2= '192.168.1.7'
TCP_PORT2= 5009
BUFFER_SIZE2= 1024
transmit2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transmit2.connect((TCP_IP2, TCP_PORT2))

def match_head():
    waypoint_heading,dist=get_heading()    
    while True:
        #waypoint_heading_opp=waypoint_heading+180
        imu_heading=get_imu_head()
        heading_diff=imu_heading-waypoint_heading
        print(imu_heading,waypoint_heading,heading_diff)
        detect()

        if imu_heading < waypoint_heading+10 and imu_heading>waypoint_heading-10:
                #brute_stop()
                break
        if heading_diff >=-180:
                if heading_diff<=0:
                		val="c"
                		transmit1.send(c.encode())
                        clockwise()
        if heading_diff <-180:
        		val="a"
                transmit1.send(c.encode())
                anticlockwise()
        if heading_diff>=0:
                if heading_diff<180:
                        turn = 2
                        val="a"
                		transmit1.send(c.encode()) 
                        anticlockwise()             
        if heading_diff >= 180:
                turn = 1
                val="c"
                transmit1.send(c.encode())
                clockwise()
    
def matchdist():
        while True:
            match_head()
            waypoint_heading,waypoint_dist=get_heading()
            if waypoint_dist>3:
                print('Matching Distance',waypoint_dist)
                val="s"
                transmit1.send(c.encode())
                straight()
                detect()
            else:
            	val="p"
                transmit1.send(c.encode())
                brute_stop()
                break
def obstacle_avoidance():
	while True:
		flag=True
		lidar_left,lidar_right=getlidar()
		if lidar_left>150 and lidar_right>150:
			val="s"
            transmit2.send(c.encode())
			straight()
		elif lidar_left<150 and lidar_right>150:
			val="a"
            transmit2.send(c.encode())
			anticlockwise()
		elif lidar_left>150 and lidar_right<150:
			val="c"
            transmit2.send(c.encode())
			clockwise()
		else:
			brute_stop()
			val="p"
            transmit2.send(c.encode())
			flag = False
		start=time.time()	
		while time.time()-start<5:
			if flag:
				straight()
				val="s"
                transmit2.send(c.encode())
			else:
				val="b"
                transmit2.send(c.encode())
				backward()	


