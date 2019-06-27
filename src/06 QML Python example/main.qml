import QtQuick 2.2
import QtQuick.Window 2.2

Window {
    Image {
        id: background
        source: "background.png"
    }
    Image {
        id: wheel
        anchors.centerIn: parent
        source: "pinwheel.png"
        Behavior on rotation {
            NumberAnimation {
                duration: 250
            }
        }
    }
    MouseArea {
        anchors.fill: parent
        onPressed: {
            wheel.rotation += 90
        }
    }
    visible: true
    width: background.width
    height: background.height
}