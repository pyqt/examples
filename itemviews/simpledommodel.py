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


from PyQt5.QtCore import QAbstractItemModel, QFile, QIODevice, QModelIndex, Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QTreeView
from PyQt5.QtXml import QDomDocument


class DomItem(object):
    def __init__(self, node, row, parent=None):
        self.domNode = node
        # Record the item's location within its parent.
        self.rowNumber = row
        self.parentItem = parent
        self.childItems = {}

    def node(self):
        return self.domNode

    def parent(self):
        return self.parentItem

    def child(self, i):
        if i in self.childItems:
            return self.childItems[i]

        if i >= 0 and i < self.domNode.childNodes().count():
            childNode = self.domNode.childNodes().item(i)
            childItem = DomItem(childNode, i, self)
            self.childItems[i] = childItem
            return childItem

        return None

    def row(self):
        return self.rowNumber


class DomModel(QAbstractItemModel):
    def __init__(self, document, parent=None):
        super(DomModel, self).__init__(parent)

        self.domDocument = document

        self.rootItem = DomItem(self.domDocument, 0)

    def columnCount(self, parent):
        return 3

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        node = item.node()
        attributes = []
        attributeMap = node.attributes()

        if index.column() == 0:
            return node.nodeName()
        
        elif index.column() == 1:
            for i in range(0, attributeMap.count()):
                attribute = attributeMap.item(i)
                attributes.append(attribute.nodeName() + '="' +
                                  attribute.nodeValue() + '"')

            return " ".join(attributes)

        if index.column() == 2:
            value = node.nodeValue()
            if value is None:
                return ''

            return ' '.join(node.nodeValue().split('\n'))

        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "Name"

            if section == 1:
                return "Attributes"

            if section == 2:
                return "Value"

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()

        childItem = child.internalPointer()
        parentItem = childItem.parent()

        if not parentItem or parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.node().childNodes().count()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction("&Open...", self.openFile, "Ctrl+O")
        self.fileMenu.addAction("E&xit", self.close, "Ctrl+Q")

        self.xmlPath = ""
        self.model = DomModel(QDomDocument(), self)
        self.view = QTreeView(self)
        self.view.setModel(self.model)

        self.setCentralWidget(self.view)
        self.setWindowTitle("Simple DOM Model")

    def openFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open File",
                self.xmlPath, "XML files (*.xml);;HTML files (*.html);;"
                "SVG files (*.svg);;User Interface files (*.ui)")

        if filePath:
            f = QFile(filePath)
            if f.open(QIODevice.ReadOnly):
                document = QDomDocument()
                if document.setContent(f):
                    newModel = DomModel(document, self)
                    self.view.setModel(newModel)
                    self.model = newModel
                    self.xmlPath = filePath

                f.close()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
