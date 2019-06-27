#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2017 Hans-Peter Jansen <hpj@urpla.net>
## Copyright (C) 2016 The Qt Company Ltd.
##
## This file is part of the examples of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:BSD$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https:#www.qt.io/terms-conditions. For further
## information use the contact form at https:#www.qt.io/contact-us.
##
## BSD License Usage
## Alternatively, you may use self file under the terms of the BSD license
## as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, self list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, self list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from self software without specific prior written permission.
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
##
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import (QAbstractItemModel, QFileInfo, QItemSelectionModel,
        QModelIndex, Qt)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAbstractItemView, QApplication,
        QFileIconProvider, QListView, QSplitter, QTableView, QTreeView)


images_dir = QFileInfo(__file__).absolutePath() + '/images'


class Node(object):
    def __init__(self, parent = None):
        self.parent = parent
        self.children = []


class Model(QAbstractItemModel):
    def __init__(self, rows, columns, parent = None):
        super(Model, self).__init__(parent)
        self.services = QIcon(images_dir + '/services.png')
        self.rc = rows
        self.cc = columns
        self.tree = [Node() for node in range(rows)]
        self.iconProvider = QFileIconProvider()

    def index(self, row, column, parent):
        if row < self.rc and row >= 0 and column < self.cc and column >= 0:
            parentNode = parent.internalPointer()
            childNode = self.node(row, parentNode)
            if childNode is not None:
                return self.createIndex(row, column, childNode)
        return QModelIndex()

    def parent(self, child):
        if isinstance(child, QModelIndex):
            # parent of QModelIndex child
            if child.isValid():
                childNode = child.internalPointer()
                parentNode = self.parent(childNode)
                if parentNode:
                    return self.createIndex(self.row(parentNode), 0, parentNode)
            return QModelIndex()
        else:
            # parent of Node
            if child:
                return child.parent

    def rowCount(self, parent):
        if parent.isValid() and parent.column() != 0:
            return 0
        return self.rc

    def columnCount(self, parent):
        return self.cc

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role == Qt.DisplayRole:
            return "Item %d:%s" % (index.row(), index.column())
        elif role == Qt.DecorationRole:
            if index.column() == 0:
                return self.iconProvider.icon(QFileIconProvider.Folder)
            return self.iconProvider.icon(QFileIconProvider.File)
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            return str(section)
        if role == Qt.DecorationRole:
            return self.services
        return super(Model, self).headerData(section, orientation, role)

    def hasChildren(self, parent):
        if parent.isValid() and parent.column() != 0:
            return False
        return self.rc > 0 and self.cc > 0

    def flags(self, index):
        if not index.isValid():
            return 0
        return Qt.ItemIsDragEnabled | super(Model, self).flags(index)

    def node(self, row, parent):
        if parent and not parent.children:
            parent.children = [Node(parent) for node in range(self.rc)]
        if parent:
            return parent.children[row]
        else:
            return self.tree[row]

    def row(self, node):
        if node.parent:
            return node.parent.children.index(node)
        else:
            return self.tree.index(node)


def main(args):
    app = QApplication(args)
    page = QSplitter()
    data = Model(1000, 10, page)
    selections = QItemSelectionModel(data)
    table = QTableView()
    table.setModel(data)
    table.setSelectionModel(selections)
    table.horizontalHeader().setSectionsMovable(True)
    table.verticalHeader().setSectionsMovable(True)
    # Set StaticContents to enable minimal repaints on resizes.
    table.viewport().setAttribute(Qt.WA_StaticContents)
    page.addWidget(table)
    tree = QTreeView()
    tree.setModel(data)
    tree.setSelectionModel(selections)
    tree.setUniformRowHeights(True)
    tree.header().setStretchLastSection(False)
    tree.viewport().setAttribute(Qt.WA_StaticContents)
    # Disable the focus rect to get minimal repaints when scrolling on Mac.
    tree.setAttribute(Qt.WA_MacShowFocusRect, False)
    page.addWidget(tree)
    list = QListView()
    list.setModel(data)
    list.setSelectionModel(selections)
    list.setViewMode(QListView.IconMode)
    list.setSelectionMode(QAbstractItemView.ExtendedSelection)
    list.setAlternatingRowColors(False)
    list.viewport().setAttribute(Qt.WA_StaticContents)
    list.setAttribute(Qt.WA_MacShowFocusRect, False)
    page.addWidget(list)
    page.setWindowIcon(QIcon(images_dir + '/interview.png'))
    page.setWindowTitle("Interview")
    page.show()
    return app.exec_()


if __name__ == '__main__':
    import sys
    main(sys.argv)
