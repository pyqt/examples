#############################################################################
##
## Copyright (C) 2015 Riverbank Computing Limited.
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


from PyQt5.QtCore import QFileInfo, QPoint, QRect, qRound, Qt, QTime, QTimer
from PyQt5.QtGui import (QFontMetricsF, QImage, QPainter, QPixmap, QPolygon,
        QRegion)
from PyQt5.QtWidgets import (QApplication, QFrame, QGraphicsScene,
        QGraphicsView, QGraphicsWidget, QMessageBox, QWidget)

from colors import Colors
from demoitem import DemoItem
from demotextitem import DemoTextItem
from imageitem import ImageItem
from menumanager import MenuManager


class MainWindow(QGraphicsView):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.imagesDir = QFileInfo(__file__).absolutePath() + '/images'

        self.updateTimer = QTimer(self)
        self.demoStartTime = QTime()
        self.fpsTime = QTime()
        self.background = QPixmap()

        self.scene = None
        self.mainSceneRoot = None
        self.frameTimeList = []
        self.fpsHistory = []

        self.currentFps = Colors.fps
        self.fpsMedian = -1
        self.fpsLabel = None
        self.pausedLabel = None
        self.doneAdapt = False
        self.useTimer = False
        self.updateTimer.setSingleShot(True)
        self.companyLogo = None
        self.qtLogo = None

        self.setupWidget()
        self.setupScene()
        self.setupSceneItems()
        self.drawBackgroundToPixmap()

    def setupWidget(self):
        desktop = QApplication.desktop()
        screenRect = desktop.screenGeometry(desktop.primaryScreen())
        windowRect = QRect(0, 0, 800, 600)

        if screenRect.width() < 800:
            windowRect.setWidth(screenRect.width())

        if screenRect.height() < 600:
            windowRect.setHeight(screenRect.height())

        windowRect.moveCenter(screenRect.center())
        self.setGeometry(windowRect)
        self.setMinimumSize(80, 60)

        self.setWindowTitle("PyQt Examples")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameStyle(QFrame.NoFrame)
        self.setRenderingSystem()
        self.updateTimer.timeout.connect(self.tick)

    def setRenderingSystem(self):
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewport(QWidget())

    def start(self):
        self.switchTimerOnOff(True)
        self.demoStartTime.restart()
        MenuManager.instance().itemSelected(MenuManager.ROOT,
                Colors.rootMenuName)
        Colors.debug("- starting demo")

    def enableMask(self, enable):
        if not enable or Colors.noWindowMask:
            self.clearMask()
        else:
            region = QPolygon([
                    # North side.
                    0, 0,
                    800, 0,
                    # East side.
                    # 800, 70,
                    # 790, 90,
                    # 790, 480,
                    # 800, 500,
                    800, 600,
                    # South side.
                    700, 600,
                    670, 590,
                    130, 590,
                    100, 600,
                    0, 600,
                    # West side.
                    # 0, 550,
                    # 10, 530,
                    # 10, 520,
                    # 0, 520,
                    0, 0])

            self.setMask(QRegion(region))

    def setupScene(self):
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 800, 600)
        self.setScene(self.scene)
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)

    def switchTimerOnOff(self, on):
        ticker = MenuManager.instance().ticker
        if ticker and ticker.scene():
            ticker.tickOnPaint = not on or Colors.noTimerUpdate

        if on and not Colors.noTimerUpdate:
            self.useTimer = True
            self.fpsTime = QTime.currentTime()
            self.updateTimer.start(int(1000 / Colors.fps))
            update_mode = QGraphicsView.NoViewportUpdate
        else:
            self.useTimer = False
            self.updateTimer.stop()

            if Colors.noTicker:
                update_mode = QGraphicsView.MinimalViewportUpdate
            else:
                update_mode = QGraphicsView.SmartViewportUpdate

        self.setViewportUpdateMode(update_mode)

    def measureFps(self):
        # Calculate time difference.
        t = self.fpsTime.msecsTo(QTime.currentTime())
        if t == 0:
            t = 0.01

        self.currentFps = (1000.0 / t)
        self.fpsHistory.append(self.currentFps)
        self.fpsTime = QTime.currentTime()

        # Calculate median.
        size = len(self.fpsHistory)

        if size == 10:
            self.fpsHistory.sort()
            self.fpsMedian = self.fpsHistory[int(size / 2)]
            if self.fpsMedian == 0:
                self.fpsMedian = 0.01

            self.fpsHistory = []

            return True

        return False

    def forceFpsMedianCalculation(self):
        # Used for adaption in case things are so slow that no median has yet
        # been calculated.
        if self.fpsMedian != -1:
            return

        size = len(self.fpsHistory)

        if size == 0:
            self.fpsMedian = 0.01
            return

        self.fpsHistory.sort()
        self.fpsMedian = self.fpsHistory[size // 2]
        if self.fpsMedian == 0:
            self.fpsMedian = 0.01

    def tick(self):
        medianChanged = self.measureFps()
        self.checkAdapt()

        if medianChanged and self.fpsLabel and Colors.showFps:
            self.fpsLabel.setText("FPS: %d" % int(self.currentFps))

        if MenuManager.instance().ticker:
            MenuManager.instance().ticker.tick()

        self.viewport().update()

        if self.useTimer:
            self.updateTimer.start(int(1000 / Colors.fps))

    def setupSceneItems(self):
        if Colors.showFps:
            self.fpsLabel = DemoTextItem("FPS: --", Colors.buttonFont(),
                    Qt.white, -1, None, DemoTextItem.DYNAMIC_TEXT)
            self.fpsLabel.setZValue(1000)
            self.fpsLabel.setPos(Colors.stageStartX,
                    600 - QFontMetricsF(Colors.buttonFont()).height() - 5)

        self.mainSceneRoot = QGraphicsWidget()
        self.scene.addItem(self.mainSceneRoot)

        self.companyLogo = ImageItem(
                QImage(self.imagesDir + '/trolltech-logo.png'),
                1000, 1000, None, True, 0.5)
        self.qtLogo = ImageItem(QImage(self.imagesDir + '/qtlogo_small.png'),
                1000, 1000, None, True, 0.5)
        self.companyLogo.setZValue(100)
        self.qtLogo.setZValue(100)
        self.pausedLabel = DemoTextItem("PAUSED", Colors.buttonFont(),
                Qt.white, -1, None)
        self.pausedLabel.setZValue(100)
        fm = QFontMetricsF(Colors.buttonFont())
        self.pausedLabel.setPos(Colors.stageWidth - fm.width("PAUSED"),
                590 - fm.height())
        self.pausedLabel.setRecursiveVisible(False)

    def checkAdapt(self):
        if self.doneAdapt or Colors.noTimerUpdate or self.demoStartTime.elapsed() < 2000:
            return

        self.doneAdapt = True
        self.forceFpsMedianCalculation()
        Colors.benchmarkFps = self.fpsMedian
        Colors.debug("- benchmark: %d FPS" % int(Colors.benchmarkFps))

        if Colors.noAdapt:
            return

        if self.fpsMedian < 30:
            ticker = MenuManager.instance().ticker
            if ticker and ticker.scene():
                self.scene.removeItem(ticker)
                Colors.noTimerUpdate = True
                self.switchTimerOnOff(False)

                if self.fpsLabel:
                    self.fpsLabel.setText("FPS: (%d)" % int(self.fpsMedian))

                Colors.debug("- benchmark adaption: removed ticker (fps < 30)")

            if self.fpsMedian < 20:
                Colors.noAnimations = True
                Colors.debug("- benchmark adaption: animations switched off (fps < 20)")

            Colors.adapted = True

    def drawBackgroundToPixmap(self):
        r = self.scene.sceneRect()
        self.background = QPixmap(qRound(r.width()), qRound(r.height()))
        self.background.fill(Qt.black)
        painter = QPainter(self.background)

        bg = QImage(self.imagesDir + '/demobg.png')
        painter.drawImage(0, 0, bg)

    def drawBackground(self, painter, rect):
        painter.drawPixmap(QPoint(0, 0), self.background)

    def toggleFullscreen(self):
        if self.isFullScreen():
            self.enableMask(True)
            self.showNormal()
            if MenuManager.instance().ticker:
                MenuManager.instance().ticker.pause(False)
        else:
            self.enableMask(False)
            self.showFullScreen()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()
        elif event.key() == Qt.Key_F1:
            s = ""
            s += "\nAdapt: "
            s += ["on", "off"][Colors.noAdapt]
            s += "\nAdaption occured: "
            s += ["no", "yes"][Colors.adapted]
            w = QWidget()
            s += "\nColor bit depth: %d" % w.depth()
            s += "\nWanted FPS: %d" % Colors.fps
            s += "\nBenchmarked FPS: ";
            if Colors.benchmarkFps != -1:
                s += "%d" % Colors.benchmarkFps
            else:
                s += "not calculated"
            s += "\nAnimations: ";
            s += ["on", "off"][Colors.noAnimations]
            s += "\nBlending: ";
            s += ["on", "off"][Colors.useEightBitPalette]
            s += "\nTicker: ";
            s += ["on", "off"][Colors.noTicker]
            s += "\nPixmaps: ";
            s += ["off", "on"][Colors.usePixmaps]
            s += "\nRescale images on resize: ";
            s += ["on", "off"][Colors.noRescale]
            s += "\nTimer based updates: ";
            s += ["on", "off"][Colors.noTimerUpdate]
            s += "\nSeparate loop: ";
            s += ["no", "yes"][Colors.useLoop]
            s += "\nScreen sync: ";
            s += ["yes", "no"][Colors.noScreenSync]
            QMessageBox.information(None, "Current configuration", s)

        super(MainWindow, self).keyPressEvent(event)

    def focusInEvent(self, event):
        if not Colors.pause:
            return

        if MenuManager.instance().ticker:
            MenuManager.instance().ticker.pause(False)

        code = MenuManager.instance().currentMenuCode
        if code in (MenuManager.ROOT, MenuManager.MENU1):
            self.switchTimerOnOff(True)

        self.pausedLabel.setRecursiveVisible(False)

    def focusOutEvent(self, event):
        if not Colors.pause:
            return

        if MenuManager.instance().ticker:
            MenuManager.instance().ticker.pause(True)

        code = MenuManager.instance().currentMenuCode
        if code in (MenuManager.ROOT, MenuManager.MENU1):
            self.switchTimerOnOff(False)

        self.pausedLabel.setRecursiveVisible(True)

    def resizeEvent(self, event):
        self.resetTransform()
        self.scale(event.size().width() / 800.0, event.size().height() / 600.0)

        super(MainWindow, self).resizeEvent(event)

        DemoItem.setTransform(self.transform())

        if self.companyLogo:
            r = self.scene.sceneRect()
            ttb = self.companyLogo.boundingRect()
            self.companyLogo.setPos(int((r.width() - ttb.width()) / 2),
                    595 - ttb.height())
            qtb = self.qtLogo.boundingRect()
            self.qtLogo.setPos(802 - qtb.width(), 0)

        # Changing size will almost always hurt FPS during the change so ignore
        # it.
        self.fpsHistory = []
