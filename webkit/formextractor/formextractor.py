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
###########################################################################


from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QMainWindow, QMessageBox,
        QWidget)

import formextractor_rc
from ui_formextractor import Ui_Form


class FormExtractor(QWidget):
    def __init__(self, parent=None):
        super(FormExtractor, self).__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        webView = self.ui.webView
        webView.setUrl(QUrl('qrc:/form.html'))
        webView.page().mainFrame().javaScriptWindowObjectCleared.connect(
                self.populateJavaScriptWindowObject)

        self.resize(300, 300)
 
    @pyqtSlot()
    def submit(self):
        frame = self.ui.webView.page().mainFrame()
        firstName = frame.findFirstElement('#firstname')
        lastName = frame.findFirstElement('#lastname')
        maleGender = frame.findFirstElement('#genderMale')
        femaleGender = frame.findFirstElement('#genderFemale')
        updates = frame.findFirstElement('#updates')

        self.ui.firstNameEdit.setText(firstName.evaluateJavaScript('this.value'))
        self.ui.lastNameEdit.setText(lastName.evaluateJavaScript('this.value'))

        if maleGender.evaluateJavaScript('this.checked'):
            self.ui.genderEdit.setText(
                    maleGender.evaluateJavaScript('this.value'))
        elif femaleGender.evaluateJavaScript('this.checked'):
            self.ui.genderEdit.setText(
                    femaleGender.evaluateJavaScript('this.value'))

        if updates.evaluateJavaScript('this.checked'):
            self.ui.updatesEdit.setText("Yes")
        else:
            self.ui.updatesEdit.setText("No")

    def populateJavaScriptWindowObject(self):
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject(
                'formExtractor', self)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.createActions()
        self.createMenus()
        self.centralWidget = FormExtractor(self)
        self.setCentralWidget(self.centralWidget)
    
    def createActions(self):
        self.exitAct = QAction("E&xit", self, statusTip="Exit the application",
                shortcut=QKeySequence.Quit, triggered=self.close)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.exitAct)
        self.menuBar().addSeparator()
        helpMenu = self.menuBar().addMenu("&Help")
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.aboutQtAct)

    def about(self):
        QMessageBox.about(self, "About Form Extractor",
                "The <b>Form Extractor</b> example demonstrates how to "
                "extract data from a web form using QtWebKit.")


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.setWindowTitle("Form Extractor")
    mainWindow.show()

    sys.exit(app.exec_())
