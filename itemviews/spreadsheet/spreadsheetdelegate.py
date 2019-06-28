#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited
## Copyright (C) 2012 Hans-Peter Jansen <hpj@urpla.net>.
## Copyright (C) 2011 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
## Contact: Nokia Corporation (qt-info@nokia.com)
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:LGPL$
## GNU Lesser General Public License Usage
## This file may be used under the terms of the GNU Lesser General Public
## License version 2.1 as published by the Free Software Foundation and
## appearing in the file LICENSE.LGPL included in the packaging of this
## file. Please review the following information to ensure the GNU Lesser
## General Public License version 2.1 requirements will be met:
## http:#www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
##
## In addition, as a special exception, Nokia gives you certain additional
## rights. These rights are described in the Nokia Qt LGPL Exception
## version 1.1, included in the file LGPL_EXCEPTION.txt in this package.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU General
## Public License version 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of this
## file. Please review the following information to ensure the GNU General
## Public License version 3.0 requirements will be met:
## http:#www.gnu.org/copyleft/gpl.html.
##
## Other Usage
## Alternatively, this file may be used in accordance with the terms and
## conditions contained in a signed written agreement between you and Nokia.
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QCompleter, QDateTimeEdit, QItemDelegate, QLineEdit


class SpreadSheetDelegate(QItemDelegate):

    def __init__(self, parent = None):
        super(SpreadSheetDelegate, self).__init__(parent)

    def createEditor(self, parent, styleOption, index):
        if index.column() == 1:
            editor = QDateTimeEdit(parent)
            editor.setDisplayFormat(self.parent().currentDateFormat)
            editor.setCalendarPopup(True)
            return editor

        editor = QLineEdit(parent)
        # create a completer with the strings in the column as model
        allStrings = []
        for i in range(1, index.model().rowCount()):
            strItem = index.model().data(index.sibling(i, index.column()), Qt.EditRole)
            if strItem not in allStrings:
                allStrings.append(strItem)

        autoComplete = QCompleter(allStrings)
        editor.setCompleter(autoComplete)
        editor.editingFinished.connect(self.commitAndCloseEditor)
        return editor

    def commitAndCloseEditor(self):
        editor = self.sender()
        self.commitData.emit(editor)
        self.closeEditor.emit(editor, QItemDelegate.NoHint)

    def setEditorData(self, editor, index):
        if isinstance(editor, QLineEdit):
            editor.setText(index.model().data(index, Qt.EditRole))
        elif isinstance(editor, QDateTimeEdit):
            editor.setDate(QDate.fromString(
                index.model().data(index, Qt.EditRole), self.parent().currentDateFormat))

    def setModelData(self, editor, model, index):
        if isinstance(editor, QLineEdit):
            model.setData(index, editor.text())
        elif isinstance(editor, QDateTimeEdit):
            model.setData(index, editor.date().toString(self.parent().currentDateFormat))
