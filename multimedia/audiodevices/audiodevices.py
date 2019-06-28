#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
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


from PyQt5.QtMultimedia import QAudio, QAudioDeviceInfo, QAudioFormat
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMainWindow

from ui_audiodevicesbase import Ui_AudioDevicesBase


class AudioDevicesBase(QMainWindow, Ui_AudioDevicesBase):

    def __init__(self, parent=None):
        super(AudioDevicesBase, self).__init__(parent)

        self.setupUi(self)


class AudioTest(AudioDevicesBase):

    def __init__(self, parent=None):
        super(AudioTest, self).__init__(parent)

        self.deviceInfo = QAudioDeviceInfo()
        self.settings = QAudioFormat()
        self.mode = QAudio.AudioOutput

        self.testButton.clicked.connect(self.test)
        self.modeBox.activated.connect(self.modeChanged)
        self.deviceBox.activated.connect(self.deviceChanged)
        self.sampleRateBox.activated.connect(self.sampleRateChanged)
        self.channelsBox.activated.connect(self.channelChanged)
        self.codecsBox.activated.connect(self.codecChanged)
        self.sampleSizesBox.activated.connect(self.sampleSizeChanged)
        self.sampleTypesBox.activated.connect(self.sampleTypeChanged)
        self.endianBox.activated.connect(self.endianChanged)
        self.populateTableButton.clicked.connect(self.populateTable)

        self.modeBox.setCurrentIndex(0)
        self.modeChanged(0)
        self.deviceBox.setCurrentIndex(0)
        self.deviceChanged(0)

    def test(self):
        self.testResult.clear()

        if not self.deviceInfo.isNull():
            if self.deviceInfo.isFormatSupported(self.settings):
                self.testResult.setText("Success")
                self.nearestSampleRate.setText("")
                self.nearestChannel.setText("")
                self.nearestCodec.setText("")
                self.nearestSampleSize.setText("")
                self.nearestSampleType.setText("")
                self.nearestEndian.setText("")
            else:
                nearest = self.deviceInfo.nearestFormat(self.settings)
                self.testResult.setText("Failed")
                self.nearestSampleRate.setText(str(nearest.sampleRate()))
                self.nearestChannel.setText(str(nearest.channelCount()))
                self.nearestCodec.setText(nearest.codec())
                self.nearestSampleSize.setText(str(nearest.sampleSize()))
                self.nearestSampleType.setText(
                        self.sampleTypeToString(nearest.sampleType()))
                self.nearestEndian.setText(
                        self.endianToString(nearest.byteOrder()))
        else:
            self.testResult.setText("No Device")

    sampleTypeMap = {
        QAudioFormat.SignedInt: "SignedInt",
        QAudioFormat.UnSignedInt: "UnSignedInt",
        QAudioFormat.Float: "Float"
    }

    @classmethod
    def sampleTypeToString(cls, sampleType):
        return cls.sampleTypeMap.get(sampleType, "Unknown")

    endianMap = {
        QAudioFormat.LittleEndian: "LittleEndian",
        QAudioFormat.BigEndian: "BigEndian"
    }

    @classmethod
    def endianToString(cls, endian):
        return cls.endianMap.get(endian, "Unknown")

    def modeChanged(self, idx):
        self.testResult.clear()

        if idx == 0:
            self.mode = QAudio.AudioInput
        else:
            self.mode = QAudio.AudioOutput

        self.deviceBox.clear()
        for deviceInfo in QAudioDeviceInfo.availableDevices(self.mode):
            self.deviceBox.addItem(deviceInfo.deviceName(), deviceInfo)

        self.deviceBox.setCurrentIndex(0)
        self.deviceChanged(0)

    def deviceChanged(self, idx):
        self.testResult.clear()

        if self.deviceBox.count() == 0:
            return

        self.deviceInfo = self.deviceBox.itemData(idx)

        self.sampleRateBox.clear()
        sampleRatez = self.deviceInfo.supportedSampleRates()
        self.sampleRateBox.addItems([str(sr) for sr in sampleRatez])
        if len(sampleRatez) != 0:
            self.settings.setSampleRate(sampleRatez[0])

        self.channelsBox.clear()
        chz = self.deviceInfo.supportedChannelCounts()
        self.channelsBox.addItems([str(ch) for ch in chz])
        if len(chz) != 0:
            self.settings.setChannelCount(chz[0])

        self.codecsBox.clear()
        codecs = self.deviceInfo.supportedCodecs()
        self.codecsBox.addItems([str(c) for c in codecs])
        if len(codecs) != 0:
            self.settings.setCodec(codecs[0])

        # Create a failed condition.
        self.codecsBox.addItem("audio/test")

        self.sampleSizesBox.clear()
        sampleSizez = self.deviceInfo.supportedSampleSizes()
        self.sampleSizesBox.addItems([str(ss) for ss in sampleSizez])
        if len(sampleSizez) != 0:
            self.settings.setSampleSize(sampleSizez[0])

        self.sampleTypesBox.clear()
        sampleTypez = self.deviceInfo.supportedSampleTypes()
        self.sampleTypesBox.addItems(
                [self.sampleTypeToString(st) for st in sampleTypez])
        if len(sampleTypez) != 0:
            self.settings.setSampleType(sampleTypez[0])

        self.endianBox.clear()
        endianz = self.deviceInfo.supportedByteOrders()
        self.endianBox.addItems([self.endianToString(e) for e in endianz])
        if len(endianz) != 0:
            self.settings.setByteOrder(endianz[0])

        self.allFormatsTable.clearContents()

    def populateTable(self):
        row = 0
        format = QAudioFormat()

        for codec in self.deviceInfo.supportedCodecs():
            format.setCodec(codec)

            for sampleRate in self.deviceInfo.supportedSampleRates():
                format.setSampleRate(sampleRate)

                for channels in self.deviceInfo.supportedChannelCounts():
                    format.setChannelCount(channels)

                    for sampleType in self.deviceInfo.supportedSampleTypes():
                        format.setSampleType(sampleType)

                        for sampleSize in self.deviceInfo.supportedSampleSizes():
                            format.setSampleSize(sampleSize)

                            for endian in self.deviceInfo.supportedByteOrders():
                                format.setByteOrder(endian)

                                if self.deviceInfo.isFormatSupported(format):
                                    self.allFormatsTable.setRowCount(row + 1)

                                    self.setFormatValue(row, 0, format.codec())
                                    self.setFormatValue(row, 1,
                                            str(format.sampleRate()))
                                    self.setFormatValue(row, 2,
                                            str(format.channelCount()))
                                    self.setFormatValue(row, 3,
                                            self.sampleTypeToString(
                                                    format.sampleType()))
                                    self.setFormatValue(row, 4,
                                            str(format.sampleSize()))
                                    self.setFormatValue(row, 5,
                                            self.endianToString(
                                                    format.byteOrder()))

                                    row += 1

    def setFormatValue(self, row, column, value):
        self.allFormatsTable.setItem(row, column, QTableWidgetItem(value))

    def sampleRateChanged(self, idx):
        self.settings.setSampleRate(int(self.sampleRateBox.itemText(idx)))

    def channelChanged(self, idx):
        self.settings.setChannelCount(int(self.channelsBox.itemText(idx)))

    def codecChanged(self, idx):
        self.settings.setCodec(self.codecsBox.itemText(idx))

    def sampleSizeChanged(self, idx):
        self.settings.setSampleSize(int(self.sampleSizesBox.itemText(idx)))

    def sampleTypeChanged(self, idx):
        sampleType = int(self.sampleTypesBox.itemText(idx))

        if sampleType == QAudioFormat.SignedInt:
            self.settings.setSampleType(QAudioFormat.SignedInt)
        elif sampleType == QAudioFormat.UnSignedInt:
            self.settings.setSampleType(QAudioFormat.UnSignedInt)
        elif sampleType == QAudioFormat.Float:
            self.settings.setSampleType(QAudioFormat.Float)

    def endianChanged(self, idx):
        endian = int(self.endianBox.itemText(idx))

        if endian == QAudioFormat.LittleEndian:
            self.settings.setByteOrder(QAudioFormat.LittleEndian)
        elif endian == QAudioFormat.BigEndian:
            self.settings.setByteOrder(QAudioFormat.BigEndian)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("Audio Device Test")

    audio = AudioTest()
    audio.show()

    sys.exit(app.exec_())
