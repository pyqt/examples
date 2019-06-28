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


from PyQt5.QtCore import (pyqtSignal, QPointF, QPropertyAnimation, QRect,
        QRectF, QState, QStateMachine, Qt)
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView,
        QGraphicsWidget)

import appchooser_rc


class Pixmap(QGraphicsWidget):
    clicked = pyqtSignal()

    def __init__(self, pix, parent=None):
        super(Pixmap, self).__init__(parent)

        self.orig = QPixmap(pix)
        self.p = QPixmap(pix)

    def paint(self, painter, option, widget):
        painter.drawPixmap(QPointF(), self.p)

    def mousePressEvent(self, ev):
        self.clicked.emit()

    def setGeometry(self, rect):
        super(Pixmap, self).setGeometry(rect)

        if rect.size().width() > self.orig.size().width():
            self.p = self.orig.scaled(rect.size().toSize())
        else:
            self.p = QPixmap(self.orig)


def createStates(objects, selectedRect, parent):
    for obj in objects:
        state = QState(parent)
        state.assignProperty(obj, 'geometry', selectedRect)
        parent.addTransition(obj.clicked, state)


def createAnimations(objects, machine):
    for obj in objects:
        animation = QPropertyAnimation(obj, b'geometry', obj)
        machine.addDefaultAnimation(animation)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    p1 = Pixmap(QPixmap(':/digikam.png'))
    p2 = Pixmap(QPixmap(':/akregator.png'))
    p3 = Pixmap(QPixmap(':/accessories-dictionary.png'))
    p4 = Pixmap(QPixmap(':/k3b.png'))

    p1.setGeometry(QRectF(0.0, 0.0, 64.0, 64.0))
    p2.setGeometry(QRectF(236.0, 0.0, 64.0, 64.0))
    p3.setGeometry(QRectF(236.0, 236.0, 64.0, 64.0))
    p4.setGeometry(QRectF(0.0, 236.0, 64.0, 64.0))

    scene = QGraphicsScene(0, 0, 300, 300)
    scene.setBackgroundBrush(Qt.white)
    scene.addItem(p1)
    scene.addItem(p2)
    scene.addItem(p3)
    scene.addItem(p4)

    window = QGraphicsView(scene)
    window.setFrameStyle(0)
    window.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    window.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    window.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    machine = QStateMachine()
    machine.setGlobalRestorePolicy(QStateMachine.RestoreProperties)

    group = QState(machine)
    selectedRect = QRect(86, 86, 128, 128)

    idleState = QState(group)
    group.setInitialState(idleState)

    objects = [p1, p2, p3, p4]
    createStates(objects, selectedRect, group)
    createAnimations(objects, machine)

    machine.setInitialState(group)
    machine.start()

    window.resize(300, 300)
    window.show()

    sys.exit(app.exec_())
