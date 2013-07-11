#!/usr/bin/env python3

from gi.repository import Gtk
import sys

color_sel = Gtk.ColorSelectionDialog("Sublime Color Picker")

if len(sys.argv) > 1:
    if Gtk.gdk.Color(sys.argv[1]):
        color_sel.colorsel.set_current_color(Gtk.gdk.Color(sys.argv[1]))

if color_sel.run() == Gtk.ResponseType.OK:
    color = color_sel.get_color_selection().get_current_color()
    #Convert to 8bit channels
    red = color.red / 256
    green = color.green / 256
    blue = color.blue / 256
    #Convert to hexa strings
    red = str(hex(int(red)))[2:]
    green = str(hex(int(green)))[2:]
    blue = str(hex(int(blue)))[2:]
    #Format
    if len(red) == 1:
        red = "0%s" % red
    if len(green) == 1:
        green = "0%s" % green
    if len(blue) == 1:
        blue = "0%s" % blue
    
    finalcolor = red+green+blue
    print(finalcolor.upper())

color_sel.destroy()
