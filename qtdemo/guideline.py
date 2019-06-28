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

from guide import Guide


class GuideLine(Guide):
    def __init__(self, line_or_point, follows=None):
        super(GuideLine, self).__init__(follows)

        if isinstance(line_or_point, QLineF):
            self.line = line_or_point
        elif follows is not None:
            self.line = QLineF(self.prevGuide.endPos(), line_or_point)
        else:
            self.line = QLineF(QPointF(0, 0), line_or_point)

    def length(self):
        return self.line.length()

    def startPos(self):
        return QPointF(self.line.p1().x() * self.scaleX,
                self.line.p1().y() * self.scaleY)

    def endPos(self):
        return QPointF(self.line.p2().x() * self.scaleX,
                self.line.p2().y() * self.scaleY)

    def guide(self, item, moveSpeed):
        frame = item.guideFrame - self.startLength
        endX = (self.line.p1().x() + (frame * self.line.dx() / self.length())) * self.scaleX
        endY = (self.line.p1().y() + (frame * self.line.dy() / self.length())) * self.scaleY
        pos = QPointF(endX, endY)
        self.move(item, pos, moveSpeed)
