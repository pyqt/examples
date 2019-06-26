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
    id: page
    width: 320; height: 480;
    color: "Black"

    // Make a ball to bounce
    Rectangle {
        id: ball

        // Add a property for the target y coordinate
        property variant direction : "right"

        x: 20; width: 20; height: 20; z: 1
        color: "Lime"

        // Move the ball to the right and back to the left repeatedly
        SequentialAnimation on x {
            loops: Animation.Infinite
            NumberAnimation { to: page.width - 40; duration: 2000 }
            PropertyAction { target: ball; property: "direction"; value: "left" }
            NumberAnimation { to: 20; duration: 2000 }
            PropertyAction { target: ball; property: "direction"; value: "right" }
        }

        // Make y move with a velocity of 200 
        Behavior on y { SpringAnimation{ velocity: 200; }
        }

        Component.onCompleted: y = page.height-10; // start the ball motion

        // Detect the ball hitting the top or bottom of the view and bounce it
        onYChanged: {
            if (y <= 0) {
                y = page.height - 20;
            } else if (y >= page.height - 20) {
                y = 0;
            }
        }
    }

    // Place bats to the left and right of the view, following the y
    // coordinates of the ball.
    Rectangle {
        id: leftBat
        color: "Lime"
        x: 2; width: 20; height: 90
        // ![0]
        y: ball.direction == 'left' ? ball.y - 45 : page.height/2 -45;
        Behavior on y { SpringAnimation{ velocity: 300 } }
        // ![0]
    }
    Rectangle {
        id: rightBat
        color: "Lime"
        x: page.width - 22; width: 20; height: 90
        y: ball.direction == 'right' ? ball.y - 45 : page.height/2 -45;
        Behavior on y { SpringAnimation{ velocity: 300 } }
    }

    // The rest, to make it look realistic, if neither ever scores...
    Rectangle { color: "Lime"; x: page.width/2-80; y: 0; width: 40; height: 60 }
    Rectangle { color: "Black"; x: page.width/2-70; y: 10; width: 20; height: 40 }
    Rectangle { color: "Lime"; x: page.width/2+40; y: 0; width: 40; height: 60 }
    Rectangle { color: "Black"; x: page.width/2+50; y: 10; width: 20; height: 40 }
    Repeater {
        model: page.height / 20
        Rectangle { color: "Lime"; x: page.width/2-5; y: index * 20; width: 10; height: 10 }
    }
}
