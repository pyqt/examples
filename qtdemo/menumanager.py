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
from xml.dom.minidom import parseString

from PyQt5.QtCore import (QByteArray, QDir, QEasingCurve, QFile, QFileInfo,
        QLibraryInfo, QObject, QPointF, QProcess, QProcessEnvironment,
        QStandardPaths, Qt, QT_VERSION, QT_VERSION_STR, QTextStream, QUrl)
from PyQt5.QtWidgets import QApplication, QMessageBox

from colors import Colors
from demoitemanimation import DemoItemAnimation
from examplecontent import ExampleContent
from itemcircleanimation import ItemCircleAnimation
from menucontent import MenuContentItem
from score import Score
from textbutton import TextButton


class MenuManager(QObject):
    ROOT, MENU1, MENU2, LAUNCH, DOCUMENTATION, QUIT, FULLSCREEN, UP, DOWN, \
            BACK, LAUNCH_QML = range(11)

    pInstance = None

    def __init__(self):
        super(MenuManager, self).__init__()

        self.contentsDoc = None
        self.assistantProcess = QProcess()
        self.helpRootUrl = ''
        self.docDir = QDir()
        self.imgDir = QDir()

        self.info = {}
        self.window = None

        self.ticker = None
        self.tickerInAnim = None
        self.upButton = None
        self.downButton = None
        self.score = Score()
        self.currentMenu = "[no menu visible]"
        self.currentCategory = "[no category visible]"
        self.currentMenuButtons = "[no menu buttons visible]"
        self.currentInfo = "[no info visible]"
        self.currentMenuCode = -1
        self.readXmlDocument()

    @classmethod
    def instance(cls):
        if cls.pInstance is None:
            cls.pInstance = cls()

        return cls.pInstance

    def getResource(self, name):
        return QByteArray()

    def readXmlDocument(self):
        root = QFileInfo(__file__).absolutePath()
        xml_file = QFile(root + '/examples.xml')
        xml_file.open(QFile.ReadOnly | QFile.Text)
        contents = xml_file.readAll().data()
        xml_file.close()

        self.contentsDoc = parseString(contents)

    def itemSelected(self, userCode, menuName):
        if userCode == MenuManager.LAUNCH:
            self.launchExample(self.currentInfo)
        elif userCode == MenuManager.LAUNCH_QML:
            self.launchQml(self.currentInfo)
        elif userCode == MenuManager.DOCUMENTATION:
            self.showDocInAssistant(self.currentInfo)
        elif userCode == MenuManager.QUIT:
            QApplication.quit()
        elif userCode == MenuManager.FULLSCREEN:
            self.window.toggleFullscreen()
        elif userCode == MenuManager.ROOT:
            # Out.
            self.score.queueMovie(self.currentMenu + ' -out', Score.FROM_START,
                    Score.LOCK_ITEMS)
            self.score.queueMovie(self.currentMenuButtons + ' -out',
                    Score.FROM_START, Score.LOCK_ITEMS)
            self.score.queueMovie(self.currentInfo + ' -out')
            self.score.queueMovie(self.currentInfo + ' -buttons -out',
                    Score.NEW_ANIMATION_ONLY)
            self.score.queueMovie('back -out', Score.ONLY_IF_VISIBLE)

            # Book-keeping.
            self.currentMenuCode = MenuManager.ROOT
            self.currentMenu = menuName + ' -menu1'
            self.currentMenuButtons = menuName + ' -buttons'
            self.currentInfo = menuName + ' -info'

            # In.
            self.score.queueMovie('upndown -shake')
            self.score.queueMovie(self.currentMenu, Score.FROM_START,
                    Score.UNLOCK_ITEMS)
            self.score.queueMovie(self.currentMenuButtons, Score.FROM_START,
                    Score.UNLOCK_ITEMS)
            self.score.queueMovie(self.currentInfo)

            if not Colors.noTicker:
                self.ticker.doIntroTransitions = True
                self.tickerInAnim.setStartDelay(2000)
                self.ticker.useGuideQt()
                self.score.queueMovie('ticker', Score.NEW_ANIMATION_ONLY)
        elif userCode == MenuManager.MENU1:
            # Out.
            self.score.queueMovie(self.currentMenu + ' -out', Score.FROM_START,
                    Score.LOCK_ITEMS)
            self.score.queueMovie(self.currentMenuButtons + ' -out',
                    Score.FROM_START, Score.LOCK_ITEMS)
            self.score.queueMovie(self.currentInfo + ' -out')

            # Book-keeping.
            self.currentMenuCode = MenuManager.MENU1
            self.currentCategory = menuName
            self.currentMenu = menuName + ' -menu1'
            self.currentInfo = menuName + ' -info'

            # In.
            self.score.queueMovie('upndown -shake')
            self.score.queueMovie('back -in')
            self.score.queueMovie(self.currentMenu, Score.FROM_START,
                    Score.UNLOCK_ITEMS)
            self.score.queueMovie(self.currentInfo)

            if not Colors.noTicker:
                self.ticker.useGuideTt()
        elif userCode == MenuManager.MENU2:
            # Out.
            self.score.queueMovie(self.currentInfo + ' -out',
                    Score.NEW_ANIMATION_ONLY)
            self.score.queueMovie(self.currentInfo + ' -buttons -out',
                    Score.NEW_ANIMATION_ONLY)

            # Book-keeping.
            self.currentMenuCode = MenuManager.MENU2
            self.currentInfo = menuName

            # In/shake.
            self.score.queueMovie('upndown -shake')
            self.score.queueMovie('back -shake')
            self.score.queueMovie(self.currentMenu + ' -shake')
            self.score.queueMovie(self.currentInfo, Score.NEW_ANIMATION_ONLY)
            self.score.queueMovie(self.currentInfo + ' -buttons',
                    Score.NEW_ANIMATION_ONLY)

            if not Colors.noTicker:
                self.score.queueMovie('ticker -out', Score.NEW_ANIMATION_ONLY)
        elif userCode == MenuManager.UP:
            backMenu = self.info[self.currentMenu]['back']
            if backMenu:
                self.score.queueMovie(self.currentMenu + ' -top_out',
                        Score.FROM_START, Score.LOCK_ITEMS)
                self.score.queueMovie(backMenu + ' -bottom_in',
                        Score.FROM_START, Score.UNLOCK_ITEMS)
                self.currentMenu = backMenu
        elif userCode == MenuManager.DOWN:
            moreMenu = self.info[self.currentMenu]['more']
            if moreMenu:
                self.score.queueMovie(self.currentMenu + ' -bottom_out',
                        Score.FROM_START, Score.LOCK_ITEMS)
                self.score.queueMovie(moreMenu + ' -top_in', Score.FROM_START,
                        Score.UNLOCK_ITEMS)
                self.currentMenu = moreMenu
        elif userCode == MenuManager.BACK:
            if self.currentMenuCode == MenuManager.MENU2:
                # Out.
                self.score.queueMovie(self.currentInfo + ' -out',
                        Score.NEW_ANIMATION_ONLY)
                self.score.queueMovie(self.currentInfo + ' -buttons -out',
                        Score.NEW_ANIMATION_ONLY)

                # Book-keeping.
                self.currentMenuCode = MenuManager.MENU1
                self.currentMenuButtons = self.currentCategory + ' -buttons'
                self.currentInfo = self.currentCategory + ' -info'

                # In/shake.
                self.score.queueMovie('upndown -shake')
                self.score.queueMovie(self.currentMenu + ' -shake')
                self.score.queueMovie(self.currentInfo,
                        Score.NEW_ANIMATION_ONLY)
                self.score.queueMovie(self.currentInfo + ' -buttons',
                        Score.NEW_ANIMATION_ONLY)

                if not Colors.noTicker:
                    self.ticker.doIntroTransitions = False
                    self.tickerInAnim.setStartDelay(500)
                    self.score.queueMovie('ticker', Score.NEW_ANIMATION_ONLY)
            elif self.currentMenuCode != MenuManager.ROOT:
                self.itemSelected(MenuManager.ROOT, Colors.rootMenuName)

        # Update back and more buttons.
        if self.info.setdefault(self.currentMenu, {}).get('back'):
            back_state = TextButton.OFF
        else:
            back_state = TextButton.DISABLED

        if self.info[self.currentMenu].get('more'):
            more_state = TextButton.OFF
        else:
            more_state = TextButton.DISABLED

        self.upButton.setState(back_state)
        self.downButton.setState(more_state)

        if self.score.hasQueuedMovies():
            self.score.playQue()
            # Playing new movies might include loading etc., so ignore the FPS
            # at this point.
            self.window.fpsHistory = []

    def showDocInAssistant(self, name):
        url = self.resolveDocUrl(name)
        Colors.debug("Sending URL to Assistant:", url)

        # Start assistant if it's not already running.
        if self.assistantProcess.state() != QProcess.Running:
            app = QLibraryInfo.location(QLibraryInfo.BinariesPath) + QDir.separator()

            if sys.platform == 'darwin':
                app += 'Assistant.app/Contents/MacOS/Assistant'
            else:
                app += 'assistant'

            args = ['-enableRemoteControl']
            self.assistantProcess.start(app, args)
            if not self.assistantProcess.waitForStarted():
                QMessageBox.critical(None, "PyQt Demo",
                        "Could not start %s." % app)
                return

        # Send command through remote control even if the process was just
        # started to activate assistant and bring it to the front.
        cmd_str = QTextStream(self.assistantProcess)
        cmd_str << 'SetSource ' << url << '\n'

    def launchExample(self, name):
        executable = self.resolveExeFile(name)

        process = QProcess(self)
        process.error.connect(self.launchError)

        if sys.platform == 'win32':
            # Make sure it finds the DLLs on Windows.
            env = QProcessEnvironment.systemEnvironment()
            env.insert('PATH',
                    QLibraryInfo.location(QLibraryInfo.BinariesPath) + ';' +
                            env.value('PATH'))
            process.setProcessEnvironment(env)

        if self.info[name]['changedirectory'] != 'false':
            workingDirectory = self.resolveDataDir(name)
            process.setWorkingDirectory(workingDirectory)
            Colors.debug("Setting working directory:", workingDirectory)

        Colors.debug("Launching:", executable)
        process.start(sys.executable, [executable])

    def launchQml(self, name):
        import_path = self.resolveDataDir(name)
        qml = self.resolveQmlFile(name)

        process = QProcess(self)
        process.error.connect(self.launchError)

        env = QProcessEnvironment.systemEnvironment()
        env.insert('QML2_IMPORT_PATH', import_path)
        process.setProcessEnvironment(env)

        executable = QLibraryInfo.location(QLibraryInfo.BinariesPath) + '/qmlscene'
        Colors.debug("Launching:", executable)
        process.start(executable, [qml])

    def launchError(self, error):
        if error != QProcess.Crashed:
            QMessageBox.critical(None, "Failed to launch the example",
                    "Could not launch the example. Ensure that it has been "
                    "built.",
                    QMessageBox.Cancel)

    def init(self, window):
        self.window = window

        # Create div.
        self.createTicker()
        self.createUpnDownButtons()
        self.createBackButton()

        # Create first level menu.
        rootElement = self.contentsDoc.documentElement
        self.createRootMenu(rootElement)

        # Create second level menus.
        level2Menu = self._first_element(rootElement)
        while level2Menu is not None:
            self.createSubMenu(level2Menu)

            # Create leaf menu and example info.
            example = self._first_element(level2Menu)
            while example is not None:
                self.readInfoAboutExample(example)
                self.createLeafMenu(example)
                example = self._next_element(example)

            level2Menu = self._next_element(level2Menu)

    @classmethod
    def _first_element(cls, node):
        return cls._skip_nonelements(node.firstChild)

    @classmethod
    def _next_element(cls, node):
        return cls._skip_nonelements(node.nextSibling)

    @staticmethod
    def _skip_nonelements(node):
        while node is not None and node.nodeType != node.ELEMENT_NODE:
            node = node.nextSibling

        return node

    def readInfoAboutExample(self, example):
        name = example.getAttribute('name')
        if name in self.info:
            Colors.debug("__WARNING: MenuManager.readInfoAboutExample: "
                         "Demo/example with name", name, "appears twice in "
                         "the xml-file!__")

        self.info.setdefault(name, {})['filename'] = example.getAttribute('filename')
        self.info[name]['dirname'] = example.parentNode.getAttribute('dirname')
        self.info[name]['changedirectory'] = example.getAttribute('changedirectory')
        self.info[name]['image'] = example.getAttribute('image')
        self.info[name]['qml'] = example.getAttribute('qml')

    def resolveDir(self, name):
        dirName = self.info[name]['dirname']
        fileName = self.info[name]['filename'].split('/')

        dir = QFileInfo(__file__).dir()
        # To the 'examples' directory.
        dir.cdUp()

        dir.cd(dirName)

        if len(fileName) > 1:
            dir.cd('/'.join(fileName[:-1]))

        # This may legitimately fail if the example is just a simple .py file.
        dir.cd(fileName[-1])

        return dir

    def resolveDataDir(self, name):
        return self.resolveDir(name).absolutePath()

    def resolveExeFile(self, name):
        dir = self.resolveDir(name)

        fileName = self.info[name]['filename'].split('/')[-1]

        pyFile = QFile(dir.path() + '/' + fileName + '.py')
        if pyFile.exists():
            return pyFile.fileName()

        pywFile = QFile(dir.path() + '/' + fileName + '.pyw')
        if pywFile.exists():
            return pywFile.fileName()

        Colors.debug("- WARNING: Could not resolve executable:", dir.path(),
                fileName)
        return '__executable not found__'

    def resolveQmlFile(self, name):
        dir = self.resolveDir(name)

        fileName = self.info[name]['filename'].split('/')[-1]

        qmlFile = QFile(dir.path() + '/' + fileName + '.qml')
        if qmlFile.exists():
            return qmlFile.fileName()

        Colors.debug("- WARNING: Could not resolve QML file:", dir.path(),
                fileName)
        return '__QML not found__'

    def resolveDocUrl(self, name):
        dirName = self.info[name]['dirname']
        fileName = self.info[name]['filename']

        return self.helpRootUrl + dirName.replace('/', '-') + '-' + fileName + '.html'

    def resolveImageUrl(self, name):
        return self.helpRootUrl + 'images/' + name

    def getHtml(self, name):
        return self.getResource(self.resolveDocUrl(name))

    def getImage(self, name):
        imageName = self.info[name]['image']
        fileName = self.info[name]['filename']

        if self.info[name]['qml'] == 'true':
            fileName = 'qml-' + fileName.split('/')[-1]

        if not imageName:
            imageName = fileName + '-example.png'

            if self.getResource(self.resolveImageUrl(imageName)).isEmpty():
                imageName = fileName + '.png'

            if self.getResource(self.resolveImageUrl(imageName)).isEmpty():
                imageName = fileName + 'example.png'

        return self.getResource(self.resolveImageUrl(imageName))

    def createRootMenu(self, el):
        name = el.getAttribute('name')
        self.createMenu(el, MenuManager.MENU1)
        self.createInfo(
                MenuContentItem(el, self.window.mainSceneRoot),
                name + ' -info')

        menuButtonsIn = self.score.insertMovie(name + ' -buttons')
        menuButtonsOut = self.score.insertMovie(name + ' -buttons -out')
        self.createLowLeftButton("Quit", MenuManager.QUIT, menuButtonsIn,
                menuButtonsOut, None)
        self.createLowRightButton("Toggle fullscreen", MenuManager.FULLSCREEN,
                menuButtonsIn, menuButtonsOut, None)

    def createSubMenu(self, el):
        name = el.getAttribute('name')
        self.createMenu(el, MenuManager.MENU2)
        self.createInfo(
                MenuContentItem(el, self.window.mainSceneRoot),
                name + ' -info')

    def createLeafMenu(self, el):
        name = el.getAttribute('name')
        self.createInfo(ExampleContent(name, self.window.mainSceneRoot), name)

        infoButtonsIn = self.score.insertMovie(name + ' -buttons')
        infoButtonsOut = self.score.insertMovie(name + ' -buttons -out')
        self.createLowRightLeafButton("Documentation", 600,
                MenuManager.DOCUMENTATION, infoButtonsIn, infoButtonsOut, None)
        if el.getAttribute('executable') != 'false':
            self.createLowRightLeafButton("Launch", 405, MenuManager.LAUNCH,
                    infoButtonsIn, infoButtonsOut, None)
        elif el.getAttribute('qml') == 'true':
            self.createLowRightLeafButton("Display", 405,
                    MenuManager.LAUNCH_QML, infoButtonsIn, infoButtonsOut,
                    None)

    def createMenu(self, category, type):
        sw = self.window.scene.sceneRect().width()
        xOffset = 15
        yOffset = 10
        maxExamples = Colors.menuCount
        menuIndex = 1
        name = category.getAttribute('name')
        currentNode = self._first_element(category)
        currentMenu = '%s -menu%d' % (name, menuIndex)

        while currentNode is not None:
            movieIn = self.score.insertMovie(currentMenu)
            movieOut = self.score.insertMovie(currentMenu + ' -out')
            movieNextTopOut = self.score.insertMovie(currentMenu + ' -top_out')
            movieNextBottomOut = self.score.insertMovie(currentMenu + ' -bottom_out')
            movieNextTopIn = self.score.insertMovie(currentMenu + ' -top_in')
            movieNextBottomIn = self.score.insertMovie(currentMenu + ' -bottom_in')
            movieShake = self.score.insertMovie(currentMenu + ' -shake')

            i = 0
            while currentNode is not None and i < maxExamples:
                # Create a normal menu button.
                label = currentNode.getAttribute('name')
                item = TextButton(label, TextButton.LEFT, type,
                        self.window.mainSceneRoot)

                item.setRecursiveVisible(False)
                item.setZValue(10)
                ih = item.sceneBoundingRect().height()
                iw = item.sceneBoundingRect().width()
                ihp = ih + 3

                # Create in-animation.
                anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_IN)
                anim.setDuration(1000 + (i * 20))
                anim.setStartValue(QPointF(xOffset, -ih))
                anim.setKeyValueAt(0.20, QPointF(xOffset, -ih))
                anim.setKeyValueAt(0.50, QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY + (10 * float(i / 4.0))))
                anim.setKeyValueAt(0.60, QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                anim.setKeyValueAt(0.70, QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY + (5 * float(i / 4.0))))
                anim.setKeyValueAt(0.80, QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                anim.setKeyValueAt(0.90, QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY + (2 * float(i / 4.0))))
                anim.setEndValue(QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                movieIn.append(anim)

                # Create out-animation.
                anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_OUT)
                anim.setHideOnFinished(True)
                anim.setDuration(700 + (30 * i))
                anim.setStartValue(QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                anim.setKeyValueAt(0.60, QPointF(xOffset, 600 - ih - ih))
                anim.setKeyValueAt(0.65, QPointF(xOffset + 20, 600 - ih))
                anim.setEndValue(QPointF(sw + iw, 600 - ih))
                movieOut.append(anim)

                # Create shake-animation.
                anim = DemoItemAnimation(item)
                anim.setDuration(700)
                anim.setStartValue(QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                anim.setKeyValueAt(0.55, QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY - i*2.0))
                anim.setKeyValueAt(0.70, QPointF(xOffset - 10, (i * ihp) + yOffset + Colors.contentStartY - i*1.5))
                anim.setKeyValueAt(0.80, QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY - i*1.0))
                anim.setKeyValueAt(0.90, QPointF(xOffset - 2, (i * ihp) + yOffset + Colors.contentStartY - i*0.5))
                anim.setEndValue(QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                movieShake.append(anim)

                # Create next-menu top-out-animation.
                anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_OUT)
                anim.setHideOnFinished(True)
                anim.setDuration(200 + (30 * i))
                anim.setStartValue(QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                anim.setKeyValueAt(0.70, QPointF(xOffset, yOffset + Colors.contentStartY))
                anim.setEndValue(QPointF(-iw, yOffset + Colors.contentStartY))
                movieNextTopOut.append(anim)

                # Create next-menu bottom-out-animation.
                anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_OUT)
                anim.setHideOnFinished(True)
                anim.setDuration(200 + (30 * i))
                anim.setStartValue(QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                anim.setKeyValueAt(0.70, QPointF(xOffset, (maxExamples * ihp) + yOffset + Colors.contentStartY))
                anim.setEndValue(QPointF(-iw, (maxExamples * ihp) + yOffset + Colors.contentStartY))
                movieNextBottomOut.append(anim)

                # Create next-menu top-in-animation.
                anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_IN)
                anim.setDuration(700 - (30 * i))
                anim.setStartValue(QPointF(-iw, yOffset + Colors.contentStartY))
                anim.setKeyValueAt(0.30, QPointF(xOffset, yOffset + Colors.contentStartY))
                anim.setEndValue(QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                movieNextTopIn.append(anim)

                # Create next-menu bottom-in-animation.
                reverse = maxExamples - i
                anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_IN)
                anim.setDuration(1000 - (30 * reverse))
                anim.setStartValue(QPointF(-iw, (maxExamples * ihp) + yOffset + Colors.contentStartY))
                anim.setKeyValueAt(0.30, QPointF(xOffset, (maxExamples * ihp) + yOffset + Colors.contentStartY))
                anim.setEndValue(QPointF(xOffset, (i * ihp) + yOffset + Colors.contentStartY))
                movieNextBottomIn.append(anim)

                i += 1
                currentNode = self._next_element(currentNode)

            if currentNode is not None and i == maxExamples:
                # We need another menu, so register for 'more' and 'back'
                # buttons.
                menuIndex += 1
                self.info.setdefault(currentMenu, {})['more'] = '%s -menu%d' % (name, menuIndex)
                currentMenu = '%s -menu%d' % (name, menuIndex)
                self.info.setdefault(currentMenu, {})['back'] = '%s -menu%d' % (name, menuIndex - 1)

    def createLowLeftButton(self, label, type, movieIn, movieOut, movieShake, menuString=""):
        button = TextButton(label, TextButton.RIGHT, type,
                self.window.mainSceneRoot, TextButton.PANEL)
        if menuString:
            button.setMenuString(menuString)
        button.setRecursiveVisible(False)
        button.setZValue(10)

        iw = button.sceneBoundingRect().width()
        xOffset = 15

        # Create in-animation.
        buttonIn = DemoItemAnimation(button, DemoItemAnimation.ANIM_IN)
        buttonIn.setDuration(1800)
        buttonIn.setStartValue(QPointF(-iw, Colors.contentStartY + Colors.contentHeight - 35))
        buttonIn.setKeyValueAt(0.5, QPointF(-iw, Colors.contentStartY + Colors.contentHeight - 35))
        buttonIn.setKeyValueAt(0.7, QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 35))
        buttonIn.setEndValue(QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 26))
        movieIn.append(buttonIn)

        # Create out-animation.
        buttonOut = DemoItemAnimation(button, DemoItemAnimation.ANIM_OUT)
        buttonOut.setHideOnFinished(True)
        buttonOut.setDuration(400)
        buttonOut.setStartValue(QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 26))
        buttonOut.setEndValue(QPointF(-iw, Colors.contentStartY + Colors.contentHeight - 26))
        movieOut.append(buttonOut)

        if movieShake is not None:
            shakeAnim = DemoItemAnimation(button, DemoItemAnimation.ANIM_UNSPECIFIED)
            shakeAnim.setDuration(650)
            shakeAnim.setStartValue(buttonIn.endValue())
            shakeAnim.setKeyValueAt(0.60, buttonIn.endValue())
            shakeAnim.setKeyValueAt(0.70, buttonIn.endValue() + QPointF(-3, 0))
            shakeAnim.setKeyValueAt(0.80, buttonIn.endValue() + QPointF(2, 0))
            shakeAnim.setKeyValueAt(0.90, buttonIn.endValue() + QPointF(-1, 0))
            shakeAnim.setEndValue(buttonIn.endValue())
            movieShake.append(shakeAnim)

    def createLowRightButton(self, label, type, movieIn, movieOut, movieShake):
        item = TextButton(label, TextButton.RIGHT, type,
                self.window.mainSceneRoot, TextButton.PANEL)
        item.setRecursiveVisible(False)
        item.setZValue(10)

        sw = self.window.scene.sceneRect().width()
        xOffset = 70

        # Create in-animation.
        anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_IN)
        anim.setDuration(1800)
        anim.setStartValue(QPointF(sw, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setKeyValueAt(0.5, QPointF(sw, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setKeyValueAt(0.7, QPointF(xOffset + 535, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setEndValue(QPointF(xOffset + 535, Colors.contentStartY + Colors.contentHeight - 26))
        movieIn.append(anim)

        # Create out-animation.
        anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_OUT)
        anim.setHideOnFinished(True)
        anim.setDuration(400)
        anim.setStartValue(QPointF(xOffset + 535, Colors.contentStartY + Colors.contentHeight - 26))
        anim.setEndValue(QPointF(sw, Colors.contentStartY + Colors.contentHeight - 26))
        movieOut.append(anim)

    def createLowRightLeafButton(self, label, xOffset, type, movieIn, movieOut, movieShake):
        item = TextButton(label, TextButton.RIGHT, type,
                self.window.mainSceneRoot, TextButton.PANEL)
        item.setRecursiveVisible(False)
        item.setZValue(10)

        sw = self.window.scene.sceneRect().width()
        sh = self.window.scene.sceneRect().height()

        # Create in-animation.
        anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_IN)
        anim.setDuration(1050)
        anim.setStartValue(QPointF(sw, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setKeyValueAt(0.10, QPointF(sw, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setKeyValueAt(0.30, QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setKeyValueAt(0.35, QPointF(xOffset + 30, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setKeyValueAt(0.40, QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setKeyValueAt(0.45, QPointF(xOffset + 5, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setKeyValueAt(0.50, QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 35))
        anim.setEndValue(QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 26))
        movieIn.append(anim)

        # Create out-animation.
        anim = DemoItemAnimation(item, DemoItemAnimation.ANIM_OUT)
        anim.setHideOnFinished(True)
        anim.setDuration(300)
        anim.setStartValue(QPointF(xOffset, Colors.contentStartY + Colors.contentHeight - 26))
        anim.setEndValue(QPointF(xOffset, sh))
        movieOut.append(anim)

    def createInfo(self, item, name):
        movie_in = self.score.insertMovie(name)
        movie_out = self.score.insertMovie(name + ' -out')
        item.setZValue(8)
        item.setRecursiveVisible(False)

        xOffset = 230.0
        infoIn = DemoItemAnimation(item, DemoItemAnimation.ANIM_IN)
        infoIn.setDuration(650)
        infoIn.setStartValue(QPointF(self.window.scene.sceneRect().width(), Colors.contentStartY))
        infoIn.setKeyValueAt(0.60, QPointF(xOffset, Colors.contentStartY))
        infoIn.setKeyValueAt(0.70, QPointF(xOffset + 20, Colors.contentStartY))
        infoIn.setKeyValueAt(0.80, QPointF(xOffset, Colors.contentStartY))
        infoIn.setKeyValueAt(0.90, QPointF(xOffset + 7, Colors.contentStartY))
        infoIn.setEndValue(QPointF(xOffset, Colors.contentStartY))
        movie_in.append(infoIn)

        infoOut = DemoItemAnimation(item, DemoItemAnimation.ANIM_OUT)
        infoOut.setCurveShape(QEasingCurve.InQuad)
        infoOut.setDuration(300)
        infoOut.setHideOnFinished(True)
        infoOut.setStartValue(QPointF(xOffset, Colors.contentStartY))
        infoOut.setEndValue(QPointF(-600, Colors.contentStartY))
        movie_out.append(infoOut)

    def createTicker(self):
        if Colors.noTicker:
            return

        movie_in = self.score.insertMovie('ticker')
        movie_out = self.score.insertMovie('ticker -out')
        movie_activate = self.score.insertMovie('ticker -activate')
        movie_deactivate = self.score.insertMovie('ticker -deactivate')

        self.ticker = ItemCircleAnimation()
        self.ticker.setZValue(50)
        self.ticker.hide()

        # Move ticker in.
        qtendpos = 485
        qtPosY = 120
        self.tickerInAnim = DemoItemAnimation(self.ticker,
                DemoItemAnimation.ANIM_IN)
        self.tickerInAnim.setDuration(500)
        self.tickerInAnim.setStartValue(QPointF(self.window.scene.sceneRect().width(), Colors.contentStartY + qtPosY))
        self.tickerInAnim.setKeyValueAt(0.60, QPointF(qtendpos, Colors.contentStartY + qtPosY))
        self.tickerInAnim.setKeyValueAt(0.70, QPointF(qtendpos + 30, Colors.contentStartY + qtPosY))
        self.tickerInAnim.setKeyValueAt(0.80, QPointF(qtendpos, Colors.contentStartY + qtPosY))
        self.tickerInAnim.setKeyValueAt(0.90, QPointF(qtendpos + 5, Colors.contentStartY + qtPosY))
        self.tickerInAnim.setEndValue(QPointF(qtendpos, Colors.contentStartY + qtPosY))
        movie_in.append(self.tickerInAnim)

        # Move ticker out.
        qtOut = DemoItemAnimation(self.ticker, DemoItemAnimation.ANIM_OUT)
        qtOut.setHideOnFinished(True)
        qtOut.setDuration(500)
        qtOut.setStartValue(QPointF(qtendpos, Colors.contentStartY + qtPosY))
        qtOut.setEndValue(QPointF(self.window.scene.sceneRect().width() + 700, Colors.contentStartY + qtPosY))
        movie_out.append(qtOut)

        # Move ticker in on activate.
        qtActivate = DemoItemAnimation(self.ticker)
        qtActivate.setDuration(400)
        qtActivate.setStartValue(QPointF(self.window.scene.sceneRect().width(), Colors.contentStartY + qtPosY))
        qtActivate.setKeyValueAt(0.60, QPointF(qtendpos, Colors.contentStartY + qtPosY))
        qtActivate.setKeyValueAt(0.70, QPointF(qtendpos + 30, Colors.contentStartY + qtPosY))
        qtActivate.setKeyValueAt(0.80, QPointF(qtendpos, Colors.contentStartY + qtPosY))
        qtActivate.setKeyValueAt(0.90, QPointF(qtendpos + 5, Colors.contentStartY + qtPosY))
        qtActivate.setEndValue(QPointF(qtendpos, Colors.contentStartY + qtPosY))
        movie_activate.append(qtActivate)

        # Move ticker out on deactivate.
        qtDeactivate = DemoItemAnimation(self.ticker)
        qtDeactivate.setHideOnFinished(True)
        qtDeactivate.setDuration(400)
        qtDeactivate.setStartValue(QPointF(qtendpos, Colors.contentStartY + qtPosY))
        qtDeactivate.setEndValue(QPointF(qtendpos, 800))
        movie_deactivate.append(qtDeactivate)

    def createUpnDownButtons(self):
        xOffset = 15.0
        yOffset = 450.0

        self.upButton = TextButton("", TextButton.LEFT, MenuManager.UP,
                self.window.mainSceneRoot, TextButton.UP)
        self.upButton.prepare()
        self.upButton.setPos(xOffset, yOffset)
        self.upButton.setState(TextButton.DISABLED)

        self.downButton = TextButton("", TextButton.LEFT, MenuManager.DOWN,
                self.window.mainSceneRoot, TextButton.DOWN)
        self.downButton.prepare()
        self.downButton.setPos(xOffset + 10 + self.downButton.sceneBoundingRect().width(), yOffset)

        movieShake = self.score.insertMovie('upndown -shake')

        shakeAnim = DemoItemAnimation(self.upButton,
                DemoItemAnimation.ANIM_UNSPECIFIED)
        shakeAnim.setDuration(650)
        shakeAnim.setStartValue(self.upButton.pos())
        shakeAnim.setKeyValueAt(0.60, self.upButton.pos())
        shakeAnim.setKeyValueAt(0.70, self.upButton.pos() + QPointF(-2, 0))
        shakeAnim.setKeyValueAt(0.80, self.upButton.pos() + QPointF(1, 0))
        shakeAnim.setKeyValueAt(0.90, self.upButton.pos() + QPointF(-1, 0))
        shakeAnim.setEndValue(self.upButton.pos())
        movieShake.append(shakeAnim)

        shakeAnim = DemoItemAnimation(self.downButton,
                DemoItemAnimation.ANIM_UNSPECIFIED)
        shakeAnim.setDuration(650)
        shakeAnim.setStartValue(self.downButton.pos())
        shakeAnim.setKeyValueAt(0.60, self.downButton.pos())
        shakeAnim.setKeyValueAt(0.70, self.downButton.pos() + QPointF(-5, 0))
        shakeAnim.setKeyValueAt(0.80, self.downButton.pos() + QPointF(-3, 0))
        shakeAnim.setKeyValueAt(0.90, self.downButton.pos() + QPointF(-1, 0))
        shakeAnim.setEndValue(self.downButton.pos())
        movieShake.append(shakeAnim)

    def createBackButton(self):
        backIn = self.score.insertMovie('back -in')
        backOut = self.score.insertMovie('back -out')
        backShake = self.score.insertMovie('back -shake')
        self.createLowLeftButton("Back", MenuManager.ROOT, backIn, backOut,
                backShake, Colors.rootMenuName)
