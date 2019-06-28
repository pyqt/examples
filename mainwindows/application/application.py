#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2014 Riverbank Computing Limited.
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


from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QRect, QSettings, QSize,
        Qt, QTextStream)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,
        QMessageBox, QTextEdit)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.curFile = ''

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

        self.readSettings()

        self.textEdit.document().contentsChanged.connect(self.documentWasModified)

        self.setCurrentFile('')

    def closeEvent(self, event):
        if self.maybeSave():
            self.writeSettings()
            event.accept()
        else:
            event.ignore()

    def newFile(self):
        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFile('')

    def open(self):
        if self.maybeSave():
            fileName, _ = QFileDialog.getOpenFileName(self)
            if fileName:
                self.loadFile(fileName)

    def save(self):
        if self.curFile:
            return self.saveFile(self.curFile)

        return self.saveAs()

    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self)
        if fileName:
            return self.saveFile(fileName)

        return False

    def about(self):
        QMessageBox.about(self, "About Application",
                "The <b>Application</b> example demonstrates how to write "
                "modern GUI applications using Qt, with a menu bar, "
                "toolbars, and a status bar.")

    def documentWasModified(self):
        self.setWindowModified(self.textEdit.document().isModified())

    def createActions(self):
        root = QFileInfo(__file__).absolutePath()

        self.newAct = QAction(QIcon(root + '/images/new.png'), "&New", self,
                shortcut=QKeySequence.New, statusTip="Create a new file",
                triggered=self.newFile)

        self.openAct = QAction(QIcon(root + '/images/open.png'), "&Open...",
                self, shortcut=QKeySequence.Open,
                statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QAction(QIcon(root + '/images/save.png'), "&Save", self,
                shortcut=QKeySequence.Save,
                statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QAction("Save &As...", self,
                shortcut=QKeySequence.SaveAs,
                statusTip="Save the document under a new name",
                triggered=self.saveAs)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application", triggered=self.close)

        self.cutAct = QAction(QIcon(root + '/images/cut.png'), "Cu&t", self,
                shortcut=QKeySequence.Cut,
                statusTip="Cut the current selection's contents to the clipboard",
                triggered=self.textEdit.cut)

        self.copyAct = QAction(QIcon(root + '/images/copy.png'), "&Copy", self,
                shortcut=QKeySequence.Copy,
                statusTip="Copy the current selection's contents to the clipboard",
                triggered=self.textEdit.copy)

        self.pasteAct = QAction(QIcon(root + '/images/paste.png'), "&Paste",
                self, shortcut=QKeySequence.Paste,
                statusTip="Paste the clipboard's contents into the current selection",
                triggered=self.textEdit.paste)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication.instance().aboutQt)

        self.cutAct.setEnabled(False)
        self.copyAct.setEnabled(False)
        self.textEdit.copyAvailable.connect(self.cutAct.setEnabled)
        self.textEdit.copyAvailable.connect(self.copyAct.setEnabled)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator();
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.cutAct)
        self.editToolBar.addAction(self.copyAct)
        self.editToolBar.addAction(self.pasteAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = QSettings("Trolltech", "Application Example")
        pos = settings.value("pos", QPoint(200, 200))
        size = settings.value("size", QSize(400, 400))
        self.resize(size)
        self.move(pos)

    def writeSettings(self):
        settings = QSettings("Trolltech", "Application Example")
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

    def maybeSave(self):
        if self.textEdit.document().isModified():
            ret = QMessageBox.warning(self, "Application",
                    "The document has been modified.\nDo you want to save "
                    "your changes?",
                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

            if ret == QMessageBox.Save:
                return self.save()

            if ret == QMessageBox.Cancel:
                return False

        return True

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return

        inf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.textEdit.setPlainText(inf.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File loaded", 2000)

    def saveFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False

        outf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outf << self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName);
        self.statusBar().showMessage("File saved", 2000)
        return True

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        self.textEdit.document().setModified(False)
        self.setWindowModified(False)

        if self.curFile:
            shownName = self.strippedName(self.curFile)
        else:
            shownName = 'untitled.txt'

        self.setWindowTitle("%s[*] - Application" % shownName)

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
