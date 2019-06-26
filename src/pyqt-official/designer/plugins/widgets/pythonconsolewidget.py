#!/usr/bin/env python

"""
pythonconsolewidget.py

A Python console custom widget for Qt Designer.

Copyright (C) 2006 David Boddie <david@boddie.org.uk>
Copyright (C) 2005-2006 Trolltech ASA. All rights reserved.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

from PyQt5.QtCore import pyqtSignal, QEvent, Qt
from PyQt5.QtWidgets import QApplication, QLineEdit


class PythonConsoleWidget(QLineEdit):
    """PythonConsoleWidget(QLineEdit)
    
    Provides a custom widget to accept Python expressions and emit output
    to other components via a custom signal.
    """
    
    pythonOutput = pyqtSignal(str)
    
    def __init__(self, parent=None):
    
        super(PythonConsoleWidget, self).__init__(parent)
        
        self.history = []
        self.current = -1
        
        self.returnPressed.connect(self.execute)
    
    def keyReleaseEvent(self, event):
    
        if event.type() == QEvent.KeyRelease:
        
            if event.key() == Qt.Key_Up:
                current = max(0, self.current - 1)
                if 0 <= current < len(self.history):
                    self.setText(self.history[current])
                    self.current = current
                
                event.accept()
            
            elif event.key() == Qt.Key_Down:
                current = min(len(self.history), self.current + 1)
                if 0 <= current < len(self.history):
                    self.setText(self.history[current])
                else:
                    self.clear()
                self.current = current
                
                event.accept()
    
    def execute(self):
    
        # Define this here to give users something to look at.
        qApp = QApplication.instance()
        
        self.expression = self.text()
        try:
            result = str(eval(str(self.expression)))
            
            # Emit the result of the evaluated expression.
            self.pythonOutput.emit(result)

            # Clear the line edit, append the successful expression to the
            # history, and update the current command index.
            self.clear()
            self.history.append(self.expression)
            self.current = len(self.history)
        except:
            pass


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    widget = PythonConsoleWidget()
    widget.show()
    sys.exit(app.exec_())
