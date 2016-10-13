#!/usr/bin/env python

#============================================================================#
# PyQt5 port of the designer/containerextension example from Qt v5.x         #
#----------------------------------------------------------------------------#
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import (QApplication, QComboBox, QLabel, QStackedWidget,
        QVBoxLayout, QWidget)


#============================================================================#
# Implementation of a MultiPageWidget using a QComboBox and a QStackedWidget #
#----------------------------------------------------------------------------#
class PyMultiPageWidget(QWidget):

    currentIndexChanged = pyqtSignal(int)

    pageTitleChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(PyMultiPageWidget, self).__init__(parent)

        self.comboBox = QComboBox()
        # MAGIC
        # It is important that the combo box has an object name beginning
        # with '__qt__passive_', otherwise, it is inactive in the form editor
        # of the designer and you can't change the current page via the
        # combo box.
        # MAGIC
        self.comboBox.setObjectName('__qt__passive_comboBox')        
        self.stackWidget = QStackedWidget()
        self.comboBox.activated.connect(self.setCurrentIndex)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.stackWidget)
        self.setLayout(self.layout)

    def sizeHint(self):
        return QSize(200, 150)

    def count(self):
        return self.stackWidget.count()

    def widget(self, index):
        return self.stackWidget.widget(index)

    @pyqtSlot(QWidget)
    def addPage(self, page):
        self.insertPage(self.count(), page)

    @pyqtSlot(int, QWidget)
    def insertPage(self, index, page):
        page.setParent(self.stackWidget)
        self.stackWidget.insertWidget(index, page)
        title = page.windowTitle()
        if title == "":
            title = "Page %d" % (self.comboBox.count() + 1)
            page.setWindowTitle(title)
        self.comboBox.insertItem(index, title)

    @pyqtSlot(int)
    def removePage(self, index):
        widget = self.stackWidget.widget(index)
        self.stackWidget.removeWidget(widget)
        self.comboBox.removeItem(index)

    def getPageTitle(self):
        cw = self.stackWidget.currentWidget()
        return cw.windowTitle() if cw is not None else ''
    
    @pyqtSlot(str)
    def setPageTitle(self, newTitle):
        cw = self.stackWidget.currentWidget()
        if cw is not None:
            self.comboBox.setItemText(self.getCurrentIndex(), newTitle)
            cw.setWindowTitle(newTitle)
            self.pageTitleChanged.emit(newTitle)

    def getCurrentIndex(self):
        return self.stackWidget.currentIndex()

    @pyqtSlot(int)
    def setCurrentIndex(self, index):
        if index != self.getCurrentIndex():
            self.stackWidget.setCurrentIndex(index)
            self.comboBox.setCurrentIndex(index)
            self.currentIndexChanged.emit(index)

    pageTitle = pyqtProperty(str, fget=getPageTitle, fset=setPageTitle, stored=False)
    currentIndex = pyqtProperty(int, fget=getCurrentIndex, fset=setCurrentIndex)


#============================================================================#
# Main for testing the class                                                 #
#----------------------------------------------------------------------------#
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = PyMultiPageWidget()
    widget.addPage(QLabel('This is page #1'))
    widget.addPage(QLabel('This is page #2'))
    widget.show()
    sys.exit(app.exec_())

#============================================================================#
# EOF                                                                        #
#----------------------------------------------------------------------------#
