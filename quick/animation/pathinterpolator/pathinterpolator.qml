/****************************************************************************
**
** Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
** Contact: http://www.qt-project.org/legal
**
** This file is part of the examples of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** You may use this file under the terms of the BSD license as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of Digia Plc and its Subsidiary(-ies) nor the names
**     of its contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

import QtQuick 2.0

Rectangle {
    id: window
    width: 320
    height: 480

    Canvas {
        id: canvas
        anchors.fill: parent
        antialiasing: true

        onPaint: {
            var context = canvas.getContext("2d")
            context.clearRect(0, 0, width, height)
            context.strokeStyle = "black"
            context.path = motionPath.path
            context.stroke()
        }
    }

    //! [0]
    PathInterpolator {
        id: motionPath

        path: Path {
            startX: 50; startY: 50

            PathCubic {
                x: window.width - 50
                y: window.height - 50

                control1X: x; control1Y: 50
                control2X: 50; control2Y: y
            }

            onChanged: canvas.requestPaint()
        }

        SequentialAnimation on progress {
            running: true
            loops: -1
            PauseAnimation { duration: 1000 }
            NumberAnimation {
                id: progressAnim
                running: false
                from: 0; to: 1
                duration: 2000
                easing.type: Easing.InQuad
            }
        }
    }
    //! [0]

    Rectangle {
        id: box

        width: 50; height: 50
        border.width: 1
        antialiasing: true

        //bind our attributes to follow the path as progress changes
        x: motionPath.x
        y: motionPath.y
        rotation: motionPath.angle
        transform: Translate { x: -box.width/2; y: -box.height/2 }

        Text {
            anchors.centerIn: parent
            text: "Box"
        }
    }
}
