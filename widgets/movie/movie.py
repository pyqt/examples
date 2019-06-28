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


from PyQt5.QtCore import QFileInfo, QSize, Qt
from PyQt5.QtGui import QMovie, QPalette
from PyQt5.QtWidgets import (QApplication, QCheckBox, QFileDialog, QGridLayout,
        QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpinBox, QStyle,
        QToolButton, QVBoxLayout, QWidget)


class MoviePlayer(QWidget):
    def __init__(self, parent=None):
        super(MoviePlayer, self).__init__(parent)

        self.movie = QMovie(self)
        self.movie.setCacheMode(QMovie.CacheAll)

        self.movieLabel = QLabel("No movie loaded")
        self.movieLabel.setAlignment(Qt.AlignCenter)
        self.movieLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.movieLabel.setBackgroundRole(QPalette.Dark)
        self.movieLabel.setAutoFillBackground(True)

        self.currentMovieDirectory = ''

        self.createControls()
        self.createButtons()

        self.movie.frameChanged.connect(self.updateFrameSlider)
        self.movie.stateChanged.connect(self.updateButtons)
        self.fitCheckBox.clicked.connect(self.fitToWindow)
        self.frameSlider.valueChanged.connect(self.goToFrame)
        self.speedSpinBox.valueChanged.connect(self.movie.setSpeed)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.movieLabel)
        mainLayout.addLayout(self.controlsLayout)
        mainLayout.addLayout(self.buttonsLayout)
        self.setLayout(mainLayout)

        self.updateFrameSlider()
        self.updateButtons()

        self.setWindowTitle("Movie Player")
        self.resize(400, 400)

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open a Movie",
                self.currentMovieDirectory)

        if fileName:
            self.openFile(fileName)

    def openFile(self, fileName):
        self.currentMovieDirectory = QFileInfo(fileName).path()

        self.movie.stop()
        self.movieLabel.setMovie(self.movie)
        self.movie.setFileName(fileName)
        self.movie.start()

        self.updateFrameSlider();
        self.updateButtons();

    def goToFrame(self, frame):
        self.movie.jumpToFrame(frame)

    def fitToWindow(self):
        self.movieLabel.setScaledContents(self.fitCheckBox.isChecked())

    def updateFrameSlider(self):
        hasFrames = (self.movie.currentFrameNumber() >= 0)

        if hasFrames:
            if self.movie.frameCount() > 0:
                self.frameSlider.setMaximum(self.movie.frameCount() - 1)
            elif self.movie.currentFrameNumber() > self.frameSlider.maximum():
                self.frameSlider.setMaximum(self.movie.currentFrameNumber())

            self.frameSlider.setValue(self.movie.currentFrameNumber())
        else:
            self.frameSlider.setMaximum(0)

        self.frameLabel.setEnabled(hasFrames)
        self.frameSlider.setEnabled(hasFrames)

    def updateButtons(self):
        state = self.movie.state()

        self.playButton.setEnabled(self.movie.isValid() and
                self.movie.frameCount() != 1 and state == QMovie.NotRunning)
        self.pauseButton.setEnabled(state != QMovie.NotRunning)
        self.pauseButton.setChecked(state == QMovie.Paused)
        self.stopButton.setEnabled(state != QMovie.NotRunning)

    def createControls(self):
        self.fitCheckBox = QCheckBox("Fit to Window")

        self.frameLabel = QLabel("Current frame:")

        self.frameSlider = QSlider(Qt.Horizontal)
        self.frameSlider.setTickPosition(QSlider.TicksBelow)
        self.frameSlider.setTickInterval(10)

        speedLabel = QLabel("Speed:")

        self.speedSpinBox = QSpinBox()
        self.speedSpinBox.setRange(1, 9999)
        self.speedSpinBox.setValue(100)
        self.speedSpinBox.setSuffix("%")

        self.controlsLayout = QGridLayout()
        self.controlsLayout.addWidget(self.fitCheckBox, 0, 0, 1, 2)
        self.controlsLayout.addWidget(self.frameLabel, 1, 0)
        self.controlsLayout.addWidget(self.frameSlider, 1, 1, 1, 2)
        self.controlsLayout.addWidget(speedLabel, 2, 0)
        self.controlsLayout.addWidget(self.speedSpinBox, 2, 1)

    def createButtons(self):
        iconSize = QSize(36, 36)

        openButton = QToolButton()
        openButton.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        openButton.setIconSize(iconSize)
        openButton.setToolTip("Open File")
        openButton.clicked.connect(self.open)

        self.playButton = QToolButton()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.setIconSize(iconSize)
        self.playButton.setToolTip("Play")
        self.playButton.clicked.connect(self.movie.start)

        self.pauseButton = QToolButton()
        self.pauseButton.setCheckable(True)
        self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.pauseButton.setIconSize(iconSize)
        self.pauseButton.setToolTip("Pause")
        self.pauseButton.clicked.connect(self.movie.setPaused)

        self.stopButton = QToolButton()
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopButton.setIconSize(iconSize)
        self.stopButton.setToolTip("Stop")
        self.stopButton.clicked.connect(self.movie.stop)

        quitButton = QToolButton()
        quitButton.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        quitButton.setIconSize(iconSize)
        quitButton.setToolTip("Quit")
        quitButton.clicked.connect(self.close)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addStretch()
        self.buttonsLayout.addWidget(openButton)
        self.buttonsLayout.addWidget(self.playButton)
        self.buttonsLayout.addWidget(self.pauseButton)
        self.buttonsLayout.addWidget(self.stopButton)
        self.buttonsLayout.addWidget(quitButton)
        self.buttonsLayout.addStretch()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    player = MoviePlayer()
    player.show()
    sys.exit(app.exec_())
