# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camera.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 768)
        MainWindow.setMouseTracking(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(1, 1, 1371, 741))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.mast_camera = App(self.widget)
        self.mast_camera.setObjectName("mast_camera")
        self.gridLayout.addWidget(self.mast_camera, 0, 0, 1, 1)
        self.axis_1 = axis_1(self.widget)
        self.axis_1.setObjectName("axis_1")
        self.gridLayout.addWidget(self.axis_1, 0, 1, 1, 1)
        self.motorcode = motor_Code(self.widget)
        self.motorcode.setObjectName("motorcode")
        self.gridLayout.addWidget(self.motorcode, 0, 2, 1, 1)
        self.axis_2 = axis_2(self.widget)
        self.axis_2.setObjectName("axis_2")
        self.gridLayout.addWidget(self.axis_2, 1, 0, 1, 1)
        self.axis_3 = axis_3(self.widget)
        self.axis_3.setObjectName("axis_3")
        self.gridLayout.addWidget(self.axis_3, 1, 1, 1, 1)
        self.axis_4 = axis_4(self.widget)
        self.axis_4.setObjectName("axis_4")
        self.gridLayout.addWidget(self.axis_4, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1366, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

from axis_1 import axis_1
from axis_2 import axis_2
from axis_3 import axis_3
from axis_4 import axis_4
from cam8 import App
from tcp_send import motor_Code
