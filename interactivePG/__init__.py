import numpy as np
from PyQt4 import QtGui, QtCore
try:
    from . import axisItemFix
except ImportError:
    import sys
    print(sys.path)
import pyqtgraph as pg
from .packageSettings import config_options
from .images.imagePlot import image as ipimage
from .curves.clickablePlotWidget import ClickablePlotWidget as PlotWidget
from .plotContainerWindow import PlotContainerWindow
pg.setConfigOption("foreground", config_options["foreground"])
pg.setConfigOption("background", config_options["background"])



plotList = []
imageList = []

qApp = None


def image(*args, **kwargs):
    global qApp, imageList
    if qApp is None:
        qApp = QtGui.QApplication([])
    img = ipimage(*args, **kwargs)
    img.destroyed.connect(imageDestroyed)
    img.show()
    imageList.append(img)
    return img

def plot(*args, **kwargs):
    global qApp, plotList
    if qApp is None:
        qApp = QtGui.QApplication([])
    try:
        if not kwargs.pop("newFigure", False):
            plt = plotList[-1]
        else:
            raise IndexError()
    except IndexError:
        # plt = PlotWidget()
        plt = PlotContainerWindow()
        plotList.append(plt)
        plt.sigPlotClosed.connect(plotDestroyed)
        plt.show()
    plt.plot(*args, **kwargs)
    return plt

def semilogy(*args, **kwargs):
    p = plot(*args, **kwargs)
    p.setLogMode(x=False, y=True)
    return p

def semilogx(*args, **kwargs):
    p = plot(*args, **kwargs)
    p.setLogMode(x=True, y=False)
    return p

def loglog(*args, **kwargs):
    p = plot(*args, **kwargs)
    p.setLogMode(x=True, y=True)
    return p

def legend(*args, **kwargs):
    global plotList
    try:
        plt = plotList[-1]
    except IndexError:
        return
    plt.addLegend()
    for curve in plt.plotItem.curves:
        plt.plotItem.legend.addItem(curve, curve.name())


def show():
    global qApp
    if qApp is not None:
        qApp.exec_()
        qApp = None

def plotDestroyed(plotWidget):
    global plotList
    try:
        plotList.pop(plotList.index(plotWidget))
    except IndexError:
        pass
    except Exception:
        print("Error removing plotWidget from list", plotWidget, plotList)

def imageDestroyed(*args, **kwargs):
    print("Image destroyed", args, kwargs)

def figure(*args, **kwargs):
    plot(newFigure=True)