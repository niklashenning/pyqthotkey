# PyQt Hotkey Picker

[![PyPI](https://img.shields.io/badge/pypi-v3.0.0-blue)](https://pypi.org/project/pyqthotkey)
[![Python](https://img.shields.io/badge/python-3.7+-blue)](https://github.com/niklashenning/pyqthotkey)
[![Build](https://img.shields.io/badge/build-passing-neon)](https://github.com/niklashenning/pyqthotkey)
[![Coverage](https://img.shields.io/badge/coverage-100%25-green)](https://github.com/niklashenning/pyqthotkey)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/niklashenning/pyqthotkey/blob/master/LICENSE)

A simple and customizable hotkey picker widget for PyQt and PySide

![pyqthotkey](https://github.com/niklashenning/pyqthotkey/assets/58544929/6def35ea-3848-4ec4-a2fe-b284679acc61)

## Features
* Simple and fully customizable UI
* Supports 469 different keys
* Supports whitelisting and blacklisting keys
* Supports customizing key names
* Works with `PyQt5`, `PyQt6`, `PySide2`, and `PySide6`

## Installation
````python
pip install pyqthotkey
````

## Usage
Import the `HotkeyPicker` class and add it to your window like any other PyQt widget:
```python
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from pyqthotkey import HotkeyPicker


class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        hotkey_picker = HotkeyPicker(self)  # Add hotkey picker with default settings
        hotkey_picker.hotkeyChanged.connect(self.hotkey_changed)  # Connect change event
    
    # Called every time the picked hotkey changes
    def hotkey_changed(self, key, key_name):
        print([key, key_name])
```
Use the `getHotkey()` and `getHotkeyName()` methods to get the key code and name of the selected hotkey:

```python
# Returns int with key code if a hotkey is selected, otherwise None
key_code = hotkey_picker.getHotkey()  # e.g. 65 (which is the same as Qt.Key.Key_A)

# Returns string with key name if a hotkey is selected, otherwise None
key_name = hotkey_picker.getHotkeyName()  # e.g. 'Shift'
```

Manually set the selected hotkey with the `setHotkey()` method:

```python
hotkey_picker.setHotkey(Qt.Key.Key_A)  # Could also directly pass int (e.g. 65)
```

Reset the hotkey picker to the default state with no selected hotkey by using the `reset()` method:
````python
hotkey_picker.reset()
````

You can also use the static `getKeyName()` method to get the name of a key:

```python
key_name_a = HotkeyPicker.getKeyName(Qt.Key.Key_A)  # 'A'
key_name_f5 = HotkeyPicker.getKeyName(16777268)  # 'F5'
```

More in-depth examples can be found in the [examples](https://github.com/niklashenning/pyqthotkey/blob/master/examples) folder.

## Customization
* **Overriding key names (static):**
  ```python
  # Change control key name from default 'Control' to 'Ctrl'
  HotkeyPicker.setKeyName(Qt.Key.Key_Control, 'Ctrl')
  ```

* **Changing the cancel key used to exit the hotkey selection:**

  ```python
  # On initialization
  hotkey_picker = HotkeyPicker(self, cancel_key=Qt.Key.Key_Return)
  
  # Or using the setter
  hotkey_picker.setCancelKey(Qt.Key.Key_Return)  # Default value: Qt.Key.Key_Escape
  ```
  
* **Changing the default text of the hotkey picker:**

   ```python
   # On initialization
   hotkey_picker = HotkeyPicker(self, default_text='Not selected..')
  
   # Or using the setter
   hotkey_picker.setDefaultText('Not selected..')  # Default value: 'None'
   ```

* **Changing the text of the hotkey picker that is shown when waiting for a key press:**

   ```python
   # On initialization
   hotkey_picker = HotkeyPicker(self, selection_text='Selecting..')
  
   # Or using the setter
   hotkey_picker.setSelectionText('Selecting..')  # Default value: '..'
   ```

* **Only allowing specific keys to be selected:**

   ```python
   # List of whitelisted keys (no other key can be selected)
   keys = [Qt.Key.Key_F1, Qt.Key.Key_F2, Qt.Key.Key_F3, Qt.Key.Key_F4,
           Qt.Key.Key_F5, Qt.Key.Key_F6, Qt.Key.Key_F7, Qt.Key.Key_F8,
           Qt.Key.Key_F9, Qt.Key.Key_F10, Qt.Key.Key_F11, Qt.Key.Key_F12]
   
   # On initialization 
   hotkey_picker = HotkeyPicker(self, key_filter_enabled=True, whitelisted_keys=keys)
   
   # Or using the setter
   hotkey_picker.setKeyFilterEnabled(True)  # Default: False
   hotkey_picker.setWhitelistedKeys(keys)   # Default: []
   ```

* **Not allowing specific keys to be selected:**

   ```python
   # List of blacklisted keys (every other key can be selected)
   keys = [Qt.Key.Key_F1, Qt.Key.Key_F2, Qt.Key.Key_F3,
           Qt.Key.Key_F4, Qt.Key.Key_F5]
   
   # On initialization 
   hotkey_picker = HotkeyPicker(self, key_filter_enabled=True, blacklisted_keys=keys)
   
   # Or using the setter
   hotkey_picker.setKeyFilterEnabled(True)  # Default: False
   hotkey_picker.setBlacklistedKeys(keys)   # Default: []
   ```
  > **Note:** <br>Only one filter option can be enabled per hotkey picker at any given time, meaning you can either specify the whitelisted keys, specify the blacklisted keys, or not enable key filtering at all.

## Tests
Installing the required test dependencies [PyQt6](https://pypi.org/project/PyQt6/), [pytest](https://github.com/pytest-dev/pytest), and [coveragepy](https://github.com/nedbat/coveragepy):
```
pip install PyQt6 pytest coverage
```

To run the tests with coverage, clone this repository, go into the main directory and run:
```
coverage run -m pytest
coverage report --ignore-errors -m
```

## License
This software is licensed under the [MIT license](https://github.com/niklashenning/pyqthotkey/blob/master/LICENSE).
