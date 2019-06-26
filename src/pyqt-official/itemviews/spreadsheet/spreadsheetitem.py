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


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem

from util import decode_pos


class SpreadSheetItem(QTableWidgetItem):

    def __init__(self, text=None):
        if text is not None:
            super(SpreadSheetItem, self).__init__(text)
        else:
            super(SpreadSheetItem, self).__init__()

        self.isResolving = False

    def clone(self):
        item = super(SpreadSheetItem, self).clone()
        item.isResolving = self.isResolving

        return item

    def formula(self):
        return super(SpreadSheetItem, self).data(Qt.DisplayRole)

    def data(self, role):
        if role in (Qt.EditRole, Qt.StatusTipRole):
            return self.formula()
        if role == Qt.DisplayRole:
            return self.display()
        t = str(self.display())
        try:
            number = int(t)
        except ValueError:
            number = None
        if role == Qt.TextColorRole:
            if number is None:
                return QColor(Qt.black)
            elif number < 0:
                return QColor(Qt.red)
            return QColor(Qt.blue)

        if role == Qt.TextAlignmentRole:
            if t and (t[0].isdigit() or t[0] == '-'):
                return Qt.AlignRight | Qt.AlignVCenter
        return super(SpreadSheetItem, self).data(role)

    def setData(self, role, value):
        super(SpreadSheetItem, self).setData(role, value)
        if self.tableWidget():
            self.tableWidget().viewport().update()

    def display(self):
        # avoid circular dependencies
        if self.isResolving:
            return None
        self.isResolving = True
        result = self.computeFormula(self.formula(), self.tableWidget())
        self.isResolving = False
        return result

    def computeFormula(self, formula, widget):
        if formula is None:
            return None
        # check if the string is actually a formula or not
        slist = formula.split(' ')
        if not slist or not widget:
            # it is a normal string
            return formula
        op = slist[0].lower()
        firstRow = -1
        firstCol = -1
        secondRow = -1
        secondCol = -1
        if len(slist) > 1:
            firstRow, firstCol = decode_pos(slist[1])
        if len(slist) > 2:
            secondRow, secondCol = decode_pos(slist[2])
        start = widget.item(firstRow, firstCol)
        end = widget.item(secondRow, secondCol)
        firstVal = 0
        try:
            firstVal = start and int(start.text()) or 0
        except ValueError:
            pass
        secondVal = 0
        try:
            secondVal = end and int(end.text()) or 0
        except ValueError:
            pass
        result = None
        if op == "sum":
            sum_ = 0
            for r in range(firstRow, secondRow + 1):
                for c in range(firstCol, secondCol + 1):
                    tableItem = widget.item(r, c)
                    if tableItem and tableItem != self:
                        try:
                            sum_ += int(tableItem.text())
                        except ValueError:
                            pass
            result = sum_
        elif op == "+":
            result = (firstVal + secondVal)
        elif op == "-":
            result = (firstVal - secondVal)
        elif op == "*":
            result = (firstVal * secondVal)
        elif op == "/":
            if secondVal == 0:
                result = "nan"
            else:
                result = (firstVal / secondVal)
        elif op == "=":
            if start:
                result = start.text()
        else:
            result = formula
        return result
