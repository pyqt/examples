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


import random

from PyQt5.QtCore import QByteArray, QDataStream, QIODevice, QSettings
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
        QMessageBox, QPushButton, QVBoxLayout)
from PyQt5.QtNetwork import (QHostAddress, QNetworkConfiguration,
        QNetworkConfigurationManager, QNetworkInterface, QNetworkSession,
        QTcpServer)


class Server(QDialog):
    FORTUNES = (
        "You've been leading a dog's life. Stay off the furniture.",
        "You've got to think about tomorrow.",
        "You will be surprised by a loud noise.",
        "You will feel hungry again in another hour.",
        "You might have mail.",
        "You cannot kill time without injuring eternity.",
        "Computers are not intelligent. They only think they are.")

    def __init__(self, parent=None):
        super(Server, self).__init__(parent)

        self.tcpServer = None
        self.networkSession = None

        self.statusLabel = QLabel()
        quitButton = QPushButton("Quit")
        quitButton.setAutoDefault(False)

        manager = QNetworkConfigurationManager()
        if manager.capabilities() & QNetworkConfigurationManager.NetworkSessionRequired:
            settings = QSettings(QSettings.UserScope, 'QtProject')
            settings.beginGroup('QtNetwork')
            id = settings.value('DefaultNetworkConfiguration', '')
            settings.endGroup()

            config = manager.configurationFromIdentifier(id)
            if config.state() & QNetworkConfiguration.Discovered == 0:
                config = manager.defaultConfiguration()

            self.networkSession = QNetworkSession(config, self)
            self.networkSession.opened.connect(self.sessionOpened)

            self.statusLabel.setText("Opening network session.")
            self.networkSession.open()
        else:
            self.sessionOpened()

        quitButton.clicked.connect(self.close)
        self.tcpServer.newConnection.connect(self.sendFortune)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle("Fortune Server")

    def sessionOpened(self):
        if self.networkSession is not None:
            config = self.networkSession.configuration()

            if config.type() == QNetworkConfiguration.UserChoice:
                id = self.networkSession.sessionProperty('UserChoiceConfiguration')
            else:
                id = config.identifier()

            settings = QSettings(QSettings.UserScope, 'QtProject')
            settings.beginGroup('QtNetwork')
            settings.setValue('DefaultNetworkConfiguration', id)
            settings.endGroup();

        self.tcpServer = QTcpServer(self)
        if not self.tcpServer.listen():
            QMessageBox.critical(self, "Fortune Server",
                    "Unable to start the server: %s." % self.tcpServer.errorString())
            self.close()
            return

        for ipAddress in QNetworkInterface.allAddresses():
            if ipAddress != QHostAddress.LocalHost and ipAddress.toIPv4Address() != 0:
                break
        else:
            ipAddress = QHostAddress(QHostAddress.LocalHost)

        ipAddress = ipAddress.toString()

        self.statusLabel.setText("The server is running on\n\nIP: %s\nport %d\n\n"
                "Run the Fortune Client example now." % (ipAddress, self.tcpServer.serverPort()))

    def sendFortune(self):
        fortune = self.FORTUNES[random.randint(0, len(self.FORTUNES) - 1)]

        block = QByteArray()
        out = QDataStream(block, QIODevice.WriteOnly)
        out.setVersion(QDataStream.Qt_4_0)
        out.writeUInt16(0)
        out.writeQString(fortune)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)

        clientConnection = self.tcpServer.nextPendingConnection()
        clientConnection.disconnected.connect(clientConnection.deleteLater)

        clientConnection.write(block)
        clientConnection.disconnectFromHost()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    server = Server()
    random.seed(None)
    sys.exit(server.exec_())
