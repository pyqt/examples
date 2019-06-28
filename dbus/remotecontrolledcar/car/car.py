#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2011 Nokia Corporation and/or its subsidiary(-ies).
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

from PyQt5.QtCore import pyqtSlot, Q_CLASSINFO, QRectF, Qt
from PyQt5.QtGui import QBrush, QPainter, QTransform
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsObject,
        QGraphicsScene, QGraphicsView)
from PyQt5.QtDBus import QDBusAbstractAdaptor, QDBusConnection


class Car(QGraphicsObject):

    def __init__(self):
        super(Car, self).__init__()

        self.color = QBrush(Qt.green)
        self.wheelsAngle = 0.0
        self.speed = 0.0

        self.startTimer(1000 // 33)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

    def accelerate(self):
        if self.speed < 10:
            self.speed += 1

    def decelerate(self):
        if self.speed > -10:
            self.speed -= 1

    def turnLeft(self):
        if self.wheelsAngle > -30:
            self.wheelsAngle -= 5

    def turnRight(self):
        if self.wheelsAngle < 30:
            self.wheelsAngle += 5

    def boundingRect(self):
        return QRectF(-35, -81, 70, 115)

    def timerEvent(self, event):
        axelDistance = 54.0
        wheelsAngleRads = (self.wheelsAngle * math.pi) / 180
        turnDistance = math.cos(wheelsAngleRads) * axelDistance * 2
        turnRateRads = wheelsAngleRads / turnDistance
        turnRate = (turnRateRads * 180) / math.pi
        rotation = self.speed * turnRate

        self.setTransform(QTransform().rotate(rotation), True)
        self.setTransform(QTransform.fromTranslate(0, -self.speed), True)
        self.update()

    def paint(self, painter, option, widget):
        painter.setBrush(Qt.gray)
        painter.drawRect(-20, -58, 40, 2)       # Front axel
        painter.drawRect(-20, 7, 40, 2)         # Rear axel

        painter.setBrush(self.color)
        painter.drawRect(-25, -79, 50, 10)      # Front wing

        painter.drawEllipse(-25, -48, 50, 20)   # Side pods
        painter.drawRect(-25, -38, 50, 35)      # Side pods
        painter.drawRect(-5, 9, 10, 10)         # Back pod

        painter.drawEllipse(-10, -81, 20, 100)  # Main body

        painter.drawRect(-17, 19, 34, 15)       # Rear wing

        painter.setBrush(Qt.black)
        painter.drawPie(-5, -51, 10, 15, 0, 180 * 16)
        painter.drawRect(-5, -44, 10, 10)       # Cockpit

        painter.save()
        painter.translate(-20, -58)
        painter.rotate(self.wheelsAngle)
        painter.drawRect(-10, -7, 10, 15)       # Front left
        painter.restore()

        painter.save()
        painter.translate(20, -58)
        painter.rotate(self.wheelsAngle)
        painter.drawRect(0, -7, 10, 15)         # Front right
        painter.restore()

        painter.drawRect(-30, 0, 12, 17)        # Rear left
        painter.drawRect(19, 0, 12, 17)         # Rear right


class CarInterfaceAdaptor(QDBusAbstractAdaptor):

    Q_CLASSINFO("D-Bus Interface", 'org.example.Examples.CarInterface')

    Q_CLASSINFO("D-Bus Introspection", ''
            '  <interface name="org.example.Examples.CarInterface">\n'
            '    <method name="accelerate"/>\n'
            '    <method name="decelerate"/>\n'
            '    <method name="turnLeft"/>\n'
            '    <method name="turnRight"/>\n'
            '  </interface>\n'
            '')

    def __init__(self, parent):
        super(CarInterfaceAdaptor, self).__init__(parent)

        self.setAutoRelaySignals(True)

    @pyqtSlot()
    def accelerate(self):
        self.parent().accelerate()

    @pyqtSlot()
    def decelerate(self):
        self.parent().decelerate()

    @pyqtSlot()
    def turnLeft(self):
        self.parent().turnLeft()

    @pyqtSlot()
    def turnRight(self):
        self.parent().turnRight()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    scene = QGraphicsScene()
    scene.setSceneRect(-500, -500, 1000, 1000)
    scene.setItemIndexMethod(QGraphicsScene.NoIndex)

    car = Car()
    scene.addItem(car)

    view = QGraphicsView(scene)
    view.setRenderHint(QPainter.Antialiasing)
    view.setBackgroundBrush(Qt.darkGray)
    view.setWindowTitle("Qt DBus Controlled Car")
    view.resize(400, 300)
    view.show()

    a = CarInterfaceAdaptor(car)
    connection = QDBusConnection.sessionBus()
    connection.registerObject('/Car', car)
    connection.registerService('org.example.CarExample')

    rc = app.exec_()

    # Make sure things get destroyed in the right order.
    del view

    sys.exit(rc)
