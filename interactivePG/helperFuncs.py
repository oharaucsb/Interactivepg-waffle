import numpy as np
import pyqtgraph as pg
import re
from pyqtgraph.graphicsItems.ScatterPlotItem import Symbols
from .packageSettings import *

def plotArgsParser(*args):
    """
    Take the args passed to a pg.plot command
    to determine if things what things look like
    use regex to compare to possible

    Need to remove this string from the args list as well,
    because a lot of pg breaks if len(args) != 1,2
    """
    settingDict = {}
    args = list(args)
    for arg in args:
        if not isinstance(arg, str):
            continue
        colPat = 'b|g|r|c|k|m'
        match = re.search(colPat, arg)
        if match:
            settingDict["color"] = match.group()

        styPat = '(?:_)|(?:\-\-)|(?:\-\.\.)|(?:\-\.)|(?:\-)|(?:\.)'
        match = re.search(styPat, arg)
        if match:
            settingDict["style"] = match.group()

        symPat = 'o|s|t|d|\+|x'
        match = re.search(symPat, arg)
        if match:
            settingDict["symbol"] = match.group()
        args.remove(arg)
        break
    return tuple(args), settingDict

def getPlotPens(pw, *args, **kwargs):
    kwargs = kwargs.copy()
    if 'marker' in kwargs:
        kwargs["symbol"] = kwargs.pop('marker')
    pen = kwargs.get('pen', None)
    if pen is None:
        pen = pg.mkPen()
        newArgs, newKwargs = plotArgsParser(*args)
        kwargs.update(newKwargs)
        args = newArgs

        if isinstance(config_options["standardColors"], int):
            numCols = config_options["standardColors"]
        else:
            numCols = len(config_options["standardColors"])

        color = kwargs.get("color", None)
        if color is None:
            if isinstance(config_options["standardColors"], int):
                idx = len(pw.plotItem.curves) % numCols
                color = pg.intColor(idx, config_options["standardColors"])
            else:
                idx = len(pw.plotItem.curves) % numCols
                color = config_options["standardColors"][idx]

        style = kwargs.get('style', None)
        if style is None:
            idx = (len(pw.plotItem.curves) // numCols) % config_options["standardLineshapes"] + 1
            style = idx
        else:
            # pass int and use the qt pen value for it
            # otherwise, parse it.
            if not isinstance(style, int):
                style = config_options["linestyleChars"].index(style)
                print("style:", style)

        if 'symbol' in kwargs and 'symbolPen' not in kwargs:
            kwargs['symbolPen'] = pg.mkPen(color=color)
        if 'symbol' in kwargs and 'symbolBrush' not in kwargs:
            kwargs['symbolBrush'] = pg.mkBrush(color=color)


        width = kwargs.get('linewidth', config_options["linewidth"])

        pen.setColor(pg.mkColor(color))
        pen.setWidth(width)
        pen.setStyle(style)
        kwargs['pen'] = pen
    return kwargs






















































