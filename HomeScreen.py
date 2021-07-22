from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton,QHBoxLayout, QVBoxLayout, QApplication, QStackedWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *


class HomeScreen(QtCore.QObject):
    def __init__(self, a, parent=None):
        super(HomeScreen, self).__init__(parent)
        self.centralwidget = QtWidgets.QWidget()
        
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
        self.label1 = QtWidgets.QLabel()
        self.label1.setText('Welcome to PyQt5 example')
        self.label1.setAutoFillBackground(True)
        self.label1.setFont(QtGui.QFont("Times", 20,weight=QtGui.QFont.Bold))
        self.label1.setAlignment(Qt.AlignCenter)
        
        self.label3 = QtWidgets.QLabel()
        self.label3.setGeometry(10, 210, 500, 23)
        self.label3.setObjectName("label3")
        
        self.gridLayout1 = QtWidgets.QGridLayout()
        self.gridLayout1.addWidget(self.label1, 0, 0)
        
        self.frame = QtWidgets.QFrame()
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.gridLayout2 = QtWidgets.QGridLayout()
        self.gridLayout2.setObjectName("gridLayout2")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout2.addWidget(self.label_2, 0, 0, 0, 1)
        
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout2.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout2.addWidget(self.pushButton, 0, 2, 1, 1)
        
        self.gridLayout.addLayout(self.gridLayout2, 0, 0, 7, 2)
        self.gridLayout.addLayout(self.gridLayout1, 0, 0, 1, 2)
        
        self.label_2.setText("File Name")
        self.pushButton.setText("Browse")
        
 
