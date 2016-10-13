# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Fri Jul 26 06:51:23 2013
#      by: PyQt5 UI code generator 5.0.1-snapshot-2a99e59669ee
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(573, 468)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setObjectName("vboxlayout")
        self.view = QtWidgets.QTreeView(self.centralwidget)
        self.view.setAlternatingRowColors(True)
        self.view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.view.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.view.setAnimated(False)
        self.view.setAllColumnsShowFocus(True)
        self.view.setObjectName("view")
        self.vboxlayout.addWidget(self.view)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 573, 31))
        self.menubar.setObjectName("menubar")
        self.fileMenu = QtWidgets.QMenu(self.menubar)
        self.fileMenu.setObjectName("fileMenu")
        self.actionsMenu = QtWidgets.QMenu(self.menubar)
        self.actionsMenu.setObjectName("actionsMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.exitAction = QtWidgets.QAction(MainWindow)
        self.exitAction.setObjectName("exitAction")
        self.insertRowAction = QtWidgets.QAction(MainWindow)
        self.insertRowAction.setObjectName("insertRowAction")
        self.removeRowAction = QtWidgets.QAction(MainWindow)
        self.removeRowAction.setObjectName("removeRowAction")
        self.insertColumnAction = QtWidgets.QAction(MainWindow)
        self.insertColumnAction.setObjectName("insertColumnAction")
        self.removeColumnAction = QtWidgets.QAction(MainWindow)
        self.removeColumnAction.setObjectName("removeColumnAction")
        self.insertChildAction = QtWidgets.QAction(MainWindow)
        self.insertChildAction.setObjectName("insertChildAction")
        self.fileMenu.addAction(self.exitAction)
        self.actionsMenu.addAction(self.insertRowAction)
        self.actionsMenu.addAction(self.insertColumnAction)
        self.actionsMenu.addSeparator()
        self.actionsMenu.addAction(self.removeRowAction)
        self.actionsMenu.addAction(self.removeColumnAction)
        self.actionsMenu.addSeparator()
        self.actionsMenu.addAction(self.insertChildAction)
        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.actionsMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Editable Tree Model"))
        self.fileMenu.setTitle(_translate("MainWindow", "&File"))
        self.actionsMenu.setTitle(_translate("MainWindow", "&Actions"))
        self.exitAction.setText(_translate("MainWindow", "E&xit"))
        self.exitAction.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.insertRowAction.setText(_translate("MainWindow", "Insert Row"))
        self.insertRowAction.setShortcut(_translate("MainWindow", "Ctrl+I, R"))
        self.removeRowAction.setText(_translate("MainWindow", "Remove Row"))
        self.removeRowAction.setShortcut(_translate("MainWindow", "Ctrl+R, R"))
        self.insertColumnAction.setText(_translate("MainWindow", "Insert Column"))
        self.insertColumnAction.setShortcut(_translate("MainWindow", "Ctrl+I, C"))
        self.removeColumnAction.setText(_translate("MainWindow", "Remove Column"))
        self.removeColumnAction.setShortcut(_translate("MainWindow", "Ctrl+R, C"))
        self.insertChildAction.setText(_translate("MainWindow", "Insert Child"))
        self.insertChildAction.setShortcut(_translate("MainWindow", "Ctrl+N"))

