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


from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor, QImage, QLinearGradient, QPainter

from colors import Colors
from demoitem import DemoItem


class ImageItem(DemoItem):
    def __init__(self, image, maxWidth, maxHeight, parent=None, adjustSize=False, scale=1.0):
        super(ImageItem, self).__init__(parent)

        self.image = image
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        self.adjustSize = adjustSize
        self.scale = scale

    def createImage(self, transform):
        original = QImage(self.image)
        if original.isNull():
            return original

        size = transform.map(QPoint(self.maxWidth, self.maxHeight))
        w = size.x()
        h = size.y()

        # Optimization: if image is smaller than maximum allowed size, just
        # return the loaded image.
        if original.size().height() <= h and original.size().width() <= w and not self.adjustSize and self.scale == 1:
            return original

        # Calculate what the size of the final image will be.
        w = min(w, float(original.size().width()) * self.scale)
        h = min(h, float(original.size().height()) * self.scale)

        adjustx = 1.0
        adjusty = 1.0
        if self.adjustSize:
            adjustx = min(transform.m11(), transform.m22())
            adjusty = max(transform.m22(), adjustx)
            w *= adjustx
            h *= adjusty

        # Create a new image with correct size, and draw original on it.
        image = QImage(int(w + 2), int(h + 2),
                QImage.Format_ARGB32_Premultiplied)
        image.fill(QColor(0, 0, 0, 0).rgba())
        painter = QPainter(image)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        if self.adjustSize:
            painter.scale(adjustx, adjusty)
        if self.scale != 1:
            painter.scale(self.scale, self.scale)
        painter.drawImage(0, 0, original)

        if not self.adjustSize:
            # Blur out edges.
            blur = 30

            if h < original.height():
                brush1 = QLinearGradient(0, h - blur, 0, h)
                brush1.setSpread(QLinearGradient.PadSpread)
                brush1.setColorAt(0.0, QColor(0, 0, 0, 0))
                brush1.setColorAt(1.0, Colors.sceneBg1)
                painter.fillRect(0, int(h) - blur, original.width(), int(h),
                        brush1)

            if w < original.width():
                brush2 = QLinearGradient(w - blur, 0, w, 0)
                brush2.setSpread(QLinearGradient.PadSpread)
                brush2.setColorAt(0.0, QColor(0, 0, 0, 0))
                brush2.setColorAt(1.0, Colors.sceneBg1)
                painter.fillRect(int(w) - blur, 0, int(w), original.height(),
                        brush2)

        return image
