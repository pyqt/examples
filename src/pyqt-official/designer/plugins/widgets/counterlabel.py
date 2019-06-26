#!/usr/bin/env python

"""
counterlabel.py

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

from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QRectF, QSize, Qt
from PyQt5.QtGui import QFont, QFontMetricsF, QPainter
from PyQt5.QtWidgets import QApplication, QWidget


class CounterLabel(QWidget):
    """CounterLabel(QWidget)

    Provides a custom label widget to be used as a counter, with signals
    similar to those provided by QAbstractSlider subclasses and properties
    similar to those provided by QLabel.
    """

    # We define two signals that are used to indicate changes to the status
    # of the widget.
    valueChanged = pyqtSignal((int, ), (str, ))

    def __init__(self, parent=None):

        super(CounterLabel, self).__init__(parent)

        self.setAutoFillBackground(False)

        self._font = QFont()
        self._minimum = 1
        self._maximum = 1
        self._value = 1
        self._offset = 0
        self.rescale()
        self.reposition()

    def paintEvent(self, event):

        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self._font)
        p.translate(self.width()/2.0, self.height()/2.0)
        p.scale(self._scale, self._scale)
        p.drawText(self._xpos, self._ypos, str(self._value))
        p.end()

    def sizeHint(self):
        return QSize(32, 32)

    def rescale(self):

        fm = QFontMetricsF(self._font, self)
        maxRect = fm.boundingRect(QRectF(self.rect()), Qt.AlignCenter,
                str(self._maximum))
        xscale = float(self.width())/maxRect.width()
        yscale = float(self.height())/maxRect.height()
        self._scale = min(xscale, yscale)

    def reposition(self):

        fm = QFontMetricsF(self._font, self)
        rect = fm.boundingRect(QRectF(self.rect()), Qt.AlignCenter,
                str(self._value))
        self._xpos = -rect.width()/2.0
        self._ypos = rect.height()/2.0 - fm.descent()
        self.update()

    # Provide getter and setter methods for the font property.

    def getFont(self):
        return self._font

    def setFont(self, font):
        self._font = font
        self.rescale()
        self.reposition()

    font = pyqtProperty(QFont, getFont, setFont)

    # Provide getter and setter methods for the minimum and maximum properties.

    def getMinimum(self):
        return self._minimum

    def setMinimum(self, value):
        self._minimum = value
        if self._minimum > self._maximum:
            self.setMaximum(self._minimum)
        if self._minimum > self._value:
            self.setValue(self._minimum)

    minimum = pyqtProperty(int, getMinimum, setMinimum)

    def getMaximum(self):
        return self._maximum

    def setMaximum(self, value):
        self._maximum = value
        self._minimum = min(self._minimum, self._maximum)
        if self._maximum < self._value:
            self.setValue(self._maximum)
        self.rescale()
        self.reposition()

    maximum = pyqtProperty(int, getMaximum, setMaximum)

    # We provide an offset property to allow the value shown to differ from
    # the internal value held by the widget.

    def getOffset(self):
        return self._offset

    def setOffset(self, value):
        self._offset = value

    offset = pyqtProperty(int, getOffset, setOffset)

    # The value property is implemented using the getValue() and setValue()
    # methods.

    def getValue(self):
        return self._value

    # The setter method for the value property can also be used as a slot.
    @pyqtSlot(int)
    def setValue(self, value):
        if not self._minimum <= value <= self._maximum:
            return
        self._value = value
        self.valueChanged[int].emit(value + self._offset)
        self.valueChanged[str].emit(str(value + self._offset))
        self.reposition()

    value = pyqtProperty(int, getValue, setValue)

    # Like QAbstractSpinBox, we provide stepUp() and stepDown() slots to
    # enable the value to be incremented and decremented.

    @pyqtSlot()
    def stepUp(self):
        self.setValue(self._value + 1)

    @pyqtSlot()
    def stepDown(self):
        self.setValue(self._value - 1)


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    widget = CounterLabel()
    widget.setValue(123)
    widget.show()
    sys.exit(app.exec_())
