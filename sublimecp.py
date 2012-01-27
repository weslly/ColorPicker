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