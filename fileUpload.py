from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton,QHBoxLayout, QVBoxLayout, QApplication, QStackedWidget, QLabel, QToolBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import json

from HomeScreen import HomeScreen
from Navigation import Navigation
from mapCode import FileOpen
          

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.setWindowTitle('Map Analyzer')
        
        self.label3 = QtWidgets.QLabel()
        self.label3.setGeometry(QtCore.QRect(10, 210, 500, 23))
        self.label3.setObjectName("label3")
        
        self.btn_Action = QtWidgets.QPushButton()
        self.btn_Action.setGeometry(QtCore.QRect(220, 200, 75, 23))
        self.btn_Action.setObjectName("btn_Action")
        
        self.gridLayout3 = QtWidgets.QGridLayout()
        self.gridLayout3.addWidget(self.label3, 0, 3, 7, 8)
        self.gridLayout3.addWidget(self.btn_Action, 0, 3, 3, 3)
        
        self.btn_Action.setText("View Chart")        
        self.label3.setText('File Uploaded, check console for its contents')
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.currentChanged.connect(self.set_button_state)
        self.btn_Action.clicked.connect(self.next_page)
        
        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
     
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.btn_Action)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.stacked_widget)
        vbox.addLayout(hbox)
        
       
        #add the to the main window
        self.toolbar = QToolBar("Edit", self)
          
        h = HomeScreen(self)
        h.pushButton.clicked.connect(self.file_open)
        self.insert_page(h.centralwidget)
        
        self.addToolBar(self.toolbar)
        
        #start with the toolbar hidden
        self.toolbar.toggleViewAction().setChecked(True)
        self.toolbar.toggleViewAction().trigger()
        
        # create main layout
        widget.setLayout(vbox)

        
    def file_open(self):
        name, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', options=QtWidgets.QFileDialog.DontUseNativeDialog)
        chartData, navData = FileOpen.openFile(name)
        navigation = Navigation(chartData, navData , self)
        self.addToolBar(navigation.toolbar)
        self.insert_page(navigation.horizontalGroupBox)
      
        
    def set_button_state(self, index):
        n_pages = len(self.stacked_widget)
        self.btn_Action.setEnabled( index % n_pages < n_pages - 1)
        
        
    def insert_page(self, widget, index=-1):
        self.stacked_widget.insertWidget(index, widget)
        self.set_button_state(self.stacked_widget.currentIndex())
        

    def next_page(self):
        new_index = self.stacked_widget.currentIndex()+1
        if new_index < len(self.stacked_widget):
            self.stacked_widget.setCurrentIndex(new_index)
            self.toolbar.toggleViewAction().trigger()
    


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(1300,1000)
    w.show()
    sys.exit(app.exec_())
    
