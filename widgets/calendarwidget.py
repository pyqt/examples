#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2015 Riverbank Computing Limited
## Copyright (C) 2010 Hans-Peter Jansen <hpj@urpla.net>.
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
###########################################################################


from PyQt5.QtCore import QDate, QLocale, Qt
from PyQt5.QtGui import QFont, QTextCharFormat
from PyQt5.QtWidgets import (QApplication, QCalendarWidget, QCheckBox,
        QComboBox, QDateEdit, QGridLayout, QGroupBox, QHBoxLayout, QLabel,
        QLayout, QWidget)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.createPreviewGroupBox()
        self.createGeneralOptionsGroupBox()
        self.createDatesGroupBox()
        self.createTextFormatsGroupBox()

        layout = QGridLayout()
        layout.addWidget(self.previewGroupBox, 0, 0)
        layout.addWidget(self.generalOptionsGroupBox, 0, 1)
        layout.addWidget(self.datesGroupBox, 1, 0)
        layout.addWidget(self.textFormatsGroupBox, 1, 1)
        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)

        self.previewLayout.setRowMinimumHeight(0,
                self.calendar.sizeHint().height())
        self.previewLayout.setColumnMinimumWidth(0,
                self.calendar.sizeHint().width())

        self.setWindowTitle("Calendar Widget")

    def localeChanged(self, index):
        self.calendar.setLocale(self.localeCombo.itemData(index))

    def firstDayChanged(self, index):
        self.calendar.setFirstDayOfWeek(
                Qt.DayOfWeek(self.firstDayCombo.itemData(index)))

    def selectionModeChanged(self, index):
        self.calendar.setSelectionMode(
                QCalendarWidget.SelectionMode(
                        self.selectionModeCombo.itemData(index)))

    def horizontalHeaderChanged(self, index):
        self.calendar.setHorizontalHeaderFormat(
                QCalendarWidget.HorizontalHeaderFormat(
                        self.horizontalHeaderCombo.itemData(index)))

    def verticalHeaderChanged(self, index):
        self.calendar.setVerticalHeaderFormat(
                QCalendarWidget.VerticalHeaderFormat(
                        self.verticalHeaderCombo.itemData(index)))

    def selectedDateChanged(self):
        self.currentDateEdit.setDate(self.calendar.selectedDate())

    def minimumDateChanged(self, date):
        self.calendar.setMinimumDate(date)
        self.maximumDateEdit.setDate(self.calendar.maximumDate())

    def maximumDateChanged(self, date):
        self.calendar.setMaximumDate(date)
        self.minimumDateEdit.setDate(self.calendar.minimumDate())

    def weekdayFormatChanged(self):
        format = QTextCharFormat()
        format.setForeground(
                Qt.GlobalColor(
                        self.weekdayColorCombo.itemData(
                                self.weekdayColorCombo.currentIndex())))

        self.calendar.setWeekdayTextFormat(Qt.Monday, format)
        self.calendar.setWeekdayTextFormat(Qt.Tuesday, format)
        self.calendar.setWeekdayTextFormat(Qt.Wednesday, format)
        self.calendar.setWeekdayTextFormat(Qt.Thursday, format)
        self.calendar.setWeekdayTextFormat(Qt.Friday, format)

    def weekendFormatChanged(self):
        format = QTextCharFormat()
        format.setForeground(
                Qt.GlobalColor(
                        self.weekendColorCombo.itemData(
                                self.weekendColorCombo.currentIndex())))

        self.calendar.setWeekdayTextFormat(Qt.Saturday, format)
        self.calendar.setWeekdayTextFormat(Qt.Sunday, format)

    def reformatHeaders(self):
        text = self.headerTextFormatCombo.currentText()
        format = QTextCharFormat()

        if text == "Bold":
            format.setFontWeight(QFont.Bold)
        elif text == "Italic":
            format.setFontItalic(True)
        elif text == "Green":
            format.setForeground(Qt.green)

        self.calendar.setHeaderTextFormat(format)

    def reformatCalendarPage(self):
        if self.firstFridayCheckBox.isChecked():
            firstFriday = QDate(self.calendar.yearShown(),
                    self.calendar.monthShown(), 1)

            while firstFriday.dayOfWeek() != Qt.Friday:
                firstFriday = firstFriday.addDays(1)

            firstFridayFormat = QTextCharFormat()
            firstFridayFormat.setForeground(Qt.blue)

            self.calendar.setDateTextFormat(firstFriday, firstFridayFormat)

        # May 1st in Red takes precedence.
        if self.mayFirstCheckBox.isChecked():
            mayFirst = QDate(self.calendar.yearShown(), 5, 1)

            mayFirstFormat = QTextCharFormat()
            mayFirstFormat.setForeground(Qt.red)

            self.calendar.setDateTextFormat(mayFirst, mayFirstFormat)

    def createPreviewGroupBox(self):
        self.previewGroupBox = QGroupBox("Preview")

        self.calendar = QCalendarWidget()
        self.calendar.setMinimumDate(QDate(1900, 1, 1))
        self.calendar.setMaximumDate(QDate(3000, 1, 1))
        self.calendar.setGridVisible(True)
        self.calendar.currentPageChanged.connect(self.reformatCalendarPage)

        self.previewLayout = QGridLayout()
        self.previewLayout.addWidget(self.calendar, 0, 0, Qt.AlignCenter)
        self.previewGroupBox.setLayout(self.previewLayout)
 
    def createGeneralOptionsGroupBox(self):
        self.generalOptionsGroupBox = QGroupBox("General Options")

        self.localeCombo = QComboBox()

        curLocaleIndex = -1
        index = 0

        this_language = self.locale().nativeLanguageName()
        this_country = self.locale().nativeCountryName()

        for locale in QLocale.matchingLocales(QLocale.AnyLanguage, QLocale.AnyScript, QLocale.AnyCountry):
            language = locale.nativeLanguageName()
            country = locale.nativeCountryName()

            if language == this_language and country == this_country:
                curLocaleIndex = index

            self.localeCombo.addItem('%s/%s' % (language, country), locale)
            index += 1

        if curLocaleIndex != -1:
            self.localeCombo.setCurrentIndex(curLocaleIndex)

        self.localeLabel = QLabel("&Locale")
        self.localeLabel.setBuddy(self.localeCombo)

        self.firstDayCombo = QComboBox()
        self.firstDayCombo.addItem("Sunday", Qt.Sunday)
        self.firstDayCombo.addItem("Monday", Qt.Monday)
        self.firstDayCombo.addItem("Tuesday", Qt.Tuesday)
        self.firstDayCombo.addItem("Wednesday", Qt.Wednesday)
        self.firstDayCombo.addItem("Thursday", Qt.Thursday)
        self.firstDayCombo.addItem("Friday", Qt.Friday)
        self.firstDayCombo.addItem("Saturday", Qt.Saturday)

        self.firstDayLabel = QLabel("Wee&k starts on:")
        self.firstDayLabel.setBuddy(self.firstDayCombo)

        self.selectionModeCombo = QComboBox()
        self.selectionModeCombo.addItem("Single selection",
                QCalendarWidget.SingleSelection)
        self.selectionModeCombo.addItem("None",
                QCalendarWidget.NoSelection)
        self.selectionModeLabel = QLabel("&Selection mode:")
        self.selectionModeLabel.setBuddy(self.selectionModeCombo)

        self.gridCheckBox = QCheckBox("&Grid")
        self.gridCheckBox.setChecked(self.calendar.isGridVisible())

        self.navigationCheckBox = QCheckBox("&Navigation bar")
        self.navigationCheckBox.setChecked(True)

        self.horizontalHeaderCombo = QComboBox()
        self.horizontalHeaderCombo.addItem("Single letter day names",
                QCalendarWidget.SingleLetterDayNames)
        self.horizontalHeaderCombo.addItem("Short day names",
                QCalendarWidget.ShortDayNames)
        self.horizontalHeaderCombo.addItem("Long day names",
                QCalendarWidget.LongDayNames)
        self.horizontalHeaderCombo.addItem("None",
                QCalendarWidget.NoHorizontalHeader)
        self.horizontalHeaderCombo.setCurrentIndex(1)

        self.horizontalHeaderLabel = QLabel("&Horizontal header:")
        self.horizontalHeaderLabel.setBuddy(self.horizontalHeaderCombo)

        self.verticalHeaderCombo = QComboBox()
        self.verticalHeaderCombo.addItem("ISO week numbers",
                QCalendarWidget.ISOWeekNumbers)
        self.verticalHeaderCombo.addItem("None",
                QCalendarWidget.NoVerticalHeader)

        self.verticalHeaderLabel = QLabel("&Vertical header:")
        self.verticalHeaderLabel.setBuddy(self.verticalHeaderCombo)

        self.localeCombo.currentIndexChanged.connect(self.localeChanged)
        self.firstDayCombo.currentIndexChanged.connect(self.firstDayChanged)
        self.selectionModeCombo.currentIndexChanged.connect(
                self.selectionModeChanged)
        self.gridCheckBox.toggled.connect(self.calendar.setGridVisible)
        self.navigationCheckBox.toggled.connect(
                self.calendar.setNavigationBarVisible)
        self.horizontalHeaderCombo.currentIndexChanged.connect(
                self.horizontalHeaderChanged)
        self.verticalHeaderCombo.currentIndexChanged.connect(
                self.verticalHeaderChanged)

        checkBoxLayout = QHBoxLayout()
        checkBoxLayout.addWidget(self.gridCheckBox)
        checkBoxLayout.addStretch()
        checkBoxLayout.addWidget(self.navigationCheckBox)

        outerLayout = QGridLayout()
        outerLayout.addWidget(self.localeLabel, 0, 0)
        outerLayout.addWidget(self.localeCombo, 0, 1)
        outerLayout.addWidget(self.firstDayLabel, 1, 0)
        outerLayout.addWidget(self.firstDayCombo, 1, 1)
        outerLayout.addWidget(self.selectionModeLabel, 2, 0)
        outerLayout.addWidget(self.selectionModeCombo, 2, 1)
        outerLayout.addLayout(checkBoxLayout, 3, 0, 1, 2)
        outerLayout.addWidget(self.horizontalHeaderLabel, 4, 0)
        outerLayout.addWidget(self.horizontalHeaderCombo, 4, 1)
        outerLayout.addWidget(self.verticalHeaderLabel, 5, 0)
        outerLayout.addWidget(self.verticalHeaderCombo, 5, 1)
        self.generalOptionsGroupBox.setLayout(outerLayout)

        self.firstDayChanged(self.firstDayCombo.currentIndex())
        self.selectionModeChanged(self.selectionModeCombo.currentIndex())
        self.horizontalHeaderChanged(self.horizontalHeaderCombo.currentIndex())
        self.verticalHeaderChanged(self.verticalHeaderCombo.currentIndex())
 
    def createDatesGroupBox(self):
        self.datesGroupBox = QGroupBox(self.tr("Dates"))

        self.minimumDateEdit = QDateEdit()
        self.minimumDateEdit.setDisplayFormat('MMM d yyyy')
        self.minimumDateEdit.setDateRange(self.calendar.minimumDate(),
                                          self.calendar.maximumDate())
        self.minimumDateEdit.setDate(self.calendar.minimumDate())

        self.minimumDateLabel = QLabel("&Minimum Date:")
        self.minimumDateLabel.setBuddy(self.minimumDateEdit)

        self.currentDateEdit = QDateEdit()
        self.currentDateEdit.setDisplayFormat('MMM d yyyy')
        self.currentDateEdit.setDate(self.calendar.selectedDate())
        self.currentDateEdit.setDateRange(self.calendar.minimumDate(),
                self.calendar.maximumDate())

        self.currentDateLabel = QLabel("&Current Date:")
        self.currentDateLabel.setBuddy(self.currentDateEdit)

        self.maximumDateEdit = QDateEdit()
        self.maximumDateEdit.setDisplayFormat('MMM d yyyy')
        self.maximumDateEdit.setDateRange(self.calendar.minimumDate(),
                self.calendar.maximumDate())
        self.maximumDateEdit.setDate(self.calendar.maximumDate())

        self.maximumDateLabel = QLabel("Ma&ximum Date:")
        self.maximumDateLabel.setBuddy(self.maximumDateEdit)

        self.currentDateEdit.dateChanged.connect(self.calendar.setSelectedDate)
        self.calendar.selectionChanged.connect(self.selectedDateChanged)
        self.minimumDateEdit.dateChanged.connect(self.minimumDateChanged)
        self.maximumDateEdit.dateChanged.connect(self.maximumDateChanged)
 
        dateBoxLayout = QGridLayout()
        dateBoxLayout.addWidget(self.currentDateLabel, 1, 0)
        dateBoxLayout.addWidget(self.currentDateEdit, 1, 1)
        dateBoxLayout.addWidget(self.minimumDateLabel, 0, 0)
        dateBoxLayout.addWidget(self.minimumDateEdit, 0, 1)
        dateBoxLayout.addWidget(self.maximumDateLabel, 2, 0)
        dateBoxLayout.addWidget(self.maximumDateEdit, 2, 1)
        dateBoxLayout.setRowStretch(3, 1)

        self.datesGroupBox.setLayout(dateBoxLayout)

    def createTextFormatsGroupBox(self):
        self.textFormatsGroupBox = QGroupBox("Text Formats")

        self.weekdayColorCombo = self.createColorComboBox()
        self.weekdayColorCombo.setCurrentIndex(
                self.weekdayColorCombo.findText("Black"))

        self.weekdayColorLabel = QLabel("&Weekday color:")
        self.weekdayColorLabel.setBuddy(self.weekdayColorCombo)

        self.weekendColorCombo = self.createColorComboBox()
        self.weekendColorCombo.setCurrentIndex(
                self.weekendColorCombo.findText("Red"))

        self.weekendColorLabel = QLabel("Week&end color:")
        self.weekendColorLabel.setBuddy(self.weekendColorCombo)

        self.headerTextFormatCombo = QComboBox()
        self.headerTextFormatCombo.addItem("Bold")
        self.headerTextFormatCombo.addItem("Italic")
        self.headerTextFormatCombo.addItem("Plain")

        self.headerTextFormatLabel = QLabel("&Header text:")
        self.headerTextFormatLabel.setBuddy(self.headerTextFormatCombo)

        self.firstFridayCheckBox = QCheckBox("&First Friday in blue")

        self.mayFirstCheckBox = QCheckBox("May &1 in red")

        self.weekdayColorCombo.currentIndexChanged.connect(
                self.weekdayFormatChanged)
        self.weekendColorCombo.currentIndexChanged.connect(
                self.weekendFormatChanged)
        self.headerTextFormatCombo.currentIndexChanged.connect(
                self.reformatHeaders)
        self.firstFridayCheckBox.toggled.connect(self.reformatCalendarPage)
        self.mayFirstCheckBox.toggled.connect(self.reformatCalendarPage)

        checkBoxLayout = QHBoxLayout()
        checkBoxLayout.addWidget(self.firstFridayCheckBox)
        checkBoxLayout.addStretch()
        checkBoxLayout.addWidget(self.mayFirstCheckBox)

        outerLayout = QGridLayout()
        outerLayout.addWidget(self.weekdayColorLabel, 0, 0)
        outerLayout.addWidget(self.weekdayColorCombo, 0, 1)
        outerLayout.addWidget(self.weekendColorLabel, 1, 0)
        outerLayout.addWidget(self.weekendColorCombo, 1, 1)
        outerLayout.addWidget(self.headerTextFormatLabel, 2, 0)
        outerLayout.addWidget(self.headerTextFormatCombo, 2, 1)
        outerLayout.addLayout(checkBoxLayout, 3, 0, 1, 2)
        self.textFormatsGroupBox.setLayout(outerLayout)

        self.weekdayFormatChanged()
        self.weekendFormatChanged()

        self.reformatHeaders()
        self.reformatCalendarPage()
 
    def createColorComboBox(self):
        comboBox = QComboBox()
        comboBox.addItem("Red", Qt.red)
        comboBox.addItem("Blue", Qt.blue)
        comboBox.addItem("Black", Qt.black)
        comboBox.addItem("Magenta", Qt.magenta)

        return comboBox


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())
