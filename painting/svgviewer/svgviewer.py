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


from PyQt5.QtCore import QFile, QSize, Qt
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPixmap, QPen
from PyQt5.QtWidgets import (QActionGroup, QApplication, QFileDialog,
        QGraphicsItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView,
        QMainWindow, QMenu, QMessageBox, QWidget)
from PyQt5.QtOpenGL import QGL, QGLFormat, QGLWidget
from PyQt5.QtSvg import QGraphicsSvgItem

import svgviewer_rc


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.currentPath = ''

        self.view = SvgView()

        fileMenu = QMenu("&File", self)
        openAction = fileMenu.addAction("&Open...")
        openAction.setShortcut("Ctrl+O")
        quitAction = fileMenu.addAction("E&xit")
        quitAction.setShortcut("Ctrl+Q")

        self.menuBar().addMenu(fileMenu)

        viewMenu = QMenu("&View", self)
        self.backgroundAction = viewMenu.addAction("&Background")
        self.backgroundAction.setEnabled(False)
        self.backgroundAction.setCheckable(True)
        self.backgroundAction.setChecked(False)
        self.backgroundAction.toggled.connect(self.view.setViewBackground)

        self.outlineAction = viewMenu.addAction("&Outline")
        self.outlineAction.setEnabled(False)
        self.outlineAction.setCheckable(True)
        self.outlineAction.setChecked(True)
        self.outlineAction.toggled.connect(self.view.setViewOutline)

        self.menuBar().addMenu(viewMenu)

        rendererMenu = QMenu("&Renderer", self)
        self.nativeAction = rendererMenu.addAction("&Native")
        self.nativeAction.setCheckable(True)
        self.nativeAction.setChecked(True)

        if QGLFormat.hasOpenGL():
            self.glAction = rendererMenu.addAction("&OpenGL")
            self.glAction.setCheckable(True)

        self.imageAction = rendererMenu.addAction("&Image")
        self.imageAction.setCheckable(True)

        if QGLFormat.hasOpenGL():
            rendererMenu.addSeparator()
            self.highQualityAntialiasingAction = rendererMenu.addAction("&High Quality Antialiasing")
            self.highQualityAntialiasingAction.setEnabled(False)
            self.highQualityAntialiasingAction.setCheckable(True)
            self.highQualityAntialiasingAction.setChecked(False)
            self.highQualityAntialiasingAction.toggled.connect(self.view.setHighQualityAntialiasing)

        rendererGroup = QActionGroup(self)
        rendererGroup.addAction(self.nativeAction)

        if QGLFormat.hasOpenGL():
            rendererGroup.addAction(self.glAction)

        rendererGroup.addAction(self.imageAction)

        self.menuBar().addMenu(rendererMenu)

        openAction.triggered.connect(self.openFile)
        quitAction.triggered.connect(QApplication.instance().quit)
        rendererGroup.triggered.connect(self.setRenderer)

        self.setCentralWidget(self.view)
        self.setWindowTitle("SVG Viewer")

    def openFile(self, path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Open SVG File",
                    self.currentPath, "SVG files (*.svg *.svgz *.svg.gz)")

        if path:
            svg_file = QFile(path)
            if not svg_file.exists():
                QMessageBox.critical(self, "Open SVG File",
                        "Could not open file '%s'." % path)

                self.outlineAction.setEnabled(False)
                self.backgroundAction.setEnabled(False)
                return

            self.view.openFile(svg_file)

            if not path.startswith(':/'):
                self.currentPath = path
                self.setWindowTitle("%s - SVGViewer" % self.currentPath)

            self.outlineAction.setEnabled(True)
            self.backgroundAction.setEnabled(True)

            self.resize(self.view.sizeHint() + QSize(80, 80 + self.menuBar().height()))

    def setRenderer(self, action):
        if QGLFormat.hasOpenGL():
            self.highQualityAntialiasingAction.setEnabled(False)

        if action == self.nativeAction:
            self.view.setRenderer(SvgView.Native)
        elif action == self.glAction:
            if QGLFormat.hasOpenGL():
                self.highQualityAntialiasingAction.setEnabled(True)
                self.view.setRenderer(SvgView.OpenGL)
        elif action == self.imageAction:
            self.view.setRenderer(SvgView.Image)


class SvgView(QGraphicsView):
    Native, OpenGL, Image = range(3)

    def __init__(self, parent=None):
        super(SvgView, self).__init__(parent)

        self.renderer = SvgView.Native
        self.svgItem = None
        self.backgroundItem = None
        self.outlineItem = None
        self.image = QImage()

        self.setScene(QGraphicsScene(self))
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        # Prepare background check-board pattern.
        tilePixmap = QPixmap(64, 64)
        tilePixmap.fill(Qt.white)
        tilePainter = QPainter(tilePixmap)
        color = QColor(220, 220, 220)
        tilePainter.fillRect(0, 0, 32, 32, color)
        tilePainter.fillRect(32, 32, 32, 32, color)
        tilePainter.end()

        self.setBackgroundBrush(QBrush(tilePixmap))

    def drawBackground(self, p, rect):
        p.save()
        p.resetTransform()
        p.drawTiledPixmap(self.viewport().rect(),
                self.backgroundBrush().texture())
        p.restore()

    def openFile(self, svg_file):
        if not svg_file.exists():
            return

        s = self.scene()

        if self.backgroundItem:
            drawBackground = self.backgroundItem.isVisible()
        else:
            drawBackground = False

        if self.outlineItem:
            drawOutline = self.outlineItem.isVisible()
        else:
            drawOutline = True

        s.clear()
        self.resetTransform()

        self.svgItem = QGraphicsSvgItem(svg_file.fileName())
        self.svgItem.setFlags(QGraphicsItem.ItemClipsToShape)
        self.svgItem.setCacheMode(QGraphicsItem.NoCache)
        self.svgItem.setZValue(0)

        self.backgroundItem = QGraphicsRectItem(self.svgItem.boundingRect())
        self.backgroundItem.setBrush(Qt.white)
        self.backgroundItem.setPen(QPen(Qt.NoPen))
        self.backgroundItem.setVisible(drawBackground)
        self.backgroundItem.setZValue(-1)

        self.outlineItem = QGraphicsRectItem(self.svgItem.boundingRect())
        outline = QPen(Qt.black, 2, Qt.DashLine)
        outline.setCosmetic(True)
        self.outlineItem.setPen(outline)
        self.outlineItem.setBrush(QBrush(Qt.NoBrush))
        self.outlineItem.setVisible(drawOutline)
        self.outlineItem.setZValue(1)

        s.addItem(self.backgroundItem)
        s.addItem(self.svgItem)
        s.addItem(self.outlineItem)

        s.setSceneRect(self.outlineItem.boundingRect().adjusted(-10, -10, 10, 10))

    def setRenderer(self, renderer):
        self.renderer = renderer

        if self.renderer == SvgView.OpenGL:
            if QGLFormat.hasOpenGL():
                self.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))
        else:
            self.setViewport(QWidget())

    def setHighQualityAntialiasing(self, highQualityAntialiasing):
        if QGLFormat.hasOpenGL():
            self.setRenderHint(QPainter.HighQualityAntialiasing,
                    highQualityAntialiasing)

    def setViewBackground(self, enable):
        if self.backgroundItem:
            self.backgroundItem.setVisible(enable)

    def setViewOutline(self, enable):
        if self.outlineItem:
            self.outlineItem.setVisible(enable)

    def paintEvent(self, event):
        if self.renderer == SvgView.Image:
            if self.image.size() != self.viewport().size():
                self.image = QImage(self.viewport().size(),
                        QImage.Format_ARGB32_Premultiplied)

            imagePainter = QPainter(self.image)
            QGraphicsView.render(self, imagePainter)
            imagePainter.end()

            p = QPainter(self.viewport())
            p.drawImage(0, 0, self.image)
        else:
            super(SvgView, self).paintEvent(event)

    def wheelEvent(self, event):
        factor = pow(1.2, event.delta() / 240.0)
        self.scale(factor, factor)
        event.accept()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    window = MainWindow()
    if len(sys.argv) == 2:
        window.openFile(sys.argv[1])
    else:
        window.openFile(':/files/bubbles.svg')
    window.show()
    sys.exit(app.exec_())
