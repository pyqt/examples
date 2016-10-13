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


from PyQt5.QtCore import QPointF, QRect, QRectF, QSize, Qt
from PyQt5.QtGui import (QColor, QImage, QLinearGradient, QPainter,
        QPainterPath, QPen)

from colors import Colors
from demoitem import DemoItem
from demoitemanimation import DemoItemAnimation
from demotextitem import DemoTextItem
from scanitem import ScanItem


class ButtonBackground(DemoItem):
    def __init__(self, type, highlighted, pressed, logicalSize, parent):
        super(ButtonBackground, self).__init__(parent)

        self.type = type
        self.highlighted = highlighted
        self.pressed = pressed
        self.logicalSize = logicalSize
        self.useSharedImage('%s%d%d%d' % (__file__, type, highlighted, pressed))

    def createImage(self, transform):
        if self.type in (TextButton.SIDEBAR, TextButton.PANEL):
            return self.createRoundButtonBackground(transform)
        else:
            return self.createArrowBackground(transform)

    def createRoundButtonBackground(self, transform):
        scaledRect = transform.mapRect(QRect(0, 0,
                self.logicalSize.width(), self.logicalSize.height()))

        image = QImage(scaledRect.width(), scaledRect.height(),
                QImage.Format_ARGB32_Premultiplied)
        image.fill(QColor(0, 0, 0, 0).rgba())
        painter = QPainter(image)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if Colors.useEightBitPalette:
            painter.setPen(QColor(120, 120, 120))
            if self.pressed:
                painter.setBrush(QColor(60, 60, 60))
            elif self.highlighted:
                painter.setBrush(QColor(100, 100, 100))
            else:
                painter.setBrush(QColor(80, 80, 80))
        else:
            outlinebrush = QLinearGradient(0, 0, 0, scaledRect.height())
            brush = QLinearGradient(0, 0, 0, scaledRect.height())

            brush.setSpread(QLinearGradient.PadSpread)
            highlight = QColor(255, 255, 255, 70)
            shadow = QColor(0, 0, 0, 70)
            sunken = QColor(220, 220, 220, 30)

            if self.type == TextButton.PANEL:
                normal1 = QColor(200, 170, 160, 50)
                normal2 = QColor(50, 10, 0, 50)
            else:
                normal1 = QColor(255, 255, 245, 60)
                normal2 = QColor(255, 255, 235, 10)

            if self.pressed:
                outlinebrush.setColorAt(0, shadow)
                outlinebrush.setColorAt(1, highlight)
                brush.setColorAt(0, sunken)
                painter.setPen(Qt.NoPen)
            else:
                outlinebrush.setColorAt(1, shadow)
                outlinebrush.setColorAt(0, highlight)
                brush.setColorAt(0, normal1)
                if not self.highlighted:
                    brush.setColorAt(1, normal2)
                painter.setPen(QPen(outlinebrush, 1))

            painter.setBrush(brush)

        if self.type == TextButton.PANEL:
            painter.drawRect(0, 0, scaledRect.width(), scaledRect.height())
        else:
            painter.drawRoundedRect(0, 0, scaledRect.width(),
                    scaledRect.height(), 10, 90, Qt.RelativeSize)

        return image

    def createArrowBackground(self, transform):
        scaledRect = transform.mapRect(QRect(0, 0,
                self.logicalSize.width(), self.logicalSize.height()))

        image = QImage(scaledRect.width(), scaledRect.height(),
                QImage.Format_ARGB32_Premultiplied)
        image.fill(QColor(0, 0, 0, 0).rgba())
        painter = QPainter(image)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if Colors.useEightBitPalette:
            painter.setPen(QColor(120, 120, 120))
            if self.pressed:
                painter.setBrush(QColor(60, 60, 60))
            elif self.highlighted:
                painter.setBrush(QColor(100, 100, 100))
            else:
                painter.setBrush(QColor(80, 80, 80))
        else:
            outlinebrush = QLinearGradient(0, 0, 0, scaledRect.height())
            brush = QLinearGradient(0, 0, 0, scaledRect.height())

            brush.setSpread(QLinearGradient.PadSpread)
            highlight = QColor(255, 255, 255, 70)
            shadow = QColor(0, 0, 0, 70)
            sunken = QColor(220, 220, 220, 30)
            normal1 = QColor(200, 170, 160, 50)
            normal2 = QColor(50, 10, 0, 50)

            if self.pressed:
                outlinebrush.setColorAt(0, shadow)
                outlinebrush.setColorAt(1, highlight)
                brush.setColorAt(0, sunken)
                painter.setPen(Qt.NoPen)
            else:
                outlinebrush.setColorAt(1, shadow)
                outlinebrush.setColorAt(0, highlight)
                brush.setColorAt(0, normal1)
                if not self.highlighted:
                    brush.setColorAt(1, normal2)
                painter.setPen(QPen(outlinebrush, 1))

            painter.setBrush(brush);

        painter.drawRect(0, 0, scaledRect.width(), scaledRect.height())

        xOff = scaledRect.width() / 2
        yOff = scaledRect.height() / 2
        sizex = 3.0 * transform.m11()
        sizey = 1.5 * transform.m22()
        if self.type == TextButton.UP:
            sizey *= -1
        path = QPainterPath()
        path.moveTo(xOff, yOff + (5 * sizey))
        path.lineTo(xOff - (4 * sizex), yOff - (3 * sizey))
        path.lineTo(xOff + (4 * sizex), yOff - (3 * sizey))
        path.lineTo(xOff, yOff + (5 * sizey))
        painter.drawPath(path)

        return image


class TextButton(DemoItem):
    BUTTON_WIDTH = 180
    BUTTON_HEIGHT = 19

    LEFT, RIGHT = range(2)

    SIDEBAR, PANEL, UP, DOWN = range(4)

    ON, OFF, HIGHLIGHT, DISABLED = range(4)

    def __init__(self, text, align=LEFT, userCode=0, parent=None, type=SIDEBAR):
        super(TextButton, self).__init__(parent)

        # Prevent a circular import.
        from menumanager import MenuManager
        self._menu_manager = MenuManager.instance()

        self.menuString = text
        self.buttonLabel = text
        self.alignment = align
        self.buttonType = type
        self.userCode = userCode
        self.scanAnim = None
        self.bgOn = None
        self.bgOff = None
        self.bgHighlight = None
        self.bgDisabled = None
        self.state = TextButton.OFF

        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.PointingHandCursor)

        # Calculate the button size.
        if type in (TextButton.SIDEBAR, TextButton.PANEL):
            self.logicalSize = QSize(TextButton.BUTTON_WIDTH, TextButton.BUTTON_HEIGHT)
        else:
            self.logicalSize = QSize(int((TextButton.BUTTON_WIDTH / 2.0) - 5), int(TextButton.BUTTON_HEIGHT * 1.5))

        self._prepared = False

    def setMenuString(self, menu):
        self.menuString = menu

    def prepare(self):
        if not self._prepared:
            self.setupHoverText()
            self.setupScanItem()
            self.setupButtonBg()
            self._prepared = True

    def boundingRect(self):
        return QRectF(0, 0, self.logicalSize.width(),
                self.logicalSize.height())

    def setupHoverText(self):
        if not self.buttonLabel:
            return

        textItem = DemoTextItem(self.buttonLabel, Colors.buttonFont(),
                Colors.buttonText, -1, self)
        textItem.setZValue(self.zValue() + 2)
        textItem.setPos(16, 0)

    def setupScanItem(self):
        if Colors.useButtonBalls:
            scanItem = ScanItem(self)
            scanItem.setZValue(self.zValue() + 1)

            self.scanAnim = DemoItemAnimation(scanItem)

            x = 1.0
            y = 1.5
            stop = TextButton.BUTTON_WIDTH - scanItem.boundingRect().width() - x
            if self.alignment == TextButton.LEFT:
                self.scanAnim.setDuration(2500)
                self.scanAnim.setKeyValueAt(0.0, QPointF(x, y))
                self.scanAnim.setKeyValueAt(0.5, QPointF(x, y))
                self.scanAnim.setKeyValueAt(0.7, QPointF(stop, y))
                self.scanAnim.setKeyValueAt(1.0, QPointF(x, y))
                scanItem.setPos(QPointF(x, y))
            else:
                self.scanAnim.setKeyValueAt(0.0, QPointF(stop, y))
                self.scanAnim.setKeyValueAt(0.5, QPointF(x, y))
                self.scanAnim.setKeyValueAt(1.0, QPointF(stop, y))
                scanItem.setPos(QPointF(stop, y))

    def setState(self, state):
        self.state = state
        self.bgOn.setRecursiveVisible(state == TextButton.ON)
        self.bgOff.setRecursiveVisible(state == TextButton.OFF)
        self.bgHighlight.setRecursiveVisible(state == TextButton.HIGHLIGHT)
        self.bgDisabled.setRecursiveVisible(state == TextButton.DISABLED)
        if state == TextButton.DISABLED:
            self.setCursor(Qt.ArrowCursor)
        else:
            self.setCursor(Qt.PointingHandCursor)

    def setupButtonBg(self):
        self.bgOn = ButtonBackground(self.buttonType, True, True,
                self.logicalSize, self)
        self.bgOff = ButtonBackground(self.buttonType, False, False,
                self.logicalSize, self)
        self.bgHighlight = ButtonBackground(self.buttonType, True, False,
                self.logicalSize, self)
        self.bgDisabled = ButtonBackground(self.buttonType, True, True,
                self.logicalSize, self)
        self.setState(TextButton.OFF)

    def hoverEnterEvent(self, event):
        if not self.isEnabled() or self.state == TextButton.DISABLED:
            return

        if self.state == TextButton.OFF:
            self.setState(TextButton.HIGHLIGHT)

            if Colors.noAnimations and Colors.useButtonBalls:
                # Wait a bit in the beginning to enhance the effect.  We have
                # to do this here so that the adaption can be dynamic.
                self.scanAnim.setDuration(1000)
                self.scanAnim.setKeyValueAt(0.2, self.scanAnim.posAt(0))

            if (self._menu_manager.window.fpsMedian > 10 or Colors.noAdapt or
                    Colors.noTimerUpdate):
                if Colors.useButtonBalls:
                    self.scanAnim.play(True, True)

    def hoverLeaveEvent(self, event):
        if self.state == TextButton.DISABLED:
            return

        self.setState(TextButton.OFF)

        if Colors.noAnimations and Colors.useButtonBalls:
            self.scanAnim.stop()

    def mousePressEvent(self, event):
        if self.state == TextButton.DISABLED:
            return

        if self.state == TextButton.HIGHLIGHT or self.state == TextButton.OFF:
            self.setState(TextButton.ON)

    def mouseReleaseEvent(self, event):
        if self.state == TextButton.ON:
            self.setState(TextButton.OFF)
            if self.isEnabled() and self.boundingRect().contains(event.pos()):
                self._menu_manager.itemSelected(self.userCode, self.menuString)

    def animationStarted(self, _):
        if self.state == TextButton.DISABLED:
            return

        self.setState(TextButton.OFF)
