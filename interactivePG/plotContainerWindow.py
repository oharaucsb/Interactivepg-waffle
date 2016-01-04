import numpy as np
import pyqtgraph as pg
from .images.ImageViewWithPlotItemContainer import ImageViewWithPlotItemContainer
from .curves.clickablePlotWidget import ClickablePlotWidget
from PyQt4 import QtCore, QtGui


class BaseIcon(QtGui.QIcon):
    def __init__(self, *args, **kwargs):
        img = QtGui.QImage(200, 200, QtGui.QImage.Format_ARGB32)
        img.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter()
        painter.begin(img)
        self.drawIconPainter(painter, img.height(), img.width())
        painter.end()
        pxmap = QtGui.QPixmap.fromImage(img)
        super(BaseIcon, self).__init__(pxmap)

    def drawIconPainter(self, p, h, w):
        """
        :type p: QtGui.QPainter
        """
        raise NotImplementedError

class CrosshairIcon(BaseIcon):
    def drawIconPainter(self, p, h, w):
        """
        :type p: QtGui.QPainter
        """

        p.setPen(pg.mkPen('r', width=8))


        path = QtGui.QPainterPath()
        path.moveTo(w/2, h*.2)
        path.lineTo(w/2, h*.8)
        path.moveTo(w*.2, h/2)
        path.lineTo(w*.8, h/2)

        p.drawPath(path)

        return p

class FitFunctionIcon(BaseIcon):
    def drawIconPainter(self, p, height, width):
        """
        :type p: QtGui.QPainter
        """
        pen = QtGui.QPen(QtCore.Qt.red)
        pen.setWidth(15)
        p.setPen(pen)

        x = np.linspace(0, 2.5*np.pi, num=100)
        yorig = -np.sin(x) + x/(1*2.5*np.pi)
        yerr = np.random.normal(0, 0.25, size=len(x))

        y = yorig + yerr
        x = x/np.max(x) * width
        yorig -= np.min(y)
        y -= np.min(y)
        yorig = yorig/np.max(y) * height
        y = y/np.max(y) * height

        yorig = height - yorig
        y = height-y

        # add some padding
        x = x*0.6 + 0.2*width
        y = y*0.6 + 0.2*height

        # path = QtGui.QPainterPath()
        pnts = [ QtCore.QPointF(xi, yi) for (xi, yi) in zip(x[::5], y[::5])]
        lns = [QtCore.QPointF(xi, yi) for (xi, yi) in zip(x, yorig)]
        p.drawPoints(*pnts)

        pen.setColor(QtCore.Qt.black)
        pen.setWidth(8)
        p.setPen(pen)
        p.drawPolyline(*lns)

class AddFunctionIcon(BaseIcon):
    def drawIconPainter(self, p, h, w):
        """
        :type p: QtGui.QPainter
        """
        font = p.font()
        font.setPointSize(80)
        p.setFont(font)
        rect = QtCore.QRectF(w*0.2, h*0.2, w*0.6, h*0.6)
        p.drawText(rect, QtCore.Qt.AlignCenter, "f(x)")


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

        a = self.plotTools.addAction(CrosshairIcon(), 'Data Crosshairs')
        a.setCheckable(True)
        a.toggled.connect(self.togglePlotCrosshairs)

        a = self.plotTools.addAction(FitFunctionIcon(), 'Fit...')
        a.setCheckable(True)
        a.toggled.connect(self.toggleFitRegion)

        a = self.plotTools.addAction(AddFunctionIcon(), 'Add function...')
        a.setCheckable(True)
        a.toggled.connect(self.toggleFunctionLine)




        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.plotTools)

    def __getattr__(self, item):
        try:
            return getattr(self.plotWidget, item)
        except Exception as e:
            print("Does it not work like this?", item, e, self.plotWidget)
            print(hasattr(self.plotWidget, item))

    def updateMousePos(self, pos):
        self.xPosStatus.setText("x={}".format(pos.x()))
        self.yPosStatus.setText("y={}".format(pos.y()))

    def togglePlotCrosshairs(self, enabled):
        if enabled:
            for act in self.plotTools.actions():
                if act is self.sender(): continue
                act.setChecked(False)
            self.plotWidget.addCrosshairs()
        if not enabled:
            self.plotWidget.removeCrosshairs()

    def toggleFitRegion(self, enabled):
        if enabled:
            for act in self.plotTools.actions():
                if act is self.sender(): continue
                act.setChecked(False)
            self.plotWidget.addFitRegion()
        else:
            self.plotWidget.removeFitRegion()

    def toggleFunctionLine(self, enabled):
        if enabled:
            for act in self.plotTools.actions():
                # if act is self.sender(): continue
                act.setChecked(False)
            self.plotWidget.addFunctionLine()


































