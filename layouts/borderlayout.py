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


from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtWidgets import (QApplication, QFrame, QLabel, QLayout,
        QTextBrowser, QWidget, QWidgetItem)


class ItemWrapper(object):
    def __init__(self, i, p):
        self.item = i
        self.position = p


class BorderLayout(QLayout):
    West, North, South, East, Center = range(5)
    MinimumSize, SizeHint = range(2)

    def __init__(self, parent=None, margin=None, spacing=-1):
        super(BorderLayout, self).__init__(parent)

        if margin is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)
        self.list = []

    def __del__(self):
        l = self.takeAt(0)
        while l is not None:
            l = self.takeAt(0)

    def addItem(self, item):
        self.add(item, self.West)

    def addWidget(self, widget, position):
        self.add(QWidgetItem(widget), position)

    def expandingDirections(self):
        return Qt.Horizontal | Qt.Vertical

    def hasHeightForWidth(self):
        return False

    def count(self):
        return len(self.list)

    def itemAt(self, index):
        if index < len(self.list):
            return self.list[index].item

        return None

    def minimumSize(self):
        return self.calculateSize(self.MinimumSize)

    def setGeometry(self, rect):
        center = None
        eastWidth = 0
        westWidth = 0
        northHeight = 0
        southHeight = 0
        centerHeight = 0

        super(BorderLayout, self).setGeometry(rect)

        for wrapper in self.list:
            item = wrapper.item
            position = wrapper.position

            if position == self.North:
                item.setGeometry(QRect(rect.x(), northHeight,
                        rect.width(), item.sizeHint().height()))    

                northHeight += item.geometry().height() + self.spacing()

            elif position == self.South:
                item.setGeometry(QRect(item.geometry().x(),
                        item.geometry().y(), rect.width(),
                        item.sizeHint().height()))

                southHeight += item.geometry().height() + self.spacing()

                item.setGeometry(QRect(rect.x(),
                        rect.y() + rect.height() - southHeight + self.spacing(),
                        item.geometry().width(), item.geometry().height()))

            elif position == self.Center:
                center = wrapper

        centerHeight = rect.height() - northHeight - southHeight

        for wrapper in self.list:
            item = wrapper.item
            position = wrapper.position

            if position == self.West:
                item.setGeometry(QRect(rect.x() + westWidth,
                        northHeight, item.sizeHint().width(), centerHeight))    

                westWidth += item.geometry().width() + self.spacing()

            elif position == self.East:
                item.setGeometry(QRect(item.geometry().x(),
                        item.geometry().y(), item.sizeHint().width(),
                        centerHeight))

                eastWidth += item.geometry().width() + self.spacing()

                item.setGeometry(QRect(rect.x() + rect.width() - eastWidth + self.spacing(),
                        northHeight, item.geometry().width(),
                        item.geometry().height()))

        if center:
            center.item.setGeometry(QRect(westWidth, northHeight,
                    rect.width() - eastWidth - westWidth, centerHeight))

    def sizeHint(self):
        return self.calculateSize(self.SizeHint)

    def takeAt(self, index):
        if index >= 0 and index < len(self.list):
            layoutStruct = self.list.pop(index)
            return layoutStruct.item

        return None

    def add(self, item, position):
        self.list.append(ItemWrapper(item, position))

    def calculateSize(self, sizeType):
        totalSize = QSize()

        for wrapper in self.list:
            position = wrapper.position
            itemSize = QSize()

            if sizeType == self.MinimumSize:
                itemSize = wrapper.item.minimumSize()
            else: # sizeType == self.SizeHint
                itemSize = wrapper.item.sizeHint()

            if position in (self.North, self.South, self.Center):
                totalSize.setHeight(totalSize.height() + itemSize.height())

            if position in (self.West, self.East, self.Center):
                totalSize.setWidth(totalSize.width() + itemSize.width())

        return totalSize


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        centralWidget = QTextBrowser()
        centralWidget.setPlainText("Central widget")

        layout = BorderLayout()
        layout.addWidget(centralWidget, BorderLayout.Center)

        # Because BorderLayout doesn't call its super-class addWidget() it
        # doesn't take ownership of the widgets until setLayout() is called.
        # Therefore we keep a local reference to each label to prevent it being
        # garbage collected too soon.
        label_n = self.createLabel("North")
        layout.addWidget(label_n, BorderLayout.North)

        label_w = self.createLabel("West")
        layout.addWidget(label_w, BorderLayout.West)

        label_e1 = self.createLabel("East 1")
        layout.addWidget(label_e1, BorderLayout.East)

        label_e2 = self.createLabel("East 2")
        layout.addWidget(label_e2, BorderLayout.East)

        label_s = self.createLabel("South")
        layout.addWidget(label_s, BorderLayout.South)

        self.setLayout(layout)

        self.setWindowTitle("Border Layout")

    def createLabel(self, text):
        label = QLabel(text)
        label.setFrameStyle(QFrame.Box | QFrame.Raised)

        return label


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())    
