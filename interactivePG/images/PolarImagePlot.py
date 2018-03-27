from PyQt5 import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np
import collections


def cosd(x):
    return np.cos(x * np.pi/180)

def sind(x):
    return np.sin(x * np.pi/180)

class PolarImagePlot(pg.ImageView):
    """
    ImageView subclass that will default set the ImageItem to the polar plot version
    of below.

    It'd be nice to extend it to add radial/azimuthal axes and stuff.
    """
    def __init__(self, r=None, theta=None, imageData = None, name="PolarImageView", parent=None, view=None, *args):
        item = PolarImageItem(r = r, theta=theta)
        super(PolarImagePlot, self).__init__(parent=parent, view=view, name=name, imageItem = item, *args)
        if imageData is not None:
            self.setImage(imageData)


class PolarPointInfo(object):
    def __init__(self, ridx=0, tidx=0, r=0, t=0, val=0):
        self.ridx = ridx
        self.tidx = tidx
        self.r = r
        self.t = t
        self.val = val



class PolarImageItem(pg.ImageItem):
    """
    Reimpleted image item that draws on a polar coordinate systems

    Makes use of the histogram/coloring/LUT information from a standard
    ImageItem. Some weird bug with red/blue channels, you can see the
    comment in render() if you care.

    Rendering is done by drawing a bunch of QPainterPath's, each path corresponding to
    a single pixel. I'd tried doing a few ways of making these paths
    (remnents are commented out in the render() function), but the one currently
    used is the only one seeming to still work. The paths are currently cached,
    and some amount of work needs to be done to figure out the best place to invalidate
    that cache, such as if the image is updated. However, I couldn't immediately see
    a way how to do that only when the internal image is changed, and not when the
    LUT table is changed or anything.

    The paths are draw onto a QImage, which has a compication. In the default
    ImageItem, there's a 1-to-1 of QImage pixel to underlaying data points. However,
    we need higher QImage resolution than this to get appropriate, anti-aliased curves.
    This is done by setting the _scaleFactor, but extensive testing hasn't really be done

    Note: The violation of the 1-to-1 correspondence from above is why the width(),
    height(), and paint() functions have been overridden, to compensate for the
    default ImageItem depending on the internal self.image data shape
    """

    # emits the above PolarPointInfo Class
    sigPointClicked = QtCore.pyqtSignal(object)
    def __init__(self, r, theta, image=None, **kwargs):
        # Enforce r to be monotonically increasing to handle the
        # rendering
        if np.all(np.diff(r))<0:
            r = r[::-1]
            raise NotImplementedError("You need to figure out how to shift the image data"
                                      "to account for this ")
            # image[]
        if not np.all(np.diff(r)):
            raise RuntimeError("Radial coordinate must be monotonic")

        self.r = r
        self.theta = theta
        self._scaleFactor = 10
        self._paintingPath = None

        super(PolarImageItem, self).__init__(image, **kwargs)


        # set it so the center of the imageItem corresponds to the view
        self.translate(-self.width()/2, -self.height()/2)


        self.allowMouseClicks = True
        self._previousClickObject = None
        # self.scene().sigMouseClicked.connect(self.handleMouseClicks)

    def setImage(self, image=None, autoLevels=None, **kargs):
        super(PolarImageItem, self).setImage(image, autoLevels, **kargs)

    def genPaintingPaths(self, radii, ang):
        self._paintingPath = []
        dr = np.diff(radii)[0]  # ASSUMES MONOTONICITY/EQUAL SPACING
        dang = np.diff(ang)[0]  ## ASSUMES MONOTONICITY/EQUAL SPACING
        rect = lambda rval: QtCore.QRectF(-rval, -rval, 2 * rval, 2 * rval)
        for ridx in range(len(radii)):
            innerPaths = []
            for tidx in range(len(ang)):
                path = QtGui.QPainterPath()
                path.arcTo(rect(radii[ridx] + dr / 2), ang[tidx] + dang / 2, -dang)
                path.lineTo(0, 0)
                path.arcTo(rect(radii[ridx] - dr / 2), ang[tidx] - dang / 2, dang)

                innerPaths.append(path)
            self._paintingPath.append(innerPaths)

    def width(self):
        if self.qimage is None:
            return 1
        return self.qimage.width()/self._scaleFactor

    def height(self):
        if self.qimage is None:
            return 1
        return self.qimage.height()/self._scaleFactor

    def render(self):
        if self.image is None or self.image.size == 0:
            return
        if isinstance(self.lut, collections.Callable):
            lut = self.lut(self.image)
        else:
            lut = self.lut
        argb, alpha = pg.fn.makeARGB(self.image, lut=lut, levels=self.levels)


        # I honestly don't know what's going on. the makeARGB function has a comment
        # that the R/B channels are swapped. I think I agree when playing around with
        # a straight default ImageItem that his swap is valid for that.
        # But for some reason, they shouldn't be swapped here. I don't know what's
        # going on, just that I need to unswap to get the colors to match.
        swap = argb[..., 2].copy();argb[..., 2] = argb[..., 0];argb[..., 0] = swap

        # I want to set np.nan values to be fully transparent (i.e. not rendered)
        nanargs = np.where(np.isnan(self.image))
        argb[nanargs[0], nanargs[1], 3] = 0


        # print(argb)
        # print(argb.shape)
        # return
        # qimage = QtGui.QImage(self.image.shape[0], self.image.shape[1], QtGui.QImage.Format_RGB32)

        radii = self.r
        radii = radii * self._scaleFactor
        dr = np.diff(radii)[0] # ASSUMES MONOTONICITY/EQUAL SPACING
        # print("Dr is", dr)



        ang = self.theta # * 16 # qt angles are in 1/16th degree
        dang = np.diff(ang)
        dang = np.diff(ang)[0]  ## ASSUMES MONOTONICITY/EQUAL SPACING
        rect = lambda rval: QtCore.QRectF(-rval, -rval, 2*rval, 2*rval)


        if self._paintingPath is None:
            self.genPaintingPaths(radii, ang)

        dim = int(max(abs(radii)))*2 + dr
        # qimage = QtGui.QImage(dim, dim, QtGui.QImage.Format_RGB32)
        qimage = QtGui.QImage(dim, dim, QtGui.QImage.Format_ARGB32)

        ## Todo: set this to the base color?
        qimage.fill(QtGui.QColor.fromRgbF(1, 1, 1, 0))


        painter = QtGui.QPainter(qimage)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)


        # Make sure to reference to the center of the image to make things easier to
        # reference
        painter.translate(qimage.width() / 2, qimage.height() / 2)
        painter.setPen(pg.mkPen("r", width=10))

        try:
            for ridx in range(len(radii)):
                for tidx in range(len(ang)):
                    # print("make color", ridx, tidx,)
                    # print("make color", ridx, tidx, argb[ridx, tidx, :])
                    color = QtGui.QColor(*argb[ridx, tidx, :].tolist())
                    path = self._paintingPath[ridx][tidx]
                    painter.fillPath(path, pg.mkBrush(color))
                    # color = QtGui.QColor("red")
                    # color.setAlphaF(0.5)
                    # print("Color", color.name())
                    # painter.setBrush(QtGui.QBrush(color))
                    # painter.drawRect(rect(ridx))
                    # print("drawing rect ", radii[ridx])
                    # print(f"plotting r={radii[ridx]:.0f}, theta={ang[tidx]:.0f}, a={self.image[ridx, tidx]:.2f}")

                    ## TODO: Keep all the painter paths,
                    ## only update the paths themselves on a new setImage
                    ## LUT changes wouldn't require redrawing paths.
                    ## Could speed things up

                    #
                    #
                    #
                    # innerPath = QtGui.QPainterPath()
                    # outerPath = QtGui.QPainterPath()
                    # try:
                    #     ## painter.drawEllipse(rect(radii[ridx]))
                    #     ## painter.drawArc(rect(radii[ridx]), ang[tidx], dang[tidx])
                    #     # innerPath.arcTo(rect(radii[ridx]-dr/2), ang[tidx], dang[tidx])
                    #     # outerPath.arcTo(rect(radii[ridx]+dr/2), ang[tidx], dang[tidx])
                    #
                    #     innerPath.arcTo(rect(radii[ridx]-dr/2), ang[tidx]-dang / 2, dang)
                    #     outerPath.arcTo(rect(radii[ridx]+dr/2), ang[tidx]+dang / 2, -dang)
                    # except IndexError:
                    #     # print("we died")
                    #     # if you're on the last arc, cut it in half?
                    #     # painter.drawArc(rect(radii[ridx]), ang[tidx], dang[tidx-1]/2)
                    #     innerPath.arcTo(rect(radii[ridx]-dr/2), ang[tidx], dang[tidx-1]/2)
                    #     outerPath.arcTo(rect(radii[ridx]+dr/2), ang[tidx], dang[tidx-1]/2)
                    # outerPath.closeSubpath()
                    # innerPath.closeSubpath()
                    # painter.setPen(pg.mkPen("r", width=10))
                    # painter.drawPath(outerPath)
                    # painter.setPen(pg.mkPen("g", width=10))
                    # painter.drawPath(innerPath)
                    #
                    # for ii in range(outerPath.elementCount()):
                    #     e = outerPath.elementAt(ii)
                    #     print(e.type, e.x, e.y)
                    #
                    #
                    # path = outerPath.subtracted(innerPath)
                    # print(path.isEmpty())
                    # painter.setPen(pg.mkPen("b", width=10))
                    # # painter.fillPath(path, pg.mkBrush('b'))
                    # painter.drawPath(path)





                    # path = QtGui.QPainterPath()

                    ## painter.drawEllipse(rect(radii[ridx]))
                    ## painter.drawArc(rect(radii[ridx]), ang[tidx], dang[tidx])
                    # innerPath.arcTo(rect(radii[ridx]-dr/2), ang[tidx], dang[tidx])
                    # outerPath.arcTo(rect(radii[ridx]+dr/2), ang[tidx], dang[tidx])

                    # path.arcTo(rect(radii[ridx] + dr / 2), ang[tidx] + dang / 2, -dang)
                    # painter.setPen(pg.mkPen("r", width=10))


                    # path.lineTo(0, 0)
                    # painter.drawPath(path)


                    # path.arcTo(rect(radii[ridx] - dr / 2), ang[tidx] - dang / 2, dang)
                    # print("size:", path.elementCount())
                    # path = path.simplified()
                    # print("\tsize:", path.elementCount())
                    # painter.setPen(pg.mkPen("g", width=10))
                    # painter.drawPath(path)
                    # painter.fillPath(path, pg.mkBrush(color))
                    # path.lineTo(0,0)

                    # outerPath.closeSubpath()
                    # innerPath.closeSubpath()
                    # painter.setPen(pg.mkPen("g", width=10))
                    # painter.drawPath(path)

                    # for ii in range(path.elementCount()):
                    #     e = path.elementAt(ii)
                    #     print(e.type, e.x, e.y)

                    # painter.setPen(pg.mkPen("b", width=10))
                    # painter.fillPath(path, pg.mkBrush('b'))
                    # painter.drawPath(path)


                    # r1 = radii[ridx] - dr / 2
                    # r2 = radii[ridx] + dr / 2
                    # t1 = ang[tidx] - dang / 2
                    # t2 = ang[tidx] + dang / 2
                    #
                    # x11, y11 = r1 * sind(t1), r1 * cosd(t1)
                    # x12, y12 = r1 * sind(t2), r1 * cosd(t2)
                    #
                    # x21, y21 = r2 * sind(t1), r2 * cosd(t1)
                    # x22, y22 = r2 * sind(t2), r2 * cosd(t2)
                    #
                    # # path.moveTo(x11, y11)  # inner r, lower theta
                    # path = QtGui.QPainterPath(QtCore.QPointF(x11, y11))
                    # path.lineTo(x21, y21)  # outter r, lower etha
                    # path.arcTo(rect(r2), t1, t2-t1) # outer r, higher theta
                    # # path.lineTo(x12, y12)
                    # # path.arcTo(rect(r1), t2, t1-t2)
                    #
                    # path.arcMoveTo(rect(r1), t1)
                    # painter.drawPath(path)
                    #
                    # painter.setPen(pg.mkPen("b", width=10))
                    # path.arcTo(rect(r1), t1, dang)
                    # painter.drawPath(path)
                    #
                    # painter.setPen(pg.mkPen("g", width=10))
                    # path.arcMoveTo(rect(r2), t2)
                    # painter.drawPath(path)

                    # painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
                    # break
                # break


        finally:
            painter.end()
        self.qimage = qimage


        # I want to make it so the center of the polar plot is the center of the viewbox...
        self.setPos(-self.width()/2, -self.height()/2)

    def paint(self, p, *args):
        """
        Need to override paint method because default argument
        fits the image into a rectangle whose dimensions match
        the image size, which isn't valid here.
        :param p:
        :param args:
        :return:
        """
        if self.image is None:
            return
        if self.qimage is None:
            self.render()
            if self.qimage is None:
                return
        if self.paintMode is not None:
            p.setCompositionMode(self.paintMode)

        # shape = self.image.shape[
        #         :2] if self.axisOrder == 'col-major' else self.image.shape[:2][::-1]
        shape = [self.width(), self.height()]
        p.drawImage(QtCore.QRectF(0, 0, *shape), self.qimage)
        if self.border is not None:
            p.setPen(self.border)
            p.drawRect(self.boundingRect())

    def mouseClickEvent(self, ev):
        if self._paintingPath is None: return

        try:
            for ridx in range(len(self._paintingPath)):
                for tidx in range(len(self._paintingPath[ridx])):
                    if self._paintingPath[ridx][tidx].contains(
                            (ev.pos()+self.pos())*self._scaleFactor
                    ):
                        raise StopIteration()
            if self._previousClickObject is not None:
                self.getViewBox().removeItem(self._previousClickObject)
                self._previousClickObject = None
        except StopIteration:
            # print("Found idx", ridx, tidx, self.r[ridx], self.theta[tidx])
            if self._previousClickObject is None:
                self._previousClickObject = QtWidgets.QGraphicsPathItem()
                self.getViewBox().addItem(self._previousClickObject)
                self._previousClickObject.setBrush(pg.mkBrush("y", width=5))
                self._previousClickObject.setPen(QtGui.QPen(QtCore.Qt.NoPen))
                self._previousClickObject.setScale(1./self._scaleFactor)
            self._previousClickObject.setPath(self._paintingPath[ridx][tidx])

            obj = PolarPointInfo(ridx, tidx, self.r[ridx], self.theta[tidx],
                                 self.image[ridx, tidx])
            self.sigPointClicked.emit(obj)
            return

        # print("Not found\n")






    def mapToPolar(self, p):
        r = np.sqrt(p.x()**2 + p.y()**2)
        t = np.arctan2(-p.y(), p.x()) * 180/np.pi
        return r, t

pg.GraphicsScene