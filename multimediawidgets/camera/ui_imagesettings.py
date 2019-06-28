# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imagesettings.ui'
#
# Created: Fri Jun 28 11:48:28 2013
#      by: PyQt5 UI code generator 5.0-snapshot-478d7f271b71
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImageSettingsUi(object):
    def setupUi(self, ImageSettingsUi):
        ImageSettingsUi.setObjectName("ImageSettingsUi")
        ImageSettingsUi.resize(332, 270)
        self.gridLayout = QtWidgets.QGridLayout(ImageSettingsUi)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(ImageSettingsUi)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 0, 0, 1, 2)
        self.imageResolutionBox = QtWidgets.QComboBox(self.groupBox_2)
        self.imageResolutionBox.setObjectName("imageResolutionBox")
        self.gridLayout_2.addWidget(self.imageResolutionBox, 1, 0, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 2)
        self.imageCodecBox = QtWidgets.QComboBox(self.groupBox_2)
        self.imageCodecBox.setObjectName("imageCodecBox")
        self.gridLayout_2.addWidget(self.imageCodecBox, 3, 0, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)
        self.imageQualitySlider = QtWidgets.QSlider(self.groupBox_2)
        self.imageQualitySlider.setMaximum(4)
        self.imageQualitySlider.setOrientation(QtCore.Qt.Horizontal)
        self.imageQualitySlider.setObjectName("imageQualitySlider")
        self.gridLayout_2.addWidget(self.imageQualitySlider, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 14, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ImageSettingsUi)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(ImageSettingsUi)
        self.buttonBox.accepted.connect(ImageSettingsUi.accept)
        self.buttonBox.rejected.connect(ImageSettingsUi.reject)
        QtCore.QMetaObject.connectSlotsByName(ImageSettingsUi)

    def retranslateUi(self, ImageSettingsUi):
        _translate = QtCore.QCoreApplication.translate
        ImageSettingsUi.setWindowTitle(_translate("ImageSettingsUi", "Dialog"))
        self.groupBox_2.setTitle(_translate("ImageSettingsUi", "Image"))
        self.label_8.setText(_translate("ImageSettingsUi", "Resolution:"))
        self.label_6.setText(_translate("ImageSettingsUi", "Image Format:"))
        self.label_7.setText(_translate("ImageSettingsUi", "Quality:"))

