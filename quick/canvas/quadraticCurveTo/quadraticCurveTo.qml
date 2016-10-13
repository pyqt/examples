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
import "../contents"
Item {
  id:container
  width:320
  height:480

  Column {
    spacing:5
    anchors.fill:parent
    Text { font.pointSize:15; text:"Quadratic Curve"; anchors.horizontalCenter:parent.horizontalCenter}

    Canvas {
      id:canvas
      width:320
      height:280
      property string strokeStyle:"steelblue"
      property string fillStyle:"yellow"
      property int lineWidth:lineWidthCtrl.value
      property bool fill:true
      property bool stroke:true
      property real alpha:alphaCtrl.value
      property real scaleX : scaleXCtrl.value
      property real scaleY : scaleYCtrl.value
      property real rotate : rotateCtrl.value
      antialiasing: true

      onLineWidthChanged:requestPaint();
      onFillChanged:requestPaint();
      onStrokeChanged:requestPaint();
      onAlphaChanged:requestPaint();
      onScaleXChanged:requestPaint();
      onScaleYChanged:requestPaint();
      onRotateChanged:requestPaint();
      Behavior on scaleX { SpringAnimation { spring: 2; damping: 0.2; loops:Animation.Infinite } }
      Behavior on scaleY { SpringAnimation { spring: 2; damping: 0.2; loops:Animation.Infinite} }
      Behavior on rotate { SpringAnimation { spring: 2; damping: 0.2; loops:Animation.Infinite} }

      onPaint: {
          var ctx = canvas.getContext('2d');
          ctx.save();
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          ctx.globalAlpha = canvas.alpha;
          ctx.strokeStyle = canvas.strokeStyle;
          ctx.fillStyle = canvas.fillStyle;
          ctx.lineWidth = canvas.lineWidth;
          ctx.scale(canvas.scaleX, canvas.scaleY);
          ctx.rotate(canvas.rotate);
          // ![0]
          ctx.beginPath();
          ctx.moveTo(75,25);
          ctx.quadraticCurveTo(25,25,25,62.5);
          ctx.quadraticCurveTo(25,100,50,100);
          ctx.quadraticCurveTo(50,120,30,125);
          ctx.quadraticCurveTo(60,120,65,100);
          ctx.quadraticCurveTo(125,100,125,62.5);
          ctx.quadraticCurveTo(125,25,75,25);
          ctx.closePath();
          // ![0]
          if (canvas.fill)
             ctx.fill();
          if (canvas.stroke)
             ctx.stroke();


          // ![1]
          ctx.fillStyle="green";
          ctx.font = "Bold 15px";

          ctx.fillText("QML酷毙了", 30, 60);
          // ![1]
          ctx.restore();
      }
    }

    Rectangle {
        id:controls
        width:320
        height:150
        Column {
          spacing:3
          Slider {id:lineWidthCtrl; width:300; height:20; min:1; max:10; init:2; name:"Line width"}
          Slider {id:scaleXCtrl; width:300; height:20; min:0.1; max:10; init:1; name:"ScaleX"}
          Slider {id:scaleYCtrl; width:300; height:20; min:0.1; max:10; init:1; name:"ScaleY"}
          Slider {id:rotateCtrl; width:300; height:20; min:0; max:Math.PI*2; init:0; name:"Rotate"}
          Slider {id:alphaCtrl; width:300; height:20; min:0; max:1; init:1; name:"Alpha"}
        }
    }
  }
}
