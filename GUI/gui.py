# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(301, 374)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Plotting = MyWidget(self.centralwidget)
        self.Plotting.setGeometry(QtCore.QRect(0, 90, 301, 281))
        self.Plotting.setStyleSheet("")
        self.Plotting.setObjectName("Plotting")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(-1, 0, 231, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Latitude_1 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.Latitude_1.setFont(font)
        self.Latitude_1.setText("")
        self.Latitude_1.setObjectName("Latitude_1")
        self.gridLayout.addWidget(self.Latitude_1, 0, 0, 1, 1)
        self.Longitude_1 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.Longitude_1.setFont(font)
        self.Longitude_1.setText("")
        self.Longitude_1.setObjectName("Longitude_1")
        self.gridLayout.addWidget(self.Longitude_1, 0, 1, 1, 1)
        self.Latitude_2 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.Latitude_2.setFont(font)
        self.Latitude_2.setText("")
        self.Latitude_2.setObjectName("Latitude_2")
        self.gridLayout.addWidget(self.Latitude_2, 0, 2, 1, 1)
        self.Longitude_2 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.Longitude_2.setFont(font)
        self.Longitude_2.setText("")
        self.Longitude_2.setObjectName("Longitude_2")
        self.gridLayout.addWidget(self.Longitude_2, 0, 3, 1, 1)
        self.Latitude_3 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.Latitude_3.setFont(font)
        self.Latitude_3.setText("")
        self.Latitude_3.setObjectName("Latitude_3")
        self.gridLayout.addWidget(self.Latitude_3, 1, 0, 1, 1)
        self.Longitude_3 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.Longitude_3.setFont(font)
        self.Longitude_3.setText("")
        self.Longitude_3.setObjectName("Longitude_3")
        self.gridLayout.addWidget(self.Longitude_3, 1, 1, 1, 1)
        self.Latitude_4 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.Latitude_4.setFont(font)
        self.Latitude_4.setText("")
        self.Latitude_4.setObjectName("Latitude_4")
        self.gridLayout.addWidget(self.Latitude_4, 1, 2, 1, 1)
        self.Longitude_4 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.Longitude_4.setFont(font)
        self.Longitude_4.setText("")
        self.Longitude_4.setObjectName("Longitude_4")
        self.gridLayout.addWidget(self.Longitude_4, 1, 3, 1, 1)
        self.Latitude_5 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.Latitude_5.setFont(font)
        self.Latitude_5.setText("")
        self.Latitude_5.setObjectName("Latitude_5")
        self.gridLayout.addWidget(self.Latitude_5, 2, 0, 1, 1)
        self.Longitude_5 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.Longitude_5.setFont(font)
        self.Longitude_5.setText("")
        self.Longitude_5.setObjectName("Longitude_5")
        self.gridLayout.addWidget(self.Longitude_5, 2, 1, 1, 1)
        self.Latitude_6 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.Latitude_6.setFont(font)
        self.Latitude_6.setText("")
        self.Latitude_6.setObjectName("Latitude_6")
        self.gridLayout.addWidget(self.Latitude_6, 2, 2, 1, 1)
        self.Longitude_6 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.Longitude_6.setFont(font)
        self.Longitude_6.setText("")
        self.Longitude_6.setObjectName("Longitude_6")
        self.gridLayout.addWidget(self.Longitude_6, 2, 3, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(225, 0, 81, 66))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.PlotButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.PlotButton.setObjectName("PlotButton")
        self.verticalLayout.addWidget(self.PlotButton)
        self.chgEnd = QtWidgets.QPushButton(self.layoutWidget1)
        self.chgEnd.setObjectName("chgEnd")
        self.verticalLayout.addWidget(self.chgEnd)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.Latitude_1, self.Longitude_1)
        MainWindow.setTabOrder(self.Longitude_1, self.Latitude_2)
        MainWindow.setTabOrder(self.Latitude_2, self.Longitude_2)
        MainWindow.setTabOrder(self.Longitude_2, self.Latitude_3)
        MainWindow.setTabOrder(self.Latitude_3, self.Longitude_3)
        MainWindow.setTabOrder(self.Longitude_3, self.Latitude_4)
        MainWindow.setTabOrder(self.Latitude_4, self.Longitude_4)
        MainWindow.setTabOrder(self.Longitude_4, self.Latitude_5)
        MainWindow.setTabOrder(self.Latitude_5, self.Longitude_5)
        MainWindow.setTabOrder(self.Longitude_5, self.Latitude_6)
        MainWindow.setTabOrder(self.Latitude_6, self.Longitude_6)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Plotting"))
        self.Latitude_1.setPlaceholderText(_translate("MainWindow", "Latitude"))
        self.Longitude_1.setPlaceholderText(_translate("MainWindow", "Longitude"))
        self.Latitude_2.setPlaceholderText(_translate("MainWindow", "Latitude"))
        self.Longitude_2.setPlaceholderText(_translate("MainWindow", "Longitude"))
        self.Latitude_3.setPlaceholderText(_translate("MainWindow", "Latitude"))
        self.Longitude_3.setPlaceholderText(_translate("MainWindow", "Longitude"))
        self.Latitude_4.setPlaceholderText(_translate("MainWindow", "Latitude"))
        self.Longitude_4.setPlaceholderText(_translate("MainWindow", "Longitude"))
        self.Latitude_5.setPlaceholderText(_translate("MainWindow", "Latitude"))
        self.Longitude_5.setPlaceholderText(_translate("MainWindow", "Longitude"))
        self.Latitude_6.setPlaceholderText(_translate("MainWindow", "Latitude"))
        self.Longitude_6.setPlaceholderText(_translate("MainWindow", "Longitude"))
        self.PlotButton.setText(_translate("MainWindow", "Plot"))
        self.chgEnd.setText(_translate("MainWindow", "Next Co-ods"))

from RPi_data import MyWidget
import xz_rc
