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


from PyQt5.QtCore import QFileInfo, QRegExp, QSize, Qt
from PyQt5.QtGui import QIcon, QImage, QPalette, QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QActionGroup,
        QApplication, QComboBox, QFileDialog, QFrame, QGridLayout, QGroupBox,
        QHBoxLayout, QHeaderView, QItemDelegate, QLabel, QMainWindow,
        QMessageBox, QRadioButton, QSizePolicy, QSpinBox, QStyle,
        QStyleFactory, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)


class IconSizeSpinBox(QSpinBox):
    @staticmethod
    def valueFromText(text):
        regExp = QRegExp("(\\d+)(\\s*[xx]\\s*\\d+)?")

        if regExp.exactMatch(text):
            return int(regExp.cap(1))
        else:
            return 0

    @staticmethod
    def textFromValue(value):
        return "%d x %d" % (value, value)


class ImageDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        comboBox = QComboBox(parent)
        if index.column() == 1:
            comboBox.addItem("Normal")
            comboBox.addItem("Active")
            comboBox.addItem("Disabled")
            comboBox.addItem("Selected")
        elif index.column() == 2:
            comboBox.addItem("Off")
            comboBox.addItem("On")

        comboBox.activated.connect(self.emitCommitData)

        return comboBox

    def setEditorData(self, editor, index):
        comboBox = editor
        if not comboBox:
            return

        pos = comboBox.findText(index.model().data(index), Qt.MatchExactly)
        comboBox.setCurrentIndex(pos)

    def setModelData(self, editor, model, index):
        comboBox = editor
        if not comboBox:
            return

        model.setData(index, comboBox.currentText())

    def emitCommitData(self):
        self.commitData.emit(self.sender())


class IconPreviewArea(QWidget):
    def __init__(self, parent=None):
        super(IconPreviewArea, self).__init__(parent)

        mainLayout = QGridLayout()
        self.setLayout(mainLayout)

        self.icon = QIcon()
        self.size = QSize()
        self.stateLabels = []
        self.modeLabels = []
        self.pixmapLabels = []

        self.stateLabels.append(self.createHeaderLabel("Off"))
        self.stateLabels.append(self.createHeaderLabel("On"))

        self.modeLabels.append(self.createHeaderLabel("Normal"))
        self.modeLabels.append(self.createHeaderLabel("Active"))
        self.modeLabels.append(self.createHeaderLabel("Disabled"))
        self.modeLabels.append(self.createHeaderLabel("Selected"))

        for j, label in enumerate(self.stateLabels):
            mainLayout.addWidget(label, j + 1, 0)

        for i, label in enumerate(self.modeLabels):
            mainLayout.addWidget(label, 0, i + 1)

            self.pixmapLabels.append([])
            for j in range(len(self.stateLabels)):
                self.pixmapLabels[i].append(self.createPixmapLabel())
                mainLayout.addWidget(self.pixmapLabels[i][j], j + 1, i + 1)

    def setIcon(self, icon):
        self.icon = icon
        self.updatePixmapLabels()

    def setSize(self, size):
        if size != self.size:
            self.size = size
            self.updatePixmapLabels()

    def createHeaderLabel(self, text):
        label = QLabel("<b>%s</b>" % text)
        label.setAlignment(Qt.AlignCenter)
        return label

    def createPixmapLabel(self):
        label = QLabel()
        label.setEnabled(False)
        label.setAlignment(Qt.AlignCenter)
        label.setFrameShape(QFrame.Box)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setBackgroundRole(QPalette.Base)
        label.setAutoFillBackground(True)
        label.setMinimumSize(132, 132)
        return label

    def updatePixmapLabels(self):
        for i in range(len(self.modeLabels)):
            if i == 0:
                mode = QIcon.Normal
            elif i == 1:
                mode = QIcon.Active
            elif i == 2:
                mode = QIcon.Disabled
            else:
                mode = QIcon.Selected

            for j in range(len(self.stateLabels)):
                state = QIcon.Off if j == 0 else QIcon.On
                pixmap = self.icon.pixmap(self.size, mode, state)
                self.pixmapLabels[i][j].setPixmap(pixmap)
                self.pixmapLabels[i][j].setEnabled(not pixmap.isNull())


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.createPreviewGroupBox()
        self.createImagesGroupBox()
        self.createIconSizeGroupBox()

        self.createActions()
        self.createMenus()
        self.createContextMenu()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.previewGroupBox, 0, 0, 1, 2)
        mainLayout.addWidget(self.imagesGroupBox, 1, 0)
        mainLayout.addWidget(self.iconSizeGroupBox, 1, 1)
        self.centralWidget.setLayout(mainLayout)

        self.setWindowTitle("Icons")
        self.checkCurrentStyle()
        self.otherRadioButton.click()

        self.resize(self.minimumSizeHint())

    def about(self):
        QMessageBox.about(self, "About Icons",
                "The <b>Icons</b> example illustrates how Qt renders an icon "
                "in different modes (active, normal, disabled and selected) "
                "and states (on and off) based on a set of images.")

    def changeStyle(self, checked):
        if not checked:
            return

        action = self.sender()
        style = QStyleFactory.create(action.data())
        if not style:
            return

        QApplication.setStyle(style)

        self.setButtonText(self.smallRadioButton, "Small (%d x %d)",
                style, QStyle.PM_SmallIconSize)
        self.setButtonText(self.largeRadioButton, "Large (%d x %d)",
                style, QStyle.PM_LargeIconSize)
        self.setButtonText(self.toolBarRadioButton, "Toolbars (%d x %d)",
                style, QStyle.PM_ToolBarIconSize)
        self.setButtonText(self.listViewRadioButton, "List views (%d x %d)",
                style, QStyle.PM_ListViewIconSize)
        self.setButtonText(self.iconViewRadioButton, "Icon views (%d x %d)",
                style, QStyle.PM_IconViewIconSize)
        self.setButtonText(self.tabBarRadioButton, "Tab bars (%d x %d)",
                style, QStyle.PM_TabBarIconSize)

        self.changeSize()

    @staticmethod
    def setButtonText(button, label, style, metric):
        metric_value = style.pixelMetric(metric)
        button.setText(label % (metric_value, metric_value))

    def changeSize(self, checked=True):
        if not checked:
            return

        if self.otherRadioButton.isChecked():
            extent = self.otherSpinBox.value()
        else:
            if self.smallRadioButton.isChecked():
                metric = QStyle.PM_SmallIconSize
            elif self.largeRadioButton.isChecked():
                metric = QStyle.PM_LargeIconSize
            elif self.toolBarRadioButton.isChecked():
                metric = QStyle.PM_ToolBarIconSize
            elif self.listViewRadioButton.isChecked():
                metric = QStyle.PM_ListViewIconSize
            elif self.iconViewRadioButton.isChecked():
                metric = QStyle.PM_IconViewIconSize
            else:
                metric = QStyle.PM_TabBarIconSize

            extent = QApplication.style().pixelMetric(metric)

        self.previewArea.setSize(QSize(extent, extent))
        self.otherSpinBox.setEnabled(self.otherRadioButton.isChecked())

    def changeIcon(self):
        icon = QIcon()

        for row in range(self.imagesTable.rowCount()):
            item0 = self.imagesTable.item(row, 0)
            item1 = self.imagesTable.item(row, 1)
            item2 = self.imagesTable.item(row, 2)

            if item0.checkState() == Qt.Checked:
                if item1.text() == "Normal":
                    mode = QIcon.Normal
                elif item1.text() == "Active":
                    mode = QIcon.Active
                elif item1.text() == "Disabled":
                    mode = QIcon.Disabled
                else:
                    mode = QIcon.Selected

                if item2.text() == "On":
                    state = QIcon.On
                else:
                    state = QIcon.Off

                fileName = item0.data(Qt.UserRole)
                image = QImage(fileName)
                if not image.isNull():
                    icon.addPixmap(QPixmap.fromImage(image), mode, state)

        self.previewArea.setIcon(icon)

    def addImage(self):
        fileNames, _ = QFileDialog.getOpenFileNames(self, "Open Images", '',
                "Images (*.png *.xpm *.jpg);;All Files (*)")

        for fileName in fileNames:
            row = self.imagesTable.rowCount()
            self.imagesTable.setRowCount(row + 1)

            imageName = QFileInfo(fileName).baseName()
            item0 = QTableWidgetItem(imageName)
            item0.setData(Qt.UserRole, fileName)
            item0.setFlags(item0.flags() & ~Qt.ItemIsEditable)

            item1 = QTableWidgetItem("Normal")
            item2 = QTableWidgetItem("Off")

            if self.guessModeStateAct.isChecked():
                if '_act' in fileName:
                    item1.setText("Active")
                elif '_dis' in fileName:
                    item1.setText("Disabled")
                elif '_sel' in fileName:
                    item1.setText("Selected")

                if '_on' in fileName:
                    item2.setText("On")

            self.imagesTable.setItem(row, 0, item0)
            self.imagesTable.setItem(row, 1, item1)
            self.imagesTable.setItem(row, 2, item2)
            self.imagesTable.openPersistentEditor(item1)
            self.imagesTable.openPersistentEditor(item2)

            item0.setCheckState(Qt.Checked)

    def removeAllImages(self):
        self.imagesTable.setRowCount(0)
        self.changeIcon()

    def createPreviewGroupBox(self):
        self.previewGroupBox = QGroupBox("Preview")

        self.previewArea = IconPreviewArea()

        layout = QVBoxLayout()
        layout.addWidget(self.previewArea)
        self.previewGroupBox.setLayout(layout)

    def createImagesGroupBox(self):
        self.imagesGroupBox = QGroupBox("Images")

        self.imagesTable = QTableWidget()
        self.imagesTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.imagesTable.setItemDelegate(ImageDelegate(self))

        self.imagesTable.horizontalHeader().setDefaultSectionSize(90)
        self.imagesTable.setColumnCount(3)
        self.imagesTable.setHorizontalHeaderLabels(("Image", "Mode", "State"))
        self.imagesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.imagesTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.imagesTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.imagesTable.verticalHeader().hide()

        self.imagesTable.itemChanged.connect(self.changeIcon)

        layout = QVBoxLayout()
        layout.addWidget(self.imagesTable)
        self.imagesGroupBox.setLayout(layout)

    def createIconSizeGroupBox(self):
        self.iconSizeGroupBox = QGroupBox("Icon Size")

        self.smallRadioButton = QRadioButton()
        self.largeRadioButton = QRadioButton()
        self.toolBarRadioButton = QRadioButton()
        self.listViewRadioButton = QRadioButton()
        self.iconViewRadioButton = QRadioButton()
        self.tabBarRadioButton = QRadioButton()
        self.otherRadioButton = QRadioButton("Other:")

        self.otherSpinBox = IconSizeSpinBox()
        self.otherSpinBox.setRange(8, 128)
        self.otherSpinBox.setValue(64)

        self.smallRadioButton.toggled.connect(self.changeSize)
        self.largeRadioButton.toggled.connect(self.changeSize)
        self.toolBarRadioButton.toggled.connect(self.changeSize)
        self.listViewRadioButton.toggled.connect(self.changeSize)
        self.iconViewRadioButton.toggled.connect(self.changeSize)
        self.tabBarRadioButton.toggled.connect(self.changeSize)
        self.otherRadioButton.toggled.connect(self.changeSize)
        self.otherSpinBox.valueChanged.connect(self.changeSize)

        otherSizeLayout = QHBoxLayout()
        otherSizeLayout.addWidget(self.otherRadioButton)
        otherSizeLayout.addWidget(self.otherSpinBox)
        otherSizeLayout.addStretch()

        layout = QGridLayout()
        layout.addWidget(self.smallRadioButton, 0, 0)
        layout.addWidget(self.largeRadioButton, 1, 0)
        layout.addWidget(self.toolBarRadioButton, 2, 0)
        layout.addWidget(self.listViewRadioButton, 0, 1)
        layout.addWidget(self.iconViewRadioButton, 1, 1)
        layout.addWidget(self.tabBarRadioButton, 2, 1)
        layout.addLayout(otherSizeLayout, 3, 0, 1, 2)
        layout.setRowStretch(4, 1)
        self.iconSizeGroupBox.setLayout(layout)

    def createActions(self):
        self.addImagesAct = QAction("&Add Images...", self, shortcut="Ctrl+A",
                triggered=self.addImage)

        self.removeAllImagesAct = QAction("&Remove All Images", self,
                shortcut="Ctrl+R", triggered=self.removeAllImages)

        self.exitAct = QAction("&Quit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.styleActionGroup = QActionGroup(self)
        for styleName in QStyleFactory.keys():
            action = QAction(self.styleActionGroup,
                    text="%s Style" % styleName, checkable=True,
                    triggered=self.changeStyle)
            action.setData(styleName)

        self.guessModeStateAct = QAction("&Guess Image Mode/State", self,
                checkable=True, checked=True)

        self.aboutAct = QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.addImagesAct)
        self.fileMenu.addAction(self.removeAllImagesAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = self.menuBar().addMenu("&View")
        for action in self.styleActionGroup.actions():
            self.viewMenu.addAction(action)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.guessModeStateAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createContextMenu(self):
        self.imagesTable.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.imagesTable.addAction(self.addImagesAct)
        self.imagesTable.addAction(self.removeAllImagesAct)

    def checkCurrentStyle(self):
        for action in self.styleActionGroup.actions():
            styleName = action.data()
            candidate = QStyleFactory.create(styleName)

            if candidate is None:
                return

            if candidate.metaObject().className() == QApplication.style().metaObject().className():
                action.trigger()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
