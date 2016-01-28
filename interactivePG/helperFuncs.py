import numpy as np
import pyqtgraph
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


























































