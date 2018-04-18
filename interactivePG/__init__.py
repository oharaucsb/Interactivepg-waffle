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
from .curves.PolarizationEllipseItem import PolarizationEllipseItem
from .plotContainerWindow import PlotContainerWindow, ManipulateWindow
from .images.ImageViewWithPlotItemContainer import ImageViewWithPlotItemContainer as ImageView
from .images.PolarImagePlot import PolarImageItem, PolarImagePlot
from .widgets.DelayEditor import DelayTimeEditor
from .widgets.LabviewSlider import LabviewSlider
from .items.DateAxis import DateAxis
pg.setConfigOption("foreground", config_options["foreground"])
pg.setConfigOption("background", config_options["background"])


plotList = {}

imageList = []

def getKeyFromItem(item, dic):
    for k, v in list(dic.items()):
        if v is item:
            return k


qApp = None

def _is_ipython():
    try:
        # If you're in an interactive ipython/jupyter console,
        # I don't want to conflict with their kernal, so don't do anything
        # to createa  new application.
        get_ipython
        return True
    except:
        return False

def startQApp():
    global qApp
    # try:
    #     # If you're in an interactive ipython/jupyter console,
    #     # I don't want to conflict with their kernal, so don't do anything
    #     # to createa  new application.
    #     get_ipython
    # except NameError:
    #     if qApp is None:
    #         qApp = QtGui.QApplication([])
    if qApp is None:
        qApp = QtGui.QApplication([])


def image(*args, **kwargs):
    global qApp, imageList
    startQApp()
    img = ipimage(*args, **kwargs)
    img.destroyed.connect(imageDestroyed)
    img.show()
    imageList.append(img)

    # how much does shit break with this?
    plotList["__LAST_FIG"] = img
    return img

def plot(*args, **kwargs):
    global qApp, plotList
    startQApp()
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
    startQApp()
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
    startQApp()
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
    startQApp()
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

def xticks(*args, **kwargs):
    """
    Set the tick spacing for the x.
    xticks(x1) sets the major/minor tick spacing to
    x1.
    xticks(x1, x2) sets the major/min spacing to x1/x2, resp.
    xticks([spacings]) gets passed to pyqtgraph.AxisItem.setTicks

    pass kwargs["applyBoth"] = False to prevent it from defaulting
    to applying the same characteristic for both sides
    :return:
    """
    fig = gcf()
    if fig is None: return
    axes = [fig.plotItem.axes["bottom"]["item"]]
    if kwargs.pop("applyBoth", True):
        axes.append(fig.plotItem.axes["top"]["item"])

    if len(args) == 1:
        if isinstance(args[0], int):
            for ax in axes:
                ax.setTickSpacing(args[0])
        else:
            for ax in axes:
                ax.setTicks(args[0])
    elif len(args)==2:
        for ax in axes:
            ax.setTickSpacing(args[0], args[1])

def yticks(*args, **kwargs):
    fig = gcf()
    if fig is None: return
    axes = [fig.plotItem.axes["left"]["item"]]
    if kwargs.pop("applyBoth", True):
        axes.append(fig.plotItem.axes["right"]["item"])

    if len(args) == 1:
        for ax in axes:
            ax.setTickSpacing(args[0], args[0])
    else:
        for ax in axes:
            ax.setTicks(args)

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
        if not _is_ipython():
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

def infiniteLine(*args, **kwargs):
    """
    convenience function to add an infinite line to a plot
    all args are passed to pyqtgraph.InfiniteLine

    Override to set the default pen. Should I do this?
    :param args:
    :param kwargs:
    :return:
    """
    if kwargs.get("pen", None) is None:
        kwargs["pen"] = pg.mkPen(config_options["infiniteLinePen"])
    line = pg.InfiniteLine(*args, **kwargs)
    fig = gcf()
    if fig is None: return
    fig.plotWidget.addItem(line)
    return line

def figure(*args, **kwargs):
    global qApp, plotList
    startQApp()
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

def getPreviousPen():
    """
    Returns the QPen which was used in the last plot
    Doesn't do symbols, though could and should,
    since it's all kept in the dataitem opts
    :return:
    """
    # plotWin = gcf()
    # return plotWin.plotWidget.plotItem.dataItems[-1]
    try:
        return gcc().opts["pen"]
    except AttributeError:
        # what is the best case here? Pass an empty pen?
        # pass none, and let the user handle it?
        # Define my own default pen in the settings, sicne
        # I think this would give no curve if plotted with
        return QtGui.QPen()

def gcc():
    """
    getCurrentCurve

    Get the last curve that was added to the  last plot plot

    :return: The last curve
    :rtype: pg.PlotDataItem
    """
    plotWin = gcf()
    try:
        return plotWin.plotWidget.plotItem.dataItems[-1]
    except IndexError:
        return None

def gcf():
    """
    Pop the last figure from the list.

    I don't 100% like how this is done, but I'm not sure of a better way at the moment
    :return:
    :rtype: ClickablePlotWidget
    """
    return plotList["__LAST_FIG"]
    return plotList.get("__LAST_FIG", None)

def gca(which="b"):
    """
    getCurrentAxes

    return the last axes.
    kwarg <which> specifies which axis (axes) to return:
       "b" bottom
       "t" top
       "l" left
       "r" right
      Chain them together to return multiple ones
       which = "tb"
      for both top and bottom axes

    :return: The specified axis. If multiple requested, return a list
       note: is it better to return a dict? Should the list order
       be the same as the input <which>'s order?
    :rtype: pg.AxisItem
    """
    if which.lower() == "bottom":
        which = "b"
    elif which.lower() == "top":
        which = "t"
    elif which.lower() == "left":
        which = "l"
    elif which.lower() == "right":
        which = "r"

    if len(which)>4:
        raise RuntimeError("Invalid axes request, should pass <b|t|l|r>, got {}".format(which))
    plotWin = gcf()
    if plotWin is None:
        return
    axesList = plotWin.plotItem.axes
    returnAxes = []
    which = which.lower()

    if "b" in which:
        returnAxes.append(axesList["bottom"]["item"])
    if "t" in which:
        returnAxes.append(axesList["top"]["item"])
    if "l" in which:
        returnAxes.append(axesList["left"]["item"])
    if "r" in which:
        returnAxes.append(axesList["right"]["item"])

    if len(returnAxes) == 1:
        return returnAxes[0]
    return returnAxes

def exportImage(plotObject, **kwargs):
    """
    Occassionally I want to save/export images from pyqtgraph, and it's easier to do
    programatically isntead of right clicking, etc.

    I'm dumping this here so I know the rough steps and can expand on it
    as I need it
    :param args:
    :param kwargs:
    :return:
    """
    from pyqtgraph.exporters import ImageExporter as E
    if isinstance(plotObject, pg.GraphicsScene):
        scene = plotObject
    elif isinstance(plotObject, PlotContainerWindow):
        scene = plotObject.plotWidget.plotItem.scene()
    elif hasattr(plotObject, "scene"):
        try:
            scene = plotObject.scene()
        except TypeError:
            scene = plotObject.scene
    else:
        print("I need a scene")

    e = E(scene)

    # e.export(copy=True)
    e.export(**kwargs)

def dirs(obj, st='', caseSensitive=False):
    """
    I very often want to do a search on the results of dir(), so
    do that more cleanly here
    :param obj: the object to be dir'd
    :param st: the strig to search
    :param caseSensitive: If False, compares .lower() for all, else doesn't
    :return: The results of dir() which contain st
    """
    if caseSensitive:
        return [ii for ii in dir(obj) if st in ii]
    return [ii for ii in dir(obj) if st.lower() in ii.lower()]

def manipulate(manipulateArgs, *args, **kwargs):
    """
    Make a Mathematica-style manipulate plot with sliders
    to change the values of a function.
    :param manipulateArgs:
    :param args:
    :param kwargs:
    :return:
    """
    global qApp, plotList
    startQApp()


    window = ManipulateWindow()
    window.plot(*args, **kwargs)



    window.setManipulators(manipulateArgs)


    window.show()

    plotList["__LAST_FIG"] = window
