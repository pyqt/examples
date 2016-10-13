#!/usr/bin/env python


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


from PyQt5.QtCore import QEventLoop, QTime
from PyQt5.QtWidgets import QApplication, QMessageBox

from colors import Colors
from mainwindow import MainWindow
from menumanager import MenuManager


def artisticSleep(sleepTime):
    time = QTime()
    time.restart()
    while time.elapsed() < sleepTime:
        QApplication.processEvents(QEventLoop.AllEvents, 50)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    Colors.parseArgs(sys.argv)

    if sys.platform == 'win32':
        QMessageBox.information(None, "Documentation Warning",
                "If you are using the GPL version of PyQt from the binary "
                "installer then you will probably see warning messages about "
                "missing documentation.  This is because the installer does "
                "not include a copy of the Qt documentation as it is so "
                "large.")

    mainWindow = MainWindow()
    MenuManager.instance().init(mainWindow)
    mainWindow.setFocus()

    if Colors.fullscreen:
        mainWindow.showFullScreen()
    else:
        mainWindow.enableMask(True)
        mainWindow.show()

    artisticSleep(500)
    mainWindow.start()

    sys.exit(app.exec_())
