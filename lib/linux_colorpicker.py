#!/usr/bin/env python

from gi.repository import Gtk
import sys

color_sel = Gtk.ColorSelectionDialog("Sublime Color Picker")

if len(sys.argv) > 1:
    if Gtk.gdk.Color(sys.argv[1]):
        color_sel.colorsel.set_current_color(Gtk.gdk.Color(sys.argv[1]))

if color_sel.run() == Gtk.ResponseType.OK:
    color = color_sel.get_color_selection().get_current_color()
    #Convert to 8bit channels
    red = int(color.red / 256)
    green = int(color.green / 256)
    blue = int(color.blue / 256)
    #Format
    finalcolor = "%02x%02x%02x" % (red, green, blue)
    print (finalcolor.upper())

color_sel.destroy()
