#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import sys

color_sel = gtk.ColorSelectionDialog("Sublime Color Picker")

if len(sys.argv) > 1:
    if gtk.gdk.Color(sys.argv[1]):
        color_sel.colorsel.set_current_color(gtk.gdk.Color(sys.argv[1]))

if color_sel.run() == gtk.RESPONSE_OK:
    color = color_sel.colorsel.get_current_color()
    #Convert to 8bit channels
    red = color.red / 256
    green = color.green / 256
    blue = color.blue / 256
    #Convert to hexa strings
    red = str(hex(red))[2:]
    green = str(hex(green))[2:]
    blue = str(hex(blue))[2:]
    #Format
    if len(red) == 1:
        red = "0%s" % red
    if len(green) == 1:
        green = "0%s" % green
    if len(blue) == 1:
        blue = "0%s" % blue
    
    finalcolor = red+green+blue
    print finalcolor.upper()

color_sel.destroy()
