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

#for the navigation bar on top
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton,QHBoxLayout, QVBoxLayout, QApplication, QStackedWidget, QLabel, QGroupBox
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import pyqtSlot,  Qt
from PyQt5.QtGui import *
import sys
import sip

from tableView import TableView
from chart import Chart


#converting the string from nav to model
def dict_to_model(item, d):
    if isinstance(d, dict):
        for k, v in d.items():
            it = QtGui.QStandardItem(k)
            item.appendRow(it)
            dict_to_model(it, v)
    elif isinstance(d, list):
        for v in d:
            dict_to_model(item, v)
    else:
        item.appendRow(QtGui.QStandardItem(str(d)))

#side list view
class Navigation(QtCore.QObject):
    clicked = QtCore.pyqtSignal(QtCore.QModelIndex)
    def __init__(self, chartData, navData , parent=None):
        super(Navigation, self).__init__(parent)
        print('navdata',navData)
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.actionTriggered.connect(self.on_actionTriggered)     
        self.model =  QtGui.QStandardItemModel(self)
        dict_to_model(self.model.invisibleRootItem(), navData)
        it = self.model.item(0, 0)
        ix = self.model.indexFromItem(it)
        root_action = self.toolbar.addAction(it.text())
        root_action.setData(QtCore.QPersistentModelIndex(ix))
        self.listview = QtWidgets.QListView()
        self.listview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listview.clicked.connect(self.on_clicked)
        self.listview.setModel(self.model)
        self.listview.setRootIndex(ix)
        
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        
        self.listview.setFixedWidth(350)
     
        self.gridLayout.addWidget(self.listview, 0, 0, 2, 1)
        
        self.frame = QtWidgets.QFrame()
        self.chart = Chart('map_file', chartData, self)
                     
        self.ly = QtWidgets.QVBoxLayout()
        self.frame.setLayout(self.ly)
                
        self.gridLayout1 = QtWidgets.QGridLayout()
        self.gridLayout1.addWidget(self.frame)
        
        self.gridLayout2 = QtWidgets.QGridLayout()
        self.gridLayout2.addWidget(self.chart.chartview)    #calling chart view
        
        self.gridLayout.addLayout(self.gridLayout2, 0, 2, 0, 1)
        self.gridLayout.addLayout(self.gridLayout1, 0, 2, 0, 1)  
        
        
        self.horizontalGroupBox = QGroupBox()
        self.horizontalGroupBox.setLayout(self.gridLayout)

        

    #make the listed items clickable
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_clicked(self, index):
        if not self.model.hasChildren(index):
            self.clicked.emit(index)
            return
        action = self.toolbar.addAction(index.data())
        action.setData(QtCore.QPersistentModelIndex(index))
        self.listview.setRootIndex(index)
        self.chart.addSeries(index.data())
        
       
    #make the breadcrumbs clickable in order to go back and forth
    #no children for object files, hence it is not listed in the nav bar
    @QtCore.pyqtSlot(QtWidgets.QAction)
    def on_actionTriggered(self, action):
        ix = action.data()
        self.chart.addSeries(ix.data())
        model = ix.model()
        self.listview.setRootIndex(QtCore.QModelIndex(ix))
        self.toolbar.clear()
        ixs = []
        while  ix.isValid():
            ixs.append(ix)
            ix = ix.parent()
        for ix in reversed(ixs):
            action = self.toolbar.addAction(ix.data())
            action.setData(ix)


