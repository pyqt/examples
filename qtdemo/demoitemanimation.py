#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial Usage
## Licensees holding valid Qt Commercial licenses may use this file in
## accordance with the Qt Commercial License Agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and Nokia.
##
## GNU Lesser General Public License Usage
## Alternatively, this file may be used under the terms of the GNU Lesser
## General Public License version 2.1 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU Lesser General Public License version 2.1 requirements
## will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
##
## In addition, as a special exception, Nokia gives you certain additional
## rights.  These rights are described in the Nokia Qt LGPL Exception
## version 1.1, included in the file LGPL_EXCEPTION.txt in this package.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3.0 as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU General Public License version 3.0 requirements will be
## met: http://www.gnu.org/copyleft/gpl.html.
##
## If you have questions regarding the use of this file, please contact
## Nokia at qt-info@nokia.com.
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import QPropertyAnimation, QTimer

from colors import Colors


class DemoItemAnimation(QPropertyAnimation):
    ANIM_IN, ANIM_OUT, ANIM_UNSPECIFIED = range(3)

    def __init__(self, item, inOrOut=ANIM_UNSPECIFIED):
        super(DemoItemAnimation, self).__init__(item, b'pos')

        self._startDelay = 0
        self._inOrOut = inOrOut
        self._hideOnFinished = False

    def prepare(self):
        self.targetObject().prepare()

    def setHideOnFinished(self, hide):
        self._hideOnFinshed = hide

    def setStartDelay(self, delay):
        self._startDelay = delay

    def setDuration(self, duration):
        duration = int(duration * Colors.animSpeed)
        super(DemoItemAnimation, self).setDuration(duration)

    def notOwnerOfItem(self):
        return self is not self.targetObject().currentAnimation

    def play(self, fromStart=True, force=False):
        item = self.targetObject()

        # If the item that this animation controls in currently under the
        # control of another animation, stop that animation first.
        if item.currentAnimation is not None:
            item.currentAnimation.stop()

        item.currentAnimation = self

        if Colors.noAnimations and not force:
            # If animations are disabled just move to the end position.
            item.setPos(self.endValue())
        else:
            if self.isVisible():
                # If the item is already visible, start the animation from the
                # item's current position rather than from the start.
                self.setStartValue(item.pos())

            if fromStart:
                self.setCurrentTime(0)
                item.setPos(self.startValue())

        if self._inOrOut == DemoItemAnimation.ANIM_IN:
            item.setRecursiveVisible(True)

        if not Colors.noAnimations or force:
            if self._startDelay:
                QTimer.singleShot(self._startDelay, self.start)
            else:
                self.start()

    def setCurveShape(self, shape):
        self.setEasingCurve(shape)

    def setEnabled(self, enabled):
        self.targetObject().setEnabled(enabled)

    def isVisible(self):
        return self.targetObject().isVisible()

    def updateState(self, new, old):
        item = self.targetObject()

        if new == QPropertyAnimation.Running:
            item.animationStarted(self._inOrOut)
        elif new == QPropertyAnimation.Stopped:
            if self._hideOnFinished:
                item.setRecursiveVisible(False)

            item.animationStopped(self._inOrOut)
