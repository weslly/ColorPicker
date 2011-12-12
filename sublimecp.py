import sublime
import sublime_plugin
import subprocess
import os
import sys

def is_valid_hex_color(s):
    if len(s) not in (3, 6):
        return False
    try:
        return 0 <= int(s, 16) <= 0xffffff
    except ValueError:
        return False

class ColorPickCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        sel = view.sel()
        start_color = None
        start_color_osx = None

        # get the currently selected color - if any
        if len(sel) > 0:
            selected = view.substr(view.word(sel[0])).strip()
            if selected.startswith('#'): selected = selected[1:]
            if is_valid_hex_color(selected):
                start_color = "#"+selected
                start_color_osx = selected
                

        if os.name == 'nt':
            args = []
        elif sys.platform == 'darwin':
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

        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        color = proc.communicate()[0].strip()

        if color:
            # replace all regions with color
            for region in sel:
                word = view.word(region)
                # if the selected word is a valid color, replace it
                if is_valid_hex_color(view.substr(word)):
                    # include '#' if present
                    if view.substr(word.a - 1) == '#':
                        word = sublime.Region(word.a - 1, word.b)
                    # replace
                    self.view.replace(edit, word, '#' + color)
                # otherwise just replace the selected region
                else:
                    self.view.replace(edit, region, '#' + color)
