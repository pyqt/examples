#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2015 Riverbank Computing Limited.
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


import sys

from PyQt5.QtCore import pyqtSignal, QFileInfo, QPoint, QSize, Qt, QTimer
from PyQt5.QtGui import (QColor, QImage, QMatrix4x4, QOpenGLShader,
        QOpenGLShaderProgram, QOpenGLTexture, QSurfaceFormat)
from PyQt5.QtWidgets import QApplication, QGridLayout, QOpenGLWidget, QWidget


class GLWidget(QOpenGLWidget):

    clicked = pyqtSignal()

    PROGRAM_VERTEX_ATTRIBUTE, PROGRAM_TEXCOORD_ATTRIBUTE = range(2)

    vsrc = """
attribute highp vec4 vertex;
attribute mediump vec4 texCoord;
varying mediump vec4 texc;
uniform mediump mat4 matrix;
void main(void)
{
    gl_Position = matrix * vertex;
    texc = texCoord;
}
"""

    fsrc = """
uniform sampler2D texture;
varying mediump vec4 texc;
void main(void)
{
    gl_FragColor = texture2D(texture, texc.st);
}
"""

    coords = (
        (( +1, -1, -1 ), ( -1, -1, -1 ), ( -1, +1, -1 ), ( +1, +1, -1 )),
        (( +1, +1, -1 ), ( -1, +1, -1 ), ( -1, +1, +1 ), ( +1, +1, +1 )),
        (( +1, -1, +1 ), ( +1, -1, -1 ), ( +1, +1, -1 ), ( +1, +1, +1 )),
        (( -1, -1, -1 ), ( -1, -1, +1 ), ( -1, +1, +1 ), ( -1, +1, -1 )),
        (( +1, -1, +1 ), ( -1, -1, +1 ), ( -1, -1, -1 ), ( +1, -1, -1 )),
        (( -1, -1, +1 ), ( +1, -1, +1 ), ( +1, +1, +1 ), ( -1, +1, +1 ))
    )

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.clearColor = QColor(Qt.black)
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.program = None

        self.lastPos = QPoint()

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(200, 200)

    def rotateBy(self, xAngle, yAngle, zAngle):
        self.xRot += xAngle
        self.yRot += yAngle
        self.zRot += zAngle
        self.update()

    def setClearColor(self, color):
        self.clearColor = color
        self.update()

    def initializeGL(self):
        self.gl = self.context().versionFunctions()
        self.gl.initializeOpenGLFunctions()

        self.makeObject()

        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        self.gl.glEnable(self.gl.GL_CULL_FACE)

        vshader = QOpenGLShader(QOpenGLShader.Vertex, self)
        vshader.compileSourceCode(self.vsrc)

        fshader = QOpenGLShader(QOpenGLShader.Fragment, self)
        fshader.compileSourceCode(self.fsrc)

        self.program = QOpenGLShaderProgram()
        self.program.addShader(vshader)
        self.program.addShader(fshader)
        self.program.bindAttributeLocation('vertex',
                self.PROGRAM_VERTEX_ATTRIBUTE)
        self.program.bindAttributeLocation('texCoord',
                self.PROGRAM_TEXCOORD_ATTRIBUTE)
        self.program.link()

        self.program.bind()
        self.program.setUniformValue('texture', 0)

        self.program.enableAttributeArray(self.PROGRAM_VERTEX_ATTRIBUTE)
        self.program.enableAttributeArray(self.PROGRAM_TEXCOORD_ATTRIBUTE)
        self.program.setAttributeArray(self.PROGRAM_VERTEX_ATTRIBUTE,
                self.vertices)
        self.program.setAttributeArray(self.PROGRAM_TEXCOORD_ATTRIBUTE,
                self.texCoords)

    def paintGL(self):
        self.gl.glClearColor(self.clearColor.redF(), self.clearColor.greenF(),
                self.clearColor.blueF(), self.clearColor.alphaF())
        self.gl.glClear(
                self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)

        m = QMatrix4x4()
        m.ortho(-0.5, 0.5, 0.5, -0.5, 4.0, 15.0)
        m.translate(0.0, 0.0, -10.0)
        m.rotate(self.xRot / 16.0, 1.0, 0.0, 0.0)
        m.rotate(self.yRot / 16.0, 0.0, 1.0, 0.0)
        m.rotate(self.zRot / 16.0, 0.0, 0.0, 1.0)

        self.program.setUniformValue('matrix', m)

        for i, texture in enumerate(self.textures):
            texture.bind()
            self.gl.glDrawArrays(self.gl.GL_TRIANGLE_FAN, i * 4, 4)

    def resizeGL(self, width, height):
        side = min(width, height)
        self.gl.glViewport((width - side) // 2, (height - side) // 2, side,
                side)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.rotateBy(8 * dy, 8 * dx, 0)
        elif event.buttons() & Qt.RightButton:
            self.rotateBy(8 * dy, 0, 8 * dx)

        self.lastPos = event.pos()

    def mouseReleaseEvent(self, event):
        self.clicked.emit()

    def makeObject(self):
        self.textures = []
        self.texCoords = []
        self.vertices = []

        root = QFileInfo(__file__).absolutePath()

        for i in range(6):
            self.textures.append(
                    QOpenGLTexture(
                            QImage(root + ('/images/side%d.png' % (i + 1))).mirrored()))

            for j in range(4):
                self.texCoords.append(((j == 0 or j == 3), (j == 0 or j == 1)))

                x, y, z = self.coords[i][j]
                self.vertices.append((0.2 * x, 0.2 * y, 0.2 * z))


class Window(QWidget):
    NumRows = 2
    NumColumns = 3

    def __init__(self):
        super(Window, self).__init__()

        self.glWidgets = []

        mainLayout = QGridLayout()

        for i in range(Window.NumRows):
            row = []

            for j in range(Window.NumColumns):
                clearColor = QColor()
                clearColor.setHsv(((i * Window.NumColumns) + j) * 255
                                  / (Window.NumRows * Window.NumColumns - 1),
                                  255, 63)

                widget = GLWidget()
                widget.setClearColor(clearColor)
                widget.rotateBy(+42 * 16, +42 * 16, -21 * 16)
                mainLayout.addWidget(widget, i, j)

                widget.clicked.connect(self.setCurrentGlWidget)

                row.append(widget)

            self.glWidgets.append(row)

        self.setLayout(mainLayout)

        self.currentGlWidget = self.glWidgets[0][0]

        timer = QTimer(self)
        timer.timeout.connect(self.rotateOneStep)
        timer.start(20)

        self.setWindowTitle("Textures")

    def setCurrentGlWidget(self):
        self.currentGlWidget = self.sender()

    def rotateOneStep(self):
        if self.currentGlWidget:
            self.currentGlWidget.rotateBy(+2 * 16, +2 * 16, -1 * 16)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    format = QSurfaceFormat()
    format.setDepthBufferSize(24)
    QSurfaceFormat.setDefaultFormat(format)

    window = Window()
    window.show()
    sys.exit(app.exec_())
