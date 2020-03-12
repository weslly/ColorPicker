###Mac OSX
![Mac OSX](http://i.minus.com/i5KI6SBAfs7Qk.png "Mac OS X")

###Linux
![Linux](http://i.minus.com/ihwLvn8m29GxZ.png "Linux")

###Windows
![Windows](http://i.minus.com/iY1DDCRG5TsyR.png "Windows")

## Installation
Install this repository via [Package Control](https://sublime.wbond.net).


## Usage
To insert or change a selected color, use:

- Linux: `ctrl+shift+c`
- Windows: `ctrl+shift+c`
- OS X: `cmd+shift+c`

or use menu action

- **`Tools`** -> **`ColorPicker`**


By default, the hex color code is inserted using uppercase letters. To use lowercase letters instead, copy the contents of **`Preferences -> Package Settings -> ColorPicker -> Settings-Default`** to the empty file created by selecting **`Preferences -> Package Settings -> ColorPicker -> Settings-User`**, then change `"color_upper_case"` to `false`.

## Calling from Other Plugins
To commands are provided to assist in calling a color picker from other plugins.  Info is shared between the plugins via a settings file.  It does not have to exist on disk; it can exist only in memory for the sole purpose of sharing the return.  It is advised to use a unique name for the settings file.  The data is returned in the settings key `color_pick_return`.  It is advised to set `color_pick_return` to `None` in your settings file before calling any of the commands. So you can tell if it set teh variable or not.

### ColorPickApiIsAvailableCommand
This command is used to test if ColorPicker is installed.

```python
>> settings = sublime.load_settings('my_shared.sublime-settings')
>> settings.set('color_pick_return', None)
>> sublime.run_command('color_pick_api_is_available', {'settings': 'my_shared.sublime-settings'})
>> print(settings.get('color_pick_return'))
True
```

### ColorPickApiGetColorCommand
This command is used to call a color picker and get the selected value.  It takes a setings file and an optional `default_color`.

```python
>> settings = sublime.load_settings('my_shared.sublime-settings')
>> settings.set('color_pick_return', None)
>> sublime.run_command('color_pick_api_get_color', {'settings': 'my_shared.sublime-settings', 'default_color': '#ff0000'})
>> print(settings.get('color_pick_return'))
#23af44
```

## Acknowledgements

- [Original colorpick plugin for OS X by jnordberg](https://github.com/jnordberg/sublime-colorpick/)
- [Original colorpick plugin for Windows by animehunter](https://github.com/animehunter/SublimeColorPickerWindowsOnly)
