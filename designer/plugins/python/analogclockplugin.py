#!/usr/bin/env python

"""
analogclockplugin.py

An analog clock custom widget plugin for Qt Designer.

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

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from analogclock import PyAnalogClock


class PyAnalogClockPlugin(QPyDesignerCustomWidgetPlugin):
    """PyAnalogClockPlugin(QPyDesignerCustomWidgetPlugin)
    
    Provides a Python custom plugin for Qt Designer by implementing the
    QDesignerCustomWidgetPlugin via a PyQt-specific custom plugin class.
    """

    # The __init__() method is only used to set up the plugin and define its
    # initialized variable.
    def __init__(self, parent=None):
    
        super(PyAnalogClockPlugin, self).__init__(parent)

        self.initialized = False

    # The initialize() and isInitialized() methods allow the plugin to set up
    # any required resources, ensuring that this can only happen once for each
    # plugin.
    def initialize(self, core):

        if self.initialized:
            return

        self.initialized = True

    def isInitialized(self):

        return self.initialized

    # This factory method creates new instances of our custom widget with the
    # appropriate parent.
    def createWidget(self, parent):
        return PyAnalogClock(parent)

    # This method returns the name of the custom widget class that is provided
    # by this plugin.
    def name(self):
        return "PyAnalogClock"

    # Returns the name of the group in Qt Designer's widget box that this
    # widget belongs to.
    def group(self):
        return "PyQt Examples"

    # Returns the icon used to represent the custom widget in Qt Designer's
    # widget box.
    def icon(self):
        return QIcon(_logo_pixmap)

    # Returns a short description of the custom widget for use in a tool tip.
    def toolTip(self):
        return ""

    # Returns a short description of the custom widget for use in a "What's
    # This?" help message for the widget.
    def whatsThis(self):
        return ""

    # Returns True if the custom widget acts as a container for other widgets;
    # otherwise returns False. Note that plugins for custom containers also
    # need to provide an implementation of the QDesignerContainerExtension
    # interface if they need to add custom editing support to Qt Designer.
    def isContainer(self):
        return False

    # Returns an XML description of a custom widget instance that describes
    # default values for its properties. Each custom widget created by this
    # plugin will be configured using this description.
    def domXml(self):
        return '<widget class="PyAnalogClock" name="analogClock">\n' \
               ' <property name="toolTip">\n' \
               '  <string>The current time</string>\n' \
               ' </property>\n' \
               ' <property name="whatsThis">\n' \
               '  <string>The analog clock widget displays the current ' \
               'time.</string>\n' \
               ' </property>\n' \
               '</widget>\n'

    # Returns the module containing the custom widget class. It may include
    # a module path.
    def includeFile(self):
        return "analogclock"


# Define the image used for the icon.
_logo_16x16_xpm = [
    "16 16 58 1",
    "L c #2d2d2d",
    "N c #4f4f4f",
    "K c #636363",
    "J c #666666",
    "I c #696969",
    "D c #727272",
    "F c #737373",
    "O c #757575",
    "G c #7f7f7f",
    "o c #878787",
    "t c #888888",
    "Y c #898989",
    "c c #8a8a8a",
    "d c #8b8b8b",
    "H c #8d8d8d",
    "Q c #8f8f8f",
    "b c #909090",
    "M c #959595",
    "g c #979797",
    "n c #989898",
    "x c #999999",
    "0 c #9a9a9a",
    "X c #9b9b9b",
    "a c #9d9d9d",
    "E c #9e9e9e",
    "1 c #9f9f9f",
    "T c #a0a0a0",
    "v c #a1a1a1",
    "r c #a2a2a2",
    "B c #a6a6a6",
    "R c #a7a7a7",
    "3 c #a8a8a8",
    "z c #aaaaaa",
    "A c #ababab",
    "m c #acacac",
    "h c #adadad",
    "u c #b1b1b1",
    "q c #b2b2b2",
    "V c #bfbfbf",
    "W c #c6c6c6",
    "w c #c7c7c7",
    "s c #c8c8c8",
    "p c #c9c9c9",
    "k c #cdcdcd",
    "l c #cfcfcf",
    "2 c #d3d3d3",
    "S c #d4d4d4",
    "C c #d5d5d5",
    "y c #d8d8d8",
    "# c #d9d9d9",
    "e c #dadada",
    "i c #dbdbdb",
    "P c #dcdcdc",
    "U c #dfdfdf",
    "j c #e1e1e1",
    "f c #fbfbfb",
    "Z c #fcfcfc",
    ". c #ffffff",
    "....#abcdbae....",
    "..fghijkljimnf..",
    ".fopjjjqrjjjstf.",
    ".gsjjjjuvjjjjwx.",
    "yvjjjjjzbjjjjjAi",
    "BCjjjjjaDjjjjjiE",
    "bjjjjjjEFjjjjjjG",
    "HjjjjjjIJjjjjjjc",
    "HjjjjjjnKLtjjjjc",
    "bjjjjjjj#MNOPjjQ",
    "RSjjjjjjjj#mdPiE",
    "#TjjjjjjjjjjUjzP",
    ".nVjjjjjjjjjjWX.",
    ".fEVjjjjjjjjWYZ.",
    "..f012jjjj2EXZ..",
    "....i3QccQ3P...."]

_logo_pixmap = QPixmap(_logo_16x16_xpm)
