#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2017 Riverbank Computing Limited.
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


from PyQt5.QtCore import (QAbstractTableModel, QDir, QModelIndex, QRect,
        QRectF, QSize, Qt)
from PyQt5.QtGui import QBrush, qGray, QImage, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import (QAbstractItemDelegate, QApplication, QDialog,
        QFileDialog, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QMenu,
        QProgressDialog, QSpinBox, QStyle, QStyleOptionViewItem, QTableView,
        QVBoxLayout, QWidget)

import pixelator_rc


ItemSize = 256


class PixelDelegate(QAbstractItemDelegate):
    def __init__(self, parent=None):
        super(PixelDelegate, self).__init__(parent)

        self.pixelSize = 12

    def paint(self, painter, option, index):
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        size = min(option.rect.width(), option.rect.height())
        brightness = index.model().data(index, Qt.DisplayRole)
        radius = (size/2.0) - (brightness/255.0 * size/2.0)
        if radius == 0.0:
            return

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if option.state & QStyle.State_Selected:
            painter.setBrush(option.palette.highlightedText())
        else:
            painter.setBrush(QBrush(Qt.black))

        painter.drawEllipse(QRectF(
                            option.rect.x() + option.rect.width()/2 - radius,
                            option.rect.y() + option.rect.height()/2 - radius,
                            2*radius, 2*radius))

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(self.pixelSize, self.pixelSize)

    def setPixelSize(self, size):
        self.pixelSize = size


class ImageModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(ImageModel, self).__init__(parent)

        self.modelImage = QImage()

    def setImage(self, image):
        self.beginResetModel()
        self.modelImage = QImage(image)
        self.endResetModel()

    def rowCount(self, parent):
        return self.modelImage.height()

    def columnCount(self, parent):
        return self.modelImage.width()

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        return qGray(self.modelImage.pixel(index.column(), index.row()))

    def headerData(self, section, orientation, role):
        if role == Qt.SizeHintRole:
            return QSize(1, 1)

        return None


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.currentPath = QDir.homePath()
        self.model = ImageModel(self)

        centralWidget = QWidget()

        self.view = QTableView()
        self.view.setShowGrid(False)
        self.view.horizontalHeader().hide()
        self.view.verticalHeader().hide()
        self.view.horizontalHeader().setMinimumSectionSize(1)
        self.view.verticalHeader().setMinimumSectionSize(1)
        self.view.setModel(self.model)

        delegate = PixelDelegate(self)
        self.view.setItemDelegate(delegate)

        pixelSizeLabel = QLabel("Pixel size:")
        pixelSizeSpinBox = QSpinBox()
        pixelSizeSpinBox.setMinimum(4)
        pixelSizeSpinBox.setMaximum(32)
        pixelSizeSpinBox.setValue(12)

        fileMenu = QMenu("&File", self)
        openAction = fileMenu.addAction("&Open...")
        openAction.setShortcut("Ctrl+O")

        self.printAction = fileMenu.addAction("&Print...")
        self.printAction.setEnabled(False)
        self.printAction.setShortcut("Ctrl+P")

        quitAction = fileMenu.addAction("E&xit")
        quitAction.setShortcut("Ctrl+Q")

        helpMenu = QMenu("&Help", self)
        aboutAction = helpMenu.addAction("&About")

        self.menuBar().addMenu(fileMenu)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(helpMenu)

        openAction.triggered.connect(self.chooseImage)
        self.printAction.triggered.connect(self.printImage)
        quitAction.triggered.connect(QApplication.instance().quit)
        aboutAction.triggered.connect(self.showAboutBox)
        pixelSizeSpinBox.valueChanged.connect(delegate.setPixelSize)
        pixelSizeSpinBox.valueChanged.connect(self.updateView)

        controlsLayout = QHBoxLayout()
        controlsLayout.addWidget(pixelSizeLabel)
        controlsLayout.addWidget(pixelSizeSpinBox)
        controlsLayout.addStretch(1)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.view)
        mainLayout.addLayout(controlsLayout)
        centralWidget.setLayout(mainLayout)

        self.setCentralWidget(centralWidget)

        self.setWindowTitle("Pixelator")
        self.resize(640, 480)

    def chooseImage(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose an Image",
                self.currentPath, '*')

        if fileName:
            self.openImage(fileName)

    def openImage(self, fileName):
        image = QImage()

        if image.load(fileName):
            self.model.setImage(image)

            if not fileName.startswith(':/'):
                self.currentPath = fileName
                self.setWindowTitle("%s - Pixelator" % self.currentPath)

            self.printAction.setEnabled(True)
            self.updateView()

    def printImage(self):
        if self.model.rowCount(QModelIndex()) * self.model.columnCount(QModelIndex()) > 90000:
            answer = QMessageBox.question(self, "Large Image Size",
                    "The printed image may be very large. Are you sure that "
                    "you want to print it?",
                    QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.No:
                return

        printer = QPrinter(QPrinter.HighResolution)

        dlg = QPrintDialog(printer, self)
        dlg.setWindowTitle("Print Image")

        if dlg.exec_() != QDialog.Accepted:
            return

        painter = QPainter()
        painter.begin(printer)

        rows = self.model.rowCount(QModelIndex())
        columns = self.model.columnCount(QModelIndex())
        sourceWidth = (columns+1) * ItemSize
        sourceHeight = (rows+1) * ItemSize

        painter.save()

        xscale = printer.pageRect().width() / float(sourceWidth)
        yscale = printer.pageRect().height() / float(sourceHeight)
        scale = min(xscale, yscale)

        painter.translate(printer.paperRect().x()+printer.pageRect().width()/2,
                          printer.paperRect().y()+printer.pageRect().height()/2)
        painter.scale(scale, scale)
        painter.translate(-sourceWidth/2, -sourceHeight/2)

        option = QStyleOptionViewItem()
        parent = QModelIndex()

        progress = QProgressDialog("Printing...", "Cancel", 0, rows, self)
        progress.setWindowModality(Qt.ApplicationModal)
        y = ItemSize / 2.0

        for row in range(rows):
            progress.setValue(row)
            QApplication.processEvents()
            if progress.wasCanceled():
                break

            x = ItemSize / 2.0

            for column in range(columns):
                option.rect = QRect(x, y, ItemSize, ItemSize)
                self.view.itemDelegate().paint(painter, option,
                        self.model.index(row, column, parent))
                x += ItemSize

            y += ItemSize

        progress.setValue(rows)

        painter.restore()
        painter.end()

        if progress.wasCanceled():
            QMessageBox.information(self, "Printing canceled",
                    "The printing process was canceled.", QMessageBox.Cancel)

    def showAboutBox(self):
        QMessageBox.about(self, "About the Pixelator example",
                "This example demonstrates how a standard view and a custom\n"
                "delegate can be used to produce a specialized "
                "representation\nof data in a simple custom model.")

    def updateView(self):
        self.view.resizeColumnsToContents()
        self.view.resizeRowsToContents()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.openImage(':/images/qt.png')
    sys.exit(app.exec_())
