#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2018 Riverbank Computing Limited.
## Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
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
##   * Neither the name of Digia Plc and its Subsidiary(-ies) nor the names
##     of its contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
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


from PyQt5.QtCore import pyqtProperty, QRectF, QUrl
from PyQt5.QtGui import QColor, QGuiApplication, QPainter, QPen
from PyQt5.QtQml import qmlRegisterType, QQmlListProperty
from PyQt5.QtQuick import QQuickItem, QQuickPaintedItem, QQuickView


class PieSlice(QQuickPaintedItem):

    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = QColor(color)

    @pyqtProperty(int)
    def fromAngle(self):
        return self._fromAngle

    @fromAngle.setter
    def fromAngle(self, fromAngle):
        self._fromAngle = fromAngle

    @pyqtProperty(int)
    def angleSpan(self):
        return self._angleSpan

    @angleSpan.setter
    def angleSpan(self, angleSpan):
        self._angleSpan = angleSpan

    def __init__(self, parent=None):
        super(PieSlice, self).__init__(parent)

        self._color = QColor()
        self._fromAngle = 0
        self._angleSpan = 0

    def paint(self, painter):
        painter.setPen(QPen(self._color, 2))
        painter.setRenderHints(QPainter.Antialiasing, True)

        rect = QRectF(0, 0, self.width(), self.height()).adjusted(1, 1, -1, -1)
        painter.drawPie(rect, self._fromAngle * 16, self._angleSpan * 16)


class PieChart(QQuickItem):

    @pyqtProperty(QQmlListProperty)
    def slices(self):
        return QQmlListProperty(PieSlice, self,
                append=lambda pie_ch, pie_sl: pie_sl.setParentItem(pie_ch))

    @pyqtProperty(str)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def __init__(self, parent=None):
        super(PieChart, self).__init__(parent)

        self._name = ''


if __name__ == '__main__':
    import os
    import sys

    app = QGuiApplication(sys.argv)

    qmlRegisterType(PieChart, "Charts", 1, 0, "PieChart")
    qmlRegisterType(PieSlice, "Charts", 1, 0, "PieSlice")

    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.setSource(
            QUrl.fromLocalFile(
                    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'app.qml')))
    view.show()

    sys.exit(app.exec_())
