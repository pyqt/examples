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


import sys

from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QMessageBox, QWidget


class Colors(object):
    # Colors:
    sceneBg1 = QColor(91, 91, 91)
    sceneBg1Line = QColor(114, 108, 104)
    sceneBg2 = QColor(0, 0, 0)
    sceneLine = QColor(255, 255, 255)
    paperBg = QColor(100, 100, 100)
    menuTextFg = QColor(255, 0, 0)
    buttonBgLow = QColor(255, 255, 255, 90)
    buttonBgHigh = QColor(255, 255, 255, 20)
    buttonText = QColor(255, 255, 255)
    tt_green = QColor(166, 206, 57)
    fadeOut = QColor(206, 246, 117, 0)
    heading = QColor(190, 230, 80)
    contentColor = "<font color='#eeeeee'>"
    glVersion = "Not detected!"

    # Guides:
    stageStartY = 8
    stageHeight = 536
    stageStartX = 8
    stageWidth = 785
    contentStartY = 22
    contentHeight = 510

    # Properties:
    noTicker = False
    noRescale = False
    noAnimations = False
    noBlending = False
    noScreenSync = False
    fullscreen = False
    usePixmaps = False
    useLoop = False
    showBoundingRect = False
    showFps = False
    noAdapt = False
    noWindowMask = True
    useButtonBalls = False
    useEightBitPalette = False
    noTimerUpdate = False
    noTickerMorph = False
    adapted = False
    verbose = False
    pause = True

    fps = 100
    menuCount = 18
    animSpeed = 1.0
    benchmarkFps = -1.0
    tickerLetterCount = 80;
    tickerMoveSpeed = 0.4
    tickerMorphSpeed = 2.5
    tickerText = ".EROM ETAERC .SSEL EDOC"
    rootMenuName = "PyQt Examples"

    @staticmethod
    def contentFont():
        font = QFont()
        font.setStyleStrategy(QFont.PreferAntialias)

        if sys.platform == 'darwin':
            font.setPixelSize(14)
            font.setFamily('Arial')
        else:
            font.setPixelSize(13)
            font.setFamily('Verdana')

        return font

    @staticmethod
    def headingFont():
        font = QFont()
        font.setStyleStrategy(QFont.PreferAntialias)

        font.setPixelSize(23)
        font.setBold(True)
        font.setFamily('Verdana')

        return font;

    @staticmethod
    def buttonFont():
        font = QFont()
        font.setStyleStrategy(QFont.PreferAntialias)

        font.setPixelSize(11)
        font.setFamily('Verdana')

        return font

    @staticmethod
    def tickerFont():
        font = QFont()
        font.setStyleStrategy(QFont.PreferAntialias)

        if sys.platform == 'darwin':
            font.setPixelSize(11)
            font.setBold(True)
            font.setFamily('Arial')
        else:
            font.setPixelSize(10)
            font.setBold(True)
            font.setFamily('sans serif')

        return font

    @classmethod
    def debug(cls, *args):
        if cls.verbose:
            sys.stderr.write("%s\n" % " ".join([str(arg) for arg in args]))

    @classmethod
    def parseArgs(cls, argv):
        # Some arguments should be processed before others.  Handle them now.
        if "-verbose" in argv:
            cls.verbose = True

        # Handle the rest of the arguments.  They may override attributes
        # already set.
        for s in argv:
            if s == "-no-ticker":
                cls.noTicker = True
            elif s.startswith("-ticker"):
                cls.noTicker =  not bool(parseFloat(s, "-ticker"))
            elif s == "-no-animations":
                cls.noAnimations = True
            elif s.startswith("-animations"):
                cls.noAnimations = not bool(parseFloat(s, "-animations"))
            elif s == "-no-adapt":
                # Don't adapt the animations based on the actual performance.
                cls.noAdapt = True
            elif s == "-low":
                cls.setLowSettings()
            elif s == "-no-rescale":
                cls.noRescale = True
            elif s == "-use-pixmaps":
                cls.usePixmaps = True
            elif s == "-fullscreen":
                cls.fullscreen = True
            elif s == "-show-br":
                cls.showBoundingRect = True
            elif s == "-show-fps":
                cls.showFps = True
            elif s == "-no-blending":
                cls.noBlending = True
            elif s == "-no-sync":
                cls.noScreenSync = True
            elif s.startswith("-menu"):
                cls.menuCount = int(parseFloat(s, "-menu"))
            elif s.startswith("-use-timer-update"):
                cls.noTimerUpdate = not bool(parseFloat(s, "-use-timer-update"))
            elif s.startswith("-pause"):
                cls.pause = bool(parseFloat(s, "-pause"))
            elif s == "-no-ticker-morph":
                cls.noTickerMorph = True
            elif s == "-use-window-mask":
                cls.noWindowMask = False
            elif s == "-use-loop":
                cls.useLoop = True
            elif s == "-use-8bit":
                cls.useEightBitPalette = True
            elif s.startswith("-8bit"):
                cls.useEightBitPalette = bool(parseFloat(s, "-8bit"))
            elif s == "-use-balls":
                cls.useButtonBalls = True
            elif s.startswith("-ticker-letters"):
                cls.tickerLetterCount = int(parseFloat(s, "-ticker-letters"))
            elif s.startswith("-ticker-text"):
                cls.tickerText = parseText(s, "-ticker-text")
            elif s.startswith("-ticker-speed"):
                cls.tickerMoveSpeed = parseFloat(s, "-ticker-speed")
            elif s.startswith("-ticker-morph-speed"):
                cls.tickerMorphSpeed = parseFloat(s, "-ticker-morph-speed")
            elif s.startswith("-animation-speed"):
                cls.animSpeed = parseFloat(s, "-animation-speed")
            elif s.startswith("-fps"):
                cls.fps = int(parseFloat(s, "-fps"))
            elif s.startswith("-h") or s.startswith("-help"):
                QMessageBox.warning(None, "Arguments",
                        "Usage: qtdemo.py [-verbose] [-no-adapt] "
                        "[-fullscreen] [-ticker[0|1]] "
                        "[-animations[0|1]] [-no-blending] [-no-sync] "
                        "[-use-timer-update[0|1]] [-pause[0|1]] "
                        "[-use-window-mask] [-no-rescale] [-use-pixmaps] "
                        "[-show-fps] [-show-br] [-8bit[0|1]] [-menu<int>] "
                        "[-use-loop] [-use-balls] [-animation-speed<float>] "
                        "[-fps<int>] [-low] [-ticker-letters<int>] "
                        "[-ticker-speed<float>] [-no-ticker-morph] "
                        "[-ticker-morph-speed<float>] [-ticker-text<string>]")
                sys.exit(0)

        cls.postConfigure()

    @classmethod
    def setLowSettings(cls):
        cls.noTicker = True
        cls.noTimerUpdate = True
        cls.fps = 30
        cls.usePixmaps = True
        cls.noAnimations = True
        cls.noBlending = True

    @classmethod
    def postConfigure(cls):
        if not cls.noAdapt:
            w = QWidget()

            if w.depth() < 16:
                cls.useEightBitPalette = True
                cls.adapted = True
                cls.debug("- Adapt: Color depth less than 16 bit. Using 8 bit palette")


def parseFloat(argument, name):
    try:
        value = float(parseText(argument, name))
    except ValueError:
        value = 0.0

    return value


def parseText(argument, name):
    if len(name) == len(argument):
        QMessageBox.warning(None, "Arguments",
                "No argument number found for %s. Remember to put name and "
                "value adjacent! (e.g. -fps100)")
        sys.exit(0)

    return argument[len(name):]
