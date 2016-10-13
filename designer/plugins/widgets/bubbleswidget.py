#!/usr/bin/env python

"""
bubbleswidget.py

A PyQt custom widget example for Qt Designer.

Copyright (C) 2006 David Boddie <david@boddie.org.uk>
Copyright (C) 2005-2006 Trolltech ASA. All rights reserved.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import random

from PyQt5.QtCore import (pyqtProperty, pyqtSignal, pyqtSlot, QPointF, QRectF,
        QSize, QSizeF, Qt, QTimer)
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QRadialGradient
from PyQt5.QtWidgets import QApplication, QWidget


class BaseClass(QWidget):
    """BaseClass(QWidget)

    Provides a base custom widget class to show that properties implemented
    in Python can be inherited and shown as belonging to distinct classes
    in Qt Designer's Property Editor.
    """

    def __init__(self, parent=None):

        super(BaseClass, self).__init__(parent)

        self.resetAuthor()

    # Define getter, setter and resetter methods for the author property.

    def getAuthor(self):
        return self._author

    def setAuthor(self, name):
        self._author = name

    def resetAuthor(self):
        self._author = "David Boddie"

    author = pyqtProperty(str, getAuthor, setAuthor, resetAuthor)


class Bubble:
    """Bubble

    Provides a class to represent individual bubbles in a BubblesWidget.
    Each Bubble instance can render itself onto a paint device using a
    QPainter passed to its drawBubble() method.
    """

    def __init__(self, position, radius, speed, innerColor, outerColor):

        self.position = position
        self.radius = radius
        self.speed = speed
        self.innerColor = innerColor
        self.outerColor = outerColor
        self.updateBrush()

    def updateBrush(self):

        gradient = QRadialGradient(
                QPointF(self.radius, self.radius), self.radius,
                QPointF(self.radius*0.5, self.radius*0.5))

        gradient.setColorAt(0, QColor(255, 255, 255, 255))
        gradient.setColorAt(0.25, self.innerColor)
        gradient.setColorAt(1, self.outerColor)
        self.brush = QBrush(gradient)

    def drawBubble(self, painter):

        painter.save()
        painter.translate(self.position.x() - self.radius,
                          self.position.y() - self.radius)
        painter.setBrush(self.brush)
        painter.drawEllipse(0.0, 0.0, 2*self.radius, 2*self.radius)
        painter.restore()


class BubblesWidget(BaseClass):
    """BubblesWidget(BaseClass)

    Provides a custom widget that shows a number of rising bubbles.
    Various properties are defined so that the user can customize the
    appearance of the widget, and change the number and behaviour of the
    bubbles shown.
    """

    # We define two signals that are used to indicate changes to the status
    # of the widget.
    bubbleLeft = pyqtSignal()
    bubblesRemaining = pyqtSignal(int)

    def __init__(self, parent=None):

        super(BubblesWidget, self).__init__(parent)

        self.pen = QPen(QColor("#cccccc"))
        self.bubbles = []
        self.backgroundColor1 = self.randomColor()
        self.backgroundColor2 = self.randomColor().darker(150)
        self.newBubble = None

        random.seed()

        self.animation_timer = QTimer(self)
        self.animation_timer.setSingleShot(False)
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.start(25)

        self.bubbleTimer = QTimer()
        self.bubbleTimer.setSingleShot(False)
        self.bubbleTimer.timeout.connect(self.expandBubble)

        self.setMouseTracking(True)
        self.setMinimumSize(QSize(200, 200))
        self.setWindowTitle("Bubble Maker")

    def paintEvent(self, event):

        background = QRadialGradient(QPointF(self.rect().topLeft()), 500,
                QPointF(self.rect().bottomRight()))
        background.setColorAt(0, self.backgroundColor1)
        background.setColorAt(1, self.backgroundColor2)

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(background))

        painter.setPen(self.pen)

        for bubble in self.bubbles:

            if QRectF(bubble.position - QPointF(bubble.radius, bubble.radius),
                      QSizeF(2*bubble.radius, 2*bubble.radius)).intersects(QRectF(event.rect())):
                bubble.drawBubble(painter)

        if self.newBubble:

            self.newBubble.drawBubble(painter)

        painter.end()

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton and self.newBubble is None:

            self.newBubble = Bubble(QPointF(event.pos()), 4.0,
                                    1.0 + random.random() * 7,
                                    self.randomColor(), self.randomColor())
            self.bubbleTimer.start(50)
            event.accept()

    def mouseMoveEvent(self, event):

        if self.newBubble:

            self.update(
                QRectF(self.newBubble.position - \
                       QPointF(self.newBubble.radius + 1, self.newBubble.radius + 1),
                       QSizeF(2*self.newBubble.radius + 2, 2*self.newBubble.radius + 2)).toRect()
                )
            self.newBubble.position = QPointF(event.pos())
            self.update(
                QRectF(self.newBubble.position - \
                       QPointF(self.newBubble.radius + 1, self.newBubble.radius + 1),
                       QSizeF(2*self.newBubble.radius + 2, 2*self.newBubble.radius + 2)).toRect()
                )

        event.accept()

    def mouseReleaseEvent(self, event):

        if self.newBubble:

            self.bubbles.append(self.newBubble)
            self.newBubble = None
            self.bubbleTimer.stop()
            self.bubblesRemaining.emit(len(self.bubbles))

        event.accept()

    def expandBubble(self):

        if self.newBubble:

            self.newBubble.radius = min(self.newBubble.radius + 4.0,
                                        self.width()/8.0, self.height()/8.0)
            self.update(
                QRectF(self.newBubble.position - \
                       QPointF(self.newBubble.radius + 1, self.newBubble.radius + 1),
                       QSizeF(2*self.newBubble.radius + 2, 2*self.newBubble.radius + 2)).toRect()
                )
            self.newBubble.updateBrush()

    def randomColor(self):

        red = 205 + random.random() * 50
        green = 205 + random.random() * 50
        blue = 205 + random.random() * 50
        alpha = 91 + random.random() * 100

        return QColor(red, green, blue, alpha)

    def animate(self):

        bubbles = []
        left = False
        for bubble in self.bubbles:

            bubble.position = bubble.position + QPointF(0, -bubble.speed)

            self.update(
                    QRectF(bubble.position - QPointF(bubble.radius + 1,
                                    bubble.radius + 1),
                            QSizeF(2*bubble.radius + 2, 2*bubble.radius + 2 + bubble.speed)).toRect())

            if bubble.position.y() + bubble.radius > 0:
                bubbles.append(bubble)
            else:
                self.bubbleLeft.emit()
                left = True

        if self.newBubble:
            self.update(
                    QRectF(self.newBubble.position - QPointF(
                                    self.newBubble.radius + 1,
                                    self.newBubble.radius + 1),
                            QSizeF(2*self.newBubble.radius + 2, 2*self.newBubble.radius + 2)).toRect())

        self.bubbles = bubbles
        if left:
            self.bubblesRemaining.emit(len(self.bubbles))

    def sizeHint(self):

        return QSize(200, 200)

    # We provide getter and setter methods for the numberOfBubbles property.
    def getBubbles(self):

        return len(self.bubbles)

    # The setBubbles() method can also be used as a slot.
    @pyqtSlot(int)
    def setBubbles(self, value):

        value = max(0, value)

        while len(self.bubbles) < value:

            newBubble = Bubble(QPointF(random.random() * self.width(),
                                       random.random() * self.height()),
                               4.0 + random.random() * 20,
                               1.0 + random.random() * 7,
                               self.randomColor(), self.randomColor())
            newBubble.updateBrush()
            self.bubbles.append(newBubble)

        self.bubbles = self.bubbles[:value]
        self.bubblesRemaining.emit(value)
        self.update()

    numberOfBubbles = pyqtProperty(int, getBubbles, setBubbles)

    # We provide getter and setter methods for the color1 and color2
    # properties. The red, green and blue components for the QColor
    # values stored in these properties can be edited individually in
    # Qt Designer.

    def getColor1(self):

        return self.backgroundColor1

    def setColor1(self, value):

        self.backgroundColor1 = QColor(value)
        self.update()

    color1 = pyqtProperty(QColor, getColor1, setColor1)

    def getColor2(self):

        return self.backgroundColor2

    def setColor2(self, value):

        self.backgroundColor2 = QColor(value)
        self.update()

    color2 = pyqtProperty(QColor, getColor2, setColor2)

    # The stop() and start() slots provide simple control over the animation
    # of the bubbles in the widget.

    @pyqtSlot()
    def stop(self):

        self.animation_timer.stop()

    @pyqtSlot()
    def start(self):

        self.animation_timer.start(25)


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    widget = BubblesWidget()
    widget.show()
    sys.exit(app.exec_())
