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
import QtQuick.Particles 2.0

Item {
    id: window
    width: 320; height: 480

    // Let's draw the sky...
    Rectangle {
        anchors { left: parent.left; top: parent.top; right: parent.right; bottom: parent.verticalCenter }
        //! [0]
        gradient: Gradient {
            GradientStop {
                position: 0.0
                SequentialAnimation on color {
                    loops: Animation.Infinite
                    ColorAnimation { from: "DeepSkyBlue"; to: "#0E1533"; duration: 5000 }
                    ColorAnimation { from: "#0E1533"; to: "DeepSkyBlue"; duration: 5000 }
                }
            }
            GradientStop {
                position: 1.0
                SequentialAnimation on color {
                    loops: Animation.Infinite
                    ColorAnimation { from: "SkyBlue"; to: "#437284"; duration: 5000 }
                    ColorAnimation { from: "#437284"; to: "SkyBlue"; duration: 5000 }
                }
            }
        }
        //! [0]
    }

    // the sun, moon, and stars
    Item {
        width: parent.width; height: 2 * parent.height
        NumberAnimation on rotation { from: 0; to: 360; duration: 10000; loops: Animation.Infinite }
        Image {
            source: "images/sun.png"; y: 10; anchors.horizontalCenter: parent.horizontalCenter
            rotation: -3 * parent.rotation
        }
        Image {
            source: "images/moon.png"; y: parent.height - 74; anchors.horizontalCenter: parent.horizontalCenter
            rotation: -parent.rotation
        }
        ParticleSystem {
            id: particlesystem
            x: 0; y: parent.height/2
            width: parent.width; height: parent.height/2
            ImageParticle {
                source: "images/star.png"
                groups: ["star"]
                color: "#00333333"
                SequentialAnimation on opacity {
                    loops: Animation.Infinite
                    NumberAnimation { from: 0; to: 1; duration: 5000 }
                    NumberAnimation { from: 1; to: 0; duration: 5000 }
                }
            }
            Emitter {
                group: "star"
                anchors.fill: parent
                emitRate: parent.width / 50
                lifeSpan: 5000
            }
        }
    }

    // ...and the ground.
    Rectangle {
        anchors { left: parent.left; top: parent.verticalCenter; right: parent.right; bottom: parent.bottom }
        gradient: Gradient {
            GradientStop {
                position: 0.0
                SequentialAnimation on color {
                    loops: Animation.Infinite
                    ColorAnimation { from: "ForestGreen"; to: "#001600"; duration: 5000 }
                    ColorAnimation { from: "#001600"; to: "ForestGreen"; duration: 5000 }
                }
            }
            GradientStop { position: 1.0; color: "DarkGreen" }
        }
    }
}
