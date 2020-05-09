import socket
import time
import pygame
from pygame import joystick
import math
import serial
from time import sleep
import os
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QPlainTextEdit
from PyQt5 import QtCore, QtGui
import sys
h=False
class Thread(QThread):
	changeText = pyqtSignal(str)
	def __init__(self, parent=None):
		QThread.__init__(self, parent=parent)
        
	
	def map1(self,x,in_min,in_max,out_min,out_max):
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
	
	def arm(self):
			
			m1=self.j.get_button(7)
			m2=self.j.get_button(6)
			m3=self.j.get_button(8)
			m4=self.j.get_button(8)
			m5=self.j.get_button(7)
			m6=self.j.get_button(9)
			m7=self.j.get_button(10)
			hat=self.j.get_hat(0)
			p=' '
			data="nM"
			if m1:
					p='2nd link'
					if hat[1]==1 :
						p='link 2 linear  up'
						data="nG"
					elif hat[1]==-1 :
						p='link 2 linear down'
						data="nH"
					
			elif m2:
					p='1st Link'
					if  hat[1]==-1:
							p='1st link linear down '
							data="nC"
					elif hat[1]==1:
							p='1st link linear up '
							data="nD"#actuator
					elif hat[0]==1:

							p='swivel clockwise '
							data="nK"
					elif hat[0]==-1:
							p='swivel anticlockwise '
							data="nL"#swivel
			elif m3:
					p='Pitch Roll'
					if hat[0]==1 :
							p='Roll clockwise '
							data="nJ"
					elif hat[0]==-1:
							p='Roll anticlockwise'
							data="nI"
					
					elif hat[1]==-1:
							p='Pitch up '
							data="nF"
					elif hat[1]==1:
							p='Pitch down'
							data="nE"
			elif m6:
					p='gripper'
					if hat[1]==-1:
							p='gripper open '
							data="nA"
					elif hat[1]==1:         
							p='gripper close'
							data="nB"
			
					
			
					
			elif m7:
					p='Allen'
					if hat[0]==1:

							p='Allen clockwise '
							data="nP"
					elif hat[0]==-1:
							p='Allen anticlockwise '
							data="nQ"#swivel

					
			else:
					p="N/A"
			pygame.display.set_caption('Motor {:2s} '.format(p))
			#print(p+data)
			self.changeText.emit(p+data)                
			self.transmit.send(data)
	
	def motorcode(self):
		global x1,y1,gear,h
		x1=self.j.get_axis(0)
		y1=self.j.get_axis(1)
		c1=self.j.get_button(6)
		c2=self.j.get_button(7)

		#print(x1,y1)
		gear=0
		gear=self.j.get_axis(3)

		hat=self.j.get_hat(0)

		gear=int(self.map1(gear,-1.0,1.0,9,0))
		x=self.map1(x1,-1.0,1.0,0.0,9999)
		y=self.map1(y1,-1.0,1.0,0.0,9999)
		
		zero=self.j.get_axis(2)
		if(zero>0.7):
				x=9999
				y=4999
		elif(zero<-0.7):
				x=0
				y=4999
	
		p=' '
	
		camera="z"
		if c1:
				p='Mast Yaw'
				if hat[1]==1:

						p='Mast Yaw clockwise '
						camera="b"
				elif hat[1]==-1:
						p='Mast Yaw anticlockwise '
						camera="a"
				p='Mast Pitch'
				if  hat[0]==-1:
						p='Mast Pitch down '
						camera="d"
				elif hat[0]==1:
						p='Mast Pitch up '
						camera="c"
	
		x=str(int(x)).zfill(4)
		y=str(int(y)).zfill(4)
		if self.j.get_button(4):
			sleep(0.2)
			if self.j.get_button(4):
				h=not h
		if h==True:
			hill='w'
		else:
			hill='m'
		val=hill+str(gear)+"x"+str(x)+"y"+str(y)+camera

		#clear()
		#print(val)
		self.changeText.emit(val)

		self.transmit.send(val)
		time.sleep(0.01)
	def run(self):

		count=0
		TCP_IP = '192.168.1.7'
		TCP_PORT = 5005
		BUFFER_SIZE = 1024

		self.transmit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.transmit.connect((TCP_IP, TCP_PORT))


		joystick.init()
		pygame.display.init()
		if pygame.joystick.get_count() == 0:
			self.changeText.emit("No joystick detected")
			exit(0)
		self.j=joystick.Joystick(0)
		self.j.init()            
		adx='a'
		ady='b'
		switch=True
		active=True
		
		try:
			while(1):    
					pygame.event.pump()
					#self.changeText.emit(self.transmit.recv(1024))
					on=self.j.get_button(1)
					if on:
							sleep(0.2)
							if self.j.get_button(1):
									if active==True:
											active=False
											self.changeText.emit('Idle')
									else:
											active=True
											self.changeText.emit('Active')

					if active:
							change=self.j.get_button(0)
							if change:
									sleep(0.2)
									if self.j.get_button(0):
											if switch==True:
													switch=False
													self.changeText.emit('Arm')
											else:
													switch=True
													self.changeText.emit('Motor')

							if switch:
								
								self.motorcode()
							else:
								
								self.arm()
		except KeyboardInterrupt:
			self.transmit.send('m4x4999y4999z')

class motor_Code(QWidget):
	EXIT_CODE_REBOOT = -123
	def __init__(self, parent=None):
		super(motor_Code, self).__init__(parent=parent)
		self.title = 'Motor Code'
		self.width = 320
		self.height = 100
		self.initUI()

	def initUI(self):
		self.label = QLabel(self)
		self.label.resize(320, 100)
		self.startButton = QPushButton(self)
		self.startButton.setGeometry(QtCore.QRect(0, 0, 85, 16))
		self.startButton.setObjectName("startButton")
		self.startButton.setText("Motor Code")
		self.startButton.clicked.connect(self.startThread)
		self.closeButton = QPushButton(self)
		self.closeButton.setObjectName("closeButton")
		self.closeButton.setText("Close")
		self.closeButton.setGeometry(QtCore.QRect(85, 0, 85, 16))
		self.closeButton.clicked.connect(self.closeWidget)
		self.textEdit = QLabel(self)
		self.textEdit.setGeometry(QtCore.QRect(0, 20, 320, 50))
		#self.textbr.setText("This string will be displayed")
	def startThread(self):
		self.th = Thread()
		self.th.start()
		self.th.changeText.connect(self.textEdit.setText)
	def closeWidget(self):
		
		os.execl(sys.executable, sys.executable, * sys.argv)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = motor_Code()
    ex.show()
    sys.exit(app.exec_())
	