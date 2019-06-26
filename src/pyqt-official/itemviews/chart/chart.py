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


import math

from PyQt5.QtCore import (QByteArray, QFile, QItemSelection,
        QItemSelectionModel, QModelIndex, QPoint, QRect, QSize, Qt,
        QTextStream)
from PyQt5.QtGui import (QBrush, QColor, QFontMetrics, QPainter, QPainterPath,
        QPalette, QPen, QRegion, QStandardItemModel)
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QFileDialog,
        QMainWindow, QMenu, QRubberBand, QSplitter, QStyle, QTableView)

import chart_rc


class PieView(QAbstractItemView):
    def __init__(self, parent=None):
        super(PieView, self).__init__(parent)

        self.horizontalScrollBar().setRange(0, 0)
        self.verticalScrollBar().setRange(0, 0)

        self.margin = 8
        self.totalSize = 300
        self.pieSize = self.totalSize - 2*self.margin
        self.validItems = 0
        self.totalValue = 0.0
        self.origin = QPoint()
        self.rubberBand = None

    def dataChanged(self, topLeft, bottomRight, roles):
        super(PieView, self).dataChanged(topLeft, bottomRight, roles)

        self.validItems = 0
        self.totalValue = 0.0

        for row in range(self.model().rowCount(self.rootIndex())):

            index = self.model().index(row, 1, self.rootIndex())
            value = self.model().data(index)

            if value is not None and value > 0.0:
                self.totalValue += value
                self.validItems += 1

        self.viewport().update()

    def edit(self, index, trigger, event):
        if index.column() == 0:
            return super(PieView, self).edit(index, trigger, event)
        else:
            return False

    def indexAt(self, point):
        if self.validItems == 0:
            return QModelIndex()

        # Transform the view coordinates into contents widget coordinates.
        wx = point.x() + self.horizontalScrollBar().value()
        wy = point.y() + self.verticalScrollBar().value()

        if wx < self.totalSize:
            cx = wx - self.totalSize/2
            cy = self.totalSize/2 - wy; # positive cy for items above the center

            # Determine the distance from the center point of the pie chart.
            d = (cx**2 + cy**2)**0.5

            if d == 0 or d > self.pieSize/2:
                return QModelIndex()

            # Determine the angle of the point.
            angle = (180 / math.pi) * math.acos(cx/d)
            if cy < 0:
                angle = 360 - angle

            # Find the relevant slice of the pie.
            startAngle = 0.0

            for row in range(self.model().rowCount(self.rootIndex())):

                index = self.model().index(row, 1, self.rootIndex())
                value = self.model().data(index)

                if value > 0.0:
                    sliceAngle = 360*value/self.totalValue

                    if angle >= startAngle and angle < (startAngle + sliceAngle):
                        return self.model().index(row, 1, self.rootIndex())

                    startAngle += sliceAngle

        else:
            itemHeight = QFontMetrics(self.viewOptions().font).height()
            listItem = int((wy - self.margin) / itemHeight)
            validRow = 0

            for row in range(self.model().rowCount(self.rootIndex())):

                index = self.model().index(row, 1, self.rootIndex())
                if self.model().data(index) > 0.0:

                    if listItem == validRow:
                        return self.model().index(row, 0, self.rootIndex())

                    # Update the list index that corresponds to the next valid
                    # row.
                    validRow += 1

        return QModelIndex()

    def isIndexHidden(self, index):
        return False

    def itemRect(self, index):
        if not index.isValid():
            return QRect()

        # Check whether the index's row is in the list of rows represented
        # by slices.

        if index.column() != 1:
            valueIndex = self.model().index(index.row(), 1, self.rootIndex())
        else:
            valueIndex = index

        if self.model().data(valueIndex) > 0.0:

            listItem = 0
            for row in range(index.row()-1, -1, -1):
                if self.model().data(self.model().index(row, 1, self.rootIndex())) > 0.0:
                    listItem += 1

            if index.column() == 0:
            
                itemHeight = QFontMetrics(self.viewOptions().font).height()
                return QRect(self.totalSize,
                             int(self.margin + listItem*itemHeight),
                             self.totalSize - self.margin, int(itemHeight))
            elif index.column() == 1:
                return self.viewport().rect()

        return QRect()

    def itemRegion(self, index):
        if not index.isValid():
            return QRegion()

        if index.column() != 1:
            return QRegion(self.itemRect(index))

        if self.model().data(index) <= 0.0:
            return QRegion()

        startAngle = 0.0
        for row in range(self.model().rowCount(self.rootIndex())):

            sliceIndex = self.model().index(row, 1, self.rootIndex())
            value = self.model().data(sliceIndex)

            if value > 0.0:
                angle = 360*value/self.totalValue

                if sliceIndex == index:
                    slicePath = QPainterPath()
                    slicePath.moveTo(self.totalSize/2, self.totalSize/2)
                    slicePath.arcTo(self.margin, self.margin,
                            self.margin+self.pieSize, self.margin+self.pieSize,
                            startAngle, angle)
                    slicePath.closeSubpath()

                    return QRegion(slicePath.toFillPolygon().toPolygon())

                startAngle += angle

        return QRegion()

    def horizontalOffset(self):
        return self.horizontalScrollBar().value()

    def mousePressEvent(self, event):
        super(PieView, self).mousePressEvent(event)

        self.origin = event.pos()
        if not self.rubberBand:
            self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.rubberBand.setGeometry(QRect(self.origin, QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if self.rubberBand:
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

        super(PieView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super(PieView, self).mouseReleaseEvent(event)

        if self.rubberBand:
            self.rubberBand.hide()

        self.viewport().update()

    def moveCursor(self, cursorAction, modifiers):
        current = self.currentIndex()

        if cursorAction in (QAbstractItemView.MoveLeft, QAbstractItemView.MoveUp):

            if current.row() > 0:
                current = self.model().index(current.row() - 1,
                        current.column(), self.rootIndex())
            else:
                current = self.model().index(0, current.column(),
                        self.rootIndex())

        elif cursorAction in (QAbstractItemView.MoveRight, QAbstractItemView.MoveDown):

            if current.row() < self.rows(current) - 1:
                current = self.model().index(current.row() + 1,
                        current.column(), self.rootIndex())
            else:
                current = self.model().index(self.rows(current) - 1,
                        current.column(), self.rootIndex())

        self.viewport().update()
        return current

    def paintEvent(self, event):
        selections = self.selectionModel()
        option = self.viewOptions()
        state = option.state

        background = option.palette.base()
        foreground = QPen(option.palette.color(QPalette.WindowText))
        textPen = QPen(option.palette.color(QPalette.Text))
        highlightedPen = QPen(option.palette.color(QPalette.HighlightedText))

        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(event.rect(), background)
        painter.setPen(foreground)

        # Viewport rectangles
        pieRect = QRect(self.margin, self.margin, self.pieSize,
                self.pieSize)
        keyPoint = QPoint(self.totalSize - self.horizontalScrollBar().value(),
                self.margin - self.verticalScrollBar().value())

        if self.validItems > 0:
            painter.save()
            painter.translate(pieRect.x() - self.horizontalScrollBar().value(),
                    pieRect.y() - self.verticalScrollBar().value())
            painter.drawEllipse(0, 0, self.pieSize, self.pieSize)
            startAngle = 0.0

            for row in range(self.model().rowCount(self.rootIndex())):

                index = self.model().index(row, 1, self.rootIndex())
                value = self.model().data(index)

                if value > 0.0:
                    angle = 360*value/self.totalValue

                    colorIndex = self.model().index(row, 0, self.rootIndex())
                    color = self.model().data(colorIndex, Qt.DecorationRole)

                    if self.currentIndex() == index:
                        painter.setBrush(QBrush(color, Qt.Dense4Pattern))
                    elif selections.isSelected(index):
                        painter.setBrush(QBrush(color, Qt.Dense3Pattern))
                    else:
                        painter.setBrush(QBrush(color))

                    painter.drawPie(0, 0, self.pieSize, self.pieSize,
                            int(startAngle*16), int(angle*16))

                    startAngle += angle

            painter.restore()

            keyNumber = 0

            for row in range(self.model().rowCount(self.rootIndex())):
                index = self.model().index(row, 1, self.rootIndex())
                value = self.model().data(index)

                if value > 0.0:
                    labelIndex = self.model().index(row, 0, self.rootIndex())

                    option = self.viewOptions()
                    option.rect = self.visualRect(labelIndex)
                    if selections.isSelected(labelIndex):
                        option.state |= QStyle.State_Selected
                    if self.currentIndex() == labelIndex:
                        option.state |= QStyle.State_HasFocus
                    self.itemDelegate().paint(painter, option, labelIndex)

                    keyNumber += 1

    def resizeEvent(self, event):
        self.updateGeometries()

    def rows(self, index):
        return self.model().rowCount(self.model().parent(index))

    def rowsInserted(self, parent, start, end):
        for row in range(start, end + 1):
            index = self.model().index(row, 1, self.rootIndex())
            value = self.model().data(index)

            if value is not None and value > 0.0:
                self.totalValue += value
                self.validItems += 1

        super(PieView, self).rowsInserted(parent, start, end)

    def rowsAboutToBeRemoved(self, parent, start, end):
        for row in range(start, end + 1):
            index = self.model().index(row, 1, self.rootIndex())
            value = self.model().data(index)

            if value is not None and value > 0.0:
                self.totalValue -= value
                self.validItems -= 1

        super(PieView, self).rowsAboutToBeRemoved(parent, start, end)

    def scrollContentsBy(self, dx, dy):
        self.viewport().scroll(dx, dy)

    def scrollTo(self, index, ScrollHint):
        area = self.viewport().rect()
        rect = self.visualRect(index)

        if rect.left() < area.left():
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() + rect.left() - area.left())
        elif rect.right() > area.right():
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() + min(
                    rect.right() - area.right(), rect.left() - area.left()))

        if rect.top() < area.top():
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + rect.top() - area.top())
        elif rect.bottom() > area.bottom():
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + min(
                    rect.bottom() - area.bottom(), rect.top() - area.top()))

    def setSelection(self, rect, command):
        # Use content widget coordinates because we will use the itemRegion()
        # function to check for intersections.

        contentsRect = rect.translated(self.horizontalScrollBar().value(),
                self.verticalScrollBar().value()).normalized()

        rows = self.model().rowCount(self.rootIndex())
        columns = self.model().columnCount(self.rootIndex())
        indexes = []

        for row in range(rows):
            for column in range(columns):
                index = self.model().index(row, column, self.rootIndex())
                region = self.itemRegion(index)
                if not region.intersect(QRegion(contentsRect)).isEmpty():
                    indexes.append(index)

        if len(indexes) > 0:
            firstRow = indexes[0].row()
            lastRow = indexes[0].row()
            firstColumn = indexes[0].column()
            lastColumn = indexes[0].column()

            for i in range(1, len(indexes)):
                firstRow = min(firstRow, indexes[i].row())
                lastRow = max(lastRow, indexes[i].row())
                firstColumn = min(firstColumn, indexes[i].column())
                lastColumn = max(lastColumn, indexes[i].column())

            selection = QItemSelection(
                self.model().index(firstRow, firstColumn, self.rootIndex()),
                self.model().index(lastRow, lastColumn, self.rootIndex()))
            self.selectionModel().select(selection, command)
        else:
            noIndex = QModelIndex()
            selection = QItemSelection(noIndex, noIndex)
            self.selectionModel().select(selection, command)

        self.update()

    def updateGeometries(self):
        self.horizontalScrollBar().setPageStep(self.viewport().width())
        self.horizontalScrollBar().setRange(0, max(0, 2*self.totalSize - self.viewport().width()))
        self.verticalScrollBar().setPageStep(self.viewport().height())
        self.verticalScrollBar().setRange(0, max(0, self.totalSize - self.viewport().height()))

    def verticalOffset(self):
        return self.verticalScrollBar().value()

    def visualRect(self, index):
        rect = self.itemRect(index)
        if rect.isValid():
            return QRect(rect.left() - self.horizontalScrollBar().value(),
                         rect.top() - self.verticalScrollBar().value(),
                         rect.width(), rect.height())
        else:
            return rect

    def visualRegionForSelection(self, selection):
        region = QRegion()

        for span in selection:
            for row in range(span.top(), span.bottom() + 1):
                for col in range(span.left(), span.right() + 1):
                    index = self.model().index(row, col, self.rootIndex())
                    region += self.visualRect(index)

        return region


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        fileMenu = QMenu("&File", self)
        openAction = fileMenu.addAction("&Open...")
        openAction.setShortcut("Ctrl+O")
        saveAction = fileMenu.addAction("&Save As...")
        saveAction.setShortcut("Ctrl+S")
        quitAction = fileMenu.addAction("E&xit")
        quitAction.setShortcut("Ctrl+Q")

        self.setupModel()
        self.setupViews()

        openAction.triggered.connect(self.openFile)
        saveAction.triggered.connect(self.saveFile)
        quitAction.triggered.connect(QApplication.instance().quit)

        self.menuBar().addMenu(fileMenu)
        self.statusBar()

        self.openFile(':/Charts/qtdata.cht')

        self.setWindowTitle("Chart")
        self.resize(870, 550)

    def setupModel(self):
        self.model = QStandardItemModel(8, 2, self)
        self.model.setHeaderData(0, Qt.Horizontal, "Label")
        self.model.setHeaderData(1, Qt.Horizontal, "Quantity")

    def setupViews(self):
        splitter = QSplitter()
        table = QTableView()
        self.pieChart = PieView()
        splitter.addWidget(table)
        splitter.addWidget(self.pieChart)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        table.setModel(self.model)
        self.pieChart.setModel(self.model)

        self.selectionModel = QItemSelectionModel(self.model)
        table.setSelectionModel(self.selectionModel)
        self.pieChart.setSelectionModel(self.selectionModel)

        table.horizontalHeader().setStretchLastSection(True)

        self.setCentralWidget(splitter)

    def openFile(self, path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Choose a data file",
                    '', '*.cht')

        if path:
            f = QFile(path)

            if f.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(f)

                self.model.removeRows(0, self.model.rowCount(QModelIndex()),
                        QModelIndex())

                row = 0
                line = stream.readLine()
                while line:
                    self.model.insertRows(row, 1, QModelIndex())

                    pieces = line.split(',')
                    self.model.setData(self.model.index(row, 0, QModelIndex()),
                                pieces[0])
                    self.model.setData(self.model.index(row, 1, QModelIndex()),
                                float(pieces[1]))
                    self.model.setData(self.model.index(row, 0, QModelIndex()),
                                QColor(pieces[2]), Qt.DecorationRole)

                    row += 1
                    line = stream.readLine()

                f.close()
                self.statusBar().showMessage("Loaded %s" % path, 2000)

    def saveFile(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save file as", '',
                '*.cht')

        if fileName:
            f = QFile(fileName)

            if f.open(QFile.WriteOnly | QFile.Text):
                for row in range(self.model.rowCount(QModelIndex())):
                    pieces = []

                    pieces.append(self.model.data(self.model.index(row, 0, QModelIndex()),
                            Qt.DisplayRole))
                    pieces.append(str(self.model.data(self.model.index(row, 1, QModelIndex()),
                            Qt.DisplayRole)))
                    pieces.append(self.model.data(self.model.index(row, 0, QModelIndex()),
                            Qt.DecorationRole).name())

                    f.write(QByteArray(','.join(pieces)))
                    f.write('\n')

            f.close()
            self.statusBar().showMessage("Saved %s" % fileName, 2000)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
