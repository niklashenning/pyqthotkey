# pyqt-hotkey-picker
A simple and customizable hotkey picker widget for PyQt5

## Installation
Download the **hotkey_picker.py** file from the **src** folder and add it to your project

## Usage
Import the `HotkeyPicker` class and add it to your window like any other PyQt Widget:
```python
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from hotkey_picker import HotkeyPicker


class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        # Add hotkey picker with default settings
        demo_hotkey_picker = HotkeyPicker(self)
        # Connect change event
        demo_hotkey_picker.hotkey_changed.connect(self.hotkey_changed)
    
    # Called every time the picked hotkey changes
    def hotkey_changed(self, key, key_name):
        print([key, key_name])
```
Use the `get_hotkey` method to get the key code of the selected hotkey:
```python
# Returns int with key code if a hotkey is selected, otherwise 0
key_code = demo_hotkey_picker.get_hotkey()  # e.g. 65 (which is the same as Qt.Key_A)
```

Use the `get_hotkey_string` method to get the name of the selected hotkey:
```python
# Returns string with key name if a hotkey is selected, otherwise empty string
key_name = demo_hotkey_picker.get_hotkey_string()  # e.g. 'Shift'
```

Use the `set_hotkey` method to set the selected hotkey manually:
```python
demo_hotkey_picker.set_hotkey(Qt.Key_A)  # could also directly pass int (e.g. 65)
```

Use the `reset` method to reset the hotkey picker to the default state with no selected hotkey:
```python
demo_hotkey_picker.reset()
```

You can also use the static `key_code_to_string` method to get the name of a key:
```python
key_name_1 = HotkeyPicker.key_code_to_string(Qt.Key_A)  # A
key_name_2 = HotkeyPicker.key_code_to_string(16777268)  # F5
```

More in-depth examples can be found in the **examples** folder

## Customization
* **Changing the cancel key used to exit the hotkey selection:**

  ```python
  # Default value: Qt.Key_Escape
  demo_hotkey_picker = HotkeyPicker(self, cancel_key=Qt.Key_Return)
  ```
  
* **Changing the default text of the hotkey picker:**

   ```python
   # Default value: 'None' 
   demo_hotkey_picker = HotkeyPicker(self, default_text='Not selected..')
   ```
  
* **Changing the text of the hotkey picker that is shown when waiting for a key press:**

   ```python
   # Default value: '..'
   demo_hotkey_picker = HotkeyPicker(self, selecting_text='Selecting..')
   ```

* **Only allowing specific keys to be selected:**

   ```python
   # List of allowed keys (no other key can be selected)
   keys = [Qt.Key_F1, Qt.Key_F2, Qt.Key_F3, Qt.Key_F4, Qt.Key_F5, Qt.Key_F6,
           Qt.Key_F7, Qt.Key_F8, Qt.Key_F9, Qt.Key_F10, Qt.Key_F11, Qt.Key_F12]
  
   demo_hotkey_picker = HotkeyPicker(self, filter_keys=True, allowed_keys=keys)
   ```

* **Not allowing specific keys to be selected:**

   ```python
   # List of forbidden keys (every other key can be selected)
   keys = [Qt.Key_F1, Qt.Key_F2, Qt.Key_F3, Qt.Key_F4, Qt.Key_F5]
  
   demo_hotkey_picker = HotkeyPicker(self, filter_keys=True, forbidden_keys=keys)
   ```
  **Note**: Only one of these filter options can be set per hotkey picker, meaning you can either specify the exact keys you want to allow or specify the exact keys you want to forbid.

## License
This software is licensed under the [MIT license](LICENSE).