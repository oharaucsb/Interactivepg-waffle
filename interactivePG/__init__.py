import numpy as np
from PyQt5 import QtGui, QtCore
try:
    from .fixes import axisItemFix, legendItemFix, ItemSampleFix, PlotItemFix, linearRegionItemFix
except ImportError as e:
    print(("failed importing axisfixes", e))
    import sys
    print((sys.path))
    raise
import pyqtgraph as pg
from .packageSettings import config_options
from .images.imagePlot import image as ipimage
from .curves.clickablePlotWidget import ClickablePlotWidget as PlotWidget
from .plotContainerWindow import PlotContainerWindow
from .images.ImageViewWithPlotItemContainer import ImageViewWithPlotItemContainer as ImageView
pg.setConfigOption("foreground", config_options["foreground"])
pg.setConfigOption("background", config_options["background"])


plotList = {}

imageList = []

def getKeyFromItem(item, dic):
    for k, v in list(dic.items()):
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

    # how much does shit break with this?
    plotList["__LAST_FIG"] = img
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

def plotxyy(*args, **kwargs):
    """
    Helper function for passing an x and multiple y curves
    Currently accepts plotxyy(x, y[:,N]) or plot(data[:,N))
    where x:= data[:,0] and y[N-1]:= data[:,1:N]

    pass kwarg "names" (NOT "name") to give the plots names.

    :param args:
    :param kwargs:
    :return:
    """
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

    aargs = list(args)
    numnp = 0
    for arg in aargs:
        if isinstance(arg, np.ndarray) or isinstance(arg, list):
            numnp += 1
        else:
            break
    if numnp == 0:
        raise RuntimeError("Should be passing np.ndarray or list, got {}".format(type(arg[0])))
    if numnp == 1:
        datum = aargs.pop(0)
        x = datum[:,0]
        y = datum[:,1:]
    elif numnp == 2:
        x = aargs.pop(0)
        y = aargs.pop(0)
    else:
        x = aargs.pop(0)
        # Need to pop(1), not pop(ii) because otherwise it will pop an index, and use
        # the modified list for future pops, resulting in taking every-other item,
        # instead of sequential items.
        y = [aargs.pop(0) for ii in range(numnp-1)]

    args = tuple(aargs)
    # Need to transpose it to take slices along columns, not along rows
    y = np.array(y)
    names = kwargs.pop("names", None)
    if names is None:
        names = [None] * y.shape[1]
    else:
        legend()

    for idx, ydata in enumerate(y.T):
        plt.plot(x, ydata, *args, name=names[idx], **kwargs)
    return plt

def brazilPlot(*args, **kwargs):
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

    plt.brazilPlot(*args, **kwargs)
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

def yscale(mode='log'):
    p = plotList["__LAST_FIG"]
    p.setLogMode(y=mode=='log')
    return p

def xscale(mode='log'):
    p = plotList["__LAST_FIG"]
    p.setLogMode(x=mode=='log')
    return p

def ylim(*args, **kwargs):
    try:
        plt = plotList["__LAST_FIG"]
    except:
        return
    if kwargs.get("padding", None) is None:
        kwargs["padding"] = 0

    # Need to match matplotlib style to pyqtgraph.
    # matplotlib wants a list, pyqtgraph wants positional arguments
    if isinstance(args[0], list):
        args = list(args)
        args = args[0] + args[1:]
    # print "DEBUG: ylim:", args, kwargs
    plt.plotWidget.setYRange(*args, **kwargs)

def xlim(*args, **kwargs):
    try:
        plt = plotList["__LAST_FIG"]
    except:
        return
    if kwargs.get("padding", None) is None:
        kwargs["padding"] = 0
    plt.plotWidget.setXRange(*args, **kwargs)

def xlabel(text=None, units=None):
    try:
        plt = plotList["__LAST_FIG"]
    except:
        return
    plt.plotWidget.plotItem.setLabel("bottom", text=text, units=units)

def ylabel(text=None, units=None):
    try:
        plt = plotList["__LAST_FIG"]
    except:
        return
    plt.plotWidget.plotItem.setLabel("left", text=text, units=units)

def title(text=None, **kwargs):
    try:
        plt = plotList["__LAST_FIG"]
    except:
        return
    plt.plotWidget.plotItem.setTitle(text, **kwargs)

def legend(*args, **kwargs):
    global plotList
    try:
        plt = plotList["__LAST_FIG"]
    except KeyError:
        print("it's a key error")
        return
    return plt.addLegend()
    print(("added", plt))
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
        print(("Error removing plotWidget from list", plotWidget, plotList))

def imageDestroyed(*args, **kwargs):
    print(("Image destroyed", args, kwargs))

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

def addLine(*args, **kwargs):
    line = pg.InfiniteLine(*args, **kwargs)
    curPlot = gcf()
    curPlot.plotWidget.getPlotItem().addItem(line)
    return line

def getPreviousPen():
    """
    Returns the QPen which was used in the last plot
    Doesn't do symbols, though could and should,
    since it's all kept in the dataitem opts
    :return:
    """
    plotWin = gcf()
    return plotWin.plotWidget.plotItem.dataItems[-1].opts["pen"]

def gcf():
    return plotList["__LAST_FIG"]
    return plotList.get("__LAST_FIG", None)
