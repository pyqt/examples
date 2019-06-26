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


from PyQt5.QtCore import QByteArray, Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox, QLabel,
        QMessageBox, QProgressBar, QPushButton, QVBoxLayout)
from PyQt5.QtNetwork import QHostAddress, QTcpServer, QTcpSocket


class Dialog(QDialog):
    TotalBytes = 50 * 1024 * 1024
    PayloadSize = 65536

    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)

        self.tcpServer = QTcpServer()
        self.tcpClient = QTcpSocket()
        self.bytesToWrite = 0
        self.bytesWritten = 0
        self.bytesReceived = 0

        self.clientProgressBar = QProgressBar()
        self.clientStatusLabel = QLabel("Client ready")
        self.serverProgressBar = QProgressBar()
        self.serverStatusLabel = QLabel("Server ready")

        self.startButton = QPushButton("&Start")
        self.quitButton = QPushButton("&Quit")

        buttonBox = QDialogButtonBox()
        buttonBox.addButton(self.startButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.quitButton, QDialogButtonBox.RejectRole)

        self.startButton.clicked.connect(self.start)
        self.quitButton.clicked.connect(self.close)
        self.tcpServer.newConnection.connect(self.acceptConnection)
        self.tcpClient.connected.connect(self.startTransfer)
        self.tcpClient.bytesWritten.connect(self.updateClientProgress)
        self.tcpClient.error.connect(self.displayError)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.clientProgressBar)
        mainLayout.addWidget(self.clientStatusLabel)
        mainLayout.addWidget(self.serverProgressBar)
        mainLayout.addWidget(self.serverStatusLabel)
        mainLayout.addStretch(1)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Loopback")

    def start(self):
        self.startButton.setEnabled(False)

        QApplication.setOverrideCursor(Qt.WaitCursor)

        self.bytesWritten = 0
        self.bytesReceived = 0

        while not self.tcpServer.isListening() and not self.tcpServer.listen():
            ret = QMessageBox.critical(self, "Loopback",
                    "Unable to start the test: %s." % self.tcpServer.errorString(),
                    QMessageBox.Retry | QMessageBox.Cancel)
            if ret == QMessageBox.Cancel:
                return

        self.serverStatusLabel.setText("Listening")
        self.clientStatusLabel.setText("Connecting")

        self.tcpClient.connectToHost(QHostAddress(QHostAddress.LocalHost), self.tcpServer.serverPort())

    def acceptConnection(self):
        self.tcpServerConnection = self.tcpServer.nextPendingConnection()
        self.tcpServerConnection.readyRead.connect(self.updateServerProgress)
        self.tcpServerConnection.error.connect(self.displayError)

        self.serverStatusLabel.setText("Accepted connection")
        self.tcpServer.close()

    def startTransfer(self):
        self.bytesToWrite = Dialog.TotalBytes - self.tcpClient.write(QByteArray(Dialog.PayloadSize, '@'))
        self.clientStatusLabel.setText("Connected")

    def updateServerProgress(self):
        self.bytesReceived += self.tcpServerConnection.bytesAvailable()
        self.tcpServerConnection.readAll()

        self.serverProgressBar.setMaximum(Dialog.TotalBytes)
        self.serverProgressBar.setValue(self.bytesReceived)
        self.serverStatusLabel.setText("Received %dMB" % (self.bytesReceived / (1024 * 1024)))

        if self.bytesReceived == Dialog.TotalBytes:
            self.tcpServerConnection.close()
            self.startButton.setEnabled(True)
            QApplication.restoreOverrideCursor()

    def updateClientProgress(self, numBytes):
        self.bytesWritten += numBytes
        if self.bytesToWrite > 0:
            self.bytesToWrite -= self.tcpClient.write(QByteArray(
                                        min(self.bytesToWrite, Dialog.PayloadSize), '@'))

        self.clientProgressBar.setMaximum(Dialog.TotalBytes)
        self.clientProgressBar.setValue(self.bytesWritten)
        self.clientStatusLabel.setText("Sent %dMB" % (self.bytesWritten / (1024 * 1024)))

    def displayError(self, socketError):
        if socketError == QTcpSocket.RemoteHostClosedError:
            return

        QMessageBox.information(self, "Network error",
                "The following error occured: %s." % self.tcpClient.errorString())

        self.tcpClient.close()
        self.tcpServer.close()
        self.clientProgressBar.reset()
        self.serverProgressBar.reset()
        self.clientStatusLabel.setText("Client ready")
        self.serverStatusLabel.setText("Server ready")
        self.startButton.setEnabled(True)
        QApplication.restoreOverrideCursor()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(dialog.exec_())
