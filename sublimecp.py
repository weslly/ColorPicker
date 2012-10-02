import sublime
import sublime_plugin
import subprocess
import os

if sublime.platform() == 'windows':
    import ctypes
    from ctypes import c_int32, c_uint32, c_void_p, c_wchar_p, pointer, POINTER

    class CHOOSECOLOR(ctypes.Structure):
         _fields_ = [('lStructSize', c_uint32),
                     ('hwndOwner', c_void_p),
                     ('hInstance', c_void_p),
                     ('rgbResult', c_uint32),
                     ('lpCustColors',POINTER(c_uint32)),
                     ('Flags', c_uint32),
                     ('lCustData', c_void_p),
                     ('lpfnHook', c_void_p),
                     ('lpTemplateName', c_wchar_p)]

    class POINT(ctypes.Structure):
         _fields_ = [('x', c_int32),
                     ('y', c_int32)]

    CustomColorArray = c_uint32 * 16
    CC_SOLIDCOLOR = 0x80
    CC_RGBINIT = 0x01
    CC_FULLOPEN = 0x02

    ChooseColorW = ctypes.windll.Comdlg32.ChooseColorW
    ChooseColorW.argtypes = [POINTER(CHOOSECOLOR)]
    ChooseColorW.restype = c_int32

    GetDC = ctypes.windll.User32.GetDC
    GetDC.argtypes = [c_void_p]
    GetDC.restype = c_void_p

    ReleaseDC = ctypes.windll.User32.ReleaseDC
    ReleaseDC.argtypes = [c_void_p, c_void_p] #hwnd, hdc
    ReleaseDC.restype = c_int32

    GetCursorPos = ctypes.windll.User32.GetCursorPos
    GetCursorPos.argtypes = [POINTER(POINT)] # POINT
    GetCursorPos.restype = c_int32

    GetPixel = ctypes.windll.Gdi32.GetPixel
    GetPixel.argtypes = [c_void_p, c_int32, c_int32] # hdc, x, y
    GetPixel.restype = c_uint32 # colorref


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

    def run(self, edit):
        paste = None
        sel = self.view.sel()
        start_color = None
        start_color_osx = None
        start_color_win = None

        # get the currently selected color - if any
        if len(sel) > 0:
            selected = self.view.substr(self.view.word(sel[0])).strip()
            if selected.startswith('#'): selected = selected[1:]

            svg_color_hex = self.SVGColors.get(selected, None)
            if svg_color_hex != None:
                selected = svg_color_hex

            if self.__is_valid_hex_color(selected):
                start_color = "#" + selected
                start_color_osx = selected
                start_color_win = self.__hexstr_to_bgr(selected)
                

        if sublime.platform() == 'windows':

            s = sublime.load_settings("ColorPicker.sublime-settings")
            custom_colors = s.get("custom_colors", ['0']*16)

            if len(custom_colors) < 16:
                custom_colors = ['0']*16
                s.set('custom_colors', custom_colors)
                
            cc = CHOOSECOLOR()
            ctypes.memset(ctypes.byref(cc), 0, ctypes.sizeof(cc))
            cc.lStructSize = ctypes.sizeof(cc)
            cc.hwndOwner = self.view.window().hwnd()
            cc.Flags = CC_SOLIDCOLOR | CC_FULLOPEN | CC_RGBINIT
            cc.rgbResult = c_uint32(start_color_win) if not paste and start_color_win else self.__get_pixel()
            cc.lpCustColors = self.__to_custom_color_array(custom_colors)

            if ChooseColorW(ctypes.byref(cc)):
                color = self.__bgr_to_hexstr(cc.rgbResult)
            else:
                color = None


        elif sublime.platform() == 'osx':
            location = os.path.join(sublime.packages_path(), 'ColorPicker', 'lib', 'osx_colorpicker')
            args = [location]

            if not os.access(location, os.X_OK):
                os.chmod(location, 0755)
                
            if start_color_osx:
                args.append('-startColor')
                args.append(start_color_osx)

        else:
            location = os.path.join(sublime.packages_path(), 'ColorPicker', 'lib', 'linux_colorpicker.py')
            args = [location]

            if not os.access(location, os.X_OK):
                os.chmod(location, 0755)
            
            if start_color:
                args.append(start_color)


        if sublime.platform() == 'osx' or sublime.platform() == 'linux':
            proc = subprocess.Popen(args, stdout=subprocess.PIPE)
            color = proc.communicate()[0].strip()

        if color:
            # replace all regions with color
            for region in sel:
                word = self.view.word(region)
                # if the selected word is a valid color, replace it
                if self.__is_valid_hex_color(self.view.substr(word)):
                    # include '#' if present
                    if self.view.substr(word.a - 1) == '#':
                        word = sublime.Region(word.a - 1, word.b)
                    # replace
                    self.view.replace(edit, word, '#' + color)
                # otherwise just replace the selected region
                else:
                    self.view.replace(edit, region, '#' + color)
                    

    def __get_pixel(self):
        hdc = GetDC(0)
        pos = POINT()
        GetCursorPos(ctypes.byref(pos))
        val = GetPixel(hdc, pos.x, pos.y)
        ReleaseDC(0, hdc)
        return val

    def __to_custom_color_array(self, custom_colors):
        cc = CustomColorArray()
        for i in range(16):
            cc[i] = int(custom_colors[i])
        return cc

    def __from_custom_color_array(self, custom_colors):
        cc = [0]*16
        for i in range(16):
            cc[i] = str(custom_colors[i])
        return cc

    def __is_valid_hex_color(self, s):
        if len(s) not in (3, 6):
            return False
        try:
            return 0 <= int(s, 16) <= 0xffffff
        except ValueError:
            return False

    def __bgr_to_hexstr(self, bgr, byte_table=list(map(lambda b: '{0:02X}'.format(b), range(256)))):
        # 0x00BBGGRR
        b = byte_table[(bgr >> 16) & 0xff]
        g = byte_table[(bgr >>  8) & 0xff]
        r = byte_table[(bgr      ) & 0xff]
        return (r+g+b)

    def __hexstr_to_bgr(self, hexstr):
        if len(hexstr) == 3:
            hexstr = hexstr[0] + hexstr[0] + hexstr[1] + hexstr[1] + hexstr[2] + hexstr[2]

        r = int(hexstr[0:2], 16)
        g = int(hexstr[2:4], 16)
        b = int(hexstr[4:6], 16)
        return (b << 16)| (g << 8) | r