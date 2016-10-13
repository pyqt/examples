#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2010 Riverbank Computing Limited.
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


from PyQt5.QtCore import QDir, QFile, QFileInfo, QIODevice, QUrl
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox,
        QHBoxLayout, QLabel, QLineEdit, QMessageBox, QProgressDialog,
        QPushButton, QVBoxLayout)
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest


class HttpWindow(QDialog):
    def __init__(self, parent=None):
        super(HttpWindow, self).__init__(parent)

        self.url = QUrl()
        self.qnam = QNetworkAccessManager()
        self.reply = None
        self.outFile = None
        self.httpGetId = 0
        self.httpRequestAborted = False

        self.urlLineEdit = QLineEdit('https://www.qt.io')

        urlLabel = QLabel("&URL:")
        urlLabel.setBuddy(self.urlLineEdit)
        self.statusLabel = QLabel(
                "Please enter the URL of a file you want to download.")
        self.statusLabel.setWordWrap(True)

        self.downloadButton = QPushButton("Download")
        self.downloadButton.setDefault(True)
        self.quitButton = QPushButton("Quit")
        self.quitButton.setAutoDefault(False)

        buttonBox = QDialogButtonBox()
        buttonBox.addButton(self.downloadButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.quitButton, QDialogButtonBox.RejectRole)

        self.progressDialog = QProgressDialog(self)

        self.urlLineEdit.textChanged.connect(self.enableDownloadButton)
        self.qnam.authenticationRequired.connect(
                self.slotAuthenticationRequired)
        self.qnam.sslErrors.connect(self.sslErrors)
        self.progressDialog.canceled.connect(self.cancelDownload)
        self.downloadButton.clicked.connect(self.downloadFile)
        self.quitButton.clicked.connect(self.close)

        topLayout = QHBoxLayout()
        topLayout.addWidget(urlLabel)
        topLayout.addWidget(self.urlLineEdit)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("HTTP")
        self.urlLineEdit.setFocus()

    def startRequest(self, url):
        self.reply = self.qnam.get(QNetworkRequest(url))
        self.reply.finished.connect(self.httpFinished)
        self.reply.readyRead.connect(self.httpReadyRead)
        self.reply.downloadProgress.connect(self.updateDataReadProgress)

    def downloadFile(self):
        self.url = QUrl(self.urlLineEdit.text())
        fileInfo = QFileInfo(self.url.path())
        fileName = fileInfo.fileName()

        if not fileName:
            fileName = 'index.html'

        if QFile.exists(fileName):
            ret = QMessageBox.question(self, "HTTP",
                    "There already exists a file called %s in the current "
                    "directory. Overwrite?" % fileName,
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if ret == QMessageBox.No:
                return

            QFile.remove(fileName)

        self.outFile = QFile(fileName)
        if not self.outFile.open(QIODevice.WriteOnly):
            QMessageBox.information(self, "HTTP",
                    "Unable to save the file %s: %s." % (fileName, self.outFile.errorString()))
            self.outFile = None
            return

        self.progressDialog.setWindowTitle("HTTP")
        self.progressDialog.setLabelText("Downloading %s." % fileName)
        self.downloadButton.setEnabled(False)

        self.httpRequestAborted = False
        self.startRequest(self.url)

    def cancelDownload(self):
        self.statusLabel.setText("Download canceled.")
        self.httpRequestAborted = True
        if self.reply is not None:
            self.reply.abort()
        self.downloadButton.setEnabled(True)

    def httpFinished(self):
        if self.httpRequestAborted:
            if self.outFile is not None:
                self.outFile.close()
                self.outFile.remove()
                self.outFile = None

            self.reply.deleteLater()
            self.reply = None
            self.progressDialog.hide()
            return

        self.progressDialog.hide()
        self.outFile.flush()
        self.outFile.close()

        redirectionTarget = self.reply.attribute(QNetworkRequest.RedirectionTargetAttribute)

        if self.reply.error():
            self.outFile.remove()
            QMessageBox.information(self, "HTTP",
                    "Download failed: %s." % self.reply.errorString())
            self.downloadButton.setEnabled(True)
        elif redirectionTarget is not None:
            newUrl = self.url.resolved(redirectionTarget)

            ret = QMessageBox.question(self, "HTTP",
                    "Redirect to %s?" % newUrl.toString(),
                    QMessageBox.Yes | QMessageBox.No)

            if ret == QMessageBox.Yes:
                self.url = newUrl
                self.reply.deleteLater()
                self.reply = None
                self.outFile.open(QIODevice.WriteOnly)
                self.outFile.resize(0)
                self.startRequest(self.url)
                return
        else:
            fileName = QFileInfo(QUrl(self.urlLineEdit.text()).path()).fileName()
            self.statusLabel.setText("Downloaded %s to %s." % (fileName, QDir.currentPath()))

            self.downloadButton.setEnabled(True)

        self.reply.deleteLater()
        self.reply = None
        self.outFile = None

    def httpReadyRead(self):
        if self.outFile is not None:
            self.outFile.write(self.reply.readAll())

    def updateDataReadProgress(self, bytesRead, totalBytes):
        if self.httpRequestAborted:
            return

        self.progressDialog.setMaximum(totalBytes)
        self.progressDialog.setValue(bytesRead)

    def enableDownloadButton(self):
        self.downloadButton.setEnabled(self.urlLineEdit.text() != '')

    def slotAuthenticationRequired(self, authenticator):
        import os
        from PyQt5 import uic

        ui = os.path.join(os.path.dirname(__file__), 'authenticationdialog.ui')
        dlg = uic.loadUi(ui)
        dlg.adjustSize()
        dlg.siteDescription.setText("%s at %s" % (authenticator.realm(), self.url.host()))

        dlg.userEdit.setText(self.url.userName())
        dlg.passwordEdit.setText(self.url.password())

        if dlg.exec_() == QDialog.Accepted:
            authenticator.setUser(dlg.userEdit.text())
            authenticator.setPassword(dlg.passwordEdit.text())

    def sslErrors(self, reply, errors):
        errorString = ", ".join([str(error.errorString()) for error in errors])

        ret = QMessageBox.warning(self, "HTTP Example",
                "One or more SSL errors has occurred: %s" % errorString,
                QMessageBox.Ignore | QMessageBox.Abort)

        if ret == QMessageBox.Ignore:
            self.reply.ignoreSslErrors()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    httpWin = HttpWindow()
    httpWin.show()
    sys.exit(httpWin.exec_())
