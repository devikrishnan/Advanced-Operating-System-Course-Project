"""Copyright (C) 2021 @gayathri,@devikrishnan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

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
        colHeaders = ['Size in B']
        for n, key in enumerate(sorted(self.data.keys())):
            rowHeaders.append(key)
            newitem = QTableWidgetItem(str(self.data[key]))
            self.setItem(n, 0, newitem)
        self.setVerticalHeaderLabels(rowHeaders)
        self.setHorizontalHeaderLabels(colHeaders)
        self.horizontalHeader().setStretchLastSection(True) 
        
        

