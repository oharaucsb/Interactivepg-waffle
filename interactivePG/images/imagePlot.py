import numpy as np
import pyqtgraph as pg
from .ImageViewWithPlotItemContainer import ImageViewWithPlotItemContainer

def image(*args, **kwargs):
    # assume a file you want to load
    if isinstance(args[0], str):
        data = np.genfromtxt(args[0])
        if np.all(np.isnan(data)):
            data = np.genfromtxt(args[0], delimiter=',')
    elif isinstance(args[0], np.ndarray):
        data = args[0]
    else:
        raise TypeError("I don't know how to interpret your data arg, {}, type: {}".format(
            arg[0], type(arg[0])
        ))

    newargs = list(args)
    newargs[0] = data
    img = ImageViewWithPlotItemContainer()
    img.view.setAspectLocked(False)
    img.view.invertY(False)
    img.setImage(*newargs, **kwargs)
    return img


