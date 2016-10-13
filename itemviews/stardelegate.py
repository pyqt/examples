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


import math

from PyQt5.QtCore import pyqtSignal, QPointF, QSize, Qt
from PyQt5.QtGui import QPainter, QPolygonF
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QStyle,
        QStyledItemDelegate, QTableWidget, QTableWidgetItem, QWidget)


class StarRating(object):
    # enum EditMode
    Editable, ReadOnly = range(2)

    PaintingScaleFactor = 20

    def __init__(self, starCount=1, maxStarCount=5):
        self._starCount = starCount
        self._maxStarCount = maxStarCount

        self.starPolygon = QPolygonF([QPointF(1.0, 0.5)])
        for i in range(5):
            self.starPolygon << QPointF(0.5 + 0.5 * math.cos(0.8 * i * math.pi),
                                        0.5 + 0.5 * math.sin(0.8 * i * math.pi))

        self.diamondPolygon = QPolygonF()
        self.diamondPolygon << QPointF(0.4, 0.5) \
                            << QPointF(0.5, 0.4) \
                            << QPointF(0.6, 0.5) \
                            << QPointF(0.5, 0.6) \
                            << QPointF(0.4, 0.5)

    def starCount(self):
        return self._starCount

    def maxStarCount(self):
        return self._maxStarCount

    def setStarCount(self, starCount):
        self._starCount = starCount

    def setMaxStarCount(self, maxStarCount):
        self._maxStarCount = maxStarCount

    def sizeHint(self):
        return self.PaintingScaleFactor * QSize(self._maxStarCount, 1)

    def paint(self, painter, rect, palette, editMode):
        painter.save()

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)

        if editMode == StarRating.Editable:
            painter.setBrush(palette.highlight())
        else:
            painter.setBrush(palette.windowText())

        yOffset = (rect.height() - self.PaintingScaleFactor) / 2
        painter.translate(rect.x(), rect.y() + yOffset)
        painter.scale(self.PaintingScaleFactor, self.PaintingScaleFactor)

        for i in range(self._maxStarCount):
            if i < self._starCount:
                painter.drawPolygon(self.starPolygon, Qt.WindingFill)
            elif editMode == StarRating.Editable:
                painter.drawPolygon(self.diamondPolygon, Qt.WindingFill)

            painter.translate(1.0, 0.0)

        painter.restore()


class StarEditor(QWidget):

    editingFinished = pyqtSignal()

    def __init__(self, parent = None):
        super(StarEditor, self).__init__(parent)

        self._starRating = StarRating()

        self.setMouseTracking(True)
        self.setAutoFillBackground(True)

    def setStarRating(self, starRating):
        self._starRating = starRating

    def starRating(self):
        return self._starRating

    def sizeHint(self):
        return self._starRating.sizeHint()

    def paintEvent(self, event):
        painter = QPainter(self)
        self._starRating.paint(painter, self.rect(), self.palette(),
                StarRating.Editable)

    def mouseMoveEvent(self, event):
        star = self.starAtPosition(event.x())

        if star != self._starRating.starCount() and star != -1:
            self._starRating.setStarCount(star)
            self.update()

    def mouseReleaseEvent(self, event):
        self.editingFinished.emit()

    def starAtPosition(self, x):
        # Enable a star, if pointer crosses the center horizontally.
        starwidth = self._starRating.sizeHint().width() // self._starRating.maxStarCount()
        star = (x + starwidth / 2) // starwidth
        if 0 <= star <= self._starRating.maxStarCount():
            return star

        return -1


class StarDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        starRating = index.data()
        if isinstance(starRating, StarRating):
            if option.state & QStyle.State_Selected:
                painter.fillRect(option.rect, option.palette.highlight())

            starRating.paint(painter, option.rect, option.palette,
                    StarRating.ReadOnly)
        else:
            super(StarDelegate, self).paint(painter, option, index)

    def sizeHint(self, option, index):
        starRating = index.data()
        if isinstance(starRating, StarRating):
            return starRating.sizeHint()
        else:
            return super(StarDelegate, self).sizeHint(option, index)

    def createEditor(self, parent, option, index):
        starRating = index.data()
        if isinstance(starRating, StarRating):
            editor = StarEditor(parent)
            editor.editingFinished.connect(self.commitAndCloseEditor)
            return editor
        else:
            return super(StarDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        starRating = index.data()
        if isinstance(starRating, StarRating):
            editor.setStarRating(starRating)
        else:
            super(StarDelegate, self).setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        starRating = index.data()
        if isinstance(starRating, StarRating):
            model.setData(index, editor.starRating())
        else:
            super(StarDelegate, self).setModelData(editor, model, index)

    def commitAndCloseEditor(self):
        editor = self.sender()
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)


def populateTableWidget(tableWidget):
    staticData = (
        ("Mass in B-Minor", "Baroque", "J.S. Bach", 5),
        ("Three More Foxes", "Jazz", "Maynard Ferguson", 4),
        ("Sex Bomb", "Pop", "Tom Jones", 3),
        ("Barbie Girl", "Pop", "Aqua", 5),
    )

    for row, (title, genre, artist, rating) in enumerate(staticData):
        item0 = QTableWidgetItem(title)
        item1 = QTableWidgetItem(genre)
        item2 = QTableWidgetItem(artist)
        item3 = QTableWidgetItem()
        item3.setData(0, StarRating(rating))
        tableWidget.setItem(row, 0, item0)
        tableWidget.setItem(row, 1, item1)
        tableWidget.setItem(row, 2, item2)
        tableWidget.setItem(row, 3, item3)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    tableWidget = QTableWidget(4, 4)
    tableWidget.setItemDelegate(StarDelegate())
    tableWidget.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
    tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    headerLabels = ("Title", "Genre", "Artist", "Rating")
    tableWidget.setHorizontalHeaderLabels(headerLabels)

    populateTableWidget(tableWidget)

    tableWidget.resizeColumnsToContents()
    tableWidget.resize(500, 300)
    tableWidget.show()

    sys.exit(app.exec_())
