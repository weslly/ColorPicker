#!/usr/bin/env python

import sys

try:
    from gi.repository import Gtk
except ImportError:
    import gtk as Gtk

try:
    Gdk = Gtk.gdk
except AttributeError:
    from gi.repository import Gdk

color_sel = Gtk.ColorSelectionDialog("Sublime Color Picker")

if len(sys.argv) > 1:
    current_color = Gdk.color_parse(sys.argv[1])
    if current_color:
        try:
            color_sel.colorsel.set_current_color(current_color)
        except AttributeError:  # newer version of GTK
            color_sel.get_color_selection().set_current_color(current_color)


if color_sel.run() == getattr(Gtk, 'RESPONSE_OK', Gtk.ResponseType.OK):
    color = color_sel.get_color_selection().get_current_color()
    #Convert to 8bit channels
    red = int(color.red / 256)
    green = int(color.green / 256)
    blue = int(color.blue / 256)
    #Format
    finalcolor = "%02x%02x%02x" % (red, green, blue)
    print (finalcolor.upper())

color_sel.destroy()
