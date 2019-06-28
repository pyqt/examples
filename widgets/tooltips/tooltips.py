#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


import random

from PyQt5.QtCore import QEvent, QPoint, QPointF, QSize, Qt
from PyQt5.QtGui import QColor, QIcon, QPainter, QPainterPath, QPalette
from PyQt5.QtWidgets import (QApplication, QStyle, QToolButton, QToolTip,
        QWidget)

import tooltips_rc


class ShapeItem(object):
    def __init__(self):    
        self.myPath = QPainterPath()
        self.myPosition = QPoint()
        self.myColor  = QColor()
        self.myToolTip = ''

    def path(self):
        return self.myPath

    def position(self):
        return self.myPosition

    def color(self):
        return self.myColor

    def toolTip(self):
        return self.myToolTip

    def setPath(self, path):
        self.myPath = path

    def setToolTip(self, toolTip):
        self.myToolTip = toolTip

    def setPosition(self, position):
        self.myPosition = position

    def setColor(self, color):
        self.myColor = color


class SortingBox(QWidget):
    circle_count = square_count = triangle_count = 1

    def __init__(self):
        super(SortingBox, self).__init__()

        self.circlePath = QPainterPath()
        self.squarePath = QPainterPath()
        self.trianglePath = QPainterPath()
        self.shapeItems = []        

        self.previousPosition = QPoint()

        self.setMouseTracking(True)
        self.setBackgroundRole(QPalette.Base)

        self.itemInMotion = None

        self.newCircleButton = self.createToolButton("New Circle",
                QIcon(':/images/circle.png'), self.createNewCircle)
        self.newSquareButton = self.createToolButton("New Square",
                QIcon(':/images/square.png'), self.createNewSquare)
        self.newTriangleButton = self.createToolButton("New Triangle",
                QIcon(':/images/triangle.png'), self.createNewTriangle)

        self.circlePath.addEllipse(0, 0, 100, 100)
        self.squarePath.addRect(0, 0, 100, 100)

        x = self.trianglePath.currentPosition().x()
        y = self.trianglePath.currentPosition().y()
        self.trianglePath.moveTo(x + 120 / 2, y)
        self.trianglePath.lineTo(0, 100)
        self.trianglePath.lineTo(120, 100)
        self.trianglePath.lineTo(x + 120 / 2, y)

        self.setWindowTitle("Tooltips")
        self.resize(500, 300)

        self.createShapeItem(self.circlePath, "Circle",
                self.initialItemPosition(self.circlePath),
                self.initialItemColor())
        self.createShapeItem(self.squarePath, "Square",
                self.initialItemPosition(self.squarePath),
                self.initialItemColor())
        self.createShapeItem(self.trianglePath, "Triangle",
                self.initialItemPosition(self.trianglePath),
                self.initialItemColor())

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            helpEvent = event
            index = self.itemAt(helpEvent.pos())
            if index != -1:
                QToolTip.showText(helpEvent.globalPos(),
                        self.shapeItems[index].toolTip())
            else:
                QToolTip.hideText()
                event.ignore()

            return True

        return super(SortingBox, self).event(event)

    def resizeEvent(self, event):
        margin = self.style().pixelMetric(QStyle.PM_DefaultTopLevelMargin)
        x = self.width() - margin
        y = self.height() - margin

        y = self.updateButtonGeometry(self.newCircleButton, x, y)
        y = self.updateButtonGeometry(self.newSquareButton, x, y)
        self.updateButtonGeometry(self.newTriangleButton, x, y)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for shapeItem in self.shapeItems:
            painter.translate(shapeItem.position())
            painter.setBrush(shapeItem.color())
            painter.drawPath(shapeItem.path())
            painter.translate(-shapeItem.position())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            index = self.itemAt(event.pos())
            if index != -1:
                self.itemInMotion = self.shapeItems[index]
                self.previousPosition = event.pos()

                value = self.shapeItems[index]
                del self.shapeItems[index]
                self.shapeItems.insert(len(self.shapeItems) - 1, value)

                self.update()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.itemInMotion:
            self.moveItemTo(event.pos())

    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton) and self.itemInMotion:
            self.moveItemTo(event.pos())
            self.itemInMotion = None

    def createNewCircle(self):
        SortingBox.circle_count += 1
        self.createShapeItem(self.circlePath,
                "Circle <%d>" % SortingBox.circle_count,
                self.randomItemPosition(), self.randomItemColor())

    def createNewSquare(self):
        SortingBox.square_count += 1
        self.createShapeItem(self.squarePath,
                "Square <%d>" % SortingBox.square_count,
                self.randomItemPosition(), self.randomItemColor())

    def createNewTriangle(self):
        SortingBox.triangle_count += 1
        self.createShapeItem(self.trianglePath,
                "Triangle <%d>" % SortingBox.triangle_count,
                self.randomItemPosition(), self.randomItemColor())

    def itemAt(self, pos):
        for i in range(len(self.shapeItems) - 1, -1, -1):
            item = self.shapeItems[i]
            if item.path().contains(QPointF(pos - item.position())):
                return i

        return -1

    def moveItemTo(self, pos):
        offset = pos - self.previousPosition
        self.itemInMotion.setPosition(self.itemInMotion.position() + offset)
        self.previousPosition = QPoint(pos)
        self.update()

    def updateButtonGeometry(self, button, x, y):
        size = button.sizeHint()
        button.setGeometry(x - size.width(), y - size.height(),
                size.width(), size.height())

        return y - size.height() - self.style().pixelMetric(QStyle.PM_DefaultLayoutSpacing)

    def createShapeItem(self, path, toolTip, pos, color):
        shapeItem = ShapeItem()
        shapeItem.setPath(path)
        shapeItem.setToolTip(toolTip)
        shapeItem.setPosition(pos)
        shapeItem.setColor(color)
        self.shapeItems.append(shapeItem)
        self.update()

    def createToolButton(self, toolTip, icon, member):
        button = QToolButton(self)
        button.setToolTip(toolTip)
        button.setIcon(icon)
        button.setIconSize(QSize(32, 32))
        button.clicked.connect(member)

        return button

    def initialItemPosition(self, path):
        y = (self.height() - path.controlPointRect().height()) / 2

        if len(self.shapeItems) == 0:
            x = ((3 * self.width()) / 2 - path.controlPointRect().width()) / 2
        else:
            x = (self.width() / len(self.shapeItems) - path.controlPointRect().width()) / 2

        return QPoint(x, y)

    def randomItemPosition(self):
        x = random.randint(0, self.width() - 120)
        y = random.randint(0, self.height() - 120)

        return QPoint(x, y)

    def initialItemColor(self):
        hue = ((len(self.shapeItems) + 1) * 85) % 256
        return QColor.fromHsv(hue, 255, 190)

    def randomItemColor(self):
        return QColor.fromHsv(random.randint(0, 256), 255, 190)


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    sortingBox = SortingBox()
    sortingBox.show()
    sys.exit(app.exec_())
