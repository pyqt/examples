# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'previewer.ui'
#
# Created: Tue May 14 22:35:29 2013
#      by: PyQt5 UI code generator 5.0-snapshot-3507ed3a4178
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(911, 688)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.editorBox = QtWidgets.QGroupBox(self.splitter)
        self.editorBox.setObjectName("editorBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.editorBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.editorBox)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_2.addWidget(self.plainTextEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.clearButton = QtWidgets.QPushButton(self.editorBox)
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout.addWidget(self.clearButton)
        self.previewButton = QtWidgets.QPushButton(self.editorBox)
        self.previewButton.setObjectName("previewButton")
        self.horizontalLayout.addWidget(self.previewButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.previewerBox = QtWidgets.QGroupBox(self.splitter)
        self.previewerBox.setObjectName("previewerBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.previewerBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.webView = QtWebKitWidgets.QWebView(self.previewerBox)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.horizontalLayout_3.addWidget(self.webView)
        self.horizontalLayout_4.addWidget(self.splitter)

        self.retranslateUi(Form)
        self.clearButton.clicked.connect(self.plainTextEdit.clear)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.editorBox.setTitle(_translate("Form", "HTML Editor"))
        self.clearButton.setText(_translate("Form", "Clear"))
        self.previewButton.setText(_translate("Form", "Preview"))
        self.previewerBox.setTitle(_translate("Form", "HTML Preview"))

from PyQt5 import QtWebKitWidgets
