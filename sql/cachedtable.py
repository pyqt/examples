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


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox,
        QHBoxLayout, QMessageBox, QPushButton, QTableView)
from PyQt5.QtSql import QSqlTableModel

import connection


class TableEditor(QDialog):
    def __init__(self, tableName, parent=None):
        super(TableEditor, self).__init__(parent)

        self.model = QSqlTableModel(self)
        self.model.setTable(tableName)
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "First name")
        self.model.setHeaderData(2, Qt.Horizontal, "Last name")

        view = QTableView()
        view.setModel(self.model)

        submitButton = QPushButton("Submit")
        submitButton.setDefault(True)
        revertButton = QPushButton("&Revert")
        quitButton = QPushButton("Quit")

        buttonBox = QDialogButtonBox(Qt.Vertical)
        buttonBox.addButton(submitButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(revertButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(quitButton, QDialogButtonBox.RejectRole)

        submitButton.clicked.connect(self.submit)
        revertButton.clicked.connect(self.model.revertAll)
        quitButton.clicked.connect(self.close)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(view)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Cached Table")

    def submit(self):
        self.model.database().transaction()
        if self.model.submitAll():
            self.model.database().commit()
        else:
            self.model.database().rollback()
            QMessageBox.warning(self, "Cached Table",
                        "The database reported an error: %s" % self.model.lastError().text())


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    if not connection.createConnection():
        sys.exit(1)

    editor = TableEditor('person')
    editor.show()
    sys.exit(editor.exec_())
