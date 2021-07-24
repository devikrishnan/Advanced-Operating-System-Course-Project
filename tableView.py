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
        for n, key in enumerate(sorted(self.data.keys())):
        #for n, key in self.data.items():
            print('...................',key)
            rowHeaders.append(key)
            #for m, item in enumerate(self.data[key].values()):
            #for m, item in self.data.items():
            #for m, item in enumerate(self.data):
            #print(self.data[key])
            print(0, n, self.data[key])
            newitem = QTableWidgetItem(str(self.data[key]))
            self.setItem(n, 0, newitem)
        self.setVerticalHeaderLabels(rowHeaders)
        

