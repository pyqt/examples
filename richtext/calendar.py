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


from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import (QColor, QFont, QTextCharFormat, QTextLength,
        QTextTableFormat)
from PyQt5.QtWidgets import (QApplication, QComboBox, QDateTimeEdit,
        QHBoxLayout, QLabel, QMainWindow, QSpinBox, QTextBrowser, QVBoxLayout,
        QWidget)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.selectedDate = QDate.currentDate()
        self.fontSize = 10

        centralWidget = QWidget()

        dateLabel = QLabel("Date:")
        monthCombo = QComboBox()

        for month in range(1, 13):
            monthCombo.addItem(QDate.longMonthName(month))

        yearEdit = QDateTimeEdit()
        yearEdit.setDisplayFormat('yyyy')
        yearEdit.setDateRange(QDate(1753, 1, 1), QDate(8000, 1, 1))

        monthCombo.setCurrentIndex(self.selectedDate.month() - 1)
        yearEdit.setDate(self.selectedDate)

        self.fontSizeLabel = QLabel("Font size:")
        self.fontSizeSpinBox = QSpinBox()
        self.fontSizeSpinBox.setRange(1, 64)
        self.fontSizeSpinBox.setValue(10)

        self.editor = QTextBrowser()
        self.insertCalendar()

        monthCombo.activated.connect(self.setMonth)
        yearEdit.dateChanged.connect(self.setYear)
        self.fontSizeSpinBox.valueChanged.connect(self.setfontSize)

        controlsLayout = QHBoxLayout()
        controlsLayout.addWidget(dateLabel)
        controlsLayout.addWidget(monthCombo)
        controlsLayout.addWidget(yearEdit)
        controlsLayout.addSpacing(24)
        controlsLayout.addWidget(self.fontSizeLabel)
        controlsLayout.addWidget(self.fontSizeSpinBox)
        controlsLayout.addStretch(1)

        centralLayout = QVBoxLayout()
        centralLayout.addLayout(controlsLayout)
        centralLayout.addWidget(self.editor, 1)
        centralWidget.setLayout(centralLayout)

        self.setCentralWidget(centralWidget)

    def insertCalendar(self):
        self.editor.clear()
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()

        date = QDate(self.selectedDate.year(), self.selectedDate.month(), 1)

        tableFormat = QTextTableFormat()
        tableFormat.setAlignment(Qt.AlignHCenter)
        tableFormat.setBackground(QColor('#e0e0e0'))
        tableFormat.setCellPadding(2)
        tableFormat.setCellSpacing(4)
        constraints = [QTextLength(QTextLength.PercentageLength, 14),
                       QTextLength(QTextLength.PercentageLength, 14),
                       QTextLength(QTextLength.PercentageLength, 14),
                       QTextLength(QTextLength.PercentageLength, 14),
                       QTextLength(QTextLength.PercentageLength, 14),
                       QTextLength(QTextLength.PercentageLength, 14),
                       QTextLength(QTextLength.PercentageLength, 14)]

        tableFormat.setColumnWidthConstraints(constraints)

        table = cursor.insertTable(1, 7, tableFormat)

        frame = cursor.currentFrame()
        frameFormat = frame.frameFormat()
        frameFormat.setBorder(1)
        frame.setFrameFormat(frameFormat)

        format = cursor.charFormat()
        format.setFontPointSize(self.fontSize)

        boldFormat = QTextCharFormat(format)
        boldFormat.setFontWeight(QFont.Bold)

        highlightedFormat = QTextCharFormat(boldFormat)
        highlightedFormat.setBackground(Qt.yellow)

        for weekDay in range(1, 8):
            cell = table.cellAt(0, weekDay-1)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(QDate.longDayName(weekDay), boldFormat)

        table.insertRows(table.rows(), 1)

        while date.month() == self.selectedDate.month():
            weekDay = date.dayOfWeek()
            cell = table.cellAt(table.rows()-1, weekDay-1)
            cellCursor = cell.firstCursorPosition()

            if date == QDate.currentDate():
                cellCursor.insertText(str(date.day()), highlightedFormat)
            else:
                cellCursor.insertText(str(date.day()), format)

            date = date.addDays(1)

            if weekDay == 7 and date.month() == self.selectedDate.month():
                table.insertRows(table.rows(), 1)

        cursor.endEditBlock()

        self.setWindowTitle("Calendar for %s %d" % (QDate.longMonthName(self.selectedDate.month()), self.selectedDate.year()))

    def setfontSize(self, size):
        self.fontSize = size
        self.insertCalendar()

    def setMonth(self, month):
        self.selectedDate = QDate(self.selectedDate.year(), month + 1,
                self.selectedDate.day())
        self.insertCalendar()

    def setYear(self, date):
        self.selectedDate = QDate(date.year(), self.selectedDate.month(),
                self.selectedDate.day())
        self.insertCalendar()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 256)
    window.show()
    sys.exit(app.exec_())    
