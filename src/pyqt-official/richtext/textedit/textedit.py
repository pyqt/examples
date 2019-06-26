#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited
## Copyright (C) 2010 Hans-Peter Jansen <hpj@urpla.net>.
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

from PyQt5.QtCore import QFile, QFileInfo, Qt, QTextCodec
from PyQt5.QtGui import (QFont, QFontDatabase, QFontInfo, QIcon, QKeySequence,
        QPixmap, QTextBlockFormat, QTextCharFormat, QTextCursor,
        QTextDocumentWriter, QTextListFormat)
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QColorDialog,
        QComboBox, QFileDialog, QFontComboBox, QMainWindow, QMenu, QMessageBox,
        QTextEdit, QToolBar)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog

import textedit_rc


if sys.platform.startswith('darwin'):
    rsrcPath = ":/images/mac"
else:
    rsrcPath = ":/images/win"


class TextEdit(QMainWindow):
    def __init__(self, fileName=None, parent=None):
        super(TextEdit, self).__init__(parent)

        self.setWindowIcon(QIcon(':/images/logo.png'))
        self.setToolButtonStyle(Qt.ToolButtonFollowStyle)
        self.setupFileActions()
        self.setupEditActions()
        self.setupTextActions()

        helpMenu = QMenu("Help", self)
        self.menuBar().addMenu(helpMenu)
        helpMenu.addAction("About", self.about)
        helpMenu.addAction("About &Qt", QApplication.instance().aboutQt)
 
        self.textEdit = QTextEdit(self)
        self.textEdit.currentCharFormatChanged.connect(
                self.currentCharFormatChanged)
        self.textEdit.cursorPositionChanged.connect(self.cursorPositionChanged)
        self.setCentralWidget(self.textEdit)
        self.textEdit.setFocus()
        self.setCurrentFileName()
        self.fontChanged(self.textEdit.font())
        self.colorChanged(self.textEdit.textColor())
        self.alignmentChanged(self.textEdit.alignment())
        self.textEdit.document().modificationChanged.connect(
                self.actionSave.setEnabled)
        self.textEdit.document().modificationChanged.connect(
                self.setWindowModified)
        self.textEdit.document().undoAvailable.connect(
                self.actionUndo.setEnabled)
        self.textEdit.document().redoAvailable.connect(
                self.actionRedo.setEnabled)
        self.setWindowModified(self.textEdit.document().isModified())
        self.actionSave.setEnabled(self.textEdit.document().isModified())
        self.actionUndo.setEnabled(self.textEdit.document().isUndoAvailable())
        self.actionRedo.setEnabled(self.textEdit.document().isRedoAvailable())
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionCut.setEnabled(False)
        self.actionCopy.setEnabled(False)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)
        self.textEdit.copyAvailable.connect(self.actionCut.setEnabled)
        self.textEdit.copyAvailable.connect(self.actionCopy.setEnabled)
        QApplication.clipboard().dataChanged.connect(self.clipboardDataChanged)

        if fileName is None:
            fileName = ':/example.html'

        if not self.load(fileName):
            self.fileNew()

    def closeEvent(self, e):
        if self.maybeSave():
            e.accept()
        else:
            e.ignore()

    def setupFileActions(self):
        tb = QToolBar(self)
        tb.setWindowTitle("File Actions")
        self.addToolBar(tb)

        menu = QMenu("&File", self)
        self.menuBar().addMenu(menu)

        self.actionNew = QAction(
                QIcon.fromTheme('document-new',
                        QIcon(rsrcPath + '/filenew.png')),
                "&New", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.New, triggered=self.fileNew)
        tb.addAction(self.actionNew)
        menu.addAction(self.actionNew)

        self.actionOpen = QAction(
                QIcon.fromTheme('document-open',
                        QIcon(rsrcPath + '/fileopen.png')),
                "&Open...", self, shortcut=QKeySequence.Open,
                triggered=self.fileOpen)
        tb.addAction(self.actionOpen)
        menu.addAction(self.actionOpen)
        menu.addSeparator()

        self.actionSave = QAction(
                QIcon.fromTheme('document-save',
                        QIcon(rsrcPath + '/filesave.png')),
                "&Save", self, shortcut=QKeySequence.Save,
                triggered=self.fileSave, enabled=False)
        tb.addAction(self.actionSave)
        menu.addAction(self.actionSave)

        self.actionSaveAs = QAction("Save &As...", self,
                priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.SHIFT + Qt.Key_S,
                triggered=self.fileSaveAs)
        menu.addAction(self.actionSaveAs)
        menu.addSeparator()
 
        self.actionPrint = QAction(
                QIcon.fromTheme('document-print',
                        QIcon(rsrcPath + '/fileprint.png')),
                "&Print...", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Print, triggered=self.filePrint)
        tb.addAction(self.actionPrint)
        menu.addAction(self.actionPrint)

        self.actionPrintPreview = QAction(
                QIcon.fromTheme('fileprint',
                        QIcon(rsrcPath + '/fileprint.png')),
                "Print Preview...", self,
                shortcut=Qt.CTRL + Qt.SHIFT + Qt.Key_P,
                triggered=self.filePrintPreview)
        menu.addAction(self.actionPrintPreview)

        self.actionPrintPdf = QAction(
                QIcon.fromTheme('exportpdf',
                        QIcon(rsrcPath + '/exportpdf.png')),
                "&Export PDF...", self, priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.Key_D,
                triggered=self.filePrintPdf)
        tb.addAction(self.actionPrintPdf)
        menu.addAction(self.actionPrintPdf)
        menu.addSeparator()

        self.actionQuit = QAction("&Quit", self, shortcut=QKeySequence.Quit,
                triggered=self.close)
        menu.addAction(self.actionQuit)

    def setupEditActions(self):
        tb = QToolBar(self)
        tb.setWindowTitle("Edit Actions")
        self.addToolBar(tb)

        menu = QMenu("&Edit", self)
        self.menuBar().addMenu(menu)

        self.actionUndo = QAction(
                QIcon.fromTheme('edit-undo',
                        QIcon(rsrcPath + '/editundo.png')),
                "&Undo", self, shortcut=QKeySequence.Undo)
        tb.addAction(self.actionUndo)
        menu.addAction(self.actionUndo)

        self.actionRedo = QAction(
                QIcon.fromTheme('edit-redo',
                        QIcon(rsrcPath + '/editredo.png')),
                "&Redo", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Redo)
        tb.addAction(self.actionRedo)
        menu.addAction(self.actionRedo)
        menu.addSeparator()

        self.actionCut = QAction(
                QIcon.fromTheme('edit-cut', QIcon(rsrcPath + '/editcut.png')),
                "Cu&t", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Cut)
        tb.addAction(self.actionCut)
        menu.addAction(self.actionCut)

        self.actionCopy = QAction(
                QIcon.fromTheme('edit-copy',
                        QIcon(rsrcPath + '/editcopy.png')),
                "&Copy", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Copy)
        tb.addAction(self.actionCopy)
        menu.addAction(self.actionCopy)

        self.actionPaste = QAction(
                QIcon.fromTheme('edit-paste',
                        QIcon(rsrcPath + '/editpaste.png')),
                "&Paste", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Paste,
                enabled=(len(QApplication.clipboard().text()) != 0))
        tb.addAction(self.actionPaste)
        menu.addAction(self.actionPaste)

    def setupTextActions(self):
        tb = QToolBar(self)
        tb.setWindowTitle("Format Actions")
        self.addToolBar(tb)

        menu = QMenu("F&ormat", self)
        self.menuBar().addMenu(menu)

        self.actionTextBold = QAction(
                QIcon.fromTheme('format-text-bold',
                        QIcon(rsrcPath + '/textbold.png')),
                "&Bold", self, priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.Key_B, triggered=self.textBold,
                checkable=True)
        bold = QFont()
        bold.setBold(True)
        self.actionTextBold.setFont(bold)
        tb.addAction(self.actionTextBold)
        menu.addAction(self.actionTextBold)

        self.actionTextItalic = QAction(
                QIcon.fromTheme('format-text-italic',
                        QIcon(rsrcPath + '/textitalic.png')),
                "&Italic", self, priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.Key_I, triggered=self.textItalic,
                checkable=True)
        italic = QFont()
        italic.setItalic(True)
        self.actionTextItalic.setFont(italic)
        tb.addAction(self.actionTextItalic)
        menu.addAction(self.actionTextItalic)

        self.actionTextUnderline = QAction(
                QIcon.fromTheme('format-text-underline',
                        QIcon(rsrcPath + '/textunder.png')),
                "&Underline", self, priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.Key_U, triggered=self.textUnderline,
                checkable=True)
        underline = QFont()
        underline.setUnderline(True)
        self.actionTextUnderline.setFont(underline)
        tb.addAction(self.actionTextUnderline)
        menu.addAction(self.actionTextUnderline)

        menu.addSeparator()

        grp = QActionGroup(self, triggered=self.textAlign)

        # Make sure the alignLeft is always left of the alignRight.
        if QApplication.isLeftToRight():
            self.actionAlignLeft = QAction(
                    QIcon.fromTheme('format-justify-left',
                            QIcon(rsrcPath + '/textleft.png')),
                    "&Left", grp)
            self.actionAlignCenter = QAction(
                    QIcon.fromTheme('format-justify-center',
                            QIcon(rsrcPath + '/textcenter.png')),
                    "C&enter", grp)
            self.actionAlignRight = QAction(
                    QIcon.fromTheme('format-justify-right',
                            QIcon(rsrcPath + '/textright.png')),
                    "&Right", grp)
        else:
            self.actionAlignRight = QAction(
                    QIcon.fromTheme('format-justify-right',
                            QIcon(rsrcPath + '/textright.png')),
                    "&Right", grp)
            self.actionAlignCenter = QAction(
                    QIcon.fromTheme('format-justify-center',
                            QIcon(rsrcPath + '/textcenter.png')),
                    "C&enter", grp)
            self.actionAlignLeft = QAction(
                    QIcon.fromTheme('format-justify-left',
                            QIcon(rsrcPath + '/textleft.png')),
                    "&Left", grp)
 
        self.actionAlignJustify = QAction(
                QIcon.fromTheme('format-justify-fill',
                        QIcon(rsrcPath + '/textjustify.png')),
                "&Justify", grp)

        self.actionAlignLeft.setShortcut(Qt.CTRL + Qt.Key_L)
        self.actionAlignLeft.setCheckable(True)
        self.actionAlignLeft.setPriority(QAction.LowPriority)

        self.actionAlignCenter.setShortcut(Qt.CTRL + Qt.Key_E)
        self.actionAlignCenter.setCheckable(True)
        self.actionAlignCenter.setPriority(QAction.LowPriority)

        self.actionAlignRight.setShortcut(Qt.CTRL + Qt.Key_R)
        self.actionAlignRight.setCheckable(True)
        self.actionAlignRight.setPriority(QAction.LowPriority)

        self.actionAlignJustify.setShortcut(Qt.CTRL + Qt.Key_J)
        self.actionAlignJustify.setCheckable(True)
        self.actionAlignJustify.setPriority(QAction.LowPriority)

        tb.addActions(grp.actions())
        menu.addActions(grp.actions())
        menu.addSeparator()

        pix = QPixmap(16, 16)
        pix.fill(Qt.black)
        self.actionTextColor = QAction(QIcon(pix), "&Color...", self,
                triggered=self.textColor)
        tb.addAction(self.actionTextColor)
        menu.addAction(self.actionTextColor)

        tb = QToolBar(self)
        tb.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
        tb.setWindowTitle("Format Actions")
        self.addToolBarBreak(Qt.TopToolBarArea)
        self.addToolBar(tb)

        comboStyle = QComboBox(tb)
        tb.addWidget(comboStyle)
        comboStyle.addItem("Standard")
        comboStyle.addItem("Bullet List (Disc)")
        comboStyle.addItem("Bullet List (Circle)")
        comboStyle.addItem("Bullet List (Square)")
        comboStyle.addItem("Ordered List (Decimal)")
        comboStyle.addItem("Ordered List (Alpha lower)")
        comboStyle.addItem("Ordered List (Alpha upper)")
        comboStyle.addItem("Ordered List (Roman lower)")
        comboStyle.addItem("Ordered List (Roman upper)")
        comboStyle.activated.connect(self.textStyle)

        self.comboFont = QFontComboBox(tb)
        tb.addWidget(self.comboFont)
        self.comboFont.activated[str].connect(self.textFamily)

        self.comboSize = QComboBox(tb)
        self.comboSize.setObjectName("comboSize")
        tb.addWidget(self.comboSize)
        self.comboSize.setEditable(True)

        db = QFontDatabase()
        for size in db.standardSizes():
            self.comboSize.addItem("%s" % (size))

        self.comboSize.activated[str].connect(self.textSize)
        self.comboSize.setCurrentIndex(
                self.comboSize.findText(
                        "%s" % (QApplication.font().pointSize())))

    def load(self, f):
        if not QFile.exists(f):
            return False

        fh = QFile(f)
        if not fh.open(QFile.ReadOnly):
            return False

        data = fh.readAll()
        codec = QTextCodec.codecForHtml(data)
        unistr = codec.toUnicode(data)

        if Qt.mightBeRichText(unistr):
            self.textEdit.setHtml(unistr)
        else:
            self.textEdit.setPlainText(unistr)

        self.setCurrentFileName(f)
        return True

    def maybeSave(self):
        if not self.textEdit.document().isModified():
            return True

        if self.fileName.startswith(':/'):
            return True

        ret = QMessageBox.warning(self, "Application",
                "The document has been modified.\n"
                "Do you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

        if ret == QMessageBox.Save:
            return self.fileSave()

        if ret == QMessageBox.Cancel:
            return False

        return True

    def setCurrentFileName(self, fileName=''):
        self.fileName = fileName
        self.textEdit.document().setModified(False)

        if not fileName:
            shownName = 'untitled.txt'
        else:
            shownName = QFileInfo(fileName).fileName()

        self.setWindowTitle(self.tr("%s[*] - %s" % (shownName, "Rich Text")))
        self.setWindowModified(False)

    def fileNew(self):
        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFileName()

    def fileOpen(self):
        fn, _ = QFileDialog.getOpenFileName(self, "Open File...", None,
                "HTML-Files (*.htm *.html);;All Files (*)")

        if fn:
            self.load(fn)

    def fileSave(self):
        if not self.fileName:
            return self.fileSaveAs()

        writer = QTextDocumentWriter(self.fileName)
        success = writer.write(self.textEdit.document())
        if success:
            self.textEdit.document().setModified(False)

        return success

    def fileSaveAs(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Save as...", None,
                "ODF files (*.odt);;HTML-Files (*.htm *.html);;All Files (*)")

        if not fn:
            return False

        lfn = fn.lower()
        if not lfn.endswith(('.odt', '.htm', '.html')):
            # The default.
            fn += '.odt'

        self.setCurrentFileName(fn)
        return self.fileSave()

    def filePrint(self):
        printer = QPrinter(QPrinter.HighResolution)
        dlg = QPrintDialog(printer, self)

        if self.textEdit.textCursor().hasSelection():
            dlg.addEnabledOption(QPrintDialog.PrintSelection)

        dlg.setWindowTitle("Print Document")

        if dlg.exec_() == QPrintDialog.Accepted:
            self.textEdit.print_(printer)

        del dlg

    def filePrintPreview(self):
        printer = QPrinter(QPrinter.HighResolution)
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self.printPreview)
        preview.exec_()

    def printPreview(self, printer):
        self.textEdit.print_(printer)

    def filePrintPdf(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Export PDF", None,
                "PDF files (*.pdf);;All Files (*)")

        if fn:
            if QFileInfo(fn).suffix().isEmpty():
                fn += '.pdf'

            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print_(printer)

    def textBold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(self.actionTextBold.isChecked() and QFont.Bold or QFont.Normal)
        self.mergeFormatOnWordOrSelection(fmt)

    def textUnderline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.actionTextUnderline.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textItalic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.actionTextItalic.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textFamily(self, family):
        fmt = QTextCharFormat()
        fmt.setFontFamily(family)
        self.mergeFormatOnWordOrSelection(fmt)

    def textSize(self, pointSize):
        pointSize = float(pointSize)
        if pointSize > 0:
            fmt = QTextCharFormat()
            fmt.setFontPointSize(pointSize)
            self.mergeFormatOnWordOrSelection(fmt)

    def textStyle(self, styleIndex):
        cursor = self.textEdit.textCursor()
        if styleIndex:
            styleDict = {
                1: QTextListFormat.ListDisc,
                2: QTextListFormat.ListCircle,
                3: QTextListFormat.ListSquare,
                4: QTextListFormat.ListDecimal,
                5: QTextListFormat.ListLowerAlpha,
                6: QTextListFormat.ListUpperAlpha,
                7: QTextListFormat.ListLowerRoman,
                8: QTextListFormat.ListUpperRoman,
            }

            style = styleDict.get(styleIndex, QTextListFormat.ListDisc)
            cursor.beginEditBlock()
            blockFmt = cursor.blockFormat()
            listFmt = QTextListFormat()

            if cursor.currentList():
                listFmt = cursor.currentList().format()
            else:
                listFmt.setIndent(blockFmt.indent() + 1)
                blockFmt.setIndent(0)
                cursor.setBlockFormat(blockFmt)

            listFmt.setStyle(style)
            cursor.createList(listFmt)
            cursor.endEditBlock()
        else:
            bfmt = QTextBlockFormat()
            bfmt.setObjectIndex(-1)
            cursor.mergeBlockFormat(bfmt)

    def textColor(self):
        col = QColorDialog.getColor(self.textEdit.textColor(), self)
        if not col.isValid():
            return

        fmt = QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(col)

    def textAlign(self, action):
        if action == self.actionAlignLeft:
            self.textEdit.setAlignment(Qt.AlignLeft | Qt.AlignAbsolute)
        elif action == self.actionAlignCenter:
            self.textEdit.setAlignment(Qt.AlignHCenter)
        elif action == self.actionAlignRight:
            self.textEdit.setAlignment(Qt.AlignRight | Qt.AlignAbsolute)
        elif action == self.actionAlignJustify:
            self.textEdit.setAlignment(Qt.AlignJustify)

    def currentCharFormatChanged(self, format):
        self.fontChanged(format.font())
        self.colorChanged(format.foreground().color())

    def cursorPositionChanged(self):
        self.alignmentChanged(self.textEdit.alignment())

    def clipboardDataChanged(self):
        self.actionPaste.setEnabled(len(QApplication.clipboard().text()) != 0)

    def about(self):
        QMessageBox.about(self, "About", 
                "This example demonstrates Qt's rich text editing facilities "
                "in action, providing an example document for you to "
                "experiment with.")

    def mergeFormatOnWordOrSelection(self, format):
        cursor = self.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)

        cursor.mergeCharFormat(format)
        self.textEdit.mergeCurrentCharFormat(format)

    def fontChanged(self, font):
        self.comboFont.setCurrentIndex(
                self.comboFont.findText(QFontInfo(font).family()))
        self.comboSize.setCurrentIndex(
                self.comboSize.findText("%s" % font.pointSize()))
        self.actionTextBold.setChecked(font.bold())
        self.actionTextItalic.setChecked(font.italic())
        self.actionTextUnderline.setChecked(font.underline())

    def colorChanged(self, color):
        pix = QPixmap(16, 16)
        pix.fill(color)
        self.actionTextColor.setIcon(QIcon(pix))

    def alignmentChanged(self, alignment):
        if alignment & Qt.AlignLeft:
            self.actionAlignLeft.setChecked(True)
        elif alignment & Qt.AlignHCenter:
            self.actionAlignCenter.setChecked(True)
        elif alignment & Qt.AlignRight:
            self.actionAlignRight.setChecked(True)
        elif alignment & Qt.AlignJustify:
            self.actionAlignJustify.setChecked(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindows = []
    for fn in sys.argv[1:] or [None]:
        textEdit = TextEdit(fn)
        textEdit.resize(700, 800)
        textEdit.show()
        mainWindows.append(textEdit)

    sys.exit(app.exec_())
