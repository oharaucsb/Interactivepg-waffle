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



plotList = {}

imageList = []

def getKeyFromItem(item, dic):
    for k, v in dic.items():
        if v is item:
            return k


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
            plt = plotList["__LAST_FIG"]
        else:
            raise IndexError()
    except KeyError:
        plt = figure()
    if 'label' in kwargs:
        kwargs['name'] = kwargs['label']
    if 'name' in kwargs:
        legend()
    plt.plot(*args, **kwargs)
    return plt

def errorbar(*args, **kwargs):
    global qApp, plotList
    if qApp is None:
        qApp = QtGui.QApplication([])
    try:
        if not kwargs.pop("newFigure", False):
            plt = plotList["__LAST_FIG"]
        else:
            raise IndexError()
    except KeyError:
        plt = figure()
    if 'label' in kwargs:
        kwargs['name'] = kwargs['label']
    if 'name' in kwargs:
        legend()
    plt.errorbars(*args, **kwargs)
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
        plt = plotList["__LAST_FIG"]
    except KeyError:
        return
    plt.addLegend()
    # for curve in plt.plotItem.curves:
    #     plt.plotItem.legend.addItem(curve, curve.name())

def show():
    global qApp, plotList
    if qApp is not None:
        qApp.exec_()
        qApp = None
        plotList = {}

def plotDestroyed(plotWidget):
    global plotList
    try:
        # plotList.pop(plotList.index(plotWidget))
        del plotList[getKeyFromItem(plotWidget)]
    except IndexError:
        pass
    except Exception:
        print("Error removing plotWidget from list", plotWidget, plotList)

def imageDestroyed(*args, **kwargs):
    print("Image destroyed", args, kwargs)

def figure(*args, **kwargs):
    global qApp, plotList
    if qApp is None:
        qApp = QtGui.QApplication([])
    try:
        name = str(args[0])
    except:
        num = len(plotList)
        while str(num) in plotList:
            num +=1
        name = str(num)
    try:
        plt = plotList[name]
    except KeyError:
        plt = PlotContainerWindow()
        plotList[name] = plt
        try:
            int(name)
            plt.setWindowTitle("Figure {}".format(name))
        except ValueError:
            plt.setWindowTitle(name)
        plt.sigPlotClosed.connect(plotDestroyed)
        plt.show()
    plotList["__LAST_FIG"] = plt



    return plt