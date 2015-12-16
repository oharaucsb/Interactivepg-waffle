__author__ = 'Home'

import pyqtgraph as pg
import numpy as np


class ImageViewWithPlotItemContainer(pg.ImageView):
    """
    I make all my uis with Qt Designer.
    I want an image view class so I can use the time-trace
    portion to display multiple ccd images as a funciton of
    "time". But it's practically necessary to have the pixel
    number labeled to compare them. THis requires passing
    the view to the imageView as a plotItem at construction

    Qt Designer doesn't allow that functionality. One option
    is to change the pyqtgrpah source so that the default
    view is a plotitem, not a viewbox, but that's super
    cumbersome to carry through to every single computer

    The alternative is to subclass it so I can force
    the view kwarg to be a plotitem, as I want

    """
    def __init__(self, *args, **kwargs):
        kwargs["view"] = pg.PlotItem()
        super(ImageViewWithPlotItemContainer, self).__init__(*args, **kwargs)
        self.timeLine.setPen(pg.mkPen('k'))
    def setImage(self, img,  *args, **kwargs):
        # if you pass a 3D image to pg.ImageView
        # of data, with data.shape=(L, M, N)
        # with N<=4, he interprets the axes differently
        # than N>4. I don't want to do this
        axes = kwargs.get("axes", None)
        if axes is None:
            kwargs["axes"] = {'t': 0, 'x': 1, 'y': 2, 'c': None}


        # I was having a lot of trouble getting ImageView
        # to accept an axes argument. That is, it was just ignoring it.
        # I couldn't figure out how to handle it, so this convenience
        # kwarg will transpose the image from my typical
        # considerations (time, x, y) to his bizarre standard,
        # (time, y, x)

        resize = kwargs.get("tranpose", True)
        if resize:
            if img.ndim == 3:
                img = np.transpose(img, (0, 2, 1))
            elif img.ndim == 2:
                img = img.T
                # need to set it to 3 axes to deal with
                # setting the axes as above

                img = img[None,:,:]

        super(ImageViewWithPlotItemContainer, self).setImage(img, *args, **kwargs)