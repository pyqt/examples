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


from PyQt5.QtCore import QByteArray, qFuzzyCompare, Qt, QTimer
from PyQt5.QtGui import QPalette, QPixmap
from PyQt5.QtMultimedia import (QAudioEncoderSettings, QCamera,
        QCameraImageCapture, QImageEncoderSettings, QMediaMetaData,
        QMediaRecorder, QMultimedia, QVideoEncoderSettings)
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QDialog,
        QMainWindow, QMessageBox)

from ui_camera import Ui_Camera
from ui_imagesettings import Ui_ImageSettingsUi
from ui_videosettings import Ui_VideoSettingsUi


class ImageSettings(QDialog):

    def __init__(self, imageCapture, parent=None):
        super(ImageSettings, self).__init__(parent)

        self.ui = Ui_ImageSettingsUi()
        self.imagecapture = imageCapture

        self.ui.setupUi(self)

        self.ui.imageCodecBox.addItem("Default image format", "")
        for codecName in self.imagecapture.supportedImageCodecs():
            description = self.imagecapture.imageCodecDescription(codecName)
            self.ui.imageCodecBox.addItem(codecName + ": " + description,
                    codecName)

        self.ui.imageQualitySlider.setRange(0, QMultimedia.VeryHighQuality)

        self.ui.imageResolutionBox.addItem("Default resolution")
        supportedResolutions, _ = self.imagecapture.supportedResolutions()
        for resolution in supportedResolutions:
            self.ui.imageResolutionBox.addItem(
                    "%dx%d" % (resolution.width(), resolution.height()),
                    resolution)

    def imageSettings(self):
        settings = self.imagecapture.encodingSettings()
        settings.setCodec(self.boxValue(self.ui.imageCodecBox))
        settings.setQuality(
                QMultimedia.EncodingQuality(
                        self.ui.imageQualitySlider.value()))
        settings.setResolution(self.boxValue(self.ui.imageResolutionBox))

        return settings

    def setImageSettings(self, settings):
        self.selectComboBoxItem(self.ui.imageCodecBox, settings.codec())
        self.selectComboBoxItem(self.ui.imageResolutionBox,
                settings.resolution())
        self.ui.imageQualitySlider.setValue(settings.quality())

    @staticmethod
    def boxValue(box):
        idx = box.currentIndex()
        if idx == -1:
            return None

        return box.itemData(idx)

    @staticmethod
    def selectComboBoxItem(box, value):
        for i in range(box.count()):
            if box.itemData(i) == value:
                box.setCurrentIndex(i)
                break


class VideoSettings(QDialog):

    def __init__(self, mediaRecorder, parent=None):
        super(VideoSettings, self).__init__(parent)

        self.ui = Ui_VideoSettingsUi()
        self.mediaRecorder = mediaRecorder

        self.ui.setupUi(self)

        self.ui.audioCodecBox.addItem("Default audio codec", "")
        for codecName in self.mediaRecorder.supportedAudioCodecs():
            description = self.mediaRecorder.audioCodecDescription(codecName)
            self.ui.audioCodecBox.addItem(codecName + ": " + description,
                    codecName)

        supportedSampleRates, _ = self.mediaRecorder.supportedAudioSampleRates()
        for sampleRate in supportedSampleRates:
            self.ui.audioSampleRateBox.addItem(str(sampleRate), sampleRate)

        self.ui.audioQualitySlider.setRange(0, QMultimedia.VeryHighQuality)

        self.ui.videoCodecBox.addItem("Default video codec", "")
        for codecName in self.mediaRecorder.supportedVideoCodecs():
            description = self.mediaRecorder.videoCodecDescription(codecName)
            self.ui.videoCodecBox.addItem(codecName + ": " + description,
                    codecName)

        self.ui.videoQualitySlider.setRange(0, QMultimedia.VeryHighQuality)

        self.ui.videoResolutionBox.addItem("Default")
        supportedResolutions, _ = self.mediaRecorder.supportedResolutions()
        for resolution in supportedResolutions:
            self.ui.videoResolutionBox.addItem(
                    "%dx%d" % (resolution.width(), resolution.height()),
                    resolution)

        self.ui.videoFramerateBox.addItem("Default")
        supportedFrameRates, _ = self.mediaRecorder.supportedFrameRates()
        for rate in supportedFrameRates:
            self.ui.videoFramerateBox.addItem("%0.2f" % rate, rate)

        self.ui.containerFormatBox.addItem("Default container", "")
        for format in self.mediaRecorder.supportedContainers():
            self.ui.containerFormatBox.addItem(
                    format + ":" + self.mediaRecorder.containerDescription(
                            format),
                    format)

    def audioSettings(self):
        settings = self.mediaRecorder.audioSettings()
        settings.setCodec(self.boxValue(self.ui.audioCodecBox))
        settings.setQuality(
                QMultimedia.EncodingQuality(
                        self.ui.audioQualitySlider.value()))
        settings.setSampleRate(self.boxValue(self.ui.audioSampleRateBox))

        return settings

    def setAudioSettings(self, settings):
        self.selectComboBoxItem(self.ui.audioCodecBox, settings.codec())
        self.selectComboBoxItem(self.ui.audioSampleRateBox,
                settings.sampleRate())
        self.ui.audioQualitySlider.setValue(settings.quality())

    def videoSettings(self):
        settings = self.mediaRecorder.videoSettings()
        settings.setCodec(self.boxValue(self.ui.videoCodecBox))
        settings.setQuality(
                QMultimedia.EncodingQuality(
                        self.ui.videoQualitySlider.value()))
        settings.setResolution(self.boxValue(self.ui.videoResolutionBox))
        settings.setFrameRate(self.boxValue(self.ui.videoFramerateBox))

        return settings

    def setVideoSettings(self, settings):
        self.selectComboBoxItem(self.ui.videoCodecBox, settings.codec())
        self.selectComboBoxItem(self.ui.videoResolutionBox,
                settings.resolution())
        self.ui.videoQualitySlider.setValue(settings.quality())

        for i in range(1, self.ui.videoFramerateBox.count()):
            itemRate = self.ui.videoFramerateBox.itemData(i)
            if qFuzzyCompare(itemRate, settings.frameRate()):
                self.ui.videoFramerateBox.setCurrentIndex(i)
                break

    def format(self):
        return self.boxValue(self.ui.containerFormatBox)

    def setFormat(self, format):
        self.selectComboBoxItem(self.ui.containerFormatBox, format)

    @staticmethod
    def boxValue(box):
        idx = box.currentIndex()
        if idx == -1:
            return None

        return box.itemData(idx)

    @staticmethod
    def selectComboBoxItem(box, value):
        for i in range(box.count()):
            if box.itemData(i) == value:
                box.setCurrentIndex(i)
                break


class Camera(QMainWindow):

    def __init__(self, parent=None):
        super(Camera, self).__init__(parent)

        self.ui = Ui_Camera()
        self.camera = None
        self.imageCapture = None
        self.mediaRecorder = None
        self.isCapturingImage = False
        self.applicationExiting = False

        self.imageSettings = QImageEncoderSettings()
        self.audioSettings = QAudioEncoderSettings()
        self.videoSettings = QVideoEncoderSettings()
        self.videoContainerFormat = ''

        self.ui.setupUi(self)

        cameraDevice = QByteArray()

        videoDevicesGroup = QActionGroup(self)
        videoDevicesGroup.setExclusive(True)

        for deviceName in QCamera.availableDevices():
            description = QCamera.deviceDescription(deviceName)
            videoDeviceAction = QAction(description, videoDevicesGroup)
            videoDeviceAction.setCheckable(True)
            videoDeviceAction.setData(deviceName)

            if cameraDevice.isEmpty():
                cameraDevice = deviceName
                videoDeviceAction.setChecked(True)

            self.ui.menuDevices.addAction(videoDeviceAction)

        videoDevicesGroup.triggered.connect(self.updateCameraDevice)
        self.ui.captureWidget.currentChanged.connect(self.updateCaptureMode)

        self.ui.lockButton.hide()

        self.setCamera(cameraDevice)

    def setCamera(self, cameraDevice):
        if cameraDevice.isEmpty():
            self.camera = QCamera()
        else:
            self.camera = QCamera(cameraDevice)

        self.camera.stateChanged.connect(self.updateCameraState)
        self.camera.error.connect(self.displayCameraError)

        self.mediaRecorder = QMediaRecorder(self.camera)
        self.mediaRecorder.stateChanged.connect(self.updateRecorderState)

        self.imageCapture = QCameraImageCapture(self.camera)

        self.mediaRecorder.durationChanged.connect(self.updateRecordTime)
        self.mediaRecorder.error.connect(self.displayRecorderError)

        self.mediaRecorder.setMetaData(QMediaMetaData.Title, "Test Title")

        self.ui.exposureCompensation.valueChanged.connect(
                self.setExposureCompensation)

        self.camera.setViewfinder(self.ui.viewfinder)

        self.updateCameraState(self.camera.state())
        self.updateLockStatus(self.camera.lockStatus(), QCamera.UserRequest)
        self.updateRecorderState(self.mediaRecorder.state())

        self.imageCapture.readyForCaptureChanged.connect(self.readyForCapture)
        self.imageCapture.imageCaptured.connect(self.processCapturedImage)
        self.imageCapture.imageSaved.connect(self.imageSaved)

        self.camera.lockStatusChanged.connect(self.updateLockStatus)

        self.ui.captureWidget.setTabEnabled(0,
                self.camera.isCaptureModeSupported(QCamera.CaptureStillImage))
        self.ui.captureWidget.setTabEnabled(1,
                self.camera.isCaptureModeSupported(QCamera.CaptureVideo))

        self.updateCaptureMode()
        self.camera.start()

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return

        if event.key() == Qt.Key_CameraFocus:
            self.displayViewfinder()
            self.camera.searchAndLock()
            event.accept()
        elif event.key() == Qt.Key_Camera:
            if self.camera.captureMode() == QCamera.CaptureStillImage:
                self.takeImage()
            elif self.mediaRecorder.state() == QMediaRecorder.RecordingState:
                self.stop()
            else:
                self.record()

            event.accept()
        else:
            super(Camera, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return

        if event.key() == Qt.Key_CameraFocus:
            self.camera.unlock()
        else:
            super(Camera, self).keyReleaseEvent(event)

    def updateRecordTime(self):
        msg = "Recorded %d sec" % (self.mediaRecorder.duration() // 1000)
        self.ui.statusbar.showMessage(msg)

    def processCapturedImage(self, requestId, img):
        scaledImage = img.scaled(self.ui.viewfinder.size(), Qt.KeepAspectRatio,
                Qt.SmoothTransformation)

        self.ui.lastImagePreviewLabel.setPixmap(QPixmap.fromImage(scaledImage))

        self.displayCapturedImage()
        QTimer.singleShot(4000, self.displayViewfinder)

    def configureCaptureSettings(self):
        if self.camera.captureMode() == QCamera.CaptureStillImage:
            self.configureImageSettings()
        elif self.camera.captureMode() == QCamera.CaptureVideo:
            self.configureVideoSettings()

    def configureVideoSettings(self):
        settingsDialog = VideoSettings(self.mediaRecorder)

        settingsDialog.setAudioSettings(self.audioSettings)
        settingsDialog.setVideoSettings(self.videoSettings)
        settingsDialog.setFormat(self.videoContainerFormat)

        if settingsDialog.exec_():
            self.audioSettings = settingsDialog.audioSettings()
            self.videoSettings = settingsDialog.videoSettings()
            self.videoContainerFormat = settingsDialog.format()

            self.mediaRecorder.setEncodingSettings(self.audioSettings,
                    self.videoSettings, self.videoContainerFormat)

    def configureImageSettings(self):
        settingsDialog = ImageSettings(self.imageCapture)

        settingsDialog.setImageSettings(self.imageSettings)

        if settingsDialog.exec_():
            self.imageSettings = settingsDialog.imageSettings()
            self.imageCapture.setEncodingSettings(self.imageSettings)

    def record(self):
        self.mediaRecorder.record()
        self.updateRecordTime()

    def pause(self):
        self.mediaRecorder.pause()

    def stop(self):
        self.mediaRecorder.stop()

    def setMuted(self, muted):
        self.mediaRecorder.setMuted(muted)

    def toggleLock(self):
        if self.camera.lockStatus() in (QCamera.Searching, QCamera.Locked):
            self.camera.unlock()
        elif self.camera.lockStatus() == QCamera.Unlocked:
            self.camera.searchAndLock()

    def updateLockStatus(self, status, reason):
        indicationColor = Qt.black

        if status == QCamera.Searching:
            self.ui.statusbar.showMessage("Focusing...")
            self.ui.lockButton.setText("Focusing...")
            indicationColor = Qt.yellow
        elif status == QCamera.Locked:
            self.ui.lockButton.setText("Unlock")
            self.ui.statusbar.showMessage("Focused", 2000)
            indicationColor = Qt.darkGreen
        elif status == QCamera.Unlocked:
            self.ui.lockButton.setText("Focus")

            if reason == QCamera.LockFailed:
                self.ui.statusbar.showMessage("Focus Failed", 2000)
                indicationColor = Qt.red

        palette = self.ui.lockButton.palette()
        palette.setColor(QPalette.ButtonText, indicationColor)
        self.ui.lockButton.setPalette(palette)

    def takeImage(self):
        self.isCapturingImage = True
        self.imageCapture.capture()

    def startCamera(self):
        self.camera.start()

    def stopCamera(self):
        self.camera.stop()

    def updateCaptureMode(self):
        tabIndex = self.ui.captureWidget.currentIndex()
        captureMode = QCamera.CaptureStillImage if tabIndex == 0 else QCamera.CaptureVideo

        if self.camera.isCaptureModeSupported(captureMode):
            self.camera.setCaptureMode(captureMode)

    def updateCameraState(self, state):
        if state == QCamera.ActiveState:
            self.ui.actionStartCamera.setEnabled(False)
            self.ui.actionStopCamera.setEnabled(True)
            self.ui.captureWidget.setEnabled(True)
            self.ui.actionSettings.setEnabled(True)
        elif state in (QCamera.UnloadedState, QCamera.LoadedState):
            self.ui.actionStartCamera.setEnabled(True)
            self.ui.actionStopCamera.setEnabled(False)
            self.ui.captureWidget.setEnabled(False)
            self.ui.actionSettings.setEnabled(False)

    def updateRecorderState(self, state):
        if state == QMediaRecorder.StoppedState:
            self.ui.recordButton.setEnabled(True)
            self.ui.pauseButton.setEnabled(True)
            self.ui.stopButton.setEnabled(False)
        elif state == QMediaRecorder.PausedState:
            self.ui.recordButton.setEnabled(True)
            self.ui.pauseButton.setEnabled(False)
            self.ui.stopButton.setEnabled(True)
        elif state == QMediaRecorder.RecordingState:
            self.ui.recordButton.setEnabled(False)
            self.ui.pauseButton.setEnabled(True)
            self.ui.stopButton.setEnabled(True)

    def setExposureCompensation(self, index):
        self.camera.exposure().setExposureCompensation(index * 0.5)

    def displayRecorderError(self):
        QMessageBox.warning(self, "Capture error",
                self.mediaRecorder.errorString())

    def displayCameraError(self):
        QMessageBox.warning(self, "Camera error", self.camera.errorString())

    def updateCameraDevice(self, action):
        self.setCamera(action.data())

    def displayViewfinder(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def displayCapturedImage(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def readyForCapture(self, ready):
        self.ui.takeImageButton.setEnabled(ready)

    def imageSaved(self, id, fileName):
        self.isCapturingImage = False

        if self.applicationExiting:
            self.close()

    def closeEvent(self, event):
        if self.isCapturingImage:
            self.setEnabled(False)
            self.applicationExiting = True
            event.ignore()
        else:
            event.accept()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    camera = Camera()
    camera.show()

    sys.exit(app.exec_())
