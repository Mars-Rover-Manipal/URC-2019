import sys
import cv2
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
import datetime
from PyQt5 import QtCore

class axis_4(QWidget):
    def __init__(self, parent=None):
        super(axis_4, self).__init__(parent=parent)
        self.title = 'Axis Camera 4'
        
        self.width = 453
        self.height = 367
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(453,367)
        # create a label
        # create a label
        self.label = QLabel(self)        
        self.label.resize(453, 367)
        self.label1 = QLabel(self)
        #self.label1.move(453, 367)

        self.axis = QPushButton(self)
        self.axis.setGeometry(QtCore.QRect(0, 0, 85, 16))
        self.axis.setObjectName("axis")
        self.axis.setText("Axis 4")
        self.axis.clicked.connect(self.startThread)
        self.closeButton = QPushButton(self)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setText("Close")
        self.closeButton.setGeometry(QtCore.QRect(85, 0, 85, 16))
        self.closeButton.clicked.connect(self.closeWidget)
        
    def startThread(self):
        self.th = Thread(self)
        self.th.changePixmap.connect(self.label.setPixmap)
        self.th.changeLabel.connect(self.label1.setText)
        self.th.start()

    def closeWidget(self):
        self.close()
        
class Thread(QThread):
    changePixmap = pyqtSignal(QPixmap)
    changeLabel = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        
        

    def run(self):
        cap = cv2.VideoCapture('http://root:mrm@192.168.1.90/axis-cgi/mjpg/video.cgi?camera=4')#'rtsp://192.168.1.8/user=admin&password=&channel=1&stream=0.sdp?real_stream--rtp-caching=1')

        while self.isRunning:

            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
                p = convertToQtFormat.scaled(453, 367)#), Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                now = datetime.datetime.now()
                sec = now.second
                self.changeLabel.emit(str(sec))
        #btn.clicked.connect(self.buttonClicked)
    def buttonClicked(self):
        os.system(cmd)
        QtCore.QCoreApplication.instance().quit()


    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = axis_1()
    ex.show()
    sys.exit(app.exec_())
