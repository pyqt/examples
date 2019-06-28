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


from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox, QLabel,
        QPushButton, QVBoxLayout)
from PyQt5.QtNetwork import QHostAddress, QUdpSocket


class Sender(QDialog):
    def __init__(self, parent=None):
        super(Sender, self).__init__(parent)

        self.statusLabel = QLabel("Ready to broadcast datagrams on port 45454")

        self.startButton = QPushButton("&Start")
        quitButton = QPushButton("&Quit")

        buttonBox = QDialogButtonBox()
        buttonBox.addButton(self.startButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(quitButton, QDialogButtonBox.RejectRole)

        self.timer = QTimer(self)
        self.udpSocket = QUdpSocket(self)
        self.messageNo = 1

        self.startButton.clicked.connect(self.startBroadcasting)
        quitButton.clicked.connect(self.close)
        self.timer.timeout.connect(self.broadcastDatagramm)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Broadcast Sender")

    def startBroadcasting(self):
        self.startButton.setEnabled(False)
        self.timer.start(1000)

    def broadcastDatagramm(self):
        self.statusLabel.setText("Now broadcasting datagram %d" % self.messageNo)
        datagram = "Broadcast message %d" % self.messageNo
        self.udpSocket.writeDatagram(datagram, QHostAddress(QHostAddress.Broadcast), 45454)
        self.messageNo += 1


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    sender = Sender()
    sender.show()
    sys.exit(sender.exec_())
