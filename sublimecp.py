import sublime
import sublime_plugin
import subprocess
import os
from stat import *
import threading
import re

sublime_version = 2

if not sublime.version() or int(sublime.version()) > 3000:
    sublime_version = 3


class ColorPickCommand(sublime_plugin.TextCommand):
    # SVG Colors spec: http://www.w3.org/TR/css3-color/#svg-color
    SVGColors = {
        "aliceblue": "F0F8FF",
        "antiquewhite": "FAEBD7",
        "aqua": "00FFFF",
        "aquamarine": "7FFFD4",
        "azure": "F0FFFF",
        "beige": "F5F5DC",
        "bisque": "FFE4C4",
        "black": "000000",
        "blanchedalmond": "FFEBCD",
        "blue": "0000FF",
        "blueviolet": "8A2BE2",
        "brown": "A52A2A",
        "burlywood": "DEB887",
        "cadetblue": "5F9EA0",
        "chartreuse": "7FFF00",
        "chocolate": "D2691E",
        "coral": "FF7F50",
        "cornflowerblue": "6495ED",
        "cornsilk": "FFF8DC",
        "crimson": "DC143C",
        "cyan": "00FFFF",
        "darkblue": "00008B",
        "darkcyan": "008B8B",
        "darkgoldenrod": "B8860B",
        "darkgray": "A9A9A9",
        "darkgreen": "006400",
        "darkgrey": "A9A9A9",
        "darkkhaki": "BDB76B",
        "darkmagenta": "8B008B",
        "darkolivegreen": "556B2F",
        "darkorange": "FF8C00",
        "darkorchid": "9932CC",
        "darkred": "8B0000",
        "darksalmon": "E9967A",
        "darkseagreen": "8FBC8F",
        "darkslateblue": "483D8B",
        "darkslategray": "2F4F4F",
        "darkslategrey": "2F4F4F",
        "darkturquoise": "00CED1",
        "darkviolet": "9400D3",
        "deeppink": "FF1493",
        "deepskyblue": "00BFFF",
        "dimgray": "696969",
        "dimgrey": "696969",
        "dodgerblue": "1E90FF",
        "firebrick": "B22222",
        "floralwhite": "FFFAF0",
        "forestgreen": "228B22",
        "fuchsia": "FF00FF",
        "gainsboro": "DCDCDC",
        "ghostwhite": "F8F8FF",
        "gold": "FFD700",
        "goldenrod": "DAA520",
        "gray": "808080",
        "green": "008000",
        "greenyellow": "ADFF2F",
        "grey": "808080",
        "honeydew": "F0FFF0",
        "hotpink": "FF69B4",
        "indianred": "CD5C5C",
        "indigo": "4B0082",
        "ivory": "FFFFF0",
        "khaki": "F0E68C",
        "lavender": "E6E6FA",
        "lavenderblush": "FFF0F5",
        "lawngreen": "7CFC00",
        "lemonchiffon": "FFFACD",
        "lightblue": "ADD8E6",
        "lightcoral": "F08080",
        "lightcyan": "E0FFFF",
        "lightgoldenrodyellow": "FAFAD2",
        "lightgray": "D3D3D3",
        "lightgreen": "90EE90",
        "lightgrey": "D3D3D3",
        "lightpink": "FFB6C1",
        "lightsalmon": "FFA07A",
        "lightseagreen": "20B2AA",
        "lightskyblue": "87CEFA",
        "lightslategray": "778899",
        "lightslategrey": "778899",
        "lightsteelblue": "B0C4DE",
        "lightyellow": "FFFFE0",
        "lime": "00FF00",
        "limegreen": "32CD32",
        "linen": "FAF0E6",
        "magenta": "FF00FF",
        "maroon": "800000",
        "mediumaquamarine": "66CDAA",
        "mediumblue": "0000CD",
        "mediumorchid": "BA55D3",
        "mediumpurple": "9370DB",
        "mediumseagreen": "3CB371",
        "mediumslateblue": "7B68EE",
        "mediumspringgreen": "00FA9A",
        "mediumturquoise": "48D1CC",
        "mediumvioletred": "C71585",
        "midnightblue": "191970",
        "mintcream": "F5FFFA",
        "mistyrose": "FFE4E1",
        "moccasin": "FFE4B5",
        "navajowhite": "FFDEAD",
        "navy": "000080",
        "oldlace": "FDF5E6",
        "olive": "808000",
        "olivedrab": "6B8E23",
        "orange": "FFA500",
        "orangered": "FF4500",
        "orchid": "DA70D6",
        "palegoldenrod": "EEE8AA",
        "palegreen": "98FB98",
        "paleturquoise": "AFEEEE",
        "palevioletred": "DB7093",
        "papayawhip": "FFEFD5",
        "peachpuff": "FFDAB9",
        "peru": "CD853F",
        "pink": "FFC0CB",
        "plum": "DDA0DD",
        "powderblue": "B0E0E6",
        "purple": "800080",
        "red": "FF0000",
        "rosybrown": "BC8F8F",
        "royalblue": "4169E1",
        "saddlebrown": "8B4513",
        "salmon": "FA8072",
        "sandybrown": "F4A460",
        "seagreen": "2E8B57",
        "seashell": "FFF5EE",
        "sienna": "A0522D",
        "silver": "C0C0C0",
        "skyblue": "87CEEB",
        "slateblue": "6A5ACD",
        "slategray": "708090",
        "slategrey": "708090",
        "snow": "FFFAFA",
        "springgreen": "00FF7F",
        "steelblue": "4682B4",
        "tan": "D2B48C",
        "teal": "008080",
        "thistle": "D8BFD8",
        "tomato": "FF6347",
        "turquoise": "40E0D0",
        "violet": "EE82EE",
        "wheat": "F5DEB3",
        "white": "FFFFFF",
        "whitesmoke": "F5F5F5",
        "yellow": "FFFF00",
        "yellowgreen": "9ACD32"
    }

    def run(self, edit, paste = True):

        color = self.get_selected(edit)     # in 'RRGGBB' format or None

        binpath = os.path.join(sublime.packages_path(), usrbin, binname)
        if sublime.platform() == 'windows':
            color = self.pick_win(binpath, color)

        else:
            args = [binpath]
            if color:
                if sublime.platform() == 'osx':
                    args.append('-startColor')
                    args.append(color)
                else:
                    args.append('#' + color)

            proc = subprocess.Popen(args, stdout=subprocess.PIPE)
            color = proc.communicate()[0].strip()


        if color:
            if sublime.platform() != 'windows' or sublime_version == 2:
                color = color.decode('utf-8')

            # color = '#' + color
            if paste:
                self.put_selected(edit, color)


    def get_selected(self, edit):
        """ return currently selected color in 'RRGGBB' format """

        # get the currently selected color - if any
        sel = self.view.sel()
        if len(sel) > 0:
            selected = self.view.substr(self.view.word(sel[0])).strip()
            line = self.view.substr(self.view.line(sel[0])).strip()
            if selected.startswith('#'): 
                selected = selected[1:]
                svg_color_hex = self.SVGColors.get(selected, None)
                if svg_color_hex != None:
                    selected = svg_color_hex
            elif "rgb" in line:
                selected = re.findall(r'(rgb[a]?\s*\([0-9\.\,\s]*\))', line)[0]
            return selected


    def put_selected(self, edit, color):
        """ replace all regions with color """

        for region in self.view.sel():
            word = self.view.word(region)
            line = self.view.substr(self.view.line(region))
            # if the selected word is a valid color, replace it
            if self.__is_valid_hex_color(self.view.substr(word)):

                # include '#' if present
                if self.view.substr(word.a - 1) == '#':
                    word = sublime.Region(word.a - 1, word.b)

                # replace
                self.view.replace(edit, word, color)

            # replace for rgb
            elif line.find("rgb"):
                repl = re.sub(r'(rgb[a]?\s*\([0-9\.\,\s]*\))', color, line)
                self.view.replace(edit, self.view.line(region), repl)

            # otherwise just replace the selected region
            else:
                self.view.replace(edit, region, color)


    def pick_win(self, binpath, color):
        import ctypes
        from ctypes import c_int32, c_uint32, c_void_p, c_wchar_p, pointer, POINTER, byref

        # ARGB
        # UINT __cdecl PickColor(CWnd *pParent, CColorRGBA & colText, CColorRGBA & colBk);
        dll = ctypes.cdll.LoadLibrary(binpath)
        fn = dll.PickColor
        fn.argtypes = [c_void_p, POINTER(c_uint32), POINTER(c_uint32)]
        fn.restype = c_uint32

        IDOK = 1

        rgb = self.__hexstr_to_rgb(color) if color else 0x00000000
        fg = c_uint32(rgb)          # black by default
        bg = c_uint32(0xFFFFFFFF)   # white background
        re = fn(None, byref(fg), byref(bg))
        if re == IDOK:
            return self.__rgb_to_hexstr(fg.value & 0xFFFFFF) # without alpha


    def __get_pixel(self):
        hdc = GetDC(0)
        pos = POINT()
        GetCursorPos(ctypes.byref(pos))
        val = GetPixel(hdc, pos.x, pos.y)
        ReleaseDC(0, hdc)
        return val


    def __is_valid_hex_color(self, s):
        if len(s) not in (3, 6):
            return False
        try:
            return 0 <= int(s, 16) <= 0xffffff
        except ValueError:
            return False

    def __rgb_to_hexstr(self, rgb):
        # 0x00RRGGBB
        r = (rgb >> 16) & 0xff
        g = (rgb >>  8) & 0xff
        b = (rgb      ) & 0xff
        return "%02x%02x%02X" % (r,g,b)

    def __hexstr_to_rgb(self, hexstr):
        if hexstr[0] == '#':
            hexstr = hexstr[1:]

        if len(hexstr) == 3:
            hexstr = hexstr[0] + hexstr[0] + hexstr[1] + hexstr[1] + hexstr[2] + hexstr[2]

        r = int(hexstr[0:2], 16)
        g = int(hexstr[2:4], 16)
        b = int(hexstr[4:6], 16)
        return (r << 16)| (g << 8) | b


if sublime.platform() == 'osx':
    binname = 'osx_colorpicker'
elif sublime.platform() == 'windows':
    binname = 'ColorPicker.dll'
else:
    binname = 'linux_colorpicker.py'

usrbin = os.path.join('User', 'ColorPicker', 'bin')

def update_binary():
    bindir = os.path.join(sublime.packages_path(), usrbin)
    binpath = os.path.join(bindir, binname)
    pkgpath = os.path.join(sublime.installed_packages_path(), 'ColorPicker.sublime-package')
    respath = 'Packages/ColorPicker/lib/' + binname
    libdir = os.path.join(sublime.packages_path(), 'ColorPicker', 'lib')
    libpath = os.path.join(libdir, binname)

    bininfo = None
    bindata = None

    if os.path.exists(binpath):
        bininfo = os.stat(binpath)
    elif not os.path.exists(bindir):
        os.makedirs(bindir, 0o755)

    if os.path.exists(libpath):
        libinfo = os.stat(libpath)
        if bininfo == None or bininfo[ST_MTIME] < libinfo[ST_MTIME]:
            with open(libpath, 'rb') as libfile:
                bindata = libfile.read()
                libfile.close()
    elif sublime_version == 3 and os.path.exists(pkgpath):
        pkginfo = os.stat(pkgpath)
        if bininfo == None or bininfo[ST_MTIME] < pkginfo[ST_MTIME]:
            bindata = sublime.load_binary_resource(respath)

    if bindata != None:
        print("* Updating " + binpath)
        with open(binpath, 'wb') as binfile:
            binfile.write(bindata)
            binfile.close()

    if not os.access(binpath, os.X_OK):
        os.chmod(binpath, 0o755)


def plugin_loaded():
    set_timeout_async(update_binary)


if sublime_version == 3:
    set_timeout_async = sublime.set_timeout_async
else:
    class Async(threading.Thread):
        def __init__(self, callback):
            self.callback = callback
            threading.Thread.__init__(self)

        def run(self):
            self.callback()

    def set_timeout_async(callback, delay_ms = 0):
        sublime.set_timeout(lambda: Async(callback).start(), delay_ms)

    plugin_loaded()
