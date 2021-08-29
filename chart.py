from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

from tableView import TableView


class Chart(QWidget):
    def __init__(self, chartKey, data, frame, parent=None):
        super(Chart, self).__init__(parent)
        self.frame = frame
        self.data = data
        self.create_chart(chartKey)
      
        
    def create_chart(self, chartKey):
        self.series = QPieSeries()
        self.series.setHoleSize(0.35)
        self.chart = QChart()
        
        #Add series to the chart
        self.addSeries(chartKey)

	# for the background and title
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitle("Code Size Visualizer")
        self.chart.setTheme(QChart.ChartThemeBlueCerulean)

        self.chartview = QChartView(self.chart)
        self.chartview.setRenderHint(QPainter.Antialiasing)
        
        
    def addSeries(self, key):
        self.chart.removeAllSeries()
        self.series = QPieSeries()
        self.series.setHoleSize(0.35)
        
        
        #Show chartview only if the content length is less than 6. Otherwise show a table view    
        if len(self.data[key]) < 6:
            for key, value in self.data[key].items():
                slice_ = QPieSlice(str(key), value)
                self.series.append(slice_)
       
            self.series.setLabelsVisible()
            self.series.setLabelsPosition(QPieSlice.LabelInsideNormal )
            
            for slice in self.series.slices():
                #slice.setLabel(slice.label())
                slice.setLabel(slice.label()+ ' - ' + str(slice.value()/1000) + ' KB ')
                self.label3 = QtWidgets.QLabel()
                self.label3.setGeometry(QtCore.QRect(10, 210, 500, 23))
                self.label3.setText('File Uploaded, check console for its contents')



            self.chart.addSeries(self.series)
            self.frame.frame.hide()
            self.chart.show()
        else:
            self.table = TableView(self.data[key], len(self.data[key]), 1)
     
            if self.frame.ly.count() > 0:
                self.frame.ly.itemAt(0).widget().setParent(None)
            
            self.frame.ly.addWidget(self.table)
            
            self.frame.frame.show()
            self.chart.hide()         
             
          
