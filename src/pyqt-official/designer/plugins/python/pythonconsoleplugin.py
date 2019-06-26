#!/usr/bin/env python

"""
pythonconsoleplugin.py

A Python console custom widget plugin for Qt Designer.

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

from pythonconsolewidget import PythonConsoleWidget


class PythonConsolePlugin(QPyDesignerCustomWidgetPlugin):
    """PythonConsolePlugin(QPyDesignerCustomWidgetPlugin)
    
    Provides a Python custom plugin for Qt Designer by implementing the
    QDesignerCustomWidgetPlugin via a PyQt-specific custom plugin class.
    """

    # The __init__() method is only used to set up the plugin and define its
    # initialized variable.
    def __init__(self, parent=None):
    
        super(PythonConsolePlugin, self).__init__(parent)

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
        return PythonConsoleWidget(parent)

    # This method returns the name of the custom widget class that is provided
    # by this plugin.
    def name(self):
        return "PythonConsoleWidget"

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
        return '<widget class="PythonConsoleWidget" name="consoleWidget">\n' \
               ' <property name="toolTip" >\n' \
               '  <string>Python console</string>\n' \
               ' </property>\n' \
               ' <property name="whatsThis" >\n' \
               '  <string>The Python console widget can be used to explore ' \
               'Qt Designer.</string>\n' \
               ' </property>\n' \
               '</widget>\n'

    # Returns the module containing the custom widget class. It may include
    # a module path.
    def includeFile(self):
        return "pythonconsolewidget"


# Define the image used for the icon.
_logo_16x16_xpm = [
    "16 16 6 1",
    " 	c None",
    ".	c #FFFFFF",
    "a	c #000000",
    "b	c #808080",
    "c	c #C0C0C0",
    "d	c #404040",
    "................",
    "................",
    "................",
    ".aa..aa..aa.....",
    "..aa..aa..aa....",
    "...aa..aa..aa...",
    "....aa..aa..aa..",
    ".....aa..aa..aa.",
    ".....aa..aa..aa.",
    "....aa..aa..aa..",
    "...aa..aa..aa...",
    "..aa..aa..aa....",
    ".aa..aa..aa.....",
    "................",
    "................",
    "................"]

_logo_pixmap = QPixmap(_logo_16x16_xpm)
