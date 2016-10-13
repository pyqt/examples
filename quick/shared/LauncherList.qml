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
    //model is a list of {"name":"somename", "url":"file:///some/url/mainfile.qml"}
    //function used to add to model A) to enforce scheme B) to allow Qt.resolveUrl in url assignments

    color: "#eee"
    function addExample(name, desc, url)
    {
        myModel.append({"name":name, "description":desc, "url":url})
    }
    function hideExample()
    {
        ei.visible = false;
    }

    ListView {
        clip: true
        delegate: SimpleLauncherDelegate{exampleItem: ei}
        model: ListModel {id:myModel}
        anchors.fill: parent
    }

    Item {
        id: ei
        visible: false
        clip: true
        property url exampleUrl
        onExampleUrlChanged: visible = (exampleUrl == '' ? false : true); //Setting exampleUrl automatically shows example
        anchors.fill: parent
        anchors.bottomMargin: 40
        Rectangle {
            id: bg
            anchors.fill: parent
            color: "white"
        }
        MouseArea{
            anchors.fill: parent
            enabled: ei.visible
            //Eats mouse events
        }
        Loader{
            focus: true
            source: ei.exampleUrl
            anchors.fill: parent
        }
    }
    Rectangle {
        id: bar
        visible: ei.visible
        anchors.bottom: parent.bottom
        width: parent.width
        height: 40

        Rectangle {
            height: 1
            color: "#ccc"
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
        }

        Rectangle {
            height: 1
            color: "#fff"
            anchors.top: parent.top
            anchors.topMargin: 1
            anchors.left: parent.left
            anchors.right: parent.right
        }

        gradient: Gradient {
            GradientStop { position: 0 ; color: "#eee" }
            GradientStop { position: 1 ; color: "#ccc" }
        }

        MouseArea{
            anchors.fill: parent
            enabled: ei.visible
            //Eats mouse events
        }

        Image {
            id: back
            source: "images/back.png"
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: 2
            anchors.left: parent.left
            anchors.leftMargin: 16

            MouseArea {
                id: mouse
                hoverEnabled: true
                anchors.centerIn: parent
                width: 38
                height: 31
                anchors.verticalCenterOffset: -1
                onClicked: ei.exampleUrl = ""
                Rectangle {
                    anchors.fill: parent
                    opacity: mouse.pressed ? 1 : 0
                    Behavior on opacity { NumberAnimation{ duration: 100 }}
                    gradient: Gradient {
                        GradientStop { position: 0 ; color: "#22000000" }
                        GradientStop { position: 0.2 ; color: "#11000000" }
                    }
                    border.color: "darkgray"
                    antialiasing: true
                    radius: 4
                }
            }
        }
    }
}
