from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton,QHBoxLayout, QVBoxLayout, QApplication, QStackedWidget, QLabel, QGroupBox
import sys
import sip
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from tableView import TableView
from chart import Chart


'''json_data = {
  "Alloys":{
    "Aluminium":{
        "Magnaliuim":["magnesium", "aluminium"],
        "Hydronalium":["magnesium", "manganese", "aluminium"],
        "Duralumin":["copper", "aluminium"]
       },
    "Copper":{
         "Beryllium copper":["Beryllium", "copper"],
   	 "Billon":["gold", "copper"],
         "Copper tungsten":["Tungsten","copper"],
     }
}}'''

json_data = {
  "pie1":{
    "lib":{
        "libgcc":["magnesium", "aluminium"],
        "libc":["magnesium", "manganese", "aluminium"],
        "libmiosix":["copper", "aluminium"],
        "libstdc++":["Beryllium", "copper"],
       },
    "nonlib":{
         "Beryllium copper":["Beryllium", "copper"],
   	 "Billon":["gold", "copper"],
         "Copper tungsten":["Tungsten","copper"],
     }
}}





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


class Navigation(QtCore.QObject):
    clicked = QtCore.pyqtSignal(QtCore.QModelIndex)
    def __init__(self, data, parent=None):
        super(Navigation, self).__init__(parent)
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.actionTriggered.connect(self.on_actionTriggered)     
        self.model =  QtGui.QStandardItemModel(self)
        dict_to_model(self.model.invisibleRootItem(), json_data)
        it = self.model.item(0, 0)
        ix = self.model.indexFromItem(it)
        root_action = self.toolbar.addAction(it.text())
        root_action.setData(QtCore.QPersistentModelIndex(ix))
        self.listview = QtWidgets.QListView()
        self.listview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listview.clicked.connect(self.on_clicked)
        self.listview.setModel(self.model)
        self.listview.setRootIndex(ix)
        self.a = 10
        
        
        
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        
        
        
        self.gridLayout.addWidget(self.listview, 0, 0, 2, 1)
        
        self.frame = QtWidgets.QFrame()
        self.chart = Chart('pie1', data, self)
        
        
        
        self.ly = QtWidgets.QVBoxLayout()
        self.frame.setLayout(self.ly)
        
        #self.layout.addWidget(self.frame)
        #self.frame.hide()
        
        
        self.gridLayout1 = QtWidgets.QGridLayout()
        self.gridLayout1.addWidget(self.frame)
        
        self.gridLayout2 = QtWidgets.QGridLayout()
        self.gridLayout2.addWidget(self.chart.chartview)
        
        
        
        self.gridLayout.addLayout(self.gridLayout2, 0, 2, 0, 1)
        self.gridLayout.addLayout(self.gridLayout1, 0, 2, 0, 1)
        
       
        
        self.horizontalGroupBox = QGroupBox()
        self.horizontalGroupBox.setLayout(self.gridLayout)

        

    #make the listed items clickable
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_clicked(self, index):
        print('aaaaaaaaaaaaaa', self.a)
        if not self.model.hasChildren(index):
            self.clicked.emit(index)
            return
        action = self.toolbar.addAction(index.data())
        action.setData(QtCore.QPersistentModelIndex(index))
        self.listview.setRootIndex(index)
        print(index.data())
        self.chart.addSeries(index.data())
        
        
    #make the breadcrumbs clickable in order to go back and forth
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


