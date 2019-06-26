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


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
        QLabel, QLineEdit, QWidget)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        echoGroup = QGroupBox("Echo")

        echoLabel = QLabel("Mode:")
        echoComboBox = QComboBox()
        echoComboBox.addItem("Normal")
        echoComboBox.addItem("Password")
        echoComboBox.addItem("PasswordEchoOnEdit")
        echoComboBox.addItem("No Echo")

        self.echoLineEdit = QLineEdit()
        self.echoLineEdit.setFocus()

        validatorGroup = QGroupBox("Validator")

        validatorLabel = QLabel("Type:")
        validatorComboBox = QComboBox()
        validatorComboBox.addItem("No validator")
        validatorComboBox.addItem("Integer validator")
        validatorComboBox.addItem("Double validator")

        self.validatorLineEdit = QLineEdit()

        alignmentGroup = QGroupBox("Alignment")

        alignmentLabel = QLabel("Type:")
        alignmentComboBox = QComboBox()
        alignmentComboBox.addItem("Left")
        alignmentComboBox.addItem("Centered")
        alignmentComboBox.addItem("Right")

        self.alignmentLineEdit = QLineEdit()

        inputMaskGroup = QGroupBox("Input mask")

        inputMaskLabel = QLabel("Type:")
        inputMaskComboBox = QComboBox()
        inputMaskComboBox.addItem("No mask")
        inputMaskComboBox.addItem("Phone number")
        inputMaskComboBox.addItem("ISO date")
        inputMaskComboBox.addItem("License key")

        self.inputMaskLineEdit = QLineEdit()

        accessGroup = QGroupBox("Access")

        accessLabel = QLabel("Read-only:")
        accessComboBox = QComboBox()
        accessComboBox.addItem("False")
        accessComboBox.addItem("True")

        self.accessLineEdit = QLineEdit()

        echoComboBox.activated.connect(self.echoChanged)
        validatorComboBox.activated.connect(self.validatorChanged)
        alignmentComboBox.activated.connect(self.alignmentChanged)
        inputMaskComboBox.activated.connect(self.inputMaskChanged)
        accessComboBox.activated.connect(self.accessChanged)

        echoLayout = QGridLayout()
        echoLayout.addWidget(echoLabel, 0, 0)
        echoLayout.addWidget(echoComboBox, 0, 1)
        echoLayout.addWidget(self.echoLineEdit, 1, 0, 1, 2)
        echoGroup.setLayout(echoLayout)

        validatorLayout = QGridLayout()
        validatorLayout.addWidget(validatorLabel, 0, 0)
        validatorLayout.addWidget(validatorComboBox, 0, 1)
        validatorLayout.addWidget(self.validatorLineEdit, 1, 0, 1, 2)
        validatorGroup.setLayout(validatorLayout)

        alignmentLayout = QGridLayout()
        alignmentLayout.addWidget(alignmentLabel, 0, 0)
        alignmentLayout.addWidget(alignmentComboBox, 0, 1)
        alignmentLayout.addWidget(self.alignmentLineEdit, 1, 0, 1, 2)
        alignmentGroup. setLayout(alignmentLayout)

        inputMaskLayout = QGridLayout()
        inputMaskLayout.addWidget(inputMaskLabel, 0, 0)
        inputMaskLayout.addWidget(inputMaskComboBox, 0, 1)
        inputMaskLayout.addWidget(self.inputMaskLineEdit, 1, 0, 1, 2)
        inputMaskGroup.setLayout(inputMaskLayout)

        accessLayout = QGridLayout()
        accessLayout.addWidget(accessLabel, 0, 0)
        accessLayout.addWidget(accessComboBox, 0, 1)
        accessLayout.addWidget(self.accessLineEdit, 1, 0, 1, 2)
        accessGroup.setLayout(accessLayout)

        layout = QGridLayout()
        layout.addWidget(echoGroup, 0, 0)
        layout.addWidget(validatorGroup, 1, 0)
        layout.addWidget(alignmentGroup, 2, 0)
        layout.addWidget(inputMaskGroup, 0, 1)
        layout.addWidget(accessGroup, 1, 1)
        self.setLayout(layout)

        self.setWindowTitle("Line Edits")

    def echoChanged(self, index):
        if index == 0:
            self.echoLineEdit.setEchoMode(QLineEdit.Normal)
        elif index == 1:
            self.echoLineEdit.setEchoMode(QLineEdit.Password)
        elif index == 2:
            self.echoLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        elif index == 3:
    	    self.echoLineEdit.setEchoMode(QLineEdit.NoEcho)

    def validatorChanged(self, index):
        if index == 0:
            self.validatorLineEdit.setValidator(0)
        elif index == 1:
            self.validatorLineEdit.setValidator(QIntValidator(self.validatorLineEdit))
        elif index == 2:
            self.validatorLineEdit.setValidator(QDoubleValidator(-999.0, 999.0, 2, self.validatorLineEdit))

        self.validatorLineEdit.clear()

    def alignmentChanged(self, index):
        if index == 0:
            self.alignmentLineEdit.setAlignment(Qt.AlignLeft)
        elif index == 1:
            self.alignmentLineEdit.setAlignment(Qt.AlignCenter)
        elif index == 2:
    	    self.alignmentLineEdit.setAlignment(Qt.AlignRight)

    def inputMaskChanged(self, index):
        if index == 0:
            self.inputMaskLineEdit.setInputMask('')
        elif index == 1:
            self.inputMaskLineEdit.setInputMask('+99 99 99 99 99;_')
        elif index == 2:
            self.inputMaskLineEdit.setInputMask('0000-00-00')
            self.inputMaskLineEdit.setText('00000000')
            self.inputMaskLineEdit.setCursorPosition(0)
        elif index == 3:
            self.inputMaskLineEdit.setInputMask('>AAAAA-AAAAA-AAAAA-AAAAA-AAAAA;#')

    def accessChanged(self, index):
        if index == 0:
            self.accessLineEdit.setReadOnly(False)
        elif index == 1:
            self.accessLineEdit.setReadOnly(True)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
