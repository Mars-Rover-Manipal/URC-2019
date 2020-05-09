from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_MainWindow 
import sys
endlat=[]
endlon=[]
n=0
class mywindow(QtWidgets.QMainWindow): 
    def __init__(self):    
        super(mywindow, self).__init__()        
        self.ui = Ui_MainWindow()        
        self.ui.setupUi(self)

        self.ui.PlotButton.clicked.connect(self.btnClicked)
        self.ui.chgEnd.clicked.connect(self.choosePoint)

    def btnClicked(self):
    	global endlat,endlon,n
        
        #locals()['self.ui.Latitude_{}'.format(i+1)]=0
        endlat=[float(self.ui.Latitude_1.text()),float(self.ui.Latitude_2.text()),float(self.ui.Latitude_3.text()),float(self.ui.Latitude_4.text()),float(self.ui.Latitude_5.text()),float(self.ui.Latitude_6.text()),0]
        endlon=[float(self.ui.Longitude_1.text()),float(self.ui.Longitude_2.text()),float(self.ui.Longitude_3.text()),float(self.ui.Longitude_4.text()),float(self.ui.Longitude_5.text()),float(self.ui.Longitude_6.text()),0]
        f=open('endlat.txt','w+')
        f.write(str(endlat[n:]))
        f.close()
        f=open('endlon.txt','w+')
        f.write(str(endlon[n:]))
        f.close()
    def choosePoint(self):
    	global n
    	n=n+1
    	if n==6:
    		n=0
 
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec_())