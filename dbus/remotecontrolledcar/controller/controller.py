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


from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtDBus import QDBusAbstractInterface, QDBusConnection

from ui_controller import Ui_Controller


class CarInterface(QDBusAbstractInterface):

    def __init__(self, service, path, connection, parent=None):
        super(CarInterface, self).__init__(service, path,
                'org.example.Examples.CarInterface', connection, parent)

    def accelerate(self):
        self.asyncCall('accelerate')

    def decelerate(self):
        self.asyncCall('decelerate')

    def turnLeft(self):
        self.asyncCall('turnLeft')

    def turnRight(self):
        self.asyncCall('turnRight')


class Controller(QWidget):

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)

        self.ui = Ui_Controller()

        self.ui.setupUi(self)

        self.car = CarInterface('org.example.CarExample', '/Car',
                QDBusConnection.sessionBus(), self)

        self.startTimer(1000)

    def timerEvent(self, event):
        if self.car.isValid():
            self.ui.label.setText("connected")
        else:
            self.ui.label.setText("disconnected")

    def on_accelerate_clicked(self):
        self.car.accelerate()

    def on_decelerate_clicked(self):
        self.car.decelerate()

    def on_left_clicked(self):
        self.car.turnLeft()

    def on_right_clicked(self):
        self.car.turnRight()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    controller = Controller()
    controller.show()

    sys.exit(app.exec_())
