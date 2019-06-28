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


from PyQt5.QtCore import (QAbstractTransition, QEasingCurve, QEvent,
        QParallelAnimationGroup, QPropertyAnimation, qrand, QRect,
        QSequentialAnimationGroup, qsrand, QState, QStateMachine, Qt, QTime,
        QTimer)
from PyQt5.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView,
        QGraphicsWidget)


class StateSwitchEvent(QEvent):
    StateSwitchType = QEvent.User + 256

    def __init__(self, rand=0):
        super(StateSwitchEvent, self).__init__(StateSwitchEvent.StateSwitchType)

        self.m_rand = rand

    def rand(self):
        return self.m_rand


class QGraphicsRectWidget(QGraphicsWidget):
    def paint(self, painter, option, widget):
        painter.fillRect(self.rect(), Qt.blue)


class StateSwitchTransition(QAbstractTransition):
    def __init__(self, rand):
        super(StateSwitchTransition, self).__init__()

        self.m_rand = rand

    def eventTest(self, event):
        return (event.type() == StateSwitchEvent.StateSwitchType and
                event.rand() == self.m_rand)

    def onTransition(self, event):
        pass


class StateSwitcher(QState):
    def __init__(self, machine):
        super(StateSwitcher, self).__init__(machine)

        self.m_stateCount = 0
        self.m_lastIndex = 0

    def onEntry(self, event):
        n = qrand() % self.m_stateCount + 1
        while n == self.m_lastIndex:
            n = qrand() % self.m_stateCount + 1

        self.m_lastIndex = n
        self.machine().postEvent(StateSwitchEvent(n))

    def onExit(self, event):
        pass

    def addState(self, state, animation):
        self.m_stateCount += 1
        trans = StateSwitchTransition(self.m_stateCount)
        trans.setTargetState(state)
        self.addTransition(trans)
        trans.addAnimation(animation)


def createGeometryState(w1, rect1, w2, rect2, w3, rect3, w4, rect4, parent):
    result = QState(parent)

    result.assignProperty(w1, 'geometry', rect1)
    result.assignProperty(w1, 'geometry', rect1)
    result.assignProperty(w2, 'geometry', rect2)
    result.assignProperty(w3, 'geometry', rect3)
    result.assignProperty(w4, 'geometry', rect4)

    return result


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    button1 = QGraphicsRectWidget()
    button2 = QGraphicsRectWidget()
    button3 = QGraphicsRectWidget()
    button4 = QGraphicsRectWidget()
    button2.setZValue(1)
    button3.setZValue(2)
    button4.setZValue(3)

    scene = QGraphicsScene(0, 0, 300, 300)
    scene.setBackgroundBrush(Qt.black)
    scene.addItem(button1)
    scene.addItem(button2)
    scene.addItem(button3)
    scene.addItem(button4)

    window = QGraphicsView(scene)
    window.setFrameStyle(0)
    window.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    window.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    window.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    machine = QStateMachine()

    group = QState()
    timer = QTimer()
    timer.setInterval(1250)
    timer.setSingleShot(True)
    group.entered.connect(timer.start)

    state1 = createGeometryState(button1, QRect(100, 0, 50, 50), button2,
            QRect(150, 0, 50, 50), button3, QRect(200, 0, 50, 50), button4,
            QRect(250, 0, 50, 50), group)

    state2 = createGeometryState(button1, QRect(250, 100, 50, 50), button2,
            QRect(250, 150, 50, 50), button3, QRect(250, 200, 50, 50), button4,
            QRect(250, 250, 50, 50), group)

    state3 = createGeometryState(button1, QRect(150, 250, 50, 50), button2,
            QRect(100, 250, 50, 50), button3, QRect(50, 250, 50, 50), button4,
            QRect(0, 250, 50, 50), group)

    state4 = createGeometryState(button1, QRect(0, 150, 50, 50), button2,
            QRect(0, 100, 50, 50), button3, QRect(0, 50, 50, 50), button4,
            QRect(0, 0, 50, 50), group)

    state5 = createGeometryState(button1, QRect(100, 100, 50, 50), button2,
            QRect(150, 100, 50, 50), button3, QRect(100, 150, 50, 50), button4,
            QRect(150, 150, 50, 50), group)

    state6 = createGeometryState(button1, QRect(50, 50, 50, 50), button2,
            QRect(200, 50, 50, 50), button3, QRect(50, 200, 50, 50), button4,
            QRect(200, 200, 50, 50), group)

    state7 = createGeometryState(button1, QRect(0, 0, 50, 50), button2,
            QRect(250, 0, 50, 50), button3, QRect(0, 250, 50, 50), button4,
            QRect(250, 250, 50, 50), group)

    group.setInitialState(state1)

    animationGroup = QParallelAnimationGroup()
    anim = QPropertyAnimation(button4, b'geometry')
    anim.setDuration(1000)
    anim.setEasingCurve(QEasingCurve.OutElastic)
    animationGroup.addAnimation(anim)

    subGroup = QSequentialAnimationGroup(animationGroup)
    subGroup.addPause(100)
    anim = QPropertyAnimation(button3, b'geometry')
    anim.setDuration(1000)
    anim.setEasingCurve(QEasingCurve.OutElastic)
    subGroup.addAnimation(anim)

    subGroup = QSequentialAnimationGroup(animationGroup)
    subGroup.addPause(150)
    anim = QPropertyAnimation(button2, b'geometry')
    anim.setDuration(1000)
    anim.setEasingCurve(QEasingCurve.OutElastic)
    subGroup.addAnimation(anim)

    subGroup = QSequentialAnimationGroup(animationGroup)
    subGroup.addPause(200)
    anim = QPropertyAnimation(button1, b'geometry')
    anim.setDuration(1000)
    anim.setEasingCurve(QEasingCurve.OutElastic)
    subGroup.addAnimation(anim)

    stateSwitcher = StateSwitcher(machine)
    group.addTransition(timer.timeout, stateSwitcher)
    stateSwitcher.addState(state1, animationGroup)
    stateSwitcher.addState(state2, animationGroup)
    stateSwitcher.addState(state3, animationGroup)
    stateSwitcher.addState(state4, animationGroup)
    stateSwitcher.addState(state5, animationGroup)
    stateSwitcher.addState(state6, animationGroup)
    stateSwitcher.addState(state7, animationGroup)

    machine.addState(group)
    machine.setInitialState(group)
    machine.start()

    window.resize(300, 300)
    window.show()

    qsrand(QTime(0, 0, 0).secsTo(QTime.currentTime()))

    sys.exit(app.exec_())
