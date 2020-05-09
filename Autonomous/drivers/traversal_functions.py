import serial 
#from magneto import get_imu_head
ser = serial.Serial(port='/dev/ttyS0',baudrate = 38400)
def straight():
	stm_send='m2x4999y0000'
	print ('Going straight')
	ser.write(stm_send.encode())
def anticlockwise():
	stm_send='m2x0000y4999'
	print('Rotating anticlockwise')
	ser.write(stm_send.encode())
def clockwise():
	stm_send='m2x9999y4999'
	print('Rotating clockwise')
	ser.write(stm_send.encode())
def backward():
	stm_send='m2x4999y9999'	
	print('Going backward')
	ser.write(stm_send.encode())
def brute_stop():
	stm_send='m2x4999y4999'
	print('Brute Stop')
	ser.write(stm_send.encode())
"""def clock_turn():
        h=get_imu_head()
        z=0
        while z-h <90:
                n=get_imu_head()
                if n<h:
                        z=360+n
                else:
                        z=n
                clockwise1()
                val=getball()
                if(val == "FOUND"):
                        brute_stop()
                        print(val,"Ball detected")
                        quit()
def anti_turn():
	h = get_imu_head()
	n = get_imu_head()
	if h>90:
		while abs(h-n)<90:
			anticlockwise()
			n =get_imu_head()
	else:
		while n>=0:
			anticlockwise()
			n=get_imu_head()
		while (360+h-n)<90:
			anticlockwise()
			n=get_imu_head()"""