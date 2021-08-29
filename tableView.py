from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
import sys


class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        print(data)
        self.setData()
        
    def setData(self): 
        rowHeaders = []
        colHeaders = ['Size']
        for n, key in enumerate(sorted(self.data.keys())):
            rowHeaders.append(key)
            newitem = QTableWidgetItem(str(self.data[key]/100))
            self.setItem(n, 0, newitem)
        self.setVerticalHeaderLabels(rowHeaders)
        self.setHorizontalHeaderLabels(colHeaders)
        self.horizontalHeader().setStretchLastSection(True) 
        
        

