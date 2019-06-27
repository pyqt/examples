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


from PyQt5.QtCore import QBuffer, QDataStream, QSharedMemory
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog

from dialog import Ui_Dialog


class Dialog(QDialog):
    """ This class is a simple example of how to use QSharedMemory.  It is a
    simple dialog that presents a few buttons.  Run the executable twice to
    create two processes running the dialog.  In one of the processes, press
    the button to load an image into a shared memory segment, and then select
    an image file to load.  Once the first process has loaded and displayed the
    image, in the second process, press the button to read the same image from
    shared memory.  The second process displays the same image loaded from its
    new location in shared memory.

    The class contains a data member sharedMemory, which is initialized with
    the key "QSharedMemoryExample" to force all instances of Dialog to access
    the same shared memory segment.  The constructor also connects the
    clicked() signal from each of the three dialog buttons to the slot function
    appropriate for handling each button.
    """

    def __init__(self, parent = None):
        super(Dialog, self).__init__(parent)

        self.sharedMemory = QSharedMemory('QSharedMemoryExample')

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.loadFromFileButton.clicked.connect(self.loadFromFile)
        self.ui.loadFromSharedMemoryButton.clicked.connect(self.loadFromMemory)

        self.setWindowTitle("SharedMemory Example")

    def loadFromFile(self):
        """ This slot function is called when the "Load Image From File..."
        button is pressed on the firs Dialog process.  First, it tests whether
        the process is already connected to a shared memory segment and, if so,
        detaches from that segment.  This ensures that we always start the
        example from the beginning if we run it multiple times with the same
        two Dialog processes.  After detaching from an existing shared memory
        segment, the user is prompted to select an image file.  The selected
        file is loaded into a QImage.  The QImage is displayed in the Dialog
        and streamed into a QBuffer with a QDataStream.  Next, it gets a new
        shared memory segment from the system big enough to hold the image data
        in the QBuffer, and it locks the segment to prevent the second Dialog
        process from accessing it.  Then it copies the image from the QBuffer
        into the shared memory segment.  Finally, it unlocks the shared memory
        segment so the second Dialog process can access it.  After self
        function runs, the user is expected to press the "Load Image from
        Shared Memory" button on the second Dialog process.
        """

        if self.sharedMemory.isAttached():
            self.detach()

        self.ui.label.setText("Select an image file")
        fileName, _ = QFileDialog.getOpenFileName(self, None, None,
                "Images (*.png *.xpm *.jpg)")
        image = QImage()
        if not image.load(fileName):
            self.ui.label.setText(
                    "Selected file is not an image, please select another.")
            return

        self.ui.label.setPixmap(QPixmap.fromImage(image))

        # Load into shared memory.
        buf = QBuffer()
        buf.open(QBuffer.ReadWrite)
        out = QDataStream(buf)
        out << image
        size = buf.size()

        if not self.sharedMemory.create(size):
            self.ui.label.setText("Unable to create shared memory segment.")
            return

        size = min(self.sharedMemory.size(), size)
        self.sharedMemory.lock()

        # Copy image data from buf into shared memory area.
        self.sharedMemory.data()[:size] = buf.data()[:size]
        self.sharedMemory.unlock()

    def loadFromMemory(self):
        """ This slot function is called in the second Dialog process, when the
        user presses the "Load Image from Shared Memory" button.  First, it
        attaches the process to the shared memory segment created by the first
        Dialog process.  Then it locks the segment for exclusive access, copies
        the image data from the segment into a QBuffer, and streams the QBuffer
        into a QImage.  Then it unlocks the shared memory segment, detaches
        from it, and finally displays the QImage in the Dialog.
        """

        if not self.sharedMemory.attach():
            self.ui.label.setText(
                    "Unable to attach to shared memory segment.\nLoad an "
                    "image first.")
            return
 
        buf = QBuffer()
        ins = QDataStream(buf)
        image = QImage()

        self.sharedMemory.lock()
        buf.setData(self.sharedMemory.constData())
        buf.open(QBuffer.ReadOnly)
        ins >> image
        self.sharedMemory.unlock()
        self.sharedMemory.detach()

        self.ui.label.setPixmap(QPixmap.fromImage(image))

    def detach(self):
        """ This private function is called by the destructor to detach the
        process from its shared memory segment.  When the last process detaches
        from a shared memory segment, the system releases the shared memory.
        """

        if not self.sharedMemory.detach():
            self.ui.label.setText("Unable to detach from shared memory.")


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())
