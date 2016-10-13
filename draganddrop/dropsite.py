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


from PyQt5.QtCore import pyqtSignal, QMimeData, Qt
from PyQt5.QtGui import QPalette, QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QDialogButtonBox,
        QFrame, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
        QVBoxLayout, QWidget)


class DropArea(QLabel):

    changed = pyqtSignal(QMimeData)

    def __init__(self, parent = None):
        super(DropArea, self).__init__(parent)

        self.setMinimumSize(200, 200)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setAutoFillBackground(True)
        self.clear()

    def dragEnterEvent(self, event):
        self.setText("<drop content>")
        self.setBackgroundRole(QPalette.Highlight)
        event.acceptProposedAction()
        self.changed.emit(event.mimeData())

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasImage():
            self.setPixmap(QPixmap(mimeData.imageData()))
        elif mimeData.hasHtml():
            self.setText(mimeData.html())
            self.setTextFormat(Qt.RichText)
        elif mimeData.hasText():
            self.setText(mimeData.text())
            self.setTextFormat(Qt.PlainText)
        elif mimeData.hasUrls():
            self.setText("\n".join([url.path() for url in mimeData.urls()]))
        else:
            self.setText("Cannot display data")

        self.setBackgroundRole(QPalette.Dark)
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.clear()
        event.accept()

    def clear(self):
        self.setText("<drop content>")
        self.setBackgroundRole(QPalette.Dark)
        self.changed.emit(None)


class DropSiteWindow(QWidget):

    def __init__(self):
        super(DropSiteWindow, self).__init__()

        self.abstractLabel = QLabel(
                "This example accepts drags from other applications and "
                "displays the MIME types provided by the drag object.")
        self.abstractLabel.setWordWrap(True)
        self.abstractLabel.adjustSize()

        self.dropArea = DropArea()
        self.dropArea.changed.connect(self.updateFormatsTable)

        self.formatsTable = QTableWidget()
        self.formatsTable.setColumnCount(2)
        self.formatsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.formatsTable.setHorizontalHeaderLabels(["Format", "Content"])
        self.formatsTable.horizontalHeader().setStretchLastSection(True)

        self.clearButton = QPushButton("Clear")
        self.quitButton = QPushButton("Quit")

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(self.clearButton, QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.quitButton, QDialogButtonBox.RejectRole)

        self.quitButton.pressed.connect(self.close)
        self.clearButton.pressed.connect(self.dropArea.clear)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.abstractLabel)
        mainLayout.addWidget(self.dropArea)
        mainLayout.addWidget(self.formatsTable)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Drop Site")
        self.setMinimumSize(350, 500)

    def updateFormatsTable(self, mimeData=None):
        self.formatsTable.setRowCount(0)

        if mimeData is None:
            return

        for format in mimeData.formats():
            formatItem = QTableWidgetItem(format)
            formatItem.setFlags(Qt.ItemIsEnabled)
            formatItem.setTextAlignment(Qt.AlignTop | Qt.AlignLeft)

            if format == 'text/plain':
                text = mimeData.text().strip()
            elif format == 'text/html':
                text = mimeData.html().strip()
            elif format == 'text/uri-list':
                text = " ".join([url.toString() for url in mimeData.urls()])
            else:
                text = " ".join(["%02X" % ord(datum) for datum in mimeData.data(format)])

            row = self.formatsTable.rowCount()
            self.formatsTable.insertRow(row)
            self.formatsTable.setItem(row, 0, QTableWidgetItem(format))
            self.formatsTable.setItem(row, 1, QTableWidgetItem(text))

        self.formatsTable.resizeColumnToContents(0)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = DropSiteWindow()
    window.show()
    sys.exit(app.exec_())

