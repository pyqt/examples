#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2016 Riverbank Computing Limited.
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


from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QUrl, QVariant
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

import abstractitemmodel_rc


class Animal(object):

    def __init__(self, type, size):
        self._type = type
        self._size = size

    def type(self):
        return self._type

    def size(self):
        return self._size


class AnimalModel(QAbstractListModel):

    TypeRole = Qt.UserRole + 1
    SizeRole = Qt.UserRole + 2

    _roles = {TypeRole: b"type", SizeRole: b"size"}

    def __init__(self, parent=None):
        super(AnimalModel, self).__init__(parent)

        self._animals = []

    def addAnimal(self, animal):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._animals.append(animal)
        self.endInsertRows()

    def rowCount(self, parent=QModelIndex()):
        return len(self._animals)

    def data(self, index, role=Qt.DisplayRole):
        try:
            animal = self._animals[index.row()]
        except IndexError:
            return QVariant()

        if role == self.TypeRole:
            return animal.type()

        if role == self.SizeRole:
            return animal.size()

        return QVariant()

    def roleNames(self):
        return self._roles


if __name__ == '__main__':
    import sys

    app = QGuiApplication(sys.argv)

    model = AnimalModel()
    model.addAnimal(Animal("Wolf", "Medium"))
    model.addAnimal(Animal("Polar bear", "Large"))
    model.addAnimal(Animal("Quoll", "Small"))

    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    ctxt = view.rootContext()
    ctxt.setContextProperty('myModel', model)

    view.setSource(QUrl('qrc:view.qml'))
    view.show()

    sys.exit(app.exec_())
