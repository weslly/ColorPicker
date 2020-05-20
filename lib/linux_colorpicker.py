#!/usr/bin/env python

import sys

wx = None
Gtk = None

try:
    from gi.repository import Gtk
except ImportError:
    try:
        import gtk as Gtk
        try:
            Gdk = Gtk.gdk
        except AttributeError:
            from gi.repository import Gdk
    except ImportError:
        try:
            import wx
        except ImportError:
            raise Exception("Neither GTK nor WxWidgets are installed.")

def open_color_picker_via_gtk():
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
        print(finalcolor.upper())

    color_sel.destroy()

#Based on https://gist.github.com/anonymous/ef7871571cd3fdf1a51d603a39aaead1
def open_color_picker_via_wxwidgets():
    def color_parse(hex_string):
        hex_vals = hex_string.lstrip('#')
        #https://stackoverflow.com/a/29643643
        return tuple(int(hex_vals[i:i + 2], 16) for i in (0, 2, 4))

    class MyPanel(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, wx.ID_ANY)
            data = wx.ColourData()
            data.SetColour(color_parse(sys.argv[1]))
            dlg = wx.ColourDialog(self, data)
            dlg.GetColourData().SetChooseFull(True)
            if dlg.ShowModal() == wx.ID_OK:
                data = dlg.GetColourData()
                rgb = data.GetColour().Get()
                finalcolor = "%02x%02x%02x" % rgb
                print(finalcolor.upper())
            frame.Close()

    app = wx.App(0)
    frame = wx.Frame(None, wx.ID_ANY, '', size=(450, 200))
    MyPanel(frame)


if Gtk:
    open_color_picker_via_gtk()
elif wx:
    open_color_picker_via_wxwidgets()
