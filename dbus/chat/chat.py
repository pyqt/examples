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


from PyQt5.QtCore import pyqtSignal, pyqtSlot, Q_CLASSINFO
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
from PyQt5.QtDBus import (QDBusAbstractAdaptor, QDBusAbstractInterface,
        QDBusConnection, QDBusMessage)

from ui_chatmainwindow import Ui_ChatMainWindow
from ui_chatsetnickname import Ui_NicknameDialog


class ChatAdaptor(QDBusAbstractAdaptor):

    Q_CLASSINFO("D-Bus Interface", 'org.example.chat')

    Q_CLASSINFO("D-Bus Introspection", ''
        '  <interface name="org.example.chat">\n'
        '    <signal name="message">\n'
        '      <arg direction="out" type="s" name="nickname"/>\n'
        '      <arg direction="out" type="s" name="text"/>\n'
        '    </signal>\n'
        '    <signal name="action">\n'
        '      <arg direction="out" type="s" name="nickname"/>\n'
        '      <arg direction="out" type="s" name="text"/>\n'
        '    </signal>\n'
        '  </interface>\n'
        '')

    action = pyqtSignal(str, str)

    message = pyqtSignal(str, str)

    def __init__(self, parent):
        super(ChatAdaptor, self).__init__(parent)

        self.setAutoRelaySignals(True)


class ChatInterface(QDBusAbstractInterface):

    action = pyqtSignal(str, str)

    message = pyqtSignal(str, str)

    def __init__(self, service, path, connection, parent=None):
        super(ChatInterface, self).__init__(service, path, 'org.example.chat',
                connection, parent)


class ChatMainWindow(QMainWindow, Ui_ChatMainWindow):

    action = pyqtSignal(str, str)

    message = pyqtSignal(str, str)

    def __init__(self):
        super(ChatMainWindow, self).__init__()

        self.m_nickname = "nickname"
        self.m_messages = []

        self.setupUi(self)
        self.sendButton.setEnabled(False)

        self.messageLineEdit.textChanged.connect(self.textChangedSlot)
        self.sendButton.clicked.connect(self.sendClickedSlot)
        self.actionChangeNickname.triggered.connect(self.changeNickname)
        self.actionAboutQt.triggered.connect(self.aboutQt)
        QApplication.instance().lastWindowClosed.connect(self.exiting)

        # Add our D-Bus interface and connect to D-Bus.
        ChatAdaptor(self)
        QDBusConnection.sessionBus().registerObject('/', self)

        iface = ChatInterface('', '', QDBusConnection.sessionBus(), self)
        QDBusConnection.sessionBus().connect('', '', 'org.example.chat',
                'message', self.messageSlot)
        iface.action.connect(self.actionSlot)

        dialog = NicknameDialog()
        dialog.cancelButton.setVisible(False)
        dialog.exec_()
        self.m_nickname = dialog.nickname.text().strip()
        self.action.emit(self.m_nickname, "joins the chat")

    def rebuildHistory(self):
        history = '\n'.join(self.m_messages)
        self.chatHistory.setPlainText(history)

    @pyqtSlot(str, str)
    def messageSlot(self, nickname, text):
        self.m_messages.append("<%s> %s" % (nickname, text))

        if len(self.m_messages) > 100:
            self.m_messages.pop(0)

        self.rebuildHistory()

    @pyqtSlot(str, str)
    def actionSlot(self, nickname, text):
        self.m_messages.append("* %s %s" % (nickname, text))

        if len(self.m_messages) > 100:
            self.m_messages.pop(0)

        self.rebuildHistory()

    @pyqtSlot(str)
    def textChangedSlot(self, newText):
        self.sendButton.setEnabled(newText != '')

    @pyqtSlot()
    def sendClickedSlot(self):
        msg = QDBusMessage.createSignal('/', 'org.example.chat', 'message')
        msg << self.m_nickname << self.messageLineEdit.text()
        QDBusConnection.sessionBus().send(msg)
        self.messageLineEdit.setText('')

    @pyqtSlot()
    def changeNickname(self):
        dialog = NicknameDialog(self)

        if dialog.exec_() == QDialog.Accepted:
            old = self.m_nickname
            self.m_nickname = dialog.nickname.text().strip()
            self.action.emit(old, "is now known as %s" % self.m_nickname)

    @pyqtSlot()
    def aboutQt(self):
        QMessageBox.aboutQt(self)

    @pyqtSlot()
    def exiting(self):
        self.action.emit(self.m_nickname, "leaves the chat")


class NicknameDialog(QDialog, Ui_NicknameDialog):

    def __init__(self, parent=None):
        super(NicknameDialog, self).__init__(parent)

        self.setupUi(self)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    if not QDBusConnection.sessionBus().isConnected():
        sys.stderr.write("Cannot connect to the D-Bus session bus.\n"
                "Please check your system settings and try again.\n")
        sys.exit(1)

    chat = ChatMainWindow()
    chat.show()

    sys.exit(app.exec_())
