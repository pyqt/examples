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


import math

from PyQt5.QtCore import QPointF

from guide import Guide


PI2 = 2 * math.pi


class GuideCircle(Guide):
    CW = 1
    CCW = -1

    def __init__(self, rect, startAngle=0.0, span=360.0, dir=CCW, follows=None):
        super(GuideCircle, self).__init__(follows)

        self.radiusX = rect.width() / 2.0
        self.radiusY = rect.height() / 2.0
        self.posX = rect.topLeft().x()
        self.posY = rect.topLeft().y()
        self.spanRad = span * PI2 / -360.0

        if dir == GuideCircle.CCW:
            self.startAngleRad = startAngle * PI2 / -360.0
            self.endAngleRad = self.startAngleRad + self.spanRad
            self.stepAngleRad = self.spanRad / self.length()
        else:
            self.startAngleRad = self.spanRad + (startAngle * PI2 / -360.0)
            self.endAngleRad = startAngle * PI2 / -360.0
            self.stepAngleRad = -self.spanRad / self.length()

    def length(self):
        return abs(self.radiusX * self.spanRad)

    def startPos(self):
        return QPointF((self.posX + self.radiusX + self.radiusX * math.cos(self.startAngleRad)) * self.scaleX,
                (self.posY + self.radiusY + self.radiusY * math.sin(self.startAngleRad)) * self.scaleY)

    def endPos(self):
        return QPointF((self.posX + self.radiusX + self.radiusX * math.cos(self.endAngleRad)) * self.scaleX,
                (self.posY + self.radiusY + self.radiusY * math.sin(self.endAngleRad)) * self.scaleY)

    def guide(self, item, moveSpeed):
        frame = item.guideFrame - self.startLength
        end = QPointF((self.posX + self.radiusX + self.radiusX * math.cos(self.startAngleRad + (frame * self.stepAngleRad))) * self.scaleX,
                (self.posY + self.radiusY + self.radiusY * math.sin(self.startAngleRad + (frame * self.stepAngleRad))) * self.scaleY)
        self.move(item, end, moveSpeed)
