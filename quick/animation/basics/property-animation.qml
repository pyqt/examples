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

Item {
    id: window
    width: 320; height: 480

    // Let's draw the sky...
    Rectangle {
        anchors { left: parent.left; top: parent.top; right: parent.right; bottom: parent.verticalCenter }
        gradient: Gradient {
            GradientStop { position: 0.0; color: "DeepSkyBlue" }
            GradientStop { position: 1.0; color: "LightSkyBlue" }
        }
    }

    // ...and the ground.
    Rectangle {
        anchors { left: parent.left; top: parent.verticalCenter; right: parent.right; bottom: parent.bottom }
        gradient: Gradient {
            GradientStop { position: 0.0; color: "ForestGreen" }
            GradientStop { position: 1.0; color: "DarkGreen" }
        }
    }

    // The shadow for the smiley face
    Image {
        anchors.horizontalCenter: parent.horizontalCenter
        y: smiley.minHeight + 58
        source: "images/shadow.png"

        // The scale property depends on the y position of the smiley face.
        scale: smiley.y * 0.5 / (smiley.minHeight - smiley.maxHeight)
    }

    Image {
        id: smiley
        property int maxHeight: window.height / 3
        property int minHeight: 2 * window.height / 3

        anchors.horizontalCenter: parent.horizontalCenter
        y: minHeight
        source: "images/face-smile.png"

        //! [0]
        // Animate the y property. Setting loops to Animation.Infinite makes the
        // animation repeat indefinitely, otherwise it would only run once.
        SequentialAnimation on y {
            loops: Animation.Infinite

            // Move from minHeight to maxHeight in 300ms, using the OutExpo easing function
            NumberAnimation {
                from: smiley.minHeight; to: smiley.maxHeight
                easing.type: Easing.OutExpo; duration: 300
            }

            // Then move back to minHeight in 1 second, using the OutBounce easing function
            NumberAnimation {
                from: smiley.maxHeight; to: smiley.minHeight
                easing.type: Easing.OutBounce; duration: 1000
            }

            // Then pause for 500ms
            PauseAnimation { duration: 500 }
        }
        //! [0]
    }
}
