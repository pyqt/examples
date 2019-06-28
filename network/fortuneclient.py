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


from PyQt5.QtCore import QDataStream, QSettings, QTimer
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QMessageBox,
        QPushButton)
from PyQt5.QtNetwork import (QAbstractSocket, QHostInfo, QNetworkConfiguration,
        QNetworkConfigurationManager, QNetworkInterface, QNetworkSession,
        QTcpSocket)


class Client(QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        self.networkSession = None
        self.blockSize = 0
        self.currentFortune = ''

        hostLabel = QLabel("&Server name:")
        portLabel = QLabel("S&erver port:")

        self.hostCombo = QComboBox()
        self.hostCombo.setEditable(True)

        name = QHostInfo.localHostName()
        if name != '':
            self.hostCombo.addItem(name)

            domain = QHostInfo.localDomainName()
            if domain != '':
                self.hostCombo.addItem(name + '.' + domain)

        if name != 'localhost':
            self.hostCombo.addItem('localhost')

        ipAddressesList = QNetworkInterface.allAddresses()

        for ipAddress in ipAddressesList:
            if not ipAddress.isLoopback():
                self.hostCombo.addItem(ipAddress.toString())

        for ipAddress in ipAddressesList:
            if ipAddress.isLoopback():
                self.hostCombo.addItem(ipAddress.toString())

        self.portLineEdit = QLineEdit()
        self.portLineEdit.setValidator(QIntValidator(1, 65535, self))

        hostLabel.setBuddy(self.hostCombo)
        portLabel.setBuddy(self.portLineEdit)

        self.statusLabel = QLabel("This examples requires that you run "
                "the Fortune Server example as well.")

        self.getFortuneButton = QPushButton("Get Fortune")
        self.getFortuneButton.setDefault(True)
        self.getFortuneButton.setEnabled(False)

        quitButton = QPushButton("Quit")

        buttonBox = QDialogButtonBox()
        buttonBox.addButton(self.getFortuneButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(quitButton, QDialogButtonBox.RejectRole)

        self.tcpSocket = QTcpSocket(self)

        self.hostCombo.editTextChanged.connect(self.enableGetFortuneButton)
        self.portLineEdit.textChanged.connect(self.enableGetFortuneButton)
        self.getFortuneButton.clicked.connect(self.requestNewFortune)
        quitButton.clicked.connect(self.close)
        self.tcpSocket.readyRead.connect(self.readFortune)
        self.tcpSocket.error.connect(self.displayError)

        mainLayout = QGridLayout()
        mainLayout.addWidget(hostLabel, 0, 0)
        mainLayout.addWidget(self.hostCombo, 0, 1)
        mainLayout.addWidget(portLabel, 1, 0)
        mainLayout.addWidget(self.portLineEdit, 1, 1)
        mainLayout.addWidget(self.statusLabel, 2, 0, 1, 2)
        mainLayout.addWidget(buttonBox, 3, 0, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle("Fortune Client")
        self.portLineEdit.setFocus()

        manager = QNetworkConfigurationManager()
        if manager.capabilities() & QNetworkConfigurationManager.NetworkSessionRequired:
            settings = QSettings(QSettings.UserScope, 'QtProject')
            settings.beginGroup('QtNetwork')
            id = settings.value('DefaultNetworkConfiguration')
            settings.endGroup()

            config = manager.configurationFromIdentifier(id)
            if config.state() & QNetworkConfiguration.Discovered == 0:
                config = manager.defaultConfiguration()

            self.networkSession = QNetworkSession(config, self)
            self.networkSession.opened.connect(self.sessionOpened)

            self.getFortuneButton.setEnabled(False)
            self.statusLabel.setText("Opening network session.")
            self.networkSession.open()

    def requestNewFortune(self):
        self.getFortuneButton.setEnabled(False)
        self.blockSize = 0
        self.tcpSocket.abort()
        self.tcpSocket.connectToHost(self.hostCombo.currentText(),
                int(self.portLineEdit.text()))

    def readFortune(self):
        instr = QDataStream(self.tcpSocket)
        instr.setVersion(QDataStream.Qt_4_0)

        if self.blockSize == 0:
            if self.tcpSocket.bytesAvailable() < 2:
                return

            self.blockSize = instr.readUInt16()

        if self.tcpSocket.bytesAvailable() < self.blockSize:
            return

        nextFortune = instr.readQString()
        if nextFortune == self.currentFortune:
            QTimer.singleShot(0, self.requestNewFortune)
            return

        self.currentFortune = nextFortune
        self.statusLabel.setText(self.currentFortune)
        self.getFortuneButton.setEnabled(True)

    def displayError(self, socketError):
        if socketError == QAbstractSocket.RemoteHostClosedError:
            pass
        elif socketError == QAbstractSocket.HostNotFoundError:
            QMessageBox.information(self, "Fortune Client",
                    "The host was not found. Please check the host name and "
                    "port settings.")
        elif socketError == QAbstractSocket.ConnectionRefusedError:
            QMessageBox.information(self, "Fortune Client",
                    "The connection was refused by the peer. Make sure the "
                    "fortune server is running, and check that the host name "
                    "and port settings are correct.")
        else:
            QMessageBox.information(self, "Fortune Client",
                    "The following error occurred: %s." % self.tcpSocket.errorString())

        self.getFortuneButton.setEnabled(True)

    def enableGetFortuneButton(self):
        self.getFortuneButton.setEnabled(
                (self.networkSession is None or self.networkSession.isOpen())
                and self.hostCombo.currentText() != ''
                and self.portLineEdit.text() != '')

    def sessionOpened(self):
        config = self.networkSession.configuration()

        if config.type() == QNetworkConfiguration.UserChoice:
            id = self.networkSession.sessionProperty('UserChoiceConfiguration')
        else:
            id = config.identifier()

        settings = QSettings(QSettings.UserScope, 'QtProject')
        settings.beginGroup('QtNetwork')
        settings.setValue('DefaultNetworkConfiguration', id)
        settings.endGroup()

        self.statusLabel.setText("This examples requires that you run the "
                            "Fortune Server example as well.")

        self.enableGetFortuneButton()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())
