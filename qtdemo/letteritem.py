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


from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QImage, QLinearGradient, QPainter

from colors import Colors
from demoitem import DemoItem


class LetterItem(DemoItem):
    def __init__(self, letter, parent=None):
        super(LetterItem, self).__init__(parent)

        self.letter = letter

        self.useSharedImage(__file__ + letter)

    def createImage(self, transform):
        scaledRect = transform.mapRect(QRect(0, 0, 25, 25))
        image = QImage(scaledRect.width(), scaledRect.height(),
                QImage.Format_ARGB32_Premultiplied)
        image.fill(0)
        painter = QPainter(image)
        painter.scale(transform.m11(), transform.m22())
        painter.setRenderHints(QPainter.TextAntialiasing | QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)

        if Colors.useEightBitPalette:
            painter.setBrush(QColor(102, 175, 54))
            painter.drawEllipse(0, 0, 25, 25)
            painter.setFont(Colors.tickerFont())
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(10, 15, self.letter)
        else:
            brush = QLinearGradient(0, 0, 0, 25)
            brush.setSpread(QLinearGradient.PadSpread)
            brush.setColorAt(0.0, QColor(102, 175, 54, 200))
            brush.setColorAt(1.0, QColor(102, 175, 54, 60))
            painter.setBrush(brush)
            painter.drawEllipse(0, 0, 25, 25)
            painter.setFont(Colors.tickerFont())
            painter.setPen(QColor(255, 255, 255, 255))
            painter.drawText(10, 15, self.letter)

        return image
