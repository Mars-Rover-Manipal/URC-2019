from PyQt5 import QtCore, QtGui, QtWidgets
from gui1 import Ui_MainWindow 
from PyQt5.QtWidgets import QApplication
import sys
endlat=[]
endlon=[]
n=0
class mywindow(QtWidgets.QMainWindow): 
    def __init__(self):    
        super(mywindow, self).__init__()        
        self.ui = Ui_MainWindow()        
        self.ui.setupUi(self)
        

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec_())