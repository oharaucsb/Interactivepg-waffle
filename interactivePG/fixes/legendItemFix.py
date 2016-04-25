import numpy as np
import pyqtgraph
from pyqtgraph import mkPen, mkBrush
from PyQt4 import QtCore, QtGui
from ..packageSettings import config_options
from LegendSettings_ui import Ui_LegendSettingsDialog
"""

pyqtgraph's legend item has a hard-coded slightly transparent,
grey background. Modify the class methods to allow you to change
that.

"""
class LegendSettingsDialog(QtGui.QDialog):
    def __init__(self, *args, **kwargs):
        self.legendItem = kwargs.pop("legendItem", pyqtgraph.LegendItem())
        super(LegendSettingsDialog, self).__init__(*args, **kwargs)
        self._pen = self.legendItem.backgroundPen.color()
        self._brush = self.legendItem.backgroundBrush.color()
        self._font = self.legendItem.items[-1][1].opts.get("size", config_options["legendFontSize"]).split('p')[0]
        self.initUI()

    def initUI(self):
        self.ui = Ui_LegendSettingsDialog()
        self.ui.setupUi(self)
        self.ui.bBGColor.setColor(self._brush)
        self.ui.bBorderColor.setColor(self._pen)
        self.ui.sbFontSize.setValue(self._font)

        self.ui.bBGColor.sigColorChanging.connect(self.updateBrushColor)
        self.ui.bBorderColor.sigColorChanging.connect(self.updatePenColor)
        self.ui.sbFontSize.setOpts(int=True, step=1, min=1)
        self.ui.sbFontSize.sigValueChanging.connect(self.updateFontSize)

    def updateBrushColor(self):
        self.legendItem.setBackgroundBrush(mkBrush(self.ui.bBGColor.color()))
        self.legendItem.update()

    def updatePenColor(self):
        self.legendItem.setBackgroundPen(mkPen(self.ui.bBorderColor.color()))
        self.legendItem.update()

    def updateFontSize(self):
        for sample, label in self.legendItem.items:
            # label.setAttr("size", "{}pt".format(self.ui.sbFontSize.value()))
            label.setText(label.text, size="{}pt".format(self.ui.sbFontSize.value()))
            sample.setScale(self.ui.sbFontSize.value()/10.)
        self.legendItem.update()
        self.legendItem.updateSize()

    @staticmethod
    def makeSettings(legendItem):
        dialog = LegendSettingsDialog(legendItem=legendItem)
        ok = dialog.exec_()
        if not ok:
            dialog.ui.bBGColor.setColor(dialog._brush)
            print "setting bg to color", dialog._brush.name()
            dialog.ui.bBorderColor.setColor(dialog._pen)
            dialog.ui.sbFontSize.setValue(dialog._font)
            dialog.updateBrushColor()
            dialog.updatePenColor()
            dialog.updateFontSize()










oldinit = pyqtgraph.LegendItem.__init__
def __init__(self, size=None, offset=None):
    oldinit(self, size, offset)
    self.backgroundBrush = mkBrush(config_options["legendBackground"])
    self.backgroundPen = mkPen(config_options["legendBorder"])
    self.layout.setColumnStretchFactor(0, 5)
    self.layout.setColumnStretchFactor(1, 5)

oldparent = pyqtgraph.LegendItem.setParentItem
def setParentItem(self, p):
    ret = oldparent(self, p)
    self.scene().sigMouseClicked.connect(self.mouseClickedEvent)
    return ret

def paint(self, p, *args):
    p.setPen(self.backgroundPen)
    p.setBrush(self.backgroundBrush)
    p.drawRect(self.boundingRect())

def setBackgroundPen(self, p):
    self.backgroundPen = mkPen(p)

def setBackgroundBrush(self, b):
    self.backgroundBrush = mkBrush(b)

def mouseClickedEvent(self, ev):
    if self.contains(self.mapFromScene(ev.scenePos())) and ev.double():
        self.openSettings()

def openSettings(self):
    LegendSettingsDialog.makeSettings(self)

pyqtgraph.LegendItem.__init__ = __init__
pyqtgraph.LegendItem.paint = paint
pyqtgraph.LegendItem.setParentItem = setParentItem
pyqtgraph.LegendItem.setBackgroundPen = setBackgroundPen
pyqtgraph.LegendItem.setBackgroundBrush = setBackgroundBrush

pyqtgraph.LegendItem.openSettings = openSettings
pyqtgraph.LegendItem.mouseClickedEvent = mouseClickedEvent





















































