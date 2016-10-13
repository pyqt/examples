#!/usr/bin/env python
"""        
Capture a web page and save its internal frames in different images

  framecapture.py <url> <outputfile>

Notes:
  'url' is the URL of the web page to be captured
  'outputfile' is the prefix of the image files to be generated

Example:
  framecapture qt.nokia.com trolltech.png

Result:
  trolltech.png (full page)
  trolltech_frame1.png (...) trolltech_frameN.png ('N' number of internal frames)
"""


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited
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

import sys

from PyQt5.QtCore import pyqtSignal, QObject, QSize, Qt, QUrl
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKitWidgets import QWebPage


def cout(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def cerr(s):
    sys.stderr.write(s)
    sys.stderr.flush()


class FrameCapture(QObject):

    finished = pyqtSignal()

    def __init__(self):
        super(FrameCapture, self).__init__()

        self._percent = 0
        self._page = QWebPage()
        self._page.mainFrame().setScrollBarPolicy(Qt.Vertical,
                Qt.ScrollBarAlwaysOff)
        self._page.mainFrame().setScrollBarPolicy(Qt.Horizontal,
                Qt.ScrollBarAlwaysOff)
        self._page.loadProgress.connect(self.printProgress)
        self._page.loadFinished.connect(self.saveResult)
 
    def load(self, url, outputFileName):
        cout("Loading %s\n" % url.toString())
        self._percent = 0
        index = outputFileName.rfind('.')
        self._fileName = index == -1 and outputFileName + ".png" or outputFileName
        self._page.mainFrame().load(url)
        self._page.setViewportSize(QSize(1024, 768))
 
    def printProgress(self, percent):
        if self._percent >= percent:
            return
        self._percent += 1
        while self._percent < percent:
            self._percent += 1
            cout("#")
 
    def saveResult(self, ok):
        cout("\n")
        # Crude error-checking.
        if not ok:
            cerr("Failed loading %s\n" % self._page.mainFrame().url().toString())
            self.finished.emit()
            return

        # Save each frame in different image files.
        self._frameCounter = 0
        self.saveFrame(self._page.mainFrame())
        self.finished.emit()
 
    def saveFrame(self, frame):
        fileName = self._fileName
        if self._frameCounter:
            index = fileName.rfind('.')
            fileName = "%s_frame%s%s" % (fileName[:index], self._frameCounter, fileName[index:])
        image = QImage(frame.contentsSize(), QImage.Format_ARGB32_Premultiplied)
        image.fill(Qt.transparent)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        frame.documentElement().render(painter)
        painter.end()
        image.save(fileName)
        self._frameCounter += 1
        for childFrame in frame.childFrames():
            self.saveFrame(childFrame)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        cerr(__doc__)
        sys.exit(1)

    url = QUrl.fromUserInput(sys.argv[1])
    fileName = sys.argv[2]

    app = QApplication(sys.argv)

    capture = FrameCapture()
    capture.finished.connect(app.quit)
    capture.load(url, fileName)

    app.exec_()
