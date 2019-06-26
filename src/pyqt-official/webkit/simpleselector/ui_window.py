# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created: Tue May 14 22:42:29 2013
#      by: PyQt5 UI code generator 5.0-snapshot-3507ed3a4178
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Window(object):
    def setupUi(self, Window):
        Window.setObjectName("Window")
        Window.resize(640, 480)
        self.verticalLayout = QtWidgets.QVBoxLayout(Window)
        self.verticalLayout.setObjectName("verticalLayout")
        self.webView = QtWebKitWidgets.QWebView(Window)
        self.webView.setUrl(QtCore.QUrl("http://webkit.org/"))
        self.webView.setObjectName("webView")
        self.verticalLayout.addWidget(self.webView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.elementLabel = QtWidgets.QLabel(Window)
        self.elementLabel.setObjectName("elementLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.elementLabel)
        self.elementLineEdit = QtWidgets.QLineEdit(Window)
        self.elementLineEdit.setObjectName("elementLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.elementLineEdit)
        self.horizontalLayout.addLayout(self.formLayout)
        self.highlightButton = QtWidgets.QPushButton(Window)
        self.highlightButton.setObjectName("highlightButton")
        self.horizontalLayout.addWidget(self.highlightButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.elementLabel.setBuddy(self.elementLineEdit)

        self.retranslateUi(Window)
        QtCore.QMetaObject.connectSlotsByName(Window)

    def retranslateUi(self, Window):
        _translate = QtCore.QCoreApplication.translate
        Window.setWindowTitle(_translate("Window", "Web Element Selector"))
        self.elementLabel.setText(_translate("Window", "&Element:"))
        self.elementLineEdit.setText(_translate("Window", "li a"))
        self.highlightButton.setText(_translate("Window", "&Highlight"))

from PyQt5 import QtWebKitWidgets
