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

from PyQt5.QtCore import (pyqtProperty, QDirIterator, QEasingCurve, QEvent,
        QEventTransition, QHistoryState, QParallelAnimationGroup, QPointF,
        QPropertyAnimation, QRectF, QSequentialAnimationGroup, QSize, QState,
        QStateMachine, Qt)
from PyQt5.QtGui import (QBrush, QColor, QFont, QLinearGradient, QPainter,
        QPalette, QPen, QPixmap, QTransform)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsObject,
        QGraphicsProxyWidget, QGraphicsRotation, QGraphicsScene, QGraphicsView,
        QKeyEventTransition, QWidget)
from PyQt5.QtOpenGL import QGL, QGLFormat, QGLWidget

import padnavigator_rc
from ui_form import Ui_Form


class PadNavigator(QGraphicsView):
    def __init__(self, size, parent=None):
        super(PadNavigator, self).__init__(parent)

        self.form = Ui_Form()

        splash = SplashItem()
        splash.setZValue(1)

        pad = FlippablePad(size)
        flipRotation = QGraphicsRotation(pad)
        xRotation = QGraphicsRotation(pad)
        yRotation = QGraphicsRotation(pad)
        flipRotation.setAxis(Qt.YAxis)
        xRotation.setAxis(Qt.YAxis)
        yRotation.setAxis(Qt.XAxis)
        pad.setTransformations([flipRotation, xRotation, yRotation])

        backItem = QGraphicsProxyWidget(pad)
        widget = QWidget()
        self.form.setupUi(widget)
        self.form.hostName.setFocus()
        backItem.setWidget(widget)
        backItem.setVisible(False)
        backItem.setFocus()
        backItem.setCacheMode(QGraphicsItem.ItemCoordinateCache)
        r = backItem.rect()
        backItem.setTransform(QTransform().rotate(180, Qt.YAxis).translate(-r.width()/2, -r.height()/2))

        selectionItem = RoundRectItem(QRectF(-60, -60, 120, 120),
                QColor(Qt.gray), pad)
        selectionItem.setZValue(0.5)

        smoothSplashMove = QPropertyAnimation(splash, b'y')
        smoothSplashOpacity = QPropertyAnimation(splash, b'opacity')
        smoothSplashMove.setEasingCurve(QEasingCurve.InQuad)
        smoothSplashMove.setDuration(250)
        smoothSplashOpacity.setDuration(250)

        smoothXSelection = QPropertyAnimation(selectionItem, b'x')
        smoothYSelection = QPropertyAnimation(selectionItem, b'y')
        smoothXRotation = QPropertyAnimation(xRotation, b'angle')
        smoothYRotation = QPropertyAnimation(yRotation, b'angle')
        smoothXSelection.setDuration(125)
        smoothYSelection.setDuration(125)
        smoothXRotation.setDuration(125)
        smoothYRotation.setDuration(125)
        smoothXSelection.setEasingCurve(QEasingCurve.InOutQuad)
        smoothYSelection.setEasingCurve(QEasingCurve.InOutQuad)
        smoothXRotation.setEasingCurve(QEasingCurve.InOutQuad)
        smoothYRotation.setEasingCurve(QEasingCurve.InOutQuad)

        smoothFlipRotation = QPropertyAnimation(flipRotation, b'angle')
        smoothFlipScale = QPropertyAnimation(pad, b'scale')
        smoothFlipXRotation = QPropertyAnimation(xRotation, b'angle')
        smoothFlipYRotation = QPropertyAnimation(yRotation, b'angle')
        flipAnimation = QParallelAnimationGroup(self)
        smoothFlipScale.setDuration(500)
        smoothFlipRotation.setDuration(500)
        smoothFlipXRotation.setDuration(500)
        smoothFlipYRotation.setDuration(500)
        smoothFlipScale.setEasingCurve(QEasingCurve.InOutQuad)
        smoothFlipRotation.setEasingCurve(QEasingCurve.InOutQuad)
        smoothFlipXRotation.setEasingCurve(QEasingCurve.InOutQuad)
        smoothFlipYRotation.setEasingCurve(QEasingCurve.InOutQuad)
        smoothFlipScale.setKeyValueAt(0, 1.0)
        smoothFlipScale.setKeyValueAt(0.5, 0.7)
        smoothFlipScale.setKeyValueAt(1, 1.0)
        flipAnimation.addAnimation(smoothFlipRotation)
        flipAnimation.addAnimation(smoothFlipScale)
        flipAnimation.addAnimation(smoothFlipXRotation)
        flipAnimation.addAnimation(smoothFlipYRotation)

        setVariablesSequence = QSequentialAnimationGroup()
        setFillAnimation = QPropertyAnimation(pad, b'fill')
        setBackItemVisibleAnimation = QPropertyAnimation(backItem, b'visible')
        setSelectionItemVisibleAnimation = QPropertyAnimation(selectionItem, b'visible')
        setFillAnimation.setDuration(0)
        setBackItemVisibleAnimation.setDuration(0)
        setSelectionItemVisibleAnimation.setDuration(0)
        setVariablesSequence.addPause(250)
        setVariablesSequence.addAnimation(setBackItemVisibleAnimation)
        setVariablesSequence.addAnimation(setSelectionItemVisibleAnimation)
        setVariablesSequence.addAnimation(setFillAnimation)
        flipAnimation.addAnimation(setVariablesSequence)

        stateMachine = QStateMachine(self)
        splashState = QState(stateMachine)
        frontState = QState(stateMachine)
        historyState = QHistoryState(frontState)
        backState = QState(stateMachine)

        frontState.assignProperty(pad, "fill", False)
        frontState.assignProperty(splash, "opacity", 0.0)
        frontState.assignProperty(backItem, "visible", False)
        frontState.assignProperty(flipRotation, "angle", 0.0)
        frontState.assignProperty(selectionItem, "visible", True)

        backState.assignProperty(pad, "fill", True)
        backState.assignProperty(backItem, "visible", True)
        backState.assignProperty(xRotation, "angle", 0.0)
        backState.assignProperty(yRotation, "angle", 0.0)
        backState.assignProperty(flipRotation, "angle", 180.0)
        backState.assignProperty(selectionItem, "visible", False)

        stateMachine.addDefaultAnimation(smoothXRotation)
        stateMachine.addDefaultAnimation(smoothYRotation)
        stateMachine.addDefaultAnimation(smoothXSelection)
        stateMachine.addDefaultAnimation(smoothYSelection)
        stateMachine.setInitialState(splashState)

        anyKeyTransition = QEventTransition(self, QEvent.KeyPress, splashState)
        anyKeyTransition.setTargetState(frontState)
        anyKeyTransition.addAnimation(smoothSplashMove)
        anyKeyTransition.addAnimation(smoothSplashOpacity)

        enterTransition = QKeyEventTransition(self, QEvent.KeyPress,
                Qt.Key_Enter, backState)
        returnTransition = QKeyEventTransition(self, QEvent.KeyPress,
                Qt.Key_Return, backState)
        backEnterTransition = QKeyEventTransition(self, QEvent.KeyPress,
                Qt.Key_Enter, frontState)
        backReturnTransition = QKeyEventTransition(self, QEvent.KeyPress,
                Qt.Key_Return, frontState)
        enterTransition.setTargetState(historyState)
        returnTransition.setTargetState(historyState)
        backEnterTransition.setTargetState(backState)
        backReturnTransition.setTargetState(backState)
        enterTransition.addAnimation(flipAnimation)
        returnTransition.addAnimation(flipAnimation)
        backEnterTransition.addAnimation(flipAnimation)
        backReturnTransition.addAnimation(flipAnimation)

        columns = size.width()
        rows = size.height()
        stateGrid = []
        for y in range(rows):
            stateGrid.append([QState(frontState) for _ in range(columns)])

        frontState.setInitialState(stateGrid[0][0])
        selectionItem.setPos(pad.iconAt(0, 0).pos())

        for y in range(rows):
            for x in range(columns):
                state = stateGrid[y][x]

                rightTransition = QKeyEventTransition(self, QEvent.KeyPress,
                        Qt.Key_Right, state)
                leftTransition = QKeyEventTransition(self, QEvent.KeyPress,
                        Qt.Key_Left, state)
                downTransition = QKeyEventTransition(self, QEvent.KeyPress,
                        Qt.Key_Down, state)
                upTransition = QKeyEventTransition(self, QEvent.KeyPress,
                        Qt.Key_Up, state)

                rightTransition.setTargetState(stateGrid[y][(x + 1) % columns])
                leftTransition.setTargetState(stateGrid[y][((x - 1) + columns) % columns])
                downTransition.setTargetState(stateGrid[(y + 1) % rows][x])
                upTransition.setTargetState(stateGrid[((y - 1) + rows) % rows][x])

                icon = pad.iconAt(x, y)
                state.assignProperty(xRotation, "angle", -icon.x() / 6.0)
                state.assignProperty(yRotation, "angle", icon.y() / 6.0)
                state.assignProperty(selectionItem, "x", icon.x())
                state.assignProperty(selectionItem, "y", icon.y())
                frontState.assignProperty(icon, "visible", True)
                backState.assignProperty(icon, "visible", False)

                setIconVisibleAnimation = QPropertyAnimation(icon, b'visible')
                setIconVisibleAnimation.setDuration(0)
                setVariablesSequence.addAnimation(setIconVisibleAnimation)

        scene = QGraphicsScene(self)
        scene.setBackgroundBrush(QBrush(QPixmap(":/images/blue_angle_swirl.jpg")))
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        scene.addItem(pad)
        scene.setSceneRect(scene.itemsBoundingRect())
        self.setScene(scene)

        sbr = splash.boundingRect()
        splash.setPos(-sbr.width() / 2, scene.sceneRect().top() - 2)
        frontState.assignProperty(splash, "y", splash.y() - 100.0)
        scene.addItem(splash)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMinimumSize(50, 50)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing |
                QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

        if QGLFormat.hasOpenGL():
            self.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))

        stateMachine.start()

    def resizeEvent(self, event):
        super(PadNavigator, self).resizeEvent(event)
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)


class RoundRectItem(QGraphicsObject):
    def __init__(self, bounds, color, parent=None):
        super(RoundRectItem, self).__init__(parent)

        self.fillRect = False
        self.bounds = QRectF(bounds)
        self.pix = QPixmap()

        self.gradient = QLinearGradient()
        self.gradient.setStart(self.bounds.topLeft())
        self.gradient.setFinalStop(self.bounds.bottomRight())
        self.gradient.setColorAt(0, color)
        self.gradient.setColorAt(1, color.darker(200))

        self.setCacheMode(QGraphicsItem.ItemCoordinateCache)

    def setFill(self, fill):
        self.fillRect = fill
        self.update()

    def fill(self):
        return self.fillRect

    fill = pyqtProperty(bool, fill, setFill)

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 64))
        painter.drawRoundedRect(self.bounds.translated(2, 2), 25.0, 25.0)

        if self.fillRect:
            painter.setBrush(QApplication.palette().brush(QPalette.Window))
        else:
            painter.setBrush(self.gradient)

        painter.setPen(QPen(Qt.black, 1))
        painter.drawRoundedRect(self.bounds, 25.0, 25.0)
        if not self.pix.isNull():
            painter.scale(1.95, 1.95)
            painter.drawPixmap(-self.pix.width() / 2, -self.pix.height() / 2, self.pix)

    def boundingRect(self):
        return self.bounds.adjusted(0, 0, 2, 2)

    def pixmap(self):
        return QPixmap(self.pix)

    def setPixmap(self, pixmap):
        self.pix = QPixmap(pixmap)
        self.update()


class FlippablePad(RoundRectItem):
    def __init__(self, size, parent=None):
        super(FlippablePad, self).__init__(self.boundsFromSize(size),
                QColor(226, 255, 92, 64), parent)

        numIcons = size.width() * size.height()
        pixmaps = []
        it = QDirIterator(":/images", ["*.png"])
        while it.hasNext() and len(pixmaps) < numIcons:
            pixmaps.append(it.next())

        iconRect = QRectF(-54, -54, 108, 108)
        iconColor = QColor(214, 240, 110, 128)
        self.iconGrid = []
        n = 0

        for y in range(size.height()):
            row = []

            for x in range(size.width()):
                rect = RoundRectItem(iconRect, iconColor, self)
                rect.setZValue(1)
                rect.setPos(self.posForLocation(x, y, size))
                rect.setPixmap(pixmaps[n % len(pixmaps)])
                n += 1

                row.append(rect)

            self.iconGrid.append(row)

    def iconAt(self, column, row):
        return self.iconGrid[row][column]

    @staticmethod
    def boundsFromSize(size):
        return QRectF((-size.width() / 2.0) * 150,
                (-size.height() / 2.0) * 150, size.width() * 150,
                size.height() * 150)

    @staticmethod
    def posForLocation(column, row, size):
        return QPointF(column * 150, row * 150) - QPointF((size.width() - 1) * 75, (size.height() - 1) * 75)


class SplashItem(QGraphicsObject):
    def __init__(self, parent=None):
        super(SplashItem, self).__init__(parent)

        self.text = "Welcome to the Pad Navigator Example. You can use the " \
                "keyboard arrows to navigate the icons, and press enter to " \
                "activate an item. Press any key to begin."

        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

    def boundingRect(self):
        return QRectF(0, 0, 400, 175)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QColor(245, 245, 255, 220))
        painter.setClipRect(self.boundingRect())
        painter.drawRoundedRect(3, -100 + 3, 400 - 6, 250 - 6, 25.0, 25.0)

        textRect = self.boundingRect().adjusted(10, 10, -10, -10)
        flags = int(Qt.AlignTop | Qt.AlignLeft) | Qt.TextWordWrap

        font = QFont()
        font.setPixelSize(18)
        painter.setPen(Qt.black)
        painter.setFont(font)
        painter.drawText(textRect, flags, self.text)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    navigator = PadNavigator(QSize(3, 3))
    navigator.show()

    sys.exit(app.exec_())
