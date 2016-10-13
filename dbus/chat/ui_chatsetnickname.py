# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatsetnickname.ui'
#
# Created: Fri Jul 26 06:48:20 2013
#      by: PyQt5 UI code generator 5.0.1-snapshot-2a99e59669ee
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NicknameDialog(object):
    def setupUi(self, NicknameDialog):
        NicknameDialog.setObjectName("NicknameDialog")
        NicknameDialog.resize(396, 105)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy(1), QtWidgets.QSizePolicy.Policy(1))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NicknameDialog.sizePolicy().hasHeightForWidth())
        NicknameDialog.setSizePolicy(sizePolicy)
        self.vboxlayout = QtWidgets.QVBoxLayout(NicknameDialog)
        self.vboxlayout.setContentsMargins(9, 9, 9, 9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.vboxlayout1 = QtWidgets.QVBoxLayout()
        self.vboxlayout1.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.label = QtWidgets.QLabel(NicknameDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy(1), QtWidgets.QSizePolicy.Policy(1))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)
        self.nickname = QtWidgets.QLineEdit(NicknameDialog)
        self.nickname.setObjectName("nickname")
        self.vboxlayout1.addWidget(self.nickname)
        self.vboxlayout.addLayout(self.vboxlayout1)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtWidgets.QSpacerItem(131, 31, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.okButton = QtWidgets.QPushButton(NicknameDialog)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(NicknameDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout.addWidget(self.cancelButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(NicknameDialog)
        self.okButton.clicked.connect(NicknameDialog.accept)
        self.cancelButton.clicked.connect(NicknameDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NicknameDialog)

    def retranslateUi(self, NicknameDialog):
        _translate = QtCore.QCoreApplication.translate
        NicknameDialog.setWindowTitle(_translate("NicknameDialog", "Set nickname"))
        self.label.setText(_translate("NicknameDialog", "New nickname:"))
        self.okButton.setText(_translate("NicknameDialog", "OK"))
        self.cancelButton.setText(_translate("NicknameDialog", "Cancel"))

