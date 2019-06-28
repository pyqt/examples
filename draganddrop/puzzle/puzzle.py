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

from PyQt5.QtCore import (pyqtSignal, QByteArray, QDataStream, QIODevice,
        QMimeData, QPoint, QRect, QSize, Qt)
from PyQt5.QtGui import QDrag, QColor, QCursor, QIcon, QPainter, QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QFrame, QHBoxLayout,
        QListView, QListWidget, QListWidgetItem, QMainWindow, QMessageBox,
        QSizePolicy, QWidget)

import puzzle_rc


class PuzzleWidget(QWidget):

    puzzleCompleted = pyqtSignal()

    def __init__(self, parent=None):
        super(PuzzleWidget, self).__init__(parent)

        self.piecePixmaps = []
        self.pieceRects = []
        self.pieceLocations = []
        self.highlightedRect = QRect()
        self.inPlace = 0

        self.setAcceptDrops(True)
        self.setMinimumSize(400, 400)
        self.setMaximumSize(400, 400)

    def clear(self):
        self.pieceLocations = []
        self.piecePixmaps = []
        self.pieceRects = []
        self.highlightedRect = QRect()
        self.inPlace = 0
        self.update()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('image/x-puzzle-piece'):
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        updateRect = self.highlightedRect
        self.highlightedRect = QRect()
        self.update(updateRect)
        event.accept()

    def dragMoveEvent(self, event):
        updateRect = self.highlightedRect.united(self.targetSquare(event.pos()))

        if event.mimeData().hasFormat('image/x-puzzle-piece') and self.findPiece(self.targetSquare(event.pos())) == -1:
            self.highlightedRect = self.targetSquare(event.pos())
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            self.highlightedRect = QRect()
            event.ignore()

        self.update(updateRect)

    def dropEvent(self, event):
        if event.mimeData().hasFormat('image/x-puzzle-piece') and self.findPiece(self.targetSquare(event.pos())) == -1:
            pieceData = event.mimeData().data('image/x-puzzle-piece')
            dataStream = QDataStream(pieceData, QIODevice.ReadOnly)
            square = self.targetSquare(event.pos())
            pixmap = QPixmap()
            location = QPoint()
            dataStream >> pixmap >> location

            self.pieceLocations.append(location)
            self.piecePixmaps.append(pixmap)
            self.pieceRects.append(square)

            self.hightlightedRect = QRect()
            self.update(square)

            event.setDropAction(Qt.MoveAction)
            event.accept()

            if location == QPoint(square.x() / 80, square.y() / 80):
                self.inPlace += 1
                if self.inPlace == 25:
                    self.puzzleCompleted.emit()
        else:
            self.highlightedRect = QRect()
            event.ignore()

    def findPiece(self, pieceRect):
        try:
            return self.pieceRects.index(pieceRect)
        except ValueError:
            return -1

    def mousePressEvent(self, event):
        square = self.targetSquare(event.pos())
        found = self.findPiece(square)

        if found == -1:
            return

        location = self.pieceLocations[found]
        pixmap = self.piecePixmaps[found]
        del self.pieceLocations[found]
        del self.piecePixmaps[found]
        del self.pieceRects[found]

        if location == QPoint(square.x() / 80, square.y() / 80):
            self.inPlace -= 1

        self.update(square)

        itemData = QByteArray()
        dataStream = QDataStream(itemData, QIODevice.WriteOnly)

        dataStream << pixmap << location

        mimeData = QMimeData()
        mimeData.setData('image/x-puzzle-piece', itemData)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - square.topLeft())
        drag.setPixmap(pixmap)

        if drag.exec_(Qt.MoveAction) != Qt.MoveAction:
            self.pieceLocations.insert(found, location)
            self.piecePixmaps.insert(found, pixmap)
            self.pieceRects.insert(found, square)
            self.update(self.targetSquare(event.pos()))

            if location == QPoint(square.x() / 80, square.y() / 80):
                self.inPlace += 1

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), Qt.white)

        if self.highlightedRect.isValid():
            painter.setBrush(QColor("#ffcccc"))
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.highlightedRect.adjusted(0, 0, -1, -1))

        for rect, pixmap in zip(self.pieceRects, self.piecePixmaps):
            painter.drawPixmap(rect, pixmap)

        painter.end()

    def targetSquare(self, position):
        return QRect(position.x() // 80 * 80, position.y() // 80 * 80, 80, 80)


class PiecesList(QListWidget):
    def __init__(self, parent=None):
        super(PiecesList, self).__init__(parent)

        self.setDragEnabled(True)
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(60, 60))
        self.setSpacing(10)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('image/x-puzzle-piece'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('image/x-puzzle-piece'):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('image/x-puzzle-piece'):
            pieceData = event.mimeData().data('image/x-puzzle-piece')
            dataStream = QDataStream(pieceData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            location = QPoint()
            dataStream >> pixmap >> location

            self.addPiece(pixmap, location)

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def addPiece(self, pixmap, location):
        pieceItem = QListWidgetItem(self)
        pieceItem.setIcon(QIcon(pixmap))
        pieceItem.setData(Qt.UserRole, pixmap)
        pieceItem.setData(Qt.UserRole+1, location)
        pieceItem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

    def startDrag(self, supportedActions):
        item = self.currentItem()

        itemData = QByteArray()
        dataStream = QDataStream(itemData, QIODevice.WriteOnly)
        pixmap = QPixmap(item.data(Qt.UserRole))
        location = item.data(Qt.UserRole+1)

        dataStream << pixmap << location

        mimeData = QMimeData()
        mimeData.setData('image/x-puzzle-piece', itemData)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)

        if drag.exec_(Qt.MoveAction) == Qt.MoveAction:
            if self.currentItem() is not None:
                self.takeItem(self.row(item))


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.puzzleImage = QPixmap()

        self.setupMenus()
        self.setupWidgets()

        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.setWindowTitle("Puzzle")

    def openImage(self, path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Open Image", '',
                    "Image Files (*.png *.jpg *.bmp)")

        if path:
            newImage = QPixmap()
            if not newImage.load(path):
                QMessageBox.warning(self, "Open Image",
                        "The image file could not be loaded.",
                        QMessageBox.Cancel)
                return

            self.puzzleImage = newImage
            self.setupPuzzle()

    def setCompleted(self):
        QMessageBox.information(self, "Puzzle Completed",
                "Congratulations! You have completed the puzzle!\nClick OK "
                "to start again.",
                QMessageBox.Ok)

        self.setupPuzzle()

    def setupPuzzle(self):
        size = min(self.puzzleImage.width(), self.puzzleImage.height())
        self.puzzleImage = self.puzzleImage.copy(
                (self.puzzleImage.width() - size)/2,
                (self.puzzleImage.height() - size)/2, size, size).scaled(400, 400, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        self.piecesList.clear()

        for y in range(5):
            for x in range(5):
                pieceImage = self.puzzleImage.copy(x*80, y*80, 80, 80)
                self.piecesList.addPiece(pieceImage, QPoint(x,y))

        random.seed(QCursor.pos().x() ^ QCursor.pos().y())

        for i in range(self.piecesList.count()):
            if random.random() < 0.5:
                item = self.piecesList.takeItem(i)
                self.piecesList.insertItem(0, item)

        self.puzzleWidget.clear()

    def setupMenus(self):
        fileMenu = self.menuBar().addMenu("&File")

        openAction = fileMenu.addAction("&Open...")
        openAction.setShortcut("Ctrl+O")

        exitAction = fileMenu.addAction("E&xit")
        exitAction.setShortcut("Ctrl+Q")

        gameMenu = self.menuBar().addMenu("&Game")

        restartAction = gameMenu.addAction("&Restart")

        openAction.triggered.connect(self.openImage)
        exitAction.triggered.connect(QApplication.instance().quit)
        restartAction.triggered.connect(self.setupPuzzle)

    def setupWidgets(self):
        frame = QFrame()
        frameLayout = QHBoxLayout(frame)

        self.piecesList = PiecesList()

        self.puzzleWidget = PuzzleWidget()

        self.puzzleWidget.puzzleCompleted.connect(self.setCompleted,
                Qt.QueuedConnection)

        frameLayout.addWidget(self.piecesList)
        frameLayout.addWidget(self.puzzleWidget)
        self.setCentralWidget(frame)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.openImage(':/images/example.jpg')
    window.show()
    sys.exit(app.exec_())
