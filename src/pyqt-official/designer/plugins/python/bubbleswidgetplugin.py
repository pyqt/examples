#!/usr/bin/env python

"""
bubbleswidgetplugin.py

A bubbles widget custom widget plugin for Qt Designer.

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

from bubbleswidget import BubblesWidget


class BubblesPlugin(QPyDesignerCustomWidgetPlugin):
    """BubblesPlugin(QPyDesignerCustomWidgetPlugin)
    
    Provides a Python custom plugin for Qt Designer by implementing the
    QDesignerCustomWidgetPlugin via a PyQt-specific custom plugin class.
    """
    
    # The __init__() method is only used to set up the plugin and define its
    # initialized variable.
    def __init__(self, parent=None):
    
        super(BubblesPlugin, self).__init__(parent)

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

        return BubblesWidget(parent)

    # This method returns the name of the custom widget class that is provided
    # by this plugin.
    def name(self):

        return "BubblesWidget"

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

        return '<widget class="BubblesWidget" name="bubblesWidget">\n' \
               ' <property name="toolTip">\n' \
               '  <string>Click and drag here</string>\n' \
               ' </property>\n' \
               ' <property name="whatsThis">\n' \
               '  <string>The bubbles widget displays colorful ' \
               'bubbles.</string>\n' \
               ' </property>\n' \
               '</widget>\n'

    # Returns the module containing the custom widget class. It may include
    # a module path.
    def includeFile(self):

        return "bubbleswidget"


# Define the image used for the icon.
_logo_16x16_xpm = [
"16 16 48 1",
"O c #d0cfcf",
"d c #d0d0d0",
"i c #d3d3d2",
"q c #d3d3d3",
"M c #dad7d7",
"g c #dad8d7",
"e c #dcd9d9",
"f c #e0dcdc",
"c c #e0e0e0",
"L c #e1dddb",
"D c #e1dddc",
"E c #e1e0e0",
"R c #e1e1e1",
"Q c #e2dedc",
"p c #e2dedd",
"j c #e3dfdf",
"b c #e7e7e7",
"S c #ebe4e3",
"z c #ebe5e3",
"r c #ece6e8",
"a c #eeeeee",
"N c #f6edeb",
"I c #f6eeed",
"o c #f6eeee",
"h c #f7f7f7",
"K c #f8efee",
"C c #f8efef",
"T c #f8f8f8",
"y c #f9f1f0",
"H c #f9f1f1",
"n c #f9f1f2",
"m c #f9f1f3",
"k c #f9f2f4",
"x c #faf3f5",
"l c #faf3f6",
"w c #faf3f7",
"G c #faf3f8",
"v c #fbf5fa",
"s c #fbf5fb",
"u c #fbf5fc",
"t c #fbf5fd",
"# c #fbfbfb",
"J c #fcf6fe",
"B c #fcf7fe",
"P c #fcfcfc",
"F c #fdf8ff",
"A c #fefbff",
". c #ffffff",
".....#abba#.....",
"...#cdeffgdc#...",
"..hijkllmnopqh..",
".#irstuvwxnyzq#.",
".cjs.ABuvwknCDE.",
"#dktAAFtsGlmHId#",
"aeluBFJusGlmHKga",
"bflvutusvGlmHKLb",
"bfmwvssvGwxmHKLb",
"agnxwGGGwlmnyKMa",
"#donklllxmnHCNOP",
".cpynmmmmnHCKQR.",
".#qzCHHHHyCKSqP.",
"..hqDIKKKKNQqT..",
"...#EdgLLMORP...",
".....#abbaP....."]

_logo_pixmap = QPixmap(_logo_16x16_xpm)
