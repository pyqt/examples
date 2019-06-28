# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'controller.ui'
#
# Created: Fri May 31 18:58:37 2013
#      by: PyQt5 UI code generator 5.0-snapshot-dd808c1bcced
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Controller(object):
    def setupUi(self, Controller):
        Controller.setObjectName("Controller")
        Controller.resize(255, 111)
        self.gridlayout = QtWidgets.QGridLayout(Controller)
        self.gridlayout.setContentsMargins(9, 9, 9, 9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        self.label = QtWidgets.QLabel(Controller)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 1, 1, 1, 1)
        self.decelerate = QtWidgets.QPushButton(Controller)
        self.decelerate.setObjectName("decelerate")
        self.gridlayout.addWidget(self.decelerate, 2, 1, 1, 1)
        self.accelerate = QtWidgets.QPushButton(Controller)
        self.accelerate.setObjectName("accelerate")
        self.gridlayout.addWidget(self.accelerate, 0, 1, 1, 1)
        self.right = QtWidgets.QPushButton(Controller)
        self.right.setObjectName("right")
        self.gridlayout.addWidget(self.right, 1, 2, 1, 1)
        self.left = QtWidgets.QPushButton(Controller)
        self.left.setObjectName("left")
        self.gridlayout.addWidget(self.left, 1, 0, 1, 1)

        self.retranslateUi(Controller)
        QtCore.QMetaObject.connectSlotsByName(Controller)

    def retranslateUi(self, Controller):
        _translate = QtCore.QCoreApplication.translate
        Controller.setWindowTitle(_translate("Controller", "Controller"))
        self.label.setText(_translate("Controller", "Controller"))
        self.decelerate.setText(_translate("Controller", "Decelerate"))
        self.accelerate.setText(_translate("Controller", "Accelerate"))
        self.right.setText(_translate("Controller", "Right"))
        self.left.setText(_translate("Controller", "Left"))

