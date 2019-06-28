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
    id: container

    property string text: "Drag me!"
    property bool animated: true

    width: 320; height: 480; color: "#474747"; focus: true

    Keys.onPressed: {
        if (event.key == Qt.Key_Delete || event.key == Qt.Key_Backspace)
            container.remove()
        else if (event.text != "") {
            container.append(event.text)
        }
    }

    function append(text) {
        container.animated = false
        var lastLetter = container.children[container.children.length - 1]
        var newLetter = letterComponent.createObject(container)
        newLetter.text = text
        newLetter.follow = lastLetter
        container.animated = true
    }

    function remove() {
        if (container.children.length)
            container.children[container.children.length - 1].destroy()
    }

    function doLayout() {
        var follow = null
        for (var i = 0; i < container.text.length; ++i) {
            var newLetter = letterComponent.createObject(container)
            newLetter.text = container.text[i]
            newLetter.follow = follow
            follow = newLetter
        }
    }

    Component {
        id: letterComponent
        Text {
            id: letter
            property variant follow

//! [0]
            x: follow ? follow.x + follow.width : container.width / 6
            y: follow ? follow.y : container.height / 2
//! [0]

            font.pixelSize: 40; font.bold: true
            color: "#999999"; styleColor: "#222222"; style: Text.Raised

            MouseArea {
                anchors.fill: parent
                drag.target: letter; drag.axis: Drag.XAndYAxis
                onPressed: letter.color = "#dddddd"
                onReleased: letter.color = "#999999"
            }

//! [1]
            Behavior on x { enabled: container.animated; SpringAnimation { spring: 3; damping: 0.3; mass: 1.0 } }
            Behavior on y { enabled: container.animated; SpringAnimation { spring: 3; damping: 0.3; mass: 1.0 } }
//! [1]
        }
    }

    Component.onCompleted: doLayout()
}
