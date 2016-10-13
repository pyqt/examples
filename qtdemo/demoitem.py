#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
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


from PyQt5.QtCore import QPointF, QRectF, qRound
from PyQt5.QtGui import QColor, QPainter, QPixmap, QTransform
from PyQt5.QtWidgets import QGraphicsObject

from colors import Colors


class SharedImage(object):
    def __init__(self):
        self.refCount = 0
        self.image = None
        self.pixmap = None
        self.transform = QTransform()
        self.unscaledBoundingRect = QRectF()


class DemoItem(QGraphicsObject):
    _sharedImageHash = {}

    _transform = QTransform()

    def __init__(self, parent=None):
        super(DemoItem, self).__init__(parent)

        self.noSubPixeling = False
        self.currentAnimation = None
        self.currGuide = None
        self.guideFrame = 0.0

        self._sharedImage = SharedImage()
        self._sharedImage.refCount += 1
        self._hashKey = ''

    def __del__(self):
        self._sharedImage.refCount -= 1
        if self._sharedImage.refCount == 0:
            if self._hashKey:
                del DemoItem._sharedImageHash[self._hashKey]

    def animationStarted(self, id=0):
        pass

    def animationStopped(self, id=0):
        pass

    def setRecursiveVisible(self, visible):
        self.setVisible(visible)
        for c in self.childItems():
            c.setVisible(visible)

    def useGuide(self, guide, startFrame):
        self.guideFrame = startFrame
        while self.guideFrame > guide.startLength + guide.length():
            if guide.nextGuide == guide.firstGuide:
                break

            guide = guide.nextGuide

        self.currGuide = guide

    def guideAdvance(self, distance):
        self.guideFrame += distance
        while self.guideFrame > self.currGuide.startLength + self.currGuide.length():
            self.currGuide = self.currGuide.nextGuide
            if self.currGuide == self.currGuide.firstGuide:
                self.guideFrame -= self.currGuide.lengthAll()

    def guideMove(self, moveSpeed):
        self.currGuide.guide(self, moveSpeed)

    def setPosUsingSheepDog(self, dest, sceneFence):
        self.setPos(dest)
        if sceneFence.isNull():
            return

        itemWidth = self.boundingRect().width()
        itemHeight = self.boundingRect().height()
        fenceRight = sceneFence.x() + sceneFence.width()
        fenceBottom = sceneFence.y() + sceneFence.height()

        if self.scenePos().x() < sceneFence.x():
            self.moveBy(self.mapFromScene(QPointF(sceneFence.x(), 0)).x(), 0)

        if self.scenePos().x() > fenceRight - itemWidth:
            self.moveBy(self.mapFromScene(QPointF(fenceRight - itemWidth, 0)).x(), 0)

        if self.scenePos().y() < sceneFence.y():
            self.moveBy(0, self.mapFromScene(QPointF(0, sceneFence.y())).y())

        if self.scenePos().y() > fenceBottom - itemHeight:
            self.moveBy(0, self.mapFromScene(QPointF(0, fenceBottom - itemHeight)).y())

    def setGuidedPos(self, pos):
        # Make sure we have a copy.
        self.guidedPos = QPointF(pos)

    def getGuidedPos(self):
        # Return a copy so that it can be changed.
        return QPointF(self.guidedPos)

    @staticmethod
    def setTransform(transform):
        DemoItem._transform = transform

    def useSharedImage(self, hashKey):
        self._hashKey = hashKey
        if hashKey not in DemoItem._sharedImageHash:
            DemoItem._sharedImageHash[hashKey] = self._sharedImage
        else:
            self._sharedImage.refCount -= 1
            self._sharedImage = DemoItem._sharedImageHash[hashKey]
            self._sharedImage.refCount += 1

    def createImage(self, transform):
        return None

    def _validateImage(self):
        if (self._sharedImage.transform != DemoItem._transform and not Colors.noRescale) or (self._sharedImage.image is None and self._sharedImage.pixmap is None):
            # (Re)create image according to new transform.
            self._sharedImage.image = None
            self._sharedImage.pixmap = None
            self._sharedImage.transform = DemoItem._transform

            # Let subclass create and draw a new image according to the new
            # transform.
            if Colors.noRescale:
                transform = QTransform()
            else:
                transform = DemoItem._transform
            image = self.createImage(transform)
            if image is not None:
                if Colors.showBoundingRect:
                    # Draw red transparent rect.
                    painter = QPainter(image)
                    painter.fillRect(image.rect(), QColor(255, 0, 0, 50))
                    painter.end()

                self._sharedImage.unscaledBoundingRect = self._sharedImage.transform.inverted()[0].mapRect(QRectF(image.rect()))

                if Colors.usePixmaps:
                    if image.isNull():
                        self._sharedImage.pixmap = QPixmap(1, 1)
                    else:
                        self._sharedImage.pixmap = QPixmap(image.size())

                    self._sharedImage.pixmap.fill(QColor(0, 0, 0, 0))
                    painter = QPainter(self._sharedImage.pixmap)
                    painter.drawImage(0, 0, image)
                else:
                    self._sharedImage.image = image

                return True
            else:
                return False

        return True

    def boundingRect(self):
        self._validateImage()
        return self._sharedImage.unscaledBoundingRect

    def paint(self, painter, option=None, widget=None):
        if self._validateImage():
            wasSmoothPixmapTransform = painter.testRenderHint(QPainter.SmoothPixmapTransform)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)

            if Colors.noRescale:
                # Let the painter scale the image for us.  This may degrade
                # both quality and performance.
                if self._sharedImage.image is not None:
                    painter.drawImage(self.pos(), self._sharedImage.image)
                else:
                    painter.drawPixmap(self.pos(), self._sharedImage.pixmap)
            else:
                m = painter.worldTransform()
                painter.setWorldTransform(QTransform())

                x = m.dx()
                y = m.dy()
                if self.noSubPixeling:
                    x = qRound(x)
                    y = qRound(y)

                if self._sharedImage.image is not None:
                    painter.drawImage(QPointF(x, y), self._sharedImage.image)
                else:
                    painter.drawPixmap(QPointF(x, y), self._sharedImage.pixmap)

            if not wasSmoothPixmapTransform:
                painter.setRenderHint(QPainter.SmoothPixmapTransform,
                        False)

    def collidesWithItem(self, item, mode):
        return False
