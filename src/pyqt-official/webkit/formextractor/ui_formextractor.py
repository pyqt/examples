# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formextractor.ui'
#
# Created: Tue May 14 17:59:08 2013
#      by: PyQt5 UI code generator 5.0-snapshot-b0831183bf83
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(680, 218)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.webFormGroupBox = QtWidgets.QGroupBox(Form)
        self.webFormGroupBox.setObjectName("webFormGroupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.webFormGroupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.webView = QtWebKitWidgets.QWebView(self.webFormGroupBox)
        self.webView.setMinimumSize(QtCore.QSize(200, 150))
        self.webView.setMaximumSize(QtCore.QSize(400, 16777215))
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.verticalLayout.addWidget(self.webView)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout.addWidget(self.webFormGroupBox)
        spacerItem = QtWidgets.QSpacerItem(28, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.dataGroupBox = QtWidgets.QGroupBox(Form)
        self.dataGroupBox.setObjectName("dataGroupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dataGroupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setObjectName("formLayout")
        self.firstNameLabel = QtWidgets.QLabel(self.dataGroupBox)
        self.firstNameLabel.setObjectName("firstNameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.firstNameLabel)
        self.firstNameEdit = QtWidgets.QLineEdit(self.dataGroupBox)
        self.firstNameEdit.setReadOnly(True)
        self.firstNameEdit.setObjectName("firstNameEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.firstNameEdit)
        self.lastNameLabel = QtWidgets.QLabel(self.dataGroupBox)
        self.lastNameLabel.setObjectName("lastNameLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lastNameLabel)
        self.lastNameEdit = QtWidgets.QLineEdit(self.dataGroupBox)
        self.lastNameEdit.setReadOnly(True)
        self.lastNameEdit.setObjectName("lastNameEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lastNameEdit)
        self.genderLabel = QtWidgets.QLabel(self.dataGroupBox)
        self.genderLabel.setObjectName("genderLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.genderLabel)
        self.genderEdit = QtWidgets.QLineEdit(self.dataGroupBox)
        self.genderEdit.setReadOnly(True)
        self.genderEdit.setObjectName("genderEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.genderEdit)
        self.updatesLabel = QtWidgets.QLabel(self.dataGroupBox)
        self.updatesLabel.setObjectName("updatesLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.updatesLabel)
        self.updatesEdit = QtWidgets.QLineEdit(self.dataGroupBox)
        self.updatesEdit.setReadOnly(True)
        self.updatesEdit.setObjectName("updatesEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.updatesEdit)
        self.verticalLayout_3.addLayout(self.formLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 24, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.dataGroupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.webFormGroupBox.setTitle(_translate("Form", "Web Form"))
        self.dataGroupBox.setTitle(_translate("Form", "Extracted Data"))
        self.firstNameLabel.setText(_translate("Form", "First Name"))
        self.lastNameLabel.setText(_translate("Form", "Last Name"))
        self.genderLabel.setText(_translate("Form", "Gender"))
        self.updatesLabel.setText(_translate("Form", "Receive Updates"))

from PyQt5 import QtWebKitWidgets
