#!/usr/bin/env python

"""
polygonwidgetplugin.py

A polygon widget custom widget plugin for Qt Designer.

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

from polygonwidget import PolygonWidget


class PolygonWidgetPlugin(QPyDesignerCustomWidgetPlugin):
    """PolygonWidgetPlugin(QPyDesignerCustomWidgetPlugin)
    
    Provides a Python custom plugin for Qt Designer by implementing the
    QDesignerCustomWidgetPlugin via a PyQt-specific custom plugin class.
    """

    # The __init__() method is only used to set up the plugin and define its
    # initialized variable.
    def __init__(self, parent=None):
    
        super(PolygonWidgetPlugin, self).__init__(parent)

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
        return PolygonWidget(parent)

    # This method returns the name of the custom widget class that is provided
    # by this plugin.
    def name(self):
        return "PolygonWidget"

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
        return '<widget class="PolygonWidget" name="polygonWidget" />\n'

    # Returns the module containing the custom widget class. It may include
    # a module path.
    def includeFile(self):
        return "polygonwidget"


# Define the image used for the icon.
_logo_16x16_xpm = [
"16 16 46 1",
". c #a5a5dc",
"l c #a69fd6",
"k c #a7a5da",
"h c #a7a6dc",
"a c #a7a7de",
"Q c #a8a5da",
"s c #a9a7d7",
"R c #a9a9e0",
"z c #abaad4",
"E c #afafda",
"M c #afafdb",
"K c #b0a8e2",
"o c #b1afe4",
"p c #b2b2d7",
"# c #b2b2ed",
"i c #b39eb6",
"F c #b3b3e1",
"e c #b4b4ef",
"t c #b58bab",
"d c #b6b6f2",
"n c #b798b8",
"P c #b798b9",
"c c #b8b6f2",
"D c #b8b89c",
"m c #b9648d",
"J c #ba84b0",
"A c #bdbdfb",
"f c #bfbffe",
"g c #c06996",
"b c #c0c0ff",
"B c #cbb889",
"L c #cbb989",
"O c #cfcf87",
"I c #d09585",
"w c #d0cf86",
"x c #dede81",
"G c #e8e87c",
"q c #edde7b",
"N c #f1e07b",
"v c #f2e07b",
"H c #f6e57c",
"j c #fb917e",
"u c #ffb580",
"r c #ffda80",
"C c #fffe80",
"y c #ffff80",
".##############a",
"#bbbbbbbbcdbbbbe",
"#bbbbbbbfghbbbbe",
"#bbbbbbbijkbbbbe",
"#blmnobpqrsbbbbe",
"#bbtuvwxyyzbbbbe",
"#bbABCyyyyDEfbbe",
"#bbbFGyyyyyHIJKe",
"#bbbFGyyyyyHIJKe",
"#bbALCyyyyDMfbbe",
"#bbtuNOxyyzbbbbe",
"#blmPobpqrsbbbbe",
"#bbbbbbbijQbbbbe",
"#bbbbbbbfghbbbbe",
"#bbbbbbbbcdbbbbe",
"aeeeeeeeeeeeeeeR"]

_logo_pixmap = QPixmap(_logo_16x16_xpm)
