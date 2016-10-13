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


from PyQt5.QtCore import QPoint, QSize, Qt, QTime, QTimer
from PyQt5.QtGui import QColor, QPainter, QPolygon, QRegion
from PyQt5.QtWidgets import QAction, QApplication, QWidget


class ShapedClock(QWidget):
    hourHand = QPolygon([
        QPoint(7, 8),
        QPoint(-7, 8),
        QPoint(0, -40)
    ])

    minuteHand = QPolygon([
        QPoint(7, 8),
        QPoint(-7, 8),
        QPoint(0, -70)
    ])

    hourColor = QColor(127, 0, 127)
    minuteColor = QColor(0, 127, 127, 191)

    def __init__(self, parent=None):
        super(ShapedClock, self).__init__(parent,
                Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

        quitAction = QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=QApplication.instance().quit)
        self.addAction(quitAction)

        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setToolTip("Drag the clock with the left mouse button.\n"
                "Use the right mouse button to open a context menu.")
        self.setWindowTitle(self.tr("Shaped Analog Clock"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def paintEvent(self, event):
        side = min(self.width(), self.height())
        time = QTime.currentTime()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        painter.setPen(Qt.NoPen)
        painter.setBrush(ShapedClock.hourColor)

        painter.save()
        painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
        painter.drawConvexPolygon(ShapedClock.hourHand)
        painter.restore()

        painter.setPen(ShapedClock.hourColor)

        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)

        painter.setPen(Qt.NoPen)
        painter.setBrush(ShapedClock.minuteColor)

        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(ShapedClock.minuteHand)
        painter.restore()

        painter.setPen(ShapedClock.minuteColor)

        for j in range(60):
            if (j % 5) != 0:
                painter.drawLine(92, 0, 96, 0)

            painter.rotate(6.0)

    def resizeEvent(self, event):
        side = min(self.width(), self.height())

        maskedRegion = QRegion(self.width()/2 - side/2, self.height()/2 - side/2, side, side, QRegion.Ellipse)
        self.setMask(maskedRegion)

    def sizeHint(self):
        return QSize(100, 100)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    clock = ShapedClock()
    clock.show()
    sys.exit(app.exec_())    
