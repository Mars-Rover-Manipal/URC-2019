from PyQt5 import QtCore, QtWidgets, QtGui
import pyqtgraph as pg
import numpy as np
import socket
import pyproj
from pyqtgraph import functions as fn
from gps3 import gps3
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import cv2
from PIL import Image

g = pyproj.Geod(ellps='WGS84')
TCP_IP = '192.168.1.70'
TCP_PORT = 5005
transmit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transmit.connect((TCP_IP, TCP_PORT))
# img = Image.open( "logo.tiff" )
# img = img.rotate(-90)  
# img = img.transpose(Image.FLIP_LEFT_RIGHT)
# img.load()
# logo = np.asarray( img, dtype="int32" )


x=[]
y=[]
endlat=[13.3500460]
endlon=[74.7916420]

#endlat=[13.3498887]
#endlon=[74.7915768]

#endlat=[13.3503957]
#endlon=[74.7915252]
#print(endlat,endlon)
#endlat=[13.3506374]
#endlon=[74.7917847]

# endlat=[13.3501817]
# endlon=[74.7912211]

# endlat=[13.3496607]
# endlon=[74.7915165]

def get_heading(longitude, latitude):
        global endlat, endlon
        (az12, az21, dist) = g.inv(longitude, latitude, endlon, endlat)
        if az12<0:
            az12=az12+360
        return az12, dist

class CenteredArrowItem(pg.ArrowItem):
    def setStyle(self, **opts):
        # http://www.pyqtgraph.org/documentation/_modules/pyqtgraph/graphicsItems/ArrowItem.html#ArrowItem.setStyle
        self.opts.update(opts)

        opt = dict([(k,self.opts[k]) for k in ['headLen', 'tipAngle', 'baseAngle', 'tailLen', 'tailWidth']])
        tr = QtGui.QTransform()
        path = fn.makeArrowPath(**opt)
        tr.rotate(self.opts['angle'])
        p = -path.boundingRect().center()
        tr.translate(p.x(), p.y())
        self.path = tr.map(path)
        self.setPath(self.path)

        self.setPen(fn.mkPen(self.opts['pen']))
        self.setBrush(fn.mkBrush(self.opts['brush']))

        if self.opts['pxMode']:
            self.setFlags(self.flags() | self.ItemIgnoresTransformations)
        else:
            self.setFlags(self.flags() & ~self.ItemIgnoresTransformations)
class MyWidget(pg.GraphicsWindow):
    

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent=parent)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100) # in milliseconds
        self.timer.start()
        self.timer.timeout.connect(self.onNewData)


        self.plotItem = self.addPlot(title="GPS Plotting")
        self.plotItem.setAspectLocked(lock=True, ratio=1)
        self.plotDataItem = self.plotItem.plot([], size=0, pen=None, symbolPen=None, symbolSize=10, symbol='o', symbolBrush=(255,255,255,10))
        
        self.plotDataItem1 = self.plotItem.plot([0,0], size=10, pen=None,symbol='o', symbolBrush=(255,0,0,255))
        #self.plotDataItem1.addLegend()
        #legend.setParentItem(plotItem)

        self.arrow = CenteredArrowItem(angle=0, tipAngle=40, baseAngle=50, headLen=80, tailLen=None, brush=None)

        # self.proxy = QtGui.QGraphicsProxyWidget()
        # self.im1 = pg.ImageView()
        # self.im1.setImage(logo)
        # self.proxy.setWidget(self.im1)
        # self.addItem(self.proxy)
        # self.im1.ui.histogram.hide()
        # self.im1.ui.menuBtn.hide()
        # self.im1.ui.roiBtn.hide()

        # self.proxy1 = QtGui.QGraphicsProxyWidget()
        # self.textbox = QLineEdit(self)
        # self.proxy1.setWidget(self.textbox)
        # self.addItem(self.proxy1)        


    def setData(self, x, y):
        global endlat,endlon
        self.plotDataItem.setData(x[len(x)-1000:], y[len(x)-1000:])
        f=open('endlat.txt','r+')
        endlat=(f.read())
        f.close()
        f=open('endlon.txt','r+')
        endlon=(f.read())
        f.close()
        endlon=[float(endlon[1:].partition(",")[0])]
        endlat=[float(endlat[1:].partition(",")[0])]
        self.plotDataItem1.setData(endlon,endlat, size=10, pen=None,symbol='o', symbolBrush=(255,0,0,255))

    

    def onNewData(self):
      global x,y,endlat,endlon
      latitude,longitude,angle=transmit.recv(1024).split(',')
      transmit.send("a")
      print(latitude,longitude,angle)        
      y.append(latitude)
      x.append(longitude)
      self.setData(x, y)
      self.plotItem.removeItem(self.arrow)
      self.arrow = CenteredArrowItem(angle=int(angle)/2+45, tipAngle=40, baseAngle=40, headLen=40, tailLen=None, brush=None)
      adjusted_angle,distance = get_heading(longitude,latitude)
      self.plotItem.setTitle('Distance: '+str(round(distance[0],3))+'   Angle: '+str(int(adjusted_angle)-int(angle)))
      self.arrow.setPos(float(longitude),float(latitude))        
      self.plotItem.addItem(self.arrow)
      #self.scene.addLine(QLineF(x1, y1, x2, y2))



def main():
    app = QtWidgets.QApplication([])

    pg.setConfigOptions(antialias=True) # True seems to work as well

    win = MyWidget()
    win.show()
    win.resize(800,600) 
    
    win.raise_()
    app.exec_()

if __name__ == "__main__":
    main()
