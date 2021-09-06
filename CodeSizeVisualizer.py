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
        
        self.setWindowTitle('Code Size Visualizer')
        
        self.stacked_widget = QStackedWidget() #to show different pages
        self.stacked_widget.currentChanged.connect(self.set_button_state)
        
        
        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
     
        vbox = QVBoxLayout()
        vbox.addWidget(self.stacked_widget)
        
        
        #add the to the main window
        self.toolbar = QToolBar("Edit", self)
          
        #on file upload chart button gets enables and upon pressing it goes to next page  
        h = HomeScreen(self) #calling this first
        self.chartBtn = h.viewChartBtn
        self.lineEdit = h.lineEdit
        self.chartBtn.clicked.connect(self.next_page)
        h.pushButton.clicked.connect(self.file_open)
        self.insert_page(h.centralwidget)
        
        self.addToolBar(self.toolbar)
        
        #start with the toolbar hidden
        self.toolbar.toggleViewAction().setChecked(True)
        self.toolbar.toggleViewAction().trigger()
        
        # create main layout
        widget.setLayout(vbox)

    #FILE OPEN    
    def file_open(self):
        name, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', "", "*.map",options=QtWidgets.QFileDialog.DontUseNativeDialog)
        self.lineEdit.setText(name)
        chartData, navData = FileOpen.openFile(name)
        navigation = Navigation(chartData, navData , self)
        self.addToolBar(navigation.toolbar)
        self.insert_page(navigation.horizontalGroupBox)
      
        
    def set_button_state(self, index):
        n_pages = len(self.stacked_widget)
        self.chartBtn.setEnabled( index % n_pages < n_pages - 1)
        
        
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
    w.showMaximized()
    w.show()
    sys.exit(app.exec_())
    
