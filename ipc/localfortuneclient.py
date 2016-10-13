#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited
## Copyright (C) 2010 Hans-Peter Jansen <hpj@urpla.net>.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial Usage
## Licensees holding valid Qt Commercial licenses may use this file in
## accordance with the Qt Commercial License Agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and Nokia.
##
## GNU Lesser General Public License Usage
## Alternatively, this file may be used under the terms of the GNU Lesser
## General Public License version 2.1 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU Lesser General Public License version 2.1 requirements
## will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
##
## In addition, as a special exception, Nokia gives you certain additional
## rights.  These rights are described in the Nokia Qt LGPL Exception
## version 1.1, included in the file LGPL_EXCEPTION.txt in this package.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3.0 as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU General Public License version 3.0 requirements will be
## met: http://www.gnu.org/copyleft/gpl.html.
##
## If you have questions regarding the use of this file, please contact
## Nokia at qt-info@nokia.com.
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import QDataStream, QTimer
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox,
        QGridLayout, QLabel, QLineEdit, QMessageBox, QPushButton)
from PyQt5.QtNetwork import QLocalSocket


class Client(QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        self.blockSize = 0
        self.currentFortune = None

        hostLabel = QLabel("&Server name:")
        self.hostLineEdit = QLineEdit("fortune")
        hostLabel.setBuddy(self.hostLineEdit)

        self.statusLabel = QLabel(
                "This examples requires that you run the Fortune Server "
                "example as well.")
        self.statusLabel.setWordWrap(True)

        self.getFortuneButton = QPushButton("Get Fortune")
        self.getFortuneButton.setDefault(True)

        quitButton = QPushButton("Quit")
        buttonBox = QDialogButtonBox()
        buttonBox.addButton(self.getFortuneButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(quitButton, QDialogButtonBox.RejectRole)

        self.socket = QLocalSocket()

        self.hostLineEdit.textChanged.connect(self.enableGetFortuneButton)
        self.getFortuneButton.clicked.connect(self.requestNewFortune)
        quitButton.clicked.connect(self.close)
        self.socket.readyRead.connect(self.readFortune)
        self.socket.error.connect(self.displayError)

        mainLayout = QGridLayout()
        mainLayout.addWidget(hostLabel, 0, 0)
        mainLayout.addWidget(self.hostLineEdit, 0, 1)
        mainLayout.addWidget(self.statusLabel, 2, 0, 1, 2)
        mainLayout.addWidget(buttonBox, 3, 0, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle("Fortune Client")
        self.hostLineEdit.setFocus()

    def requestNewFortune(self):
        self.getFortuneButton.setEnabled(False)
        self.blockSize = 0
        self.socket.abort()
        self.socket.connectToServer(self.hostLineEdit.text())

    def readFortune(self):
        ins = QDataStream(self.socket)
        ins.setVersion(QDataStream.Qt_4_0)

        if self.blockSize == 0:
            if self.socket.bytesAvailable() < 2:
                return
            self.blockSize = ins.readUInt16()

        if ins.atEnd():
            return

        nextFortune = ins.readQString()
        if nextFortune == self.currentFortune:
            QTimer.singleShot(0, self.requestNewFortune)
            return
 
        self.currentFortune = nextFortune
        self.statusLabel.setText(self.currentFortune)
        self.getFortuneButton.setEnabled(True)

    def displayError(self, socketError):
        errors = {
            QLocalSocket.ServerNotFoundError:
                "The host was not found. Please check the host name and port "
                "settings.",

            QLocalSocket.ConnectionRefusedError:
                "The connection was refused by the peer. Make sure the "
                "fortune server is running, and check that the host name and "
                "port settings are correct.",

            QLocalSocket.PeerClosedError:
                None,
        }

        msg = errors.get(socketError,
                "The following error occurred: %s." % self.socket.errorString())
        if msg is not None:
            QMessageBox.information(self, "Fortune Client", msg)

        self.getFortuneButton.setEnabled(True)

    def enableGetFortuneButton(self):
        self.getFortuneButton.setEnabled(self.hostLineEdit.text() != "")


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())
