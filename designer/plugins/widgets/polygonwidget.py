#!/usr/bin/env python

"""
polygonwidget.py

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

import math

from PyQt5.QtCore import pyqtProperty, pyqtSlot, QPointF, QSize
from PyQt5.QtGui import QBrush, QColor, QPainter, QPainterPath, QRadialGradient
from PyQt5.QtWidgets import QApplication, QWidget


class PolygonWidget(QWidget):
    """PolygonWidget(QWidget)
    
    Provides a custom widget to display a polygon with properties and slots
    that can be used to customize its appearance.
    """
    
    def __init__(self, parent=None):
    
        super(PolygonWidget, self).__init__(parent)
        
        self._sides = 5
        self._innerRadius = 20
        self._outerRadius = 50
        self._angle = 0
        
        self.createPath()
        
        self._innerColor = QColor(255, 255, 128)
        self._outerColor = QColor(255, 0, 128)
        
        self.createGradient()
    
    def paintEvent(self, event):
    
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(192, 192, 255)))
        painter.drawRect(event.rect())
        
        painter.translate(self.width()/2.0, self.height()/2.0)
        painter.rotate(self._angle)
        painter.setBrush(QBrush(self.gradient))
        painter.drawPath(self.path)
        painter.end()
    
    def sizeHint(self):
    
        return QSize(2*self._outerRadius + 20, 2*self._outerRadius + 20)
    
    def createPath(self):
    
        self.path = QPainterPath()
        angle = 2*math.pi/self._sides
        self.path.moveTo(self._outerRadius, 0)
        for step in range(1, self._sides + 1):
            self.path.lineTo(
                self._innerRadius * math.cos((step - 0.5) * angle),
                self._innerRadius * math.sin((step - 0.5) * angle)
                )
            self.path.lineTo(
                self._outerRadius * math.cos(step * angle),
                self._outerRadius * math.sin(step * angle)
                )
        self.path.closeSubpath()
    
    def createGradient(self):
    
        center = QPointF(0, 0)
        self.gradient = QRadialGradient(center, self._outerRadius, center)
        self.gradient.setColorAt(0.5, QColor(self._innerColor))
        self.gradient.setColorAt(1.0, QColor(self._outerColor))
    
    # The angle property is implemented using the getAngle() and setAngle()
    # methods.
    
    def getAngle(self):
        return self._angle
    
    # The setAngle() setter method is also a slot.
    @pyqtSlot(int)
    def setAngle(self, angle):
        self._angle = min(max(0, angle), 360)
        self.update()
    
    angle = pyqtProperty(int, getAngle, setAngle)
    
    # The innerRadius property is implemented using the getInnerRadius() and
    # setInnerRadius() methods.
    
    def getInnerRadius(self):
        return self._innerRadius
    
    # The setInnerRadius() setter method is also a slot.
    @pyqtSlot(int)
    def setInnerRadius(self, radius):
        self._innerRadius = radius
        self.createPath()
        self.createGradient()
        self.update()
    
    innerRadius = pyqtProperty(int, getInnerRadius, setInnerRadius)
    
    # The outerRadius property is implemented using the getOuterRadius() and
    # setOuterRadius() methods.
    
    def getOuterRadius(self):
        return self._outerRadius
    
    # The setOuterRadius() setter method is also a slot.
    @pyqtSlot(int)
    def setOuterRadius(self, radius):
        self._outerRadius = radius
        self.createPath()
        self.createGradient()
        self.update()
    
    outerRadius = pyqtProperty(int, getOuterRadius, setOuterRadius)
    
    # The numberOfSides property is implemented using the getNumberOfSides()
    # and setNumberOfSides() methods.
    
    def getNumberOfSides(self):
        return self._sides
    
    # The setNumberOfSides() setter method is also a slot.
    @pyqtSlot(int)
    def setNumberOfSides(self, sides):
        self._sides = max(3, sides)
        self.createPath()
        self.update()
    
    numberOfSides = pyqtProperty(int, getNumberOfSides, setNumberOfSides)
    
    # The innerColor property is implemented using the getInnerColor() and
    # setInnerColor() methods.
    
    def getInnerColor(self):
        return self._innerColor
    
    def setInnerColor(self, color):
        self._innerColor = max(3, color)
        self.createGradient()
        self.update()
    
    innerColor = pyqtProperty(QColor, getInnerColor, setInnerColor)
    
    # The outerColor property is implemented using the getOuterColor() and
    # setOuterColor() methods.
    
    def getOuterColor(self):
        return self._outerColor
    
    def setOuterColor(self, color):
        self._outerColor = color
        self.createGradient()
        self.update()
    
    outerColor = pyqtProperty(QColor, getOuterColor, setOuterColor)


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    window = PolygonWidget()
    window.show()
    sys.exit(app.exec_())
