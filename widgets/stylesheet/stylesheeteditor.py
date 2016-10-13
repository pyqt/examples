#############################################################################
##
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


from PyQt5.QtCore import pyqtSlot, QFile, QRegExp, Qt, QTextStream
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QMessageBox,
        QStyleFactory)

from ui_stylesheeteditor import Ui_StyleSheetEditor


class StyleSheetEditor(QDialog):
    def __init__(self, parent=None):
        super(StyleSheetEditor, self).__init__(parent)

        self.ui = Ui_StyleSheetEditor()
        self.ui.setupUi(self)

        regExp = QRegExp(r'.(.*)\+?Style')
        defaultStyle = QApplication.style().metaObject().className()
        if regExp.exactMatch(defaultStyle):
            defaultStyle = regExp.cap(1)

        self.ui.styleCombo.addItems(QStyleFactory.keys())
        self.ui.styleCombo.setCurrentIndex(
                self.ui.styleCombo.findText(defaultStyle, Qt.MatchContains))

        self.ui.styleSheetCombo.setCurrentIndex(
                self.ui.styleSheetCombo.findText('Coffee'))

        self.loadStyleSheet('Coffee')

    @pyqtSlot(str)
    def on_styleCombo_activated(self, styleName):
        QApplication.setStyle(styleName)
        self.ui.applyButton.setEnabled(False)

    @pyqtSlot(str)
    def on_styleSheetCombo_activated(self, sheetName):
        self.loadStyleSheet(sheetName)

    def on_styleTextEdit_textChanged(self):
        self.ui.applyButton.setEnabled(True)

    def on_applyButton_clicked(self):
        QApplication.instance().setStyleSheet(
                self.ui.styleTextEdit.toPlainText())
        self.ui.applyButton.setEnabled(False)

    def on_saveButton_clicked(self):
        fileName, _ = QFileDialog.getSaveFileName(self)
        if fileName:
            self.saveStyleSheet(fileName)

    def loadStyleSheet(self, sheetName):
        file = QFile(':/qss/%s.qss' % sheetName.lower())
        file.open(QFile.ReadOnly)

        styleSheet = file.readAll()
        try:
            # Python v2.
            styleSheet = unicode(styleSheet, encoding='utf8')
        except NameError:
            # Python v3.
            styleSheet = str(styleSheet, encoding='utf8')

        self.ui.styleTextEdit.setPlainText(styleSheet)
        QApplication.instance().setStyleSheet(styleSheet)
        self.ui.applyButton.setEnabled(False)

    def saveStyleSheet(self, fileName):
        styleSheet = self.ui.styleTextEdit.toPlainText()
        file = QFile(fileName)
        if file.open(QFile.WriteOnly):
            QTextStream(file) << styleSheet
        else:
            QMessageBox.information(self, "Unable to open file",
                    file.errorString())
