import numpy as np
import pyqtgraph as pg
from .images.ImageViewWithPlotItemContainer import ImageViewWithPlotItemContainer
from .curves.clickablePlotWidget import ClickablePlotWidget
from PyQt4 import QtCore, QtGui


class PlotContainerWindow(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(PlotContainerWindow, self).__init__()
        self.plotWidget = kwargs.pop("plotWidget", None)
        if self.plotWidget is None:
            self.plotWidget = ClickablePlotWidget()
        self.setCentralWidget(self.plotWidget)
        self.plotWidget.sigMouseMoved.connect(self.updateMousePos)

        self.xPosStatus = QtGui.QLabel(self)
        self.xPosStatus.setText("x=")
        self.yPosStatus = QtGui.QLabel(self)
        self.yPosStatus.setText("y=")
        self.statusBar().addPermanentWidget(self.xPosStatus)
        self.statusBar().addPermanentWidget(self.yPosStatus)

        self.plotTools = QtGui.QToolBar()
        self.plotTools.setMovable(False)

        n=0
        for i in range(n, n+15):
            self.plotTools.addAction(QtGui.QApplication.style().standardIcon(i), '{}'.format(i))

        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.plotTools)

    def __getattr__(self, item):
        try:
            return getattr(self.plotWidget, item)
        except Exception as e:
            print("Does it not work like this?", item, e, self.plotWidget)
            print hasattr(self.plotWidget, item)

    def updateMousePos(self, pos):
        self.xPosStatus.setText("x={}".format(pos.x()))
        self.yPosStatus.setText("y={}".format(pos.y()))
































