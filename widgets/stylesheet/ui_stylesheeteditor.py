# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stylesheeteditor.ui'
#
# Created: Fri Jul 26 06:50:07 2013
#      by: PyQt5 UI code generator 5.0.1-snapshot-2a99e59669ee
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StyleSheetEditor(object):
    def setupUi(self, StyleSheetEditor):
        StyleSheetEditor.setObjectName("StyleSheetEditor")
        StyleSheetEditor.resize(445, 289)
        self.gridlayout = QtWidgets.QGridLayout(StyleSheetEditor)
        self.gridlayout.setContentsMargins(9, 9, 9, 9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        spacerItem = QtWidgets.QSpacerItem(32, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 0, 6, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(32, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 0, 0, 1, 1)
        self.styleSheetCombo = QtWidgets.QComboBox(StyleSheetEditor)
        self.styleSheetCombo.setObjectName("styleSheetCombo")
        self.styleSheetCombo.addItem("")
        self.styleSheetCombo.addItem("")
        self.styleSheetCombo.addItem("")
        self.gridlayout.addWidget(self.styleSheetCombo, 0, 5, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(10, 16, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2, 0, 3, 1, 1)
        self.styleCombo = QtWidgets.QComboBox(StyleSheetEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.styleCombo.sizePolicy().hasHeightForWidth())
        self.styleCombo.setSizePolicy(sizePolicy)
        self.styleCombo.setObjectName("styleCombo")
        self.gridlayout.addWidget(self.styleCombo, 0, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(StyleSheetEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.gridlayout.addWidget(self.label_7, 0, 1, 1, 1)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem3 = QtWidgets.QSpacerItem(321, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem3)
        self.saveButton = QtWidgets.QPushButton(StyleSheetEditor)
        self.saveButton.setEnabled(True)
        self.saveButton.setObjectName("saveButton")
        self.hboxlayout.addWidget(self.saveButton)
        self.applyButton = QtWidgets.QPushButton(StyleSheetEditor)
        self.applyButton.setEnabled(False)
        self.applyButton.setObjectName("applyButton")
        self.hboxlayout.addWidget(self.applyButton)
        self.gridlayout.addLayout(self.hboxlayout, 2, 0, 1, 7)
        self.styleTextEdit = QtWidgets.QTextEdit(StyleSheetEditor)
        self.styleTextEdit.setObjectName("styleTextEdit")
        self.gridlayout.addWidget(self.styleTextEdit, 1, 0, 1, 7)
        self.label_8 = QtWidgets.QLabel(StyleSheetEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.gridlayout.addWidget(self.label_8, 0, 4, 1, 1)

        self.retranslateUi(StyleSheetEditor)
        QtCore.QMetaObject.connectSlotsByName(StyleSheetEditor)

    def retranslateUi(self, StyleSheetEditor):
        _translate = QtCore.QCoreApplication.translate
        StyleSheetEditor.setWindowTitle(_translate("StyleSheetEditor", "Style Editor"))
        self.styleSheetCombo.setItemText(0, _translate("StyleSheetEditor", "Default"))
        self.styleSheetCombo.setItemText(1, _translate("StyleSheetEditor", "Coffee"))
        self.styleSheetCombo.setItemText(2, _translate("StyleSheetEditor", "Pagefold"))
        self.label_7.setText(_translate("StyleSheetEditor", "Style:"))
        self.saveButton.setText(_translate("StyleSheetEditor", "&Save"))
        self.applyButton.setText(_translate("StyleSheetEditor", "&Apply"))
        self.label_8.setText(_translate("StyleSheetEditor", "Style Sheet:"))

