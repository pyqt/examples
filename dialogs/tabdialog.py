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


from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDialog,
        QDialogButtonBox, QFrame, QGroupBox, QLabel, QLineEdit, QListWidget,
        QTabWidget, QVBoxLayout, QWidget)


class TabDialog(QDialog):
    def __init__(self, fileName, parent=None):
        super(TabDialog, self).__init__(parent)

        fileInfo = QFileInfo(fileName)

        tabWidget = QTabWidget()
        tabWidget.addTab(GeneralTab(fileInfo), "General")
        tabWidget.addTab(PermissionsTab(fileInfo), "Permissions")
        tabWidget.addTab(ApplicationsTab(fileInfo), "Applications")

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Tab Dialog")


class GeneralTab(QWidget):
    def __init__(self, fileInfo, parent=None):
        super(GeneralTab, self).__init__(parent)

        fileNameLabel = QLabel("File Name:")
        fileNameEdit = QLineEdit(fileInfo.fileName())

        pathLabel = QLabel("Path:")
        pathValueLabel = QLabel(fileInfo.absoluteFilePath())
        pathValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        sizeLabel = QLabel("Size:")
        size = fileInfo.size() // 1024
        sizeValueLabel = QLabel("%d K" % size)
        sizeValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        lastReadLabel = QLabel("Last Read:")
        lastReadValueLabel = QLabel(fileInfo.lastRead().toString())
        lastReadValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        lastModLabel = QLabel("Last Modified:")
        lastModValueLabel = QLabel(fileInfo.lastModified().toString())
        lastModValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(fileNameLabel)
        mainLayout.addWidget(fileNameEdit)
        mainLayout.addWidget(pathLabel)
        mainLayout.addWidget(pathValueLabel)
        mainLayout.addWidget(sizeLabel)
        mainLayout.addWidget(sizeValueLabel)
        mainLayout.addWidget(lastReadLabel)
        mainLayout.addWidget(lastReadValueLabel)
        mainLayout.addWidget(lastModLabel)
        mainLayout.addWidget(lastModValueLabel)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)


class PermissionsTab(QWidget):
    def __init__(self, fileInfo, parent=None):
        super(PermissionsTab, self).__init__(parent)

        permissionsGroup = QGroupBox("Permissions")

        readable = QCheckBox("Readable")
        if fileInfo.isReadable():
            readable.setChecked(True)

        writable = QCheckBox("Writable")
        if fileInfo.isWritable():
            writable.setChecked(True)

        executable = QCheckBox("Executable")
        if fileInfo.isExecutable():
            executable.setChecked(True)

        ownerGroup = QGroupBox("Ownership")

        ownerLabel = QLabel("Owner")
        ownerValueLabel = QLabel(fileInfo.owner())
        ownerValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        groupLabel = QLabel("Group")
        groupValueLabel = QLabel(fileInfo.group())
        groupValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        permissionsLayout = QVBoxLayout()
        permissionsLayout.addWidget(readable)
        permissionsLayout.addWidget(writable)
        permissionsLayout.addWidget(executable)
        permissionsGroup.setLayout(permissionsLayout)

        ownerLayout = QVBoxLayout()
        ownerLayout.addWidget(ownerLabel)
        ownerLayout.addWidget(ownerValueLabel)
        ownerLayout.addWidget(groupLabel)
        ownerLayout.addWidget(groupValueLabel)
        ownerGroup.setLayout(ownerLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(permissionsGroup)
        mainLayout.addWidget(ownerGroup)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)


class ApplicationsTab(QWidget):
    def __init__(self, fileInfo, parent=None):
        super(ApplicationsTab, self).__init__(parent)

        topLabel = QLabel("Open with:")

        applicationsListBox = QListWidget()
        applications = []

        for i in range(1, 31):
            applications.append("Application %d" % i)

        applicationsListBox.insertItems(0, applications)

        alwaysCheckBox = QCheckBox()

        if fileInfo.suffix():
            alwaysCheckBox = QCheckBox("Always use this application to open "
                    "files with the extension '%s'" % fileInfo.suffix())
        else:
            alwaysCheckBox = QCheckBox("Always use this application to open "
                    "this type of file")

        layout = QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(applicationsListBox)
        layout.addWidget(alwaysCheckBox)
        self.setLayout(layout)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    else:
        fileName = "."

    tabdialog = TabDialog(fileName)
    tabdialog.show()
    sys.exit(app.exec_())
