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


from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor, QImage, QPainter
from PyQt5.QtWidgets import QGraphicsTextItem, QStyleOptionGraphicsItem

from demoitem import DemoItem


class DemoTextItem(DemoItem):
    STATIC_TEXT, DYNAMIC_TEXT = range(2)

    def __init__(self, text, font, textColor, textWidth, parent=None, type=STATIC_TEXT, bgColor=QColor()):
        super(DemoTextItem, self).__init__(parent)

        self.type = type
        self.text = text
        self.font = font
        self.textColor = textColor
        self.bgColor = bgColor
        self.textWidth = textWidth
        self.noSubPixeling = True

    def setText(self, text):
        self.text = text
        self.update()

    def createImage(self, transform):
        if self.type == DemoTextItem.DYNAMIC_TEXT:
            return None

        sx = min(transform.m11(), transform.m22())
        sy = max(transform.m22(), sx)

        textItem = QGraphicsTextItem()
        textItem.setHtml(self.text)
        textItem.setTextWidth(self.textWidth)
        textItem.setFont(self.font)
        textItem.setDefaultTextColor(self.textColor)
        textItem.document().setDocumentMargin(2)

        w = textItem.boundingRect().width()
        h = textItem.boundingRect().height()
        image = QImage(int(w * sx), int(h * sy),
                QImage.Format_ARGB32_Premultiplied)
        image.fill(QColor(0, 0, 0, 0).rgba())
        painter = QPainter(image)
        painter.scale(sx, sy)
        style = QStyleOptionGraphicsItem()
        textItem.paint(painter, style, None)

        return image

    def animationStarted(self, id=0):
        self.noSubPixeling = False

    def animationStopped(self, id=0):
        self.noSubPixeling = True

    def boundingRect(self):
        if self.type == DemoTextItem.STATIC_TEXT:
            return super(DemoTextItem, self).boundingRect()

        # Sorry for using magic number.
        return QRectF(0, 0, 50, 20)

    def paint(self, painter, option, widget):
        if self.type == DemoTextItem.STATIC_TEXT:
            super(DemoTextItem, self).paint(painter, option, widget)
            return

        painter.setPen(self.textColor)
        painter.drawText(0, 0, self.text)
