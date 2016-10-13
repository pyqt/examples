# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'embeddeddialog.ui'
#
# Created: Wed May 15 16:13:29 2013
#      by: PyQt5 UI code generator 5.0-snapshot-8d430da208a7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_embeddedDialog(object):
    def setupUi(self, embeddedDialog):
        embeddedDialog.setObjectName("embeddedDialog")
        embeddedDialog.resize(407, 134)
        self.formLayout = QtWidgets.QFormLayout(embeddedDialog)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(embeddedDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.layoutDirection = QtWidgets.QComboBox(embeddedDialog)
        self.layoutDirection.setObjectName("layoutDirection")
        self.layoutDirection.addItem("")
        self.layoutDirection.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.layoutDirection)
        self.label_2 = QtWidgets.QLabel(embeddedDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.fontComboBox = QtWidgets.QFontComboBox(embeddedDialog)
        self.fontComboBox.setObjectName("fontComboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.fontComboBox)
        self.label_3 = QtWidgets.QLabel(embeddedDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.style = QtWidgets.QComboBox(embeddedDialog)
        self.style.setObjectName("style")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.style)
        self.label_4 = QtWidgets.QLabel(embeddedDialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.spacing = QtWidgets.QSlider(embeddedDialog)
        self.spacing.setOrientation(QtCore.Qt.Horizontal)
        self.spacing.setObjectName("spacing")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spacing)
        self.label.setBuddy(self.layoutDirection)
        self.label_2.setBuddy(self.fontComboBox)
        self.label_3.setBuddy(self.style)
        self.label_4.setBuddy(self.spacing)

        self.retranslateUi(embeddedDialog)
        QtCore.QMetaObject.connectSlotsByName(embeddedDialog)

    def retranslateUi(self, embeddedDialog):
        _translate = QtCore.QCoreApplication.translate
        embeddedDialog.setWindowTitle(_translate("embeddedDialog", "Embedded Dialog"))
        self.label.setText(_translate("embeddedDialog", "Layout Direction:"))
        self.layoutDirection.setItemText(0, _translate("embeddedDialog", "Left to Right"))
        self.layoutDirection.setItemText(1, _translate("embeddedDialog", "Right to Left"))
        self.label_2.setText(_translate("embeddedDialog", "Select Font:"))
        self.label_3.setText(_translate("embeddedDialog", "Style:"))
        self.label_4.setText(_translate("embeddedDialog", "Layout spacing:"))

