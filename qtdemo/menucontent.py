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


from PyQt5.QtCore import QFile, QFileInfo, QRectF, QTextStream

from colors import Colors
from demoitem import DemoItem
from demoitemanimation import DemoItemAnimation
from demotextitem import DemoTextItem
from headingitem import HeadingItem


class MenuContentItem(DemoItem):
    def __init__(self, el, parent=None):
        super(MenuContentItem, self).__init__(parent)

        self.name = el.getAttribute('name')
        self.heading = None
        self.description1 = None
        self.description2 = None

        readme_dir = QFileInfo(__file__).dir()
        readme_dir.cdUp()
        readme_dir.cd(el.getAttribute('dirname'))

        self.readmePath = readme_dir.absoluteFilePath('README')

        self._prepared = False

    def prepare(self):
        if not self._prepared:
            self.createContent()
            self._prepared= True

    def animationStopped(self, id):
        if self.name == Colors.rootMenuName:
            # Optimization hack.
            return

        if id == DemoItemAnimation.ANIM_OUT:
            # Free up some memory
            self.heading = None
            self.description1 = None
            self.description2 = None
            self._prepared = False

    def loadDescription(self, startPara, nrPara):
        readme = QFile(self.readmePath)
        if not readme.open(QFile.ReadOnly):
            Colors.debug("- MenuContentItem.loadDescription: Could not load:", self.readmePath)
            return ""

        in_str = QTextStream(readme)
        # Skip a certain number of paragraphs.
        while startPara:
            if not in_str.readLine():
                startPara -= 1

        # Read in the number of wanted paragraphs.
        result = ''
        line = in_str.readLine()
        while True:
            result += line + " "
            line = in_str.readLine()
            if not line:
                nrPara -= 1
                line = "<br><br>" + in_str.readLine()

            if nrPara == 0 or in_str.atEnd():
                break

        return Colors.contentColor + result

    def createContent(self):
        # Create the items.
        self.heading = HeadingItem(self.name, self)
        para1 = self.loadDescription(0, 1)
        if not para1:
            para1 = Colors.contentColor + "Could not load description. Ensure that the documentation for Qt is built."
        bgcolor = Colors.sceneBg1.darker(200)
        bgcolor.setAlpha(100)
        self.description1 = DemoTextItem(para1, Colors.contentFont(),
                Colors.heading, 500, self, DemoTextItem.STATIC_TEXT)
        self.description2 = DemoTextItem(self.loadDescription(1, 2),
                Colors.contentFont(), Colors.heading, 250, self,
                DemoTextItem.STATIC_TEXT)

        # Place the items on screen.
        self.heading.setPos(0, 3)
        self.description1.setPos(0, self.heading.pos().y() + self.heading.boundingRect().height() + 10)
        self.description2.setPos(0, self.description1.pos().y() + self.description1.boundingRect().height() + 15)

    def boundingRect(self):
        return QRectF(0, 0, 500, 350)
