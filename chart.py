from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *


class Chart(QWidget):
    def __init__(self, chartKey, data, parent=None):
        super(Chart, self).__init__(parent)
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
        self.chart.setTitle("Size Distribution")
        self.chart.setTheme(QChart.ChartThemeBlueCerulean)

        self.chartview = QChartView(self.chart)
        self.chartview.setRenderHint(QPainter.Antialiasing)
        
        
    def addSeries(self, key):
        self.chart.removeAllSeries()
        self.series = QPieSeries()
        self.series.setHoleSize(0.35)
            
        for key, value in self.data[key].items():
            print("adding series", str(key), value)
            slice_ = QPieSlice(str(key), value)
            self.series.append(slice_)
       
        self.chart.addSeries(self.series)
        self.series.doubleClicked.connect(self.handle_double_clicked)
         
             
          
    #Show the update chart with the distribution of the selected slice
    def handle_double_clicked(self, slice):
        slice.setExploded()
        slice.setLabelVisible()
     
        if slice.label() in self.data.keys():
            print("slice",slice.label());
            self.addSeries(slice.label())
           

