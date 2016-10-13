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


import sys

from PyQt5.QtCore import (QByteArray, QDate, QDateTime, QEvent, QPoint, QRect,
        QRegExp, QSettings, QSize, Qt, QTime, QTimer)
from PyQt5.QtGui import QColor, QIcon, QRegExpValidator, QValidator
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QApplication,
        QComboBox, QDialog, QDialogButtonBox, QFileDialog, QGridLayout,
        QGroupBox, QHeaderView, QInputDialog, QItemDelegate, QLabel, QLineEdit,
        QMainWindow, QMessageBox, QStyle, QStyleOptionViewItem, QTableWidget,
        QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QVBoxLayout)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.settingsTree = SettingsTree()
        self.setCentralWidget(self.settingsTree)

        self.locationDialog = None

        self.createActions()
        self.createMenus()

        self.autoRefreshAct.setChecked(True)
        self.fallbacksAct.setChecked(True)

        self.setWindowTitle("Settings Editor")
        self.resize(500, 600)

    def openSettings(self):
        if self.locationDialog is None:
            self.locationDialog = LocationDialog(self)

        if self.locationDialog.exec_():
            settings = QSettings(self.locationDialog.format(),
                                        self.locationDialog.scope(),
                                        self.locationDialog.organization(),
                                        self.locationDialog.application())
            self.setSettingsObject(settings)
            self.fallbacksAct.setEnabled(True)

    def openIniFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open INI File", '',
                "INI Files (*.ini *.conf)")

        if fileName:
            settings = QSettings(fileName, QSettings.IniFormat)
            self.setSettingsObject(settings)
            self.fallbacksAct.setEnabled(False)

    def openPropertyList(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Property List",
                '', "Property List Files (*.plist)")

        if fileName:
            settings = QSettings(fileName, QSettings.NativeFormat)
            self.setSettingsObject(settings)
            self.fallbacksAct.setEnabled(False)

    def openRegistryPath(self):
        path, ok = QInputDialog.getText(self, "Open Registry Path",
                "Enter the path in the Windows registry:", QLineEdit.Normal,
                'HKEY_CURRENT_USER\\')

        if ok and path != '':
            settings = QSettings(path, QSettings.NativeFormat)
            self.setSettingsObject(settings)
            self.fallbacksAct.setEnabled(False)

    def about(self):
        QMessageBox.about(self, "About Settings Editor",
                "The <b>Settings Editor</b> example shows how to access "
                "application settings using Qt.")

    def createActions(self):
        self.openSettingsAct = QAction("&Open Application Settings...", self,
                shortcut="Ctrl+O", triggered=self.openSettings)

        self.openIniFileAct = QAction("Open I&NI File...", self,
                shortcut="Ctrl+N", triggered=self.openIniFile)

        self.openPropertyListAct = QAction("Open Mac &Property List...", self,
                shortcut="Ctrl+P", triggered=self.openPropertyList)
        if sys.platform != 'darwin':
            self.openPropertyListAct.setEnabled(False)

        self.openRegistryPathAct = QAction("Open Windows &Registry Path...",
                self, shortcut="Ctrl+G", triggered=self.openRegistryPath)
        if sys.platform != 'win32':
            self.openRegistryPathAct.setEnabled(False)

        self.refreshAct = QAction("&Refresh", self, shortcut="Ctrl+R",
                enabled=False, triggered=self.settingsTree.refresh)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.autoRefreshAct = QAction("&Auto-Refresh", self, shortcut="Ctrl+A",
                checkable=True, enabled=False)
        self.autoRefreshAct.triggered.connect(self.settingsTree.setAutoRefresh)
        self.autoRefreshAct.triggered.connect(self.refreshAct.setDisabled)

        self.fallbacksAct = QAction("&Fallbacks", self, shortcut="Ctrl+F",
                checkable=True, enabled=False,
                triggered=self.settingsTree.setFallbacksEnabled)

        self.aboutAct = QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openSettingsAct)
        self.fileMenu.addAction(self.openIniFileAct)
        self.fileMenu.addAction(self.openPropertyListAct)
        self.fileMenu.addAction(self.openRegistryPathAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.refreshAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.optionsMenu = self.menuBar().addMenu("&Options")
        self.optionsMenu.addAction(self.autoRefreshAct)
        self.optionsMenu.addAction(self.fallbacksAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def setSettingsObject(self, settings):
        settings.setFallbacksEnabled(self.fallbacksAct.isChecked())
        self.settingsTree.setSettingsObject(settings)

        self.refreshAct.setEnabled(True)
        self.autoRefreshAct.setEnabled(True)

        niceName = settings.fileName()
        niceName.replace('\\', '/')
        niceName = niceName.split('/')[-1]

        if not settings.isWritable():
            niceName += " (read only)"

        self.setWindowTitle("%s - Settings Editor" % niceName)


class LocationDialog(QDialog):
    def __init__(self, parent=None):
        super(LocationDialog, self).__init__(parent)

        self.formatComboBox = QComboBox()
        self.formatComboBox.addItem("Native")
        self.formatComboBox.addItem("INI")

        self.scopeComboBox = QComboBox()
        self.scopeComboBox.addItem("User")
        self.scopeComboBox.addItem("System")

        self.organizationComboBox = QComboBox()
        self.organizationComboBox.addItem("Trolltech")
        self.organizationComboBox.setEditable(True)

        self.applicationComboBox = QComboBox()
        self.applicationComboBox.addItem("Any")
        self.applicationComboBox.addItem("Application Example")
        self.applicationComboBox.addItem("Assistant")
        self.applicationComboBox.addItem("Designer")
        self.applicationComboBox.addItem("Linguist")
        self.applicationComboBox.setEditable(True)
        self.applicationComboBox.setCurrentIndex(3)

        formatLabel = QLabel("&Format:")
        formatLabel.setBuddy(self.formatComboBox)

        scopeLabel = QLabel("&Scope:")
        scopeLabel.setBuddy(self.scopeComboBox)

        organizationLabel = QLabel("&Organization:")
        organizationLabel.setBuddy(self.organizationComboBox)

        applicationLabel = QLabel("&Application:")
        applicationLabel.setBuddy(self.applicationComboBox)

        self.locationsGroupBox = QGroupBox("Setting Locations")

        self.locationsTable = QTableWidget()
        self.locationsTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.locationsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.locationsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.locationsTable.setColumnCount(2)
        self.locationsTable.setHorizontalHeaderLabels(("Location", "Access"))
        self.locationsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.locationsTable.horizontalHeader().resizeSection(1, 180)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.formatComboBox.activated.connect(self.updateLocationsTable)
        self.scopeComboBox.activated.connect(self.updateLocationsTable)
        self.organizationComboBox.lineEdit().editingFinished.connect(self.updateLocationsTable)
        self.applicationComboBox.lineEdit().editingFinished.connect(self.updateLocationsTable)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        locationsLayout = QVBoxLayout()
        locationsLayout.addWidget(self.locationsTable)
        self.locationsGroupBox.setLayout(locationsLayout)

        mainLayout = QGridLayout()
        mainLayout.addWidget(formatLabel, 0, 0)
        mainLayout.addWidget(self.formatComboBox, 0, 1)
        mainLayout.addWidget(scopeLabel, 1, 0)
        mainLayout.addWidget(self.scopeComboBox, 1, 1)
        mainLayout.addWidget(organizationLabel, 2, 0)
        mainLayout.addWidget(self.organizationComboBox, 2, 1)
        mainLayout.addWidget(applicationLabel, 3, 0)
        mainLayout.addWidget(self.applicationComboBox, 3, 1)
        mainLayout.addWidget(self.locationsGroupBox, 4, 0, 1, 2)
        mainLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.setLayout(mainLayout)

        self.updateLocationsTable()

        self.setWindowTitle("Open Application Settings")
        self.resize(650, 400)

    def format(self):
        if self.formatComboBox.currentIndex() == 0:
            return QSettings.NativeFormat
        else:
            return QSettings.IniFormat

    def scope(self):
        if self.scopeComboBox.currentIndex() == 0:
            return QSettings.UserScope
        else:
            return QSettings.SystemScope

    def organization(self):
        return self.organizationComboBox.currentText()

    def application(self):
        if self.applicationComboBox.currentText() == "Any":
            return ''

        return self.applicationComboBox.currentText()

    def updateLocationsTable(self):
        self.locationsTable.setUpdatesEnabled(False)
        self.locationsTable.setRowCount(0)

        for i in range(2):
            if i == 0:
                if self.scope() == QSettings.SystemScope:
                    continue

                actualScope = QSettings.UserScope
            else:
                actualScope = QSettings.SystemScope

            for j in range(2):
                if j == 0:
                    if not self.application():
                        continue

                    actualApplication = self.application()
                else:
                    actualApplication = ''

                settings = QSettings(self.format(), actualScope,
                        self.organization(), actualApplication)

                row = self.locationsTable.rowCount()
                self.locationsTable.setRowCount(row + 1)

                item0 = QTableWidgetItem()
                item0.setText(settings.fileName())

                item1 = QTableWidgetItem()
                disable = not (settings.childKeys() or settings.childGroups())

                if row == 0:
                    if settings.isWritable():
                        item1.setText("Read-write")
                        disable = False
                    else:
                        item1.setText("Read-only")
                    self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(disable)
                else:
                    item1.setText("Read-only fallback")

                if disable:
                    item0.setFlags(item0.flags() & ~Qt.ItemIsEnabled)
                    item1.setFlags(item1.flags() & ~Qt.ItemIsEnabled)

                self.locationsTable.setItem(row, 0, item0)
                self.locationsTable.setItem(row, 1, item1)

        self.locationsTable.setUpdatesEnabled(True)


class SettingsTree(QTreeWidget):
    def __init__(self, parent=None):
        super(SettingsTree, self).__init__(parent)

        self.setItemDelegate(VariantDelegate(self))

        self.setHeaderLabels(("Setting", "Type", "Value"))
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header().setSectionResizeMode(2, QHeaderView.Stretch)

        self.settings = None
        self.refreshTimer = QTimer()
        self.refreshTimer.setInterval(2000)
        self.autoRefresh = False

        self.groupIcon = QIcon()
        self.groupIcon.addPixmap(self.style().standardPixmap(QStyle.SP_DirClosedIcon),
                QIcon.Normal, QIcon.Off)
        self.groupIcon.addPixmap(self.style().standardPixmap(QStyle.SP_DirOpenIcon),
                QIcon.Normal, QIcon.On)
        self.keyIcon = QIcon()
        self.keyIcon.addPixmap(self.style().standardPixmap(QStyle.SP_FileIcon))

        self.refreshTimer.timeout.connect(self.maybeRefresh)

    def setSettingsObject(self, settings):
        self.settings = settings
        self.clear()

        if self.settings is not None:
            self.settings.setParent(self)
            self.refresh()
            if self.autoRefresh:
                self.refreshTimer.start()
        else:
            self.refreshTimer.stop()

    def sizeHint(self):
        return QSize(800, 600)

    def setAutoRefresh(self, autoRefresh):
        self.autoRefresh = autoRefresh

        if self.settings is not None:
            if self.autoRefresh:
                self.maybeRefresh()
                self.refreshTimer.start()
            else:
                self.refreshTimer.stop()

    def setFallbacksEnabled(self, enabled):
        if self.settings is not None:
            self.settings.setFallbacksEnabled(enabled)
            self.refresh()

    def maybeRefresh(self):
        if self.state() != QAbstractItemView.EditingState:
            self.refresh()

    def refresh(self):
        if self.settings is None:
            return

        # The signal might not be connected.
        try:
            self.itemChanged.disconnect(self.updateSetting)
        except:
            pass

        self.settings.sync()
        self.updateChildItems(None)

        self.itemChanged.connect(self.updateSetting)

    def event(self, event):
        if event.type() == QEvent.WindowActivate:
            if self.isActiveWindow() and self.autoRefresh:
                self.maybeRefresh()

        return super(SettingsTree, self).event(event)

    def updateSetting(self, item):
        key = item.text(0)
        ancestor = item.parent()

        while ancestor:
            key = ancestor.text(0) + '/' + key
            ancestor = ancestor.parent()

        d = item.data(2, Qt.UserRole)
        self.settings.setValue(key, item.data(2, Qt.UserRole))

        if self.autoRefresh:
            self.refresh()

    def updateChildItems(self, parent):
        dividerIndex = 0

        for group in self.settings.childGroups():
            childIndex = self.findChild(parent, group, dividerIndex)
            if childIndex != -1:
                child = self.childAt(parent, childIndex)
                child.setText(1, '')
                child.setText(2, '')
                child.setData(2, Qt.UserRole, None)
                self.moveItemForward(parent, childIndex, dividerIndex)
            else:
                child = self.createItem(group, parent, dividerIndex)

            child.setIcon(0, self.groupIcon)
            dividerIndex += 1

            self.settings.beginGroup(group)
            self.updateChildItems(child)
            self.settings.endGroup()

        for key in self.settings.childKeys():
            childIndex = self.findChild(parent, key, 0)
            if childIndex == -1 or childIndex >= dividerIndex:
                if childIndex != -1:
                    child = self.childAt(parent, childIndex)
                    for i in range(child.childCount()):
                        self.deleteItem(child, i)
                    self.moveItemForward(parent, childIndex, dividerIndex)
                else:
                    child = self.createItem(key, parent, dividerIndex)
                child.setIcon(0, self.keyIcon)
                dividerIndex += 1
            else:
                child = self.childAt(parent, childIndex)

            value = self.settings.value(key)
            if value is None:
                child.setText(1, 'Invalid')
            else:
                child.setText(1, value.__class__.__name__)
            child.setText(2, VariantDelegate.displayText(value))
            child.setData(2, Qt.UserRole, value)

        while dividerIndex < self.childCount(parent):
            self.deleteItem(parent, dividerIndex)

    def createItem(self, text, parent, index):
        after = None

        if index != 0:
            after = self.childAt(parent, index - 1)

        if parent is not None:
            item = QTreeWidgetItem(parent, after)
        else:
            item = QTreeWidgetItem(self, after)

        item.setText(0, text)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        return item

    def deleteItem(self, parent, index):
        if parent is not None:
            item = parent.takeChild(index)
        else:
            item = self.takeTopLevelItem(index)
        del item

    def childAt(self, parent, index):
        if parent is not None:
            return parent.child(index)
        else:
            return self.topLevelItem(index)

    def childCount(self, parent):
        if parent is not None:
            return parent.childCount()
        else:
            return self.topLevelItemCount()

    def findChild(self, parent, text, startIndex):
        for i in range(self.childCount(parent)):
            if self.childAt(parent, i).text(0) == text:
                return i
        return -1

    def moveItemForward(self, parent, oldIndex, newIndex):
        for int in range(oldIndex - newIndex):
            self.deleteItem(parent, newIndex)


class VariantDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(VariantDelegate, self).__init__(parent)

        self.boolExp = QRegExp()
        self.boolExp.setPattern('true|false')
        self.boolExp.setCaseSensitivity(Qt.CaseInsensitive)

        self.byteArrayExp = QRegExp()
        self.byteArrayExp.setPattern('[\\x00-\\xff]*')

        self.charExp = QRegExp()
        self.charExp.setPattern('.')

        self.colorExp = QRegExp()
        self.colorExp.setPattern('\\(([0-9]*),([0-9]*),([0-9]*),([0-9]*)\\)')

        self.doubleExp = QRegExp()
        self.doubleExp.setPattern('')

        self.pointExp = QRegExp()
        self.pointExp.setPattern('\\((-?[0-9]*),(-?[0-9]*)\\)')

        self.rectExp = QRegExp()
        self.rectExp.setPattern('\\((-?[0-9]*),(-?[0-9]*),(-?[0-9]*),(-?[0-9]*)\\)')

        self.signedIntegerExp = QRegExp()
        self.signedIntegerExp.setPattern('-?[0-9]*')

        self.sizeExp = QRegExp(self.pointExp)

        self.unsignedIntegerExp = QRegExp()
        self.unsignedIntegerExp.setPattern('[0-9]*')

        self.dateExp = QRegExp()
        self.dateExp.setPattern('([0-9]{,4})-([0-9]{,2})-([0-9]{,2})')

        self.timeExp = QRegExp()
        self.timeExp.setPattern('([0-9]{,2}):([0-9]{,2}):([0-9]{,2})')

        self.dateTimeExp = QRegExp()
        self.dateTimeExp.setPattern(self.dateExp.pattern() + 'T' + self.timeExp.pattern())

    def paint(self, painter, option, index):
        if index.column() == 2:
            value = index.model().data(index, Qt.UserRole)
            if not self.isSupportedType(value):
                myOption = QStyleOptionViewItem(option)
                myOption.state &= ~QStyle.State_Enabled
                super(VariantDelegate, self).paint(painter, myOption, index)
                return

        super(VariantDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        if index.column() != 2:
            return None

        originalValue = index.model().data(index, Qt.UserRole)
        if not self.isSupportedType(originalValue):
            return None

        lineEdit = QLineEdit(parent)
        lineEdit.setFrame(False)

        if isinstance(originalValue, bool):
            regExp = self.boolExp
        elif isinstance(originalValue, float):
            regExp = self.doubleExp
        elif isinstance(originalValue, int):
            regExp = self.signedIntegerExp
        elif isinstance(originalValue, QByteArray):
            regExp = self.byteArrayExp
        elif isinstance(originalValue, QColor):
            regExp = self.colorExp
        elif isinstance(originalValue, QDate):
            regExp = self.dateExp
        elif isinstance(originalValue, QDateTime):
            regExp = self.dateTimeExp
        elif isinstance(originalValue, QTime):
            regExp = self.timeExp
        elif isinstance(originalValue, QPoint):
            regExp = self.pointExp
        elif isinstance(originalValue, QRect):
            regExp = self.rectExp
        elif isinstance(originalValue, QSize):
            regExp = self.sizeExp
        else:
            regExp = QRegExp()

        if not regExp.isEmpty():
            validator = QRegExpValidator(regExp, lineEdit)
            lineEdit.setValidator(validator)

        return lineEdit

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.UserRole)
        if editor is not None:
            editor.setText(self.displayText(value))

    def setModelData(self, editor, model, index):
        if not editor.isModified():
            return

        text = editor.text()
        validator = editor.validator()
        if validator is not None:
            state, text, _ = validator.validate(text, 0)
            if state != QValidator.Acceptable:
                return

        originalValue = index.model().data(index, Qt.UserRole)

        if isinstance(originalValue, QColor):
            self.colorExp.exactMatch(text)
            value = QColor(min(int(self.colorExp.cap(1)), 255),
                           min(int(self.colorExp.cap(2)), 255),
                           min(int(self.colorExp.cap(3)), 255),
                           min(int(self.colorExp.cap(4)), 255))
        elif isinstance(originalValue, QDate):
            value = QDate.fromString(text, Qt.ISODate)
            if not value.isValid():
                return
        elif isinstance(originalValue, QDateTime):
            value = QDateTime.fromString(text, Qt.ISODate)
            if not value.isValid():
                return
        elif isinstance(originalValue, QTime):
            value = QTime.fromString(text, Qt.ISODate)
            if not value.isValid():
                return
        elif isinstance(originalValue, QPoint):
            self.pointExp.exactMatch(text)
            value = QPoint(int(self.pointExp.cap(1)),
                           int(self.pointExp.cap(2)))
        elif isinstance(originalValue, QRect):
            self.rectExp.exactMatch(text)
            value = QRect(int(self.rectExp.cap(1)),
                          int(self.rectExp.cap(2)),
                          int(self.rectExp.cap(3)),
                          int(self.rectExp.cap(4)))
        elif isinstance(originalValue, QSize):
            self.sizeExp.exactMatch(text)
            value = QSize(int(self.sizeExp.cap(1)),
                          int(self.sizeExp.cap(2)))
        elif isinstance(originalValue, list):
            value = text.split(',')
        else:
            value = type(originalValue)(text)

        model.setData(index, self.displayText(value), Qt.DisplayRole)
        model.setData(index, value, Qt.UserRole)

    @staticmethod
    def isSupportedType(value):
        return isinstance(value, (bool, float, int, QByteArray, str, QColor,
                QDate, QDateTime, QTime, QPoint, QRect, QSize, list))

    @staticmethod
    def displayText(value):
        if isinstance(value, (bool, int, QByteArray)):
            return str(value)
        if isinstance(value, str):
            return value
        elif isinstance(value, float):
            return '%g' % value
        elif isinstance(value, QColor):
            return '(%u,%u,%u,%u)' % (value.red(), value.green(), value.blue(), value.alpha())
        elif isinstance(value, (QDate, QDateTime, QTime)):
            return value.toString(Qt.ISODate)
        elif isinstance(value, QPoint):
            return '(%d,%d)' % (value.x(), value.y())
        elif isinstance(value, QRect):
            return '(%d,%d,%d,%d)' % (value.x(), value.y(), value.width(), value.height())
        elif isinstance(value, QSize):
            return '(%d,%d)' % (value.width(), value.height())
        elif isinstance(value, list):
            return ','.join(value)
        elif value is None:
            return '<Invalid>'

        return '<%s>' % value


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
