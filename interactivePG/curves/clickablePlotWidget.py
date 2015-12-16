from __future__ import print_function
import pyqtgraph as pg
import numpy as np
import sys
from PyQt4 import QtCore, QtGui
from clickablePlotSettings_ui import Ui_LineSettingsDialog
from PlotDataErrorItem import *
from ..packageSettings import config_options

class signalBlocker(object):
    def __init__(self, toBlock):
        # print("Init. To block", toBlock)
        self.toBlock = toBlock
    def __call__(self, f):
        # print("called, f", f)
        def wrappedf(*args, **kwargs):
            args[0].ui.__getattribute__(self.toBlock).blockSignals(True)
            ret = f(*args, **kwargs)
            args[0].ui.__getattribute__(self.toBlock).blockSignals(False)
            return ret

        return wrappedf


class ClickablePlotWidget(pg.PlotWidget):
    # emitted when the window is closed
    sigPlotClosed = QtCore.pyqtSignal(object)
    sigMouseMoved = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(ClickablePlotWidget, self).__init__(*args, **kwargs)

        self.opts = config_options.copy()
        self.updateOpts()

        self.selectedCurves = {}

        # set up a timer to tell when you've double
        # clicked a
        self.doubleClickTimer = QtCore.QTimer()
        self.doubleClickTimer.setInterval(250)
        self.doubleClickTimer.setSingleShot(True)

        self.scene().sigMouseMoved.connect(self.mousemove)

        self.doubleClickCurve = None
    def updateOpts(self, **opts):
        self.opts.update(opts)
        if self.opts["boundedAxes"]:
            self.plotItem.showAxis("top")

            self.plotItem.showAxis("right")
        for pos in ["top", "left", "right", "bottom"]:
            print(pos)
            axis = self.plotItem.getAxis(pos)
            axis.setTickFont(QtGui.QFont("", self.opts["axisFontSize"]))
            axis.setLabel(**{"font-size":"{}pt".format(self.opts["axisLabelFontSize"])})
            axis.setPen(color=self.opts["foreground"],width=self.opts["axisThickness"])
            axis.setStyle(tickLength=self.opts["axisTickLength"])
            if axis.orientation in ["left", "right"]:
                # axis.setWidth(100)
                pass
                # axis.setStyle(tickTextOffset=20, tickTextWidth=20, autoExpandTextSpace=True)
            elif axis.orientation in ["bottom", "top"]:
                pass
            # axis.setMinimumWidth(300)
            # axis.setMinimumHeight(300)

    def plot(self, *args, **kwargs):
        pen = kwargs.get('pen', 'l')
        if 'width' in kwargs:
            pen = pg.mkPen(pen)
            pen.setWidth(kwargs['width'])
            kwargs['pen'] = pen
        p = self.plotItem.plot(*args, **kwargs)
        self.setItemClickable(p)
        return p

    def errorbars(self, *args, **kwargs):
        """
        create and add an errordataitem

        errorbars(<xdata>, <ydata>, <error>, *kwargs)
        errorbars(<ydata>, <errors>, **kwargs) to assume
            x as an index
        errorbars(x=<xdata>, y=<ydata>, errorbars=<errors>, **kwargs)
        errorbars(Nx(2, 3), **kwargs) to unpack as
            x, y, yerr
        """
        if len(args)==2:
            kwargs.update(y=args[0])
            kwargs.update(errorbars=args[1])
        elif len(args)==3:
            kwargs.update(x=args[0])
            kwargs.update(y=args[1])
            kwargs.update(errorbars=args[2])
        elif len(args) == 1 and isinstance(args[0], np.ndarray):
            if args[0].shape[1] == 2:
                kwargs.update(y=args[0][:,0])
                kwargs.update(errorbars=args[0][:,1])
            elif args[0].shape[1] == 3:
                kwargs.update(x=args[0][:,0])
                kwargs.update(y=args[0][:,1])
                kwargs.update(errorbars=args[0][:,2])
            else:
                raise RuntimeError("I do not know how to parse this np.ndarray")
        elif len(args)==1:
            raise RuntimeError("I do not know how to parse this argument", args)

        assert 'y' in kwargs
        assert 'errorbars' in kwargs

        erroritem = PlotDataErrorItem(**kwargs)
        self.addItem(erroritem)

        self.setItemClickable(erroritem)
        return erroritem

    def setItemClickable(self, item):
        """
        item: a data item which should be modified
        to add behavior for when it can be clicked
        and modified by the UI
        """

        item.curve.setClickable(True)
        item.sigClicked.connect(self._updateCurveClicked)
        item.opts['isEnabled'] = True
        item.opts['isSelected'] = False
        item.opts["plotWidget"] = self
        item.opts["xOffset"] = 0
        item.opts["yOffset"] = 0

    def updateLegendNames(self, curveItem):
        if curveItem.name() is None:
            return
        for sample, label in self.plotItem.legend.items:
            if sample.item is curveItem:
                label.setText(curveItem.opts["name"])
                # The legend will resize to fit new text,
                # but will not shrink back down after changing
                # to a shorter name.
                # For some reason. LegendItem.updateSize() doesn't
                # work properly.
                # For some reason, setting the geometry to 0 causes
                # it to resize properly.
                # Not sure what the miscommunication is from
                # PyQt/graph is.
                self.plotItem.legend.setGeometry(0, 0, 0, 0)
                break
        else:
            self.plotItem.legend.addItem(curveItem, name=curveItem.opts["name"])

    def _updateCurveClicked(self, plotDataItem):
        pen = plotDataItem.opts['pen']
        pen = pg.mkPen(pen)
        width = pen.width()
        # print("Curve clicked. Current width: {}".format(pen.width()))
        if self.doubleClickTimer.isActive():
            self.doubleClickTimer.stop()
            CurveItemSettings.getNewParameters(self, self.plotItem.curves, plotDataItem)
        elif plotDataItem.opts["isSelected"]:
            pen.setWidth(width - config_options["selectionThickness"])
            plotDataItem.setPen(pen)
            self.doubleClickTimer.start()
            plotDataItem.opts["isSelected"] = False
        else:
            pen.setWidth(width + config_options["selectionThickness"])
            plotDataItem.setPen(pen)
            plotDataItem.opts["isSelected"] = True
            self.doubleClickTimer.start()

    def closeEvent(self, *args, **kwargs):
        self.sigPlotClosed.emit(self)

    def mousemove(self, *args, **kwargs):
        self.sigMouseMoved.emit(self.plotItem.vb.mapSceneToView(args[0]))

class CurveItemSettings(QtGui.QDialog):
    # QListWidgets allows multiple selection of listItems
    # However, if you toggle the checkbox of a set of selected items,
    # it will de-select all but the checked one, which is frustrating
    # if you want to toggle it (i.e. to quickly see differences).
    # I put this in place to prevent this. If you check multiple
    # items, start a quick single-shot timer, which another
    # function will check to see if it's running to reselect those
    # items.
    _multiSelectHelper = {"timer": QtCore.QTimer(),
                          "selectionList": []}
    def __init__(self, *args, **kwargs):
        curveList = kwargs.pop('curves', None)
        clickedCurve = kwargs.pop('clickedCurve', None)
        super(CurveItemSettings, self).__init__(*args, **kwargs)
        if curveList is None:
            curveList = [pg.PlotDataItem()]
        self.listViewCurveItems = {}
        self.initUI(curveList, clickedCurve)

        self._multiSelectHelper["timer"].setInterval(100)
        self._multiSelectHelper["timer"].setSingleShot(True)


    def initUI(self, curveList, firstCurve):
        """

        :param curveItem: curveitim
        :type curveItem: pg.PlotDataItem
        :return:
        """
        self.ui = Ui_LineSettingsDialog()
        self.ui.setupUi(self)
        self.ui.sbLineWidth.setMinimum(0)
        self.ui.sbLineWidth.setSingleStep(1)
        self.ui.sbLineWidth.setOpts(int=True)

        self.ui.sbMarkerSize.setMinimum(0)
        self.ui.sbMarkerSize.setSingleStep(1)
        self.ui.sbMarkerSize.setOpts(int=True)
        self.originalSettings = {}

        initialListItem = None

        for curveItem in curveList:
            listItem = QtGui.QListWidgetItem(self.ui.lwCurves)
            listItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsSelectable |
                              QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
            listItem.setCheckState(QtCore.Qt.Unchecked)
            listItem.setSelected(curveItem.opts["isSelected"])
            if curveItem is firstCurve:
                initialListItem = listItem

            name = curveItem.name()
            if name is None:
                name = str(curveItem)
            listItem.setText(name)

            cs = QtCore.Qt.Checked if curveItem.opts["isEnabled"] else QtCore.Qt.Unchecked
            listItem.setCheckState(cs)


            self.ui.lwCurves.addItem(listItem)
            self.listViewCurveItems[curveItem] = listItem
            self.originalSettings[curveItem] = curveItem.opts.copy()


        self.ui.lwCurves.currentItemChanged.connect(self.handlecurrentItemChanged)
        self.ui.lwCurves.itemChanged.connect(self.handleitemChanged)
        self.ui.lwCurves.itemSelectionChanged.connect(self.handleitemSelectionChanged)

        self.ui.colLine.sigColorChanging.connect(self.updateLineColors)
        self.ui.cbLineStyle.currentIndexChanged.connect(self.updateLineStyle)
        self.ui.sbLineWidth.sigValueChanging.connect(self.updateLineWidth)

        self.ui.colMarker.sigColorChanging.connect(self.updateMarkerBrushColor)
        self.ui.cbMarkerStyle.currentIndexChanged.connect(self.updateMarkerStyle)
        self.ui.sbMarkerSize.sigValueChanging.connect(self.updateMarkerSize)


        self.show()
        # toggle it to set the interface to have the settings
        # of the clicked line
        self.handlecurrentItemChanged(initialListItem)

    def getCurveFromItem(self, item):
        for k, v in self.listViewCurveItems.items():
            if v is item: return k

    def handlecurrentItemChanged(self, *args, **kwargs):
        item = args[0]
        curve = self.getCurveFromItem(item)
        pen = pg.mkPen(curve.opts["pen"])
        opts = curve.opts

        self.ui.colLine.blockSignals(True)
        self.ui.colLine.setColor(pen.color())
        self.ui.colLine.blockSignals(False)

        self.ui.cbLineStyle.blockSignals(True)
        self.ui.cbLineStyle.setCurrentIndex(pen.style())
        self.ui.cbLineStyle.blockSignals(False)

        self.ui.sbLineWidth.blockSignals(True)
        self.ui.sbLineWidth.setValue(pen.width() -
                                     config_options["selectionThickness"]*int(curve.opts["isSelected"]))
        self.ui.sbLineWidth.blockSignals(False)

        self.ui.cbMarkerStyle.blockSignals(True)
        self.ui.cbMarkerStyle.setCurrentIndex(
            self.ui.cbMarkerStyle.findText(str(opts["symbol"]))
        )
        self.ui.cbMarkerStyle.blockSignals(False)

        self.ui.sbMarkerSize.blockSignals(True)
        self.ui.sbMarkerSize.setValue(opts["symbolSize"])
        self.ui.sbMarkerSize.blockSignals(False)


        self.ui.colMarker.blockSignals(True)
        self.ui.colMarker.setColor(pg.mkBrush(opts["symbolBrush"]).color())
        self.ui.colMarker.blockSignals(False)

    @signalBlocker("lwCurves")
    def handleitemChanged(self, *args, **kwargs):
        clickedItem = args[0]
        if clickedItem not in self.ui.lwCurves.selectedItems():
            self.ui.lwCurves.setCurrentItem(clickedItem)
        for listItem in self.ui.lwCurves.selectedItems():
            curve = self.getCurveFromItem(listItem)
            if listItem is clickedItem:
                pass
            else:
                # Want to toggle other things if they're not in this list
                listItem.setCheckState(2*(not listItem.checkState()))
                listItem.setSelected(True)
            # if curve.opts["isEnabled"] ^ (listItem.checkState() == QtCore.Qt.Checked):
            if True:
                curve.opts["isEnabled"] = (listItem.checkState() == QtCore.Qt.Checked)
                if not curve.opts["isEnabled"]:
                    curve.curve.hide()
                    curve.scatter.hide()
                    if hasattr(curve, 'errorbars'):
                        curve.errorbars.hide()
                else:
                    curve.curve.show()
                    curve.scatter.show()
                    if hasattr(curve, 'errorbars'):
                        curve.errorbars.show()
        item = args[0]
        curve = self.getCurveFromItem(item)

        if curve.name() != str(item.text()):
            curve.opts["name"] = str(item.text())
            if curve.opts["plotWidget"].plotItem.legend is not None:
                curve.opts["plotWidget"].updateLegendNames(curve)

        self._multiSelectHelper["selectionList"] = self.ui.lwCurves.selectedItems()
        self._multiSelectHelper["timer"].start()

    @signalBlocker("lwCurves")
    def handleitemSelectionChanged(self, *args, **kwargs):
        if self._multiSelectHelper["timer"].isActive():
            for item in self._multiSelectHelper["selectionList"]:
                item.setSelected(True)
        # print("Timer active?", self._multiSelectHelper["timer"].isActive())
        # print("Selectionlist:", self._multiSelectHelper["selectionList"])

    def updateLineColors(self, colorButton):
        for listItem in self.ui.lwCurves.selectedItems():
            curve = self.getCurveFromItem(listItem)
            p = pg.mkPen(curve.opts["pen"])
            p.setColor(colorButton.color())
            curve.setPen(p)

    def updateLineStyle(self, newIdx):
        for listItem in self.ui.lwCurves.selectedItems():
            curve  = self.getCurveFromItem(listItem)
            p = pg.mkPen(curve.opts["pen"])
            p.setStyle(newIdx)
            curve.setPen(p)

    def updateLineWidth(self, sb):
        for listItem in self.ui.lwCurves.selectedItems():
            curve  = self.getCurveFromItem(listItem)
            p = pg.mkPen(curve.opts["pen"])
            p.setWidth(sb.value() +
                       config_options["selectionThickness"]*int(curve.opts["isSelected"]))
            curve.setPen(p)

    def updateMarkerStyle(self, newIdx):
        for listItem in self.ui.lwCurves.selectedItems():
            curve  = self.getCurveFromItem(listItem)
            if str(self.ui.cbMarkerStyle.currentText()) == "None":
                curve.setSymbol(None)
            else:
                curve.setSymbol(
                    str(self.ui.cbMarkerStyle.currentText())
                )

    def updateMarkerSize(self, sb):
        for listItem in self.ui.lwCurves.selectedItems():
            curve  = self.getCurveFromItem(listItem)
            curve.setSymbolSize(sb.value())

    def updateMarkerBrushColor(self, colorButton):
        for listItem in self.ui.lwCurves.selectedItems():
            curve  = self.getCurveFromItem(listItem)
            brush = pg.mkBrush(curve.opts["symbolBrush"])
            brush.setColor(colorButton.color())
            curve.setSymbolBrush(brush)

    @staticmethod
    def getNewParameters(parent, curves, clickedCurve = None):
        dialog = CurveItemSettings(curves=curves, clickedCurve = clickedCurve)
        parent.sigPlotClosed.connect(dialog.close)
        ok = dialog.exec_()
        if not ok:
            for curve in curves:
                # curve.opts = dialog.originalSettings[curve].copy()
                curve.opts.update(dialog.originalSettings[curve])
                curve.updateItems()
                if curve.opts["plotWidget"].plotItem.legend is not None:
                    curve.opts["plotWidget"].updateLegendNames(curve)


if __name__=='__main__':
    ex = QtGui.QApplication([])
    wid = ClickablePlotWidget()
    wid.plotItem.addLegend()
    wid.plot([0, 1, 2, 3, 4], pen='g', width=5, name='green')
    p = wid.plot([1, -2, 4, 8, 2], pen='r', name='r')
    wid.plot([1]*5, pen='y')
    x = np.arange(5)
    y = np.random.normal(1, 1, 5)
    err = np.ones(5)

    err = wid.errorbars(np.column_stack((x, y, err)), pen='c', name='errors')

    wid.show()
    # sys.exit()
    sys.exit(ex.exec_())