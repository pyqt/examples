#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited
## Copyright (C) 2010 Hans-Peter Jansen <hpj@urpla.net>.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial Usage
## Licensees holding valid Qt Commercial licenses may use this file in
## accordance with the Qt Commercial License Agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and Nokia.
##
## GNU Lesser General Public License Usage
## Alternatively, this file may be used under the terms of the GNU Lesser
## General Public License version 2.1 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU Lesser General Public License version 2.1 requirements
## will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
##
## In addition, as a special exception, Nokia gives you certain additional
## rights.  These rights are described in the Nokia Qt LGPL Exception
## version 1.1, included in the file LGPL_EXCEPTION.txt in this package.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3.0 as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU General Public License version 3.0 requirements will be
## met: http://www.gnu.org/copyleft/gpl.html.
##
## If you have questions regarding the use of this file, please contact
## Nokia at qt-info@nokia.com.
## $QT_END_LICENSE$
##
#############################################################################


import math

from PyQt5.QtCore import (pyqtSignal, QBasicTimer, QObject, QPoint, QPointF,
        QRect, QSize, QStandardPaths, Qt, QUrl)
from PyQt5.QtGui import (QColor, QDesktopServices, QImage, QPainter,
        QPainterPath, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QWidget
from PyQt5.QtNetwork import (QNetworkAccessManager, QNetworkDiskCache,
        QNetworkRequest)


# how long (milliseconds) the user need to hold (after a tap on the screen)
# before triggering the magnifying glass feature
# 701, a prime number, is the sum of 229, 233, 239
# (all three are also prime numbers, consecutive!)
HOLD_TIME = 701

# maximum size of the magnifier
# Hint: see above to find why I picked self one :)
MAX_MAGNIFIER = 229

# tile size in pixels
TDIM = 256


class Point(QPoint):
    """QPoint, that is fully qualified as a dict key"""
    def __init__(self, *par):
        if par:
            super(Point, self).__init__(*par)
        else:
            super(Point, self).__init__()

    def __hash__(self):
        return self.x() * 17 ^ self.y()

    def __repr__(self):
        return "Point(%s, %s)" % (self.x(), self.y())


def tileForCoordinate(lat, lng, zoom):
    zn = float(1 << zoom)
    tx = float(lng + 180.0) / 360.0
    ty = (1.0 - math.log(math.tan(lat * math.pi / 180.0) +
          1.0 / math.cos(lat * math.pi / 180.0)) / math.pi) / 2.0

    return QPointF(tx * zn, ty * zn)


def longitudeFromTile(tx, zoom):
    zn = float(1 << zoom)
    lat = tx / zn * 360.0 - 180.0

    return lat


def latitudeFromTile(ty, zoom):
    zn = float(1 << zoom)
    n = math.pi - 2 * math.pi * ty / zn
    lng = 180.0 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n)))

    return lng


class SlippyMap(QObject):

    updated = pyqtSignal(QRect)

    def __init__(self, parent=None):
        super(SlippyMap, self).__init__(parent)

        self._offset = QPoint()
        self._tilesRect = QRect()
        self._tilePixmaps = {} # Point(x, y) to QPixmap mapping
        self._manager = QNetworkAccessManager()
        self._url = QUrl()
        # public vars
        self.width = 400
        self.height = 300
        self.zoom = 15
        self.latitude = 59.9138204
        self.longitude = 10.7387413

        self._emptyTile = QPixmap(TDIM, TDIM)
        self._emptyTile.fill(Qt.lightGray)

        cache = QNetworkDiskCache()
        cache.setCacheDirectory(
            QStandardPaths.writableLocation(QStandardPaths.CacheLocation))
        self._manager.setCache(cache)
        self._manager.finished.connect(self.handleNetworkData)

    def invalidate(self):
        if self.width <= 0 or self.height <= 0:
            return

        ct = tileForCoordinate(self.latitude, self.longitude, self.zoom)
        tx = ct.x()
        ty = ct.y()

        # top-left corner of the center tile
        xp = int(self.width / 2 - (tx - math.floor(tx)) * TDIM)
        yp = int(self.height / 2 - (ty - math.floor(ty)) * TDIM)

        # first tile vertical and horizontal
        xa = (xp + TDIM - 1) / TDIM
        ya = (yp + TDIM - 1) / TDIM
        xs = int(tx) - xa
        ys = int(ty) - ya

        # offset for top-left tile
        self._offset = QPoint(xp - xa * TDIM, yp - ya * TDIM)

        # last tile vertical and horizontal
        xe = int(tx) + (self.width - xp - 1) / TDIM
        ye = int(ty) + (self.height - yp - 1) / TDIM

        # build a rect
        self._tilesRect = QRect(xs, ys, xe - xs + 1, ye - ys + 1)

        if self._url.isEmpty():
            self.download()

        self.updated.emit(QRect(0, 0, self.width, self.height))

    def render(self, p, rect):
        for x in range(self._tilesRect.width()):
            for y in range(self._tilesRect.height()):
                tp = Point(x + self._tilesRect.left(), y + self._tilesRect.top())
                box = self.tileRect(tp)
                if rect.intersects(box):
                    p.drawPixmap(box, self._tilePixmaps.get(tp, self._emptyTile))
   
    def pan(self, delta):
        dx = QPointF(delta) / float(TDIM)
        center = tileForCoordinate(self.latitude, self.longitude, self.zoom) - dx
        self.latitude = latitudeFromTile(center.y(), self.zoom)
        self.longitude = longitudeFromTile(center.x(), self.zoom)
        self.invalidate()

    # slots
    def handleNetworkData(self, reply):
        img = QImage()
        tp = Point(reply.request().attribute(QNetworkRequest.User))
        url = reply.url()
        if not reply.error():
            if img.load(reply, None):
                self._tilePixmaps[tp] = QPixmap.fromImage(img)
        reply.deleteLater()
        self.updated.emit(self.tileRect(tp))

        # purge unused tiles
        bound = self._tilesRect.adjusted(-2, -2, 2, 2)
        for tp in list(self._tilePixmaps.keys()):
            if not bound.contains(tp):
                del self._tilePixmaps[tp]
        self.download()

    def download(self):
        grab = None
        for x in range(self._tilesRect.width()):
            for y in range(self._tilesRect.height()):
                tp = Point(self._tilesRect.topLeft() + QPoint(x, y))
                if tp not in self._tilePixmaps:
                    grab = QPoint(tp)
                    break

        if grab is None:
            self._url = QUrl()
            return

        path = 'http://tile.openstreetmap.org/%d/%d/%d.png' % (self.zoom, grab.x(), grab.y())
        self._url = QUrl(path)
        request = QNetworkRequest()
        request.setUrl(self._url)
        request.setRawHeader(b'User-Agent', b'Nokia (PyQt) Graphics Dojo 1.0')
        request.setAttribute(QNetworkRequest.User, grab)
        self._manager.get(request)

    def tileRect(self, tp):
        t = tp - self._tilesRect.topLeft()
        x = t.x() * TDIM + self._offset.x()
        y = t.y() * TDIM + self._offset.y()

        return QRect(x, y, TDIM, TDIM)


class LightMaps(QWidget):
    def __init__(self, parent = None):
        super(LightMaps, self).__init__(parent)

        self.pressed = False
        self.snapped = False
        self.zoomed = False
        self.invert = False
        self._normalMap = SlippyMap(self)
        self._largeMap = SlippyMap(self)
        self.pressPos = QPoint()
        self.dragPos = QPoint()
        self.tapTimer = QBasicTimer()
        self.zoomPixmap = QPixmap()
        self.maskPixmap = QPixmap()
        self._normalMap.updated.connect(self.updateMap)
        self._largeMap.updated.connect(self.update)
 
    def setCenter(self, lat, lng):
        self._normalMap.latitude = lat
        self._normalMap.longitude = lng
        self._normalMap.invalidate()
        self._largeMap.invalidate()

    # slots
    def toggleNightMode(self):
        self.invert = not self.invert
        self.update()
 
    def updateMap(self, r):
        self.update(r)

    def activateZoom(self):
        self.zoomed = True
        self.tapTimer.stop()
        self._largeMap.zoom = self._normalMap.zoom + 1
        self._largeMap.width = self._normalMap.width * 2
        self._largeMap.height = self._normalMap.height * 2
        self._largeMap.latitude = self._normalMap.latitude
        self._largeMap.longitude = self._normalMap.longitude
        self._largeMap.invalidate()
        self.update()
 
    def resizeEvent(self, event):
        self._normalMap.width = self.width()
        self._normalMap.height = self.height()
        self._normalMap.invalidate()
        self._largeMap.width = self._normalMap.width * 2
        self._largeMap.height = self._normalMap.height * 2
        self._largeMap.invalidate()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self._normalMap.render(p, event.rect())
        p.setPen(Qt.black)
        p.drawText(self.rect(), Qt.AlignBottom | Qt.TextWordWrap,
                   "Map data CCBYSA 2009 OpenStreetMap.org contributors")
        p.end()

        if self.zoomed:
            dim = min(self.width(), self.height())
            magnifierSize = min(MAX_MAGNIFIER, dim * 2 / 3)
            radius = magnifierSize / 2
            ring = radius - 15
            box = QSize(magnifierSize, magnifierSize)

            # reupdate our mask
            if self.maskPixmap.size() != box:
                self.maskPixmap = QPixmap(box)
                self.maskPixmap.fill(Qt.transparent)
                g = QRadialGradient()
                g.setCenter(radius, radius)
                g.setFocalPoint(radius, radius)
                g.setRadius(radius)
                g.setColorAt(1.0, QColor(255, 255, 255, 0))
                g.setColorAt(0.5, QColor(128, 128, 128, 255))
                mask = QPainter(self.maskPixmap)
                mask.setRenderHint(QPainter.Antialiasing)
                mask.setCompositionMode(QPainter.CompositionMode_Source)
                mask.setBrush(g)
                mask.setPen(Qt.NoPen)
                mask.drawRect(self.maskPixmap.rect())
                mask.setBrush(QColor(Qt.transparent))
                mask.drawEllipse(g.center(), ring, ring)
                mask.end()

            center = self.dragPos - QPoint(0, radius)
            center += QPoint(0, radius / 2)
            corner = center - QPoint(radius, radius)
            xy = center * 2 - QPoint(radius, radius)
            # only set the dimension to the magnified portion
            if self.zoomPixmap.size() != box:
                self.zoomPixmap = QPixmap(box)
                self.zoomPixmap.fill(Qt.lightGray)
    
            if True:
                p = QPainter(self.zoomPixmap)
                p.translate(-xy)
                self._largeMap.render(p, QRect(xy, box))
                p.end()

            clipPath = QPainterPath()
            clipPath.addEllipse(QPointF(center), ring, ring)
            p = QPainter(self)
            p.setRenderHint(QPainter.Antialiasing)
            p.setClipPath(clipPath)
            p.drawPixmap(corner, self.zoomPixmap)
            p.setClipping(False)
            p.drawPixmap(corner, self.maskPixmap)
            p.setPen(Qt.gray)
            p.drawPath(clipPath)

        if self.invert:
            p = QPainter(self)
            p.setCompositionMode(QPainter.CompositionMode_Difference)
            p.fillRect(event.rect(), Qt.white)
            p.end()

    def timerEvent(self, event):
        if not self.zoomed:
            self.activateZoom()

        self.update()
 
    def mousePressEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return

        self.pressed = self.snapped = True
        self.pressPos = self.dragPos = event.pos()
        self.tapTimer.stop()
        self.tapTimer.start(HOLD_TIME, self)

    def mouseMoveEvent(self, event):
        if not event.buttons():
            return

        if not self.zoomed:
            if not self.pressed or not self.snapped:
                delta = event.pos() - self.pressPos
                self.pressPos = event.pos()
                self._normalMap.pan(delta)
                return
            else:
                threshold = 10
                delta = event.pos() - self.pressPos
                if self.snapped:
                    self.snapped &= delta.x() < threshold
                    self.snapped &= delta.y() < threshold
                    self.snapped &= delta.x() > -threshold
                    self.snapped &= delta.y() > -threshold

                if not self.snapped:
                    self.tapTimer.stop()

        else:
            self.dragPos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.zoomed = False
        self.update()
 
    def keyPressEvent(self, event):
        if not self.zoomed:
            if event.key() == Qt.Key_Left:
                self._normalMap.pan(QPoint(20, 0))
            if event.key() == Qt.Key_Right:
                self._normalMap.pan(QPoint(-20, 0))
            if event.key() == Qt.Key_Up:
                self._normalMap.pan(QPoint(0, 20))
            if event.key() == Qt.Key_Down:
                self._normalMap.pan(QPoint(0, -20))
            if event.key() == Qt.Key_Z or event.key() == Qt.Key_Select:
                self.dragPos = QPoint(self.width() / 2, self.height() / 2)
                self.activateZoom()
        else:
            if event.key() == Qt.Key_Z or event.key() == Qt.Key_Select:
                self.zoomed = False
                self.update()

            delta = QPoint(0, 0)
            if event.key() == Qt.Key_Left:
                delta = QPoint(-15, 0)
            if event.key() == Qt.Key_Right:
                delta = QPoint(15, 0)
            if event.key() == Qt.Key_Up:
                delta = QPoint(0, -15)
            if event.key() == Qt.Key_Down:
                delta = QPoint(0, 15)
            if delta != QPoint(0, 0):
                self.dragPos += delta
                self.update()


class MapZoom(QMainWindow):
    def __init__(self):
        super(MapZoom, self).__init__(None)

        self.map_ = LightMaps(self)
        self.setCentralWidget(self.map_)
        self.map_.setFocus()
        self.osloAction = QAction("&Oslo", self)
        self.berlinAction = QAction("&Berlin", self)
        self.jakartaAction = QAction("&Jakarta", self)
        self.nightModeAction = QAction("Night Mode", self)
        self.nightModeAction.setCheckable(True)
        self.nightModeAction.setChecked(False)
        self.osmAction = QAction("About OpenStreetMap", self)
        self.osloAction.triggered.connect(self.chooseOslo)
        self.berlinAction.triggered.connect(self.chooseBerlin)
        self.jakartaAction.triggered.connect(self.chooseJakarta)
        self.nightModeAction.triggered.connect(self.map_.toggleNightMode)
        self.osmAction.triggered.connect(self.aboutOsm)

        menu = self.menuBar().addMenu("&Options")
        menu.addAction(self.osloAction)
        menu.addAction(self.berlinAction)
        menu.addAction(self.jakartaAction)
        menu.addSeparator()
        menu.addAction(self.nightModeAction)
        menu.addAction(self.osmAction)

    # slots
    def chooseOslo(self):
        self.map_.setCenter(59.9138204, 10.7387413)

    def chooseBerlin(self):
        self.map_.setCenter(52.52958999943302, 13.383053541183472)

    def chooseJakarta(self):
        self.map_.setCenter(-6.211544, 106.845172)

    def aboutOsm(self):
        QDesktopServices.openUrl(QUrl('http://www.openstreetmap.org'))


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('LightMaps')
    w = MapZoom()
    w.setWindowTitle("OpenStreetMap")
    w.resize(600, 450)
    w.show()
    sys.exit(app.exec_())
