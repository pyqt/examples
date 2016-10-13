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


from PyQt5.QtCore import QLineF, QPointF


class Guide(object):
    def __init__(self, follows=None):
        self.scaleX = 1.0
        self.scaleY = 1.0

        if follows is not None:
            while follows.nextGuide is not follows.firstGuide:
                follows = follows.nextGuide

            follows.nextGuide = self
            self.prevGuide = follows
            self.firstGuide = follows.firstGuide
            self.nextGuide = follows.firstGuide
            self.startLength = int(follows.startLength + follows.length()) + 1
        else:
            self.prevGuide = self
            self.firstGuide = self
            self.nextGuide = self
            self.startLength = 0

    def setScale(self, scaleX, scaleY, all=True):
        self.scaleX = scaleX
        self.scaleY = scaleY

        if all:
            next = self.nextGuide
            while next is not self:
                next.scaleX = scaleX
                next.scaleY = scaleY
                next = next.nextGuide

    def setFence(self, fence, all=True):
        self.fence = fence

        if all:
            next = self.nextGuide
            while next is not self:
                next.fence = fence
                next = next.nextGuide

    def lengthAll(self):
        len = self.length()
        next = self.nextGuide
        while next is not self:
            len += next.length()
            next = next.nextGuide

        return len

    def move(self, item, dest, moveSpeed):
        walkLine = QLineF(item.getGuidedPos(), dest)
        if moveSpeed >= 0 and walkLine.length() > moveSpeed:
            # The item is too far away from it's destination point so we move
            # it towards it instead.
            dx = walkLine.dx()
            dy = walkLine.dy()

            if abs(dx) > abs(dy):
                # Walk along x-axis.
                if dx != 0:
                    d = moveSpeed * dy / abs(dx)

                    if dx > 0:
                        s = moveSpeed
                    else:
                        s = -moveSpeed

                    dest.setX(item.getGuidedPos().x() + s)
                    dest.setY(item.getGuidedPos().y() + d)
            else:
                # Walk along y-axis.
                if dy != 0:
                    d = moveSpeed * dx / abs(dy)

                    if dy > 0:
                        s = moveSpeed
                    else:
                        s = -moveSpeed

                    dest.setX(item.getGuidedPos().x() + d)
                    dest.setY(item.getGuidedPos().y() + s)

        item.setGuidedPos(dest)

    def startPos(self):
        return QPointF(0, 0)

    def endPos(self):
        return QPointF(0, 0)

    def length(self):
        return 1.0

    def guide(self, item, moveSpeed):
        raise NotImplementedError
