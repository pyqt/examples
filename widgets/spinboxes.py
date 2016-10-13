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


from PyQt5.QtCore import QDate, QDateTime, Qt, QTime
from PyQt5.QtWidgets import (QApplication, QComboBox, QDateEdit, QDateTimeEdit,
        QDoubleSpinBox, QGroupBox, QHBoxLayout, QLabel, QSpinBox, QTimeEdit,
        QVBoxLayout, QWidget)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.createSpinBoxes()
        self.createDateTimeEdits()
        self.createDoubleSpinBoxes()

        layout = QHBoxLayout()
        layout.addWidget(self.spinBoxesGroup)
        layout.addWidget(self.editsGroup)
        layout.addWidget(self.doubleSpinBoxesGroup)
        self.setLayout(layout)

        self.setWindowTitle("Spin Boxes")

    def createSpinBoxes(self):
        self.spinBoxesGroup = QGroupBox("Spinboxes")

        integerLabel = QLabel("Enter a value between %d and %d:" % (-20, 20))
        integerSpinBox = QSpinBox()
        integerSpinBox.setRange(-20, 20)
        integerSpinBox.setSingleStep(1)
        integerSpinBox.setValue(0)

        zoomLabel = QLabel("Enter a zoom value between %d and %d:" % (0, 1000))
        zoomSpinBox = QSpinBox()
        zoomSpinBox.setRange(0, 1000)
        zoomSpinBox.setSingleStep(10)
        zoomSpinBox.setSuffix('%')
        zoomSpinBox.setSpecialValueText("Automatic")
        zoomSpinBox.setValue(100)

        priceLabel = QLabel("Enter a price between %d and %d:" % (0, 999))
        priceSpinBox = QSpinBox()
        priceSpinBox.setRange(0, 999)
        priceSpinBox.setSingleStep(1)
        priceSpinBox.setPrefix('$')
        priceSpinBox.setValue(99)

        spinBoxLayout = QVBoxLayout()
        spinBoxLayout.addWidget(integerLabel)
        spinBoxLayout.addWidget(integerSpinBox)
        spinBoxLayout.addWidget(zoomLabel)
        spinBoxLayout.addWidget(zoomSpinBox)
        spinBoxLayout.addWidget(priceLabel)
        spinBoxLayout.addWidget(priceSpinBox)
        self.spinBoxesGroup.setLayout(spinBoxLayout)

    def createDateTimeEdits(self):
        self.editsGroup = QGroupBox("Date and time spin boxes")

        dateLabel = QLabel()
        dateEdit = QDateEdit(QDate.currentDate())
        dateEdit.setDateRange(QDate(2005, 1, 1), QDate(2010, 12, 31))
        dateLabel.setText("Appointment date (between %s and %s):" %
                    (dateEdit.minimumDate().toString(Qt.ISODate),
                    dateEdit.maximumDate().toString(Qt.ISODate)))

        timeLabel = QLabel()
        timeEdit = QTimeEdit(QTime.currentTime())
        timeEdit.setTimeRange(QTime(9, 0, 0, 0), QTime(16, 30, 0, 0))
        timeLabel.setText("Appointment time (between %s and %s):" %
                    (timeEdit.minimumTime().toString(Qt.ISODate),
                    timeEdit.maximumTime().toString(Qt.ISODate)))

        self.meetingLabel = QLabel()
        self.meetingEdit = QDateTimeEdit(QDateTime.currentDateTime())

        formatLabel = QLabel("Format string for the meeting date and time:")

        formatComboBox = QComboBox()
        formatComboBox.addItem('yyyy-MM-dd hh:mm:ss (zzz \'ms\')')
        formatComboBox.addItem('hh:mm:ss MM/dd/yyyy')
        formatComboBox.addItem('hh:mm:ss dd/MM/yyyy')
        formatComboBox.addItem('hh:mm:ss')
        formatComboBox.addItem('hh:mm ap')

        formatComboBox.activated[str].connect(self.setFormatString)

        self.setFormatString(formatComboBox.currentText())

        editsLayout = QVBoxLayout()
        editsLayout.addWidget(dateLabel)
        editsLayout.addWidget(dateEdit)
        editsLayout.addWidget(timeLabel)
        editsLayout.addWidget(timeEdit)
        editsLayout.addWidget(self.meetingLabel)
        editsLayout.addWidget(self.meetingEdit)
        editsLayout.addWidget(formatLabel)
        editsLayout.addWidget(formatComboBox)
        self.editsGroup.setLayout(editsLayout)

    def setFormatString(self, formatString):
        self.meetingEdit.setDisplayFormat(formatString)

        if self.meetingEdit.displayedSections() & QDateTimeEdit.DateSections_Mask:
            self.meetingEdit.setDateRange(QDate(2004, 11, 1), QDate(2005, 11, 30))
            self.meetingLabel.setText("Meeting date (between %s and %s):" %
                    (self.meetingEdit.minimumDate().toString(Qt.ISODate),
                    self.meetingEdit.maximumDate().toString(Qt.ISODate)))
        else:
            self.meetingEdit.setTimeRange(QTime(0, 7, 20, 0), QTime(21, 0, 0, 0))
            self.meetingLabel.setText("Meeting time (between %s and %s):" %
                    (self.meetingEdit.minimumTime().toString(Qt.ISODate),
                    self.meetingEdit.maximumTime().toString(Qt.ISODate)))

    def createDoubleSpinBoxes(self):
        self.doubleSpinBoxesGroup = QGroupBox("Double precision spinboxes")

        precisionLabel = QLabel("Number of decimal places to show:")
        precisionSpinBox = QSpinBox()
        precisionSpinBox.setRange(0, 100)
        precisionSpinBox.setValue(2)

        doubleLabel = QLabel("Enter a value between %d and %d:" % (-20, 20))
        self.doubleSpinBox = QDoubleSpinBox()
        self.doubleSpinBox.setRange(-20.0, 20.0)
        self.doubleSpinBox.setSingleStep(1.0)
        self.doubleSpinBox.setValue(0.0)

        scaleLabel = QLabel("Enter a scale factor between %d and %d:" % (0, 1000))
        self.scaleSpinBox = QDoubleSpinBox()
        self.scaleSpinBox.setRange(0.0, 1000.0)
        self.scaleSpinBox.setSingleStep(10.0)
        self.scaleSpinBox.setSuffix('%')
        self.scaleSpinBox.setSpecialValueText("No scaling")
        self.scaleSpinBox.setValue(100.0)

        priceLabel = QLabel("Enter a price between %d and %d:" % (0, 1000))
        self.priceSpinBox = QDoubleSpinBox()
        self.priceSpinBox.setRange(0.0, 1000.0)
        self.priceSpinBox.setSingleStep(1.0)
        self.priceSpinBox.setPrefix('$')
        self.priceSpinBox.setValue(99.99)

        precisionSpinBox.valueChanged.connect(self.changePrecision)

        spinBoxLayout = QVBoxLayout()
        spinBoxLayout.addWidget(precisionLabel)
        spinBoxLayout.addWidget(precisionSpinBox)
        spinBoxLayout.addWidget(doubleLabel)
        spinBoxLayout.addWidget(self.doubleSpinBox)
        spinBoxLayout.addWidget(scaleLabel)
        spinBoxLayout.addWidget(self.scaleSpinBox)
        spinBoxLayout.addWidget(priceLabel)
        spinBoxLayout.addWidget(self.priceSpinBox)
        self.doubleSpinBoxesGroup.setLayout(spinBoxLayout)

    def changePrecision(self, decimals):
        self.doubleSpinBox.setDecimals(decimals)
        self.scaleSpinBox.setDecimals(decimals)
        self.priceSpinBox.setDecimals(decimals)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)    
    window = Window()
    window.show()    
    sys.exit(app.exec_())
