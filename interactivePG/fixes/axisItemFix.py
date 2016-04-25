import numpy as np
import pyqtgraph
from PyQt4 import QtCore, QtGui

# pyqtgraph's axis item is slightly broken
# it doesn't account for the increase
# in font size of the tick labels
# which causes them to clip if you want to change
# those. I intercept them here to fix those



oldDrawSpecs = pyqtgraph.AxisItem.generateDrawSpecs
def newDrawSpecs(self, p):
    if False:
        self = pyqtgraph.AxisItem
    axisSpec, tickSpecs, textSpecs = oldDrawSpecs(self, p)


    bounds = self.mapRectFromParent(self.geometry())

    linkedView = self.linkedView()
    if linkedView is None or self.grid is False:
        tickBounds = bounds
    else:
        tickBounds = linkedView.mapRectToItem(self, linkedView.boundingRect())

    if self.orientation == 'left':
        span = (bounds.topRight(), bounds.bottomRight())
        tickStart = tickBounds.right()
        tickStop = bounds.right()
        tickDir = -1
        axis = 0
    elif self.orientation == 'right':
        span = (bounds.topLeft(), bounds.bottomLeft())
        tickStart = tickBounds.left()
        tickStop = bounds.left()
        tickDir = 1
        axis = 0
    elif self.orientation == 'top':
        span = (bounds.bottomLeft(), bounds.bottomRight())
        tickStart = tickBounds.bottom()
        tickStop = bounds.bottom()
        tickDir = -1
        axis = 1
    elif self.orientation == 'bottom':
        span = (bounds.topLeft(), bounds.topRight())
        tickStart = tickBounds.top()
        tickStop = bounds.top()
        tickDir = 1
        axis = 1

    tickFontSize = 10.
    if self.tickFont is not None:
        tickFontSize = float(self.tickFont.pointSize())

    textOffset = self.style['tickTextOffset'][axis]

    newTextSpecs = []
    textSize2 = 0
    for ii, (rect, textFlags, vstr) in enumerate(textSpecs):
        if False:
            rect = QtCore.QRectF()

        x = tickSpecs[ii][2]
        if axis:
            # tickStop = x.y()
            x = x.x()
        else:
            # tickStop = x.x()
            x = x.y()


        rect.setWidth(rect.width() * tickFontSize/7.)
        rect.setHeight(rect.height() * tickFontSize/5.)

        # if self.style["tickLength"]<0:
        #     tickStop += 2*abs(self.style["tickLength"])
        textRect = rect
        height = textRect.height()
        width = textRect.width()

        length = self.style["tickLength"]
        # tickStop = max(0, tickStop)

        offset = max(0,length) + textOffset
        # offset = max(0,abs(self.style['tickLength'])) + textOffset

        if self.orientation == 'left':
            textFlags = QtCore.Qt.TextDontClip|QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
            rect = QtCore.QRectF(tickStop-offset-width, x-(height/2), width, height)
        elif self.orientation == 'right':
            textFlags = QtCore.Qt.TextDontClip|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter
            rect = QtCore.QRectF(tickStop+offset, x-(height/2), width, height)
        elif self.orientation == 'top':
            textFlags = QtCore.Qt.TextDontClip|QtCore.Qt.AlignCenter|QtCore.Qt.AlignBottom
            rect = QtCore.QRectF(x-width/2., tickStop-offset-height, width, height)
        elif self.orientation == 'bottom':
            textFlags = QtCore.Qt.TextDontClip|QtCore.Qt.AlignCenter|QtCore.Qt.AlignTop
            rect = QtCore.QRectF(x-width/2., tickStop+offset, width, height)



        newTextSpecs.append((rect, textFlags, vstr))



    if axis == 0:
        textSize = np.sum([r[0].height() for r in newTextSpecs])
        textSize2 = np.max([r[0].width() for r in newTextSpecs])
    else:
        textSize = np.sum([r[0].width() for r in newTextSpecs])
        textSize2 = np.max([r[0].height() for r in newTextSpecs])

    self._updateMaxTextSize(textSize2)
    return axisSpec, tickSpecs, newTextSpecs

oldinit = pyqtgraph.AxisItem.__init__
def __init__(self, *args, **kwargs):
    oldinit(self, *args, **kwargs)
    try:
        self.parent().scene().sigMouseClicked.connect(self.mouseClickEvent)
    except AttributeError:
        pass

def mouseClickEvent(self, ev):
    print "got mouse click"



pyqtgraph.AxisItem.generateDrawSpecs = newDrawSpecs
pyqtgraph.AxisItem.__init__ = __init__
pyqtgraph.AxisItem.mouseClickEvent = mouseClickEvent




















































