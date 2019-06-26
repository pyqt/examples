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


from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
        QGridLayout, QHBoxLayout, QLabel, QLineEdit, QSizePolicy)


class RegExpDialog(QDialog):
    MaxCaptures = 6

    def __init__(self, parent=None):
        super(RegExpDialog, self).__init__(parent)

        self.patternComboBox = QComboBox()
        self.patternComboBox.setEditable(True)
        self.patternComboBox.setSizePolicy(QSizePolicy.Expanding,
                QSizePolicy.Preferred)

        patternLabel = QLabel("&Pattern:")
        patternLabel.setBuddy(self.patternComboBox)

        self.escapedPatternLineEdit = QLineEdit()
        self.escapedPatternLineEdit.setReadOnly(True)
        palette = self.escapedPatternLineEdit.palette()
        palette.setBrush(QPalette.Base,
                palette.brush(QPalette.Disabled, QPalette.Base))
        self.escapedPatternLineEdit.setPalette(palette)

        escapedPatternLabel = QLabel("&Escaped Pattern:")
        escapedPatternLabel.setBuddy(self.escapedPatternLineEdit)

        self.syntaxComboBox = QComboBox()
        self.syntaxComboBox.addItem("Regular expression v1", QRegExp.RegExp)
        self.syntaxComboBox.addItem("Regular expression v2", QRegExp.RegExp2)
        self.syntaxComboBox.addItem("Wildcard", QRegExp.Wildcard)
        self.syntaxComboBox.addItem("Fixed string", QRegExp.FixedString)

        syntaxLabel = QLabel("&Pattern Syntax:")
        syntaxLabel.setBuddy(self.syntaxComboBox)

        self.textComboBox = QComboBox()
        self.textComboBox.setEditable(True)
        self.textComboBox.setSizePolicy(QSizePolicy.Expanding,
                QSizePolicy.Preferred)

        textLabel = QLabel("&Text:")
        textLabel.setBuddy(self.textComboBox)

        self.caseSensitiveCheckBox = QCheckBox("Case &Sensitive")
        self.caseSensitiveCheckBox.setChecked(True)
        self.minimalCheckBox = QCheckBox("&Minimal")

        indexLabel = QLabel("Index of Match:")
        self.indexEdit = QLineEdit()
        self.indexEdit.setReadOnly(True)

        matchedLengthLabel = QLabel("Matched Length:")
        self.matchedLengthEdit = QLineEdit()
        self.matchedLengthEdit.setReadOnly(True)

        self.captureLabels = []
        self.captureEdits = []
        for i in range(self.MaxCaptures):
            self.captureLabels.append(QLabel("Capture %d:" % i))
            self.captureEdits.append(QLineEdit())
            self.captureEdits[i].setReadOnly(True)
        self.captureLabels[0].setText("Match:")

        checkBoxLayout = QHBoxLayout()
        checkBoxLayout.addWidget(self.caseSensitiveCheckBox)
        checkBoxLayout.addWidget(self.minimalCheckBox)
        checkBoxLayout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addWidget(patternLabel, 0, 0)
        mainLayout.addWidget(self.patternComboBox, 0, 1)
        mainLayout.addWidget(escapedPatternLabel, 1, 0)
        mainLayout.addWidget(self.escapedPatternLineEdit, 1, 1)
        mainLayout.addWidget(syntaxLabel, 2, 0)
        mainLayout.addWidget(self.syntaxComboBox, 2, 1)
        mainLayout.addLayout(checkBoxLayout, 3, 0, 1, 2)
        mainLayout.addWidget(textLabel, 4, 0)
        mainLayout.addWidget(self.textComboBox, 4, 1)
        mainLayout.addWidget(indexLabel, 5, 0)
        mainLayout.addWidget(self.indexEdit, 5, 1)
        mainLayout.addWidget(matchedLengthLabel, 6, 0)
        mainLayout.addWidget(self.matchedLengthEdit, 6, 1)

        for i in range(self.MaxCaptures):
            mainLayout.addWidget(self.captureLabels[i], 7 + i, 0)
            mainLayout.addWidget(self.captureEdits[i], 7 + i, 1)
        self.setLayout(mainLayout)

        self.patternComboBox.editTextChanged.connect(self.refresh)
        self.textComboBox.editTextChanged.connect(self.refresh)
        self.caseSensitiveCheckBox.toggled.connect(self.refresh)
        self.minimalCheckBox.toggled.connect(self.refresh)
        self.syntaxComboBox.currentIndexChanged.connect(self.refresh)

        self.patternComboBox.addItem("[A-Za-z_]+([A-Za-z_0-9]*)")
        self.textComboBox.addItem("(10 + delta4)* 32")

        self.setWindowTitle("RegExp")
        self.setFixedHeight(self.sizeHint().height())
        self.refresh()

    def refresh(self):
        self.setUpdatesEnabled(False)

        pattern = self.patternComboBox.currentText()
        text = self.textComboBox.currentText()

        escaped = str(pattern)
        escaped.replace('\\', '\\\\')
        escaped.replace('"', '\\"')
        self.escapedPatternLineEdit.setText('"' + escaped + '"')

        rx = QRegExp(pattern)
        cs = Qt.CaseSensitive if self.caseSensitiveCheckBox.isChecked() else Qt.CaseInsensitive
        rx.setCaseSensitivity(cs)
        rx.setMinimal(self.minimalCheckBox.isChecked())
        syntax = self.syntaxComboBox.itemData(self.syntaxComboBox.currentIndex())
        rx.setPatternSyntax(syntax)

        palette = self.patternComboBox.palette()
        if rx.isValid():
            palette.setColor(QPalette.Text,
                    self.textComboBox.palette().color(QPalette.Text))
        else:
            palette.setColor(QPalette.Text, Qt.red)
        self.patternComboBox.setPalette(palette)

        self.indexEdit.setText(str(rx.indexIn(text)))
        self.matchedLengthEdit.setText(str(rx.matchedLength()))

        for i in range(self.MaxCaptures):
            self.captureLabels[i].setEnabled(i <= rx.captureCount())
            self.captureEdits[i].setEnabled(i <= rx.captureCount())
            self.captureEdits[i].setText(rx.cap(i))

        self.setUpdatesEnabled(True)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    dialog = RegExpDialog()
    dialog.show()
    sys.exit(app.exec_())
