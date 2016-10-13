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
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import (pyqtSignal, QBuffer, QByteArray, QFileInfo,
        QIODevice, QMimeData, QPoint, QSize, Qt)
from PyQt5.QtGui import (qBlue, QColor, QDrag, qGreen, QImage, QKeySequence,
        QPalette, QPixmap, qRed)
from PyQt5.QtWidgets import (QApplication, QColorDialog, QFileDialog, QFrame,
        QGridLayout, QLabel, QLayout, QMainWindow, QMenu, QMessageBox,
        QPushButton, QVBoxLayout)


class FinalWidget(QFrame):

    def __init__(self, parent, name, labelSize):
        super(FinalWidget, self).__init__(parent)

        self.dragStartPosition = QPoint()

        self.hasImage = False
        self.imageLabel = QLabel()
        self.imageLabel.setFrameShadow(QFrame.Sunken)
        self.imageLabel.setFrameShape(QFrame.StyledPanel)
        self.imageLabel.setMinimumSize(labelSize)
        self.nameLabel = QLabel(name)

        layout = QVBoxLayout()
        layout.addWidget(self.imageLabel, 1)
        layout.addWidget(self.nameLabel, 0)
        self.setLayout(layout)

    def mouseMoveEvent(self, event):
        """ If the mouse moves far enough when the left mouse button is held
            down, start a drag and drop operation.
        """
        if not event.buttons() & Qt.LeftButton:
            return

        if (event.pos() - self.dragStartPosition).manhattanLength() \
             < QApplication.startDragDistance():
            return

        if not self.hasImage:
            return

        drag = QDrag(self)
        mimeData = QMimeData()

        output = QByteArray()
        outputBuffer = QBuffer(output)
        outputBuffer.open(QIODevice.WriteOnly)
        self.imageLabel.pixmap().toImage().save(outputBuffer, 'PNG')
        outputBuffer.close()
        mimeData.setData('image/png', output)

        drag.setMimeData(mimeData)
        drag.setPixmap(self.imageLabel.pixmap().scaled(64, 64, Qt.KeepAspectRatio))
        drag.setHotSpot(QPoint(drag.pixmap().width() / 2,
                                      drag.pixmap().height()))
        drag.start()

    def mousePressEvent(self, event):
        """ Check for left mouse button presses in order to enable drag and
            drop.
        """
        if event.button() == Qt.LeftButton:
            self.dragStartPosition = event.pos()

    def pixmap(self):
        return self.imageLabel.pixmap()

    def setPixmap(self, pixmap):
        self.imageLabel.setPixmap(pixmap)
        self.hasImage = True


class ScreenWidget(QFrame):
    # Separation.
    Cyan, Magenta, Yellow = range(3)

    convertMap = {
        Cyan: qRed,
        Magenta: qGreen,
        Yellow: qBlue,
    }

    imageChanged = pyqtSignal()

    def __init__(self, parent, initialColor, name, mask, labelSize):
        """ Initializes the paint color, the mask color (cyan, magenta, or
        yellow), connects the color selector and invert checkbox to functions,
        and creates a two-by-two grid layout.
        """
        super(ScreenWidget, self).__init__(parent)

        self.originalImage = QImage()
        self.newImage = QImage()

        self.paintColor = initialColor
        self.maskColor = mask
        self.inverted = False

        self.imageLabel = QLabel()
        self.imageLabel.setFrameShadow(QFrame.Sunken)
        self.imageLabel.setFrameShape(QFrame.StyledPanel)
        self.imageLabel.setMinimumSize(labelSize)

        self.nameLabel = QLabel(name)
        self.colorButton = QPushButton("Modify...")
        self.colorButton.setBackgroundRole(QPalette.Button)
        self.colorButton.setMinimumSize(32, 32)

        palette = QPalette(self.colorButton.palette())
        palette.setColor(QPalette.Button, initialColor)
        self.colorButton.setPalette(palette)

        self.invertButton = QPushButton("Invert")
        self.invertButton.setEnabled(False)

        self.colorButton.clicked.connect(self.setColor)
        self.invertButton.clicked.connect(self.invertImage)

        gridLayout = QGridLayout()
        gridLayout.addWidget(self.imageLabel, 0, 0, 1, 2)
        gridLayout.addWidget(self.nameLabel, 1, 0)
        gridLayout.addWidget(self.colorButton, 1, 1)
        gridLayout.addWidget(self.invertButton, 2, 1, 1, 1)
        self.setLayout(gridLayout)

    def createImage(self):
        """ Creates a new image by separating out the cyan, magenta, or yellow
            component, depending on the mask color specified in the constructor.
            The amount of the component found in each pixel of the image is used
            to determine how much of a user-selected ink is used for each pixel
            in the new image for the label widget.
        """
        self.newImage = newImage = self.originalImage.copy()

        # Create CMY components for the ink being used.
        cyanInk = float(255 - QColor(self.paintColor).red()) / 255.0
        magentaInk = float(255 - QColor(self.paintColor).green()) / 255.0
        yellowInk = float(255 - QColor(self.paintColor).blue()) / 255.0

        convert = self.convertMap[self.maskColor]

        for y in range(newImage.height()):
            for x in range(newImage.width()):
                p = self.originalImage.pixel(x, y)

                # Separate the source pixel into its cyan component.
                if self.inverted:
                    amount = convert(p)
                else:
                    amount = 255 - convert(p)

                newColor = QColor(
                    255 - min(int(amount * cyanInk), 255),
                    255 - min(int(amount * magentaInk), 255),
                    255 - min(int(amount * yellowInk), 255))

                newImage.setPixel(x, y, newColor.rgb())

        self.imageLabel.setPixmap(QPixmap.fromImage(newImage))

    def image(self):
        """ Returns a reference to the modified image. """
        return self.newImage

    def invertImage(self):
        """ Sets whether the amount of ink applied to the canvas is to be
            inverted (subtracted from the maximum value) before the ink is
            applied.
        """
        self.inverted = not self.inverted
        self.createImage()
        self.imageChanged.emit()

    def setColor(self):
        """ Separate the current image into cyan, magenta, and yellow
            components.  Create a representation of how each component might
            appear when applied to a blank white piece of paper.
        """
        newColor = QColorDialog.getColor(self.paintColor)

        if newColor.isValid():
            self.paintColor = newColor
            palette = QPalette(self.colorButton.palette())
            palette.setColor(QPalette.Button, self.paintColor)
            self.colorButton.setPalette(palette)
            self.createImage()
            self.imageChanged.emit()

    def setImage(self, image):
        """ Records the original image selected by the user, creates a color
            separation, and enables the invert image checkbox.
        """
        self.originalImage = image
        self.createImage()
        self.invertButton.setEnabled(True)


class Viewer(QMainWindow):
    # Brightness.
    Gloom, Quarter, Half, ThreeQuarters, Full = range(5)

    # Brightness value map.
    brightnessValueMap = {
        Gloom: 0,
        Quarter: 64,
        Half: 128,
        ThreeQuarters: 191,
        Full: 255,
    }

    def __init__(self):
        """ Constructor initializes a default value for the brightness, creates
            the main menu entries, and constructs a central widget that contains
            enough space for images to be displayed.
        """
        super(Viewer, self).__init__()

        self.scaledImage = QImage()
        self.menuMap = {}
        self.path = ''
        self.brightness = 255

        self.setWindowTitle("QImage Color Separations")

        self.createMenus()
        self.setCentralWidget(self.createCentralWidget())

    def createMenus(self):
        """ Creates a main menu with two entries: a File menu, to allow the image
            to be selected, and a Brightness menu to allow the brightness of the
            separations to be changed.
            Initially, the Brightness menu items are disabled, but the first entry in
            the menu is checked to reflect the default brightness.
        """
        self.fileMenu = QMenu("&File", self)
        self.brightnessMenu = QMenu("&Brightness", self)

        self.openAction = self.fileMenu.addAction("&Open...")
        self.openAction.setShortcut(QKeySequence('Ctrl+O'))
        self.saveAction = self.fileMenu.addAction("&Save...")
        self.saveAction.setShortcut(QKeySequence('Ctrl+S'))
        self.saveAction.setEnabled(False)
        self.quitAction = self.fileMenu.addAction("E&xit")
        self.quitAction.setShortcut(QKeySequence('Ctrl+Q'))

        self.noBrightness = self.brightnessMenu.addAction("&0%")
        self.noBrightness.setCheckable(True)
        self.quarterBrightness = self.brightnessMenu.addAction("&25%")
        self.quarterBrightness.setCheckable(True)
        self.halfBrightness = self.brightnessMenu.addAction("&50%")
        self.halfBrightness.setCheckable(True)
        self.threeQuartersBrightness = self.brightnessMenu.addAction("&75%")
        self.threeQuartersBrightness.setCheckable(True)
        self.fullBrightness = self.brightnessMenu.addAction("&100%")
        self.fullBrightness.setCheckable(True)

        self.menuMap[self.noBrightness] = self.Gloom
        self.menuMap[self.quarterBrightness] = self.Quarter
        self.menuMap[self.halfBrightness] = self.Half
        self.menuMap[self.threeQuartersBrightness] = self.ThreeQuarters
        self.menuMap[self.fullBrightness] = self.Full

        self.currentBrightness = self.fullBrightness
        self.currentBrightness.setChecked(True)
        self.brightnessMenu.setEnabled(False)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.brightnessMenu)

        self.openAction.triggered.connect(self.chooseFile)
        self.saveAction.triggered.connect(self.saveImage)
        self.quitAction.triggered.connect(QApplication.instance().quit)
        self.brightnessMenu.triggered.connect(self.setBrightness)

    def createCentralWidget(self):
        """ Constructs a central widget for the window consisting of a two-by-two
            grid of labels, each of which will contain an image. We restrict the
            size of the labels to 256 pixels, and ensure that the window cannot
            be resized.
        """
        frame = QFrame(self)
        grid = QGridLayout(frame)
        grid.setSpacing(8)
        grid.setContentsMargins(4, 4, 4, 4)

        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        labelSize = QSize(256, 256)

        self.finalWidget = FinalWidget(frame, "Final image", labelSize)

        self.cyanWidget = ScreenWidget(frame, Qt.cyan, "Cyan",
                ScreenWidget.Cyan, labelSize)
        self.magentaWidget = ScreenWidget(frame, Qt.magenta, "Magenta",
                ScreenWidget.Magenta, labelSize)
        self.yellowWidget = ScreenWidget(frame, Qt.yellow, "Yellow",
                ScreenWidget.Yellow, labelSize)

        self.cyanWidget.imageChanged.connect(self.createImage)
        self.magentaWidget.imageChanged.connect(self.createImage)
        self.yellowWidget.imageChanged.connect(self.createImage)

        grid.addWidget(self.finalWidget, 0, 0, Qt.AlignTop | Qt.AlignHCenter)
        grid.addWidget(self.cyanWidget, 0, 1, Qt.AlignTop | Qt.AlignHCenter)
        grid.addWidget(self.magentaWidget, 1, 0, Qt.AlignTop | Qt.AlignHCenter)
        grid.addWidget(self.yellowWidget, 1, 1, Qt.AlignTop | Qt.AlignHCenter)

        return frame

    def chooseFile(self):
        """ Provides a dialog window to allow the user to specify an image file.
            If a file is selected, the appropriate function is called to process
            and display it.
        """
        imageFile, _ = QFileDialog.getOpenFileName(self,
                "Choose an image file to open", self.path, "Images (*.*)")

        if imageFile != '':
            self.openImageFile(imageFile)
            self.path = imageFile

    def setBrightness(self, action):
        """ Changes the value of the brightness according to the entry selected in the
            Brightness menu. The selected entry is checked, and the previously selected
            entry is unchecked.
            The color separations are updated to use the new value for the brightness.
        """
        if action not in self.menuMap or self.scaledImage.isNull():
            return

        self.brightness = self.brightnessValueMap.get(self.menuMap[action])
        if self.brightness is None:
            return

        self.currentBrightness.setChecked(False)
        self.currentBrightness = action
        self.currentBrightness.setChecked(True)

        self.createImage()

    def openImageFile(self, imageFile):
        """ Load the image from the file given, and create four pixmaps based
            on the original image.
            The window caption is set, and the Brightness menu enabled if the image file
            can be loaded.
        """
        originalImage = QImage()

        if originalImage.load(imageFile):
            self.setWindowTitle(imageFile)
            self.saveAction.setEnabled(True)
            self.brightnessMenu.setEnabled(True)

            self.scaledImage = originalImage.scaled(256, 256, Qt.KeepAspectRatio)

            self.cyanWidget.setImage(self.scaledImage)
            self.magentaWidget.setImage(self.scaledImage)
            self.yellowWidget.setImage(self.scaledImage)
            self.createImage()
        else:
            QMessageBox.warning(self, "Cannot open file",
                    "The selected file could not be opened.",
                    QMessageBox.Cancel, QMessageBox.NoButton,
                    QMessageBox.NoButton)

    def createImage(self):
        """ Creates an image by combining the contents of the three screens
            to present a page preview.
            The image associated with each screen is separated into cyan,
            magenta, and yellow components. We add up the values for each
            component from the three screen images, and subtract the totals
            from the maximum value for each corresponding primary color.
        """
        newImage = self.scaledImage.copy()

        image1 = self.cyanWidget.image()
        image2 = self.magentaWidget.image()
        image3 = self.yellowWidget.image()
        darkness = 255 - self.brightness

        for y in range(newImage.height()):
            for x in range(newImage.width()):
                # Create three screens, using the quantities of the source CMY
                # components to determine how much of each of the inks are to
                # be put on each screen.
                p1 = image1.pixel(x, y)
                cyan1 = float(255 - qRed(p1))
                magenta1 = float(255 - qGreen(p1))
                yellow1 = float(255 - qBlue(p1))

                p2 = image2.pixel(x, y)
                cyan2 = float(255 - qRed(p2))
                magenta2 = float(255 - qGreen(p2))
                yellow2 = float(255 - qBlue(p2))

                p3 = image3.pixel(x, y)
                cyan3 = float(255 - qRed(p3))
                magenta3 = float(255 - qGreen(p3))
                yellow3 = float(255 - qBlue(p3))

                newColor = QColor(
                    max(255 - int(cyan1 + cyan2 + cyan3) - darkness, 0),
                    max(255 - int(magenta1 + magenta2 + magenta3) - darkness, 0),
                    max(255 - int(yellow1 + yellow2 + yellow3) - darkness, 0))

                newImage.setPixel(x, y, newColor.rgb())

        self.finalWidget.setPixmap(QPixmap.fromImage(newImage))

    def saveImage(self):
        """ Provides a dialog window to allow the user to save the image file.
        """
        imageFile, _ = QFileDialog.getSaveFileName(self,
                "Choose a filename to save the image", "", "Images (*.png)")

        info = QFileInfo(imageFile)

        if info.baseName() != '':
            newImageFile = QFileInfo(info.absoluteDir(),
                    info.baseName() + '.png').absoluteFilePath()

            if not self.finalWidget.pixmap().save(newImageFile, 'PNG'):
                QMessageBox.warning(self, "Cannot save file",
                        "The file could not be saved.",
                        QMessageBox.Cancel, QMessageBox.NoButton,
                        QMessageBox.NoButton)
        else:
            QMessageBox.warning(self, "Cannot save file",
                    "Please enter a valid filename.", QMessageBox.Cancel,
                    QMessageBox.NoButton, QMessageBox.NoButton)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Viewer()
    window.show()
    sys.exit(app.exec_())
