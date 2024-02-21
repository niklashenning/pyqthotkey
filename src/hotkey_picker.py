from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton


class HotkeyPicker(QPushButton):

    # Signal that hotkey has changed
    hotkey_changed = pyqtSignal(int, str)

    # Key code map
    key_code_map = {}
    for key, value in vars(Qt).items():
        if isinstance(value, Qt.Key):
            key_code_map[value] = key.partition('_')[2]

    # Manually change name for some keys
    key_code_map[Qt.Key_Adiaeresis] = 'Ä'
    key_code_map[Qt.Key_Odiaeresis] = 'Ö'
    key_code_map[Qt.Key_Udiaeresis] = 'Ü'

    def __init__(self, parent=None, default_text='None', selecting_text='..',
                 cancel_key=Qt.Key_Escape, filter_keys=False, allowed_keys=[], forbidden_keys=[]):
        """Create a new HotkeyPicker instance

        :param parent: the parent widget
        :param default_text: the text shown when no hotkey is selected
        :param selecting_text: the text shown when in selection
        :param cancel_key: the key that is used to exit the current key selection
        :param filter_keys: if the hotkey picker should use a filter instead of accepting every key
        :param allowed_keys: list of keys that can be chosen (filter_keys must be enabled)
        :param forbidden_keys: list of keys that cannot be chosen (filter_keys must be enabled)
        """

        super(HotkeyPicker, self).__init__(parent)

        # Init arguments
        self.default_text = default_text
        self.selecting_text = selecting_text
        self.cancel_key = cancel_key
        self.filter_keys = filter_keys
        self.allowed_keys = allowed_keys
        self.forbidden_keys = forbidden_keys

        # Make sure either allowed_keys or forbidden_keys is emtpy
        if allowed_keys and forbidden_keys:
            self.forbidden_keys = []

        # Init variables
        self.selected_key_code = 0
        self.selected_key_string = ''
        self.in_selection = False

        # Prevent the hotkey picker from focusing automatically (e.g. if it is the only widget)
        self.setFocusPolicy(Qt.ClickFocus)

        self.setText(self.default_text)

    def focusInEvent(self, event):
        """Set text to selection text

        :param event: event sent by PyQt
        """

        self.in_selection = True
        self.setText(self.selecting_text)

    def focusOutEvent(self, event):
        """Unset selection text if focused out without new key being selected

        :param event: event sent by PyQt
        """

        # Focus out without a new key being selected
        if self.selected_key_code == 0 and self.in_selection:
            self.setText(self.default_text)
            self.in_selection = False
        elif self.selected_key_code != 0 and self.in_selection:
            self.setText(HotkeyPicker.key_code_to_string(self.selected_key_code))
            self.in_selection = False

    def keyPressEvent(self, event):
        """Get key from event and set it as the hotkey

        :param event: event sent by PyQt
        """

        key = event.key()
        key_string = HotkeyPicker.key_code_to_string(key)

        # Check if entered key is cancel key
        if key == self.cancel_key:
            self.setText(self.default_text)
            self.selected_key_code = 0
            self.selected_key_string = ''
        else:
            # Ignore key press if key is not in allowed_keys
            if self.filter_keys and self.allowed_keys and key not in self.allowed_keys:
                return
            # Ignore key press if key is in forbidden_keys
            elif self.filter_keys and self.forbidden_keys and key in self.forbidden_keys:
                return

            self.setText(key_string)
            self.selected_key_code = key
            self.selected_key_string = key_string

        # Clear selection and widget focus
        self.in_selection = False
        self.clearFocus()

        # Emit signal
        self.__emit_hotkey_changed_signal()

    def get_hotkey(self):
        """Get the currently selected hotkey

        :return: int with the key code, 0 if no hotkey is selected
        """

        return self.selected_key_code

    def get_hotkey_string(self):
        """Get the name of the currently selected hotkey

        :return: string with the key name, empty string if no hotkey is selected
        """

        return self.selected_key_string

    def set_hotkey(self, hotkey):
        """Set the hotkey

        :param hotkey: the key code of the hotkey (e.g. 65 or Qt.Key_A)
        """

        key_string = HotkeyPicker.key_code_to_string(hotkey)

        # Ignore if filter is enabled and key code is not in allowed keys
        if self.filter_keys and self.allowed_keys and hotkey not in self.allowed_keys:
            return
        # Ignore if filter is enabled and key code is in forbidden keys
        elif self.filter_keys and self.forbidden_keys and hotkey in self.forbidden_keys:
            return

        # Input key code valid
        if key_string is not None:
            self.selected_key_code = hotkey
            self.selected_key_string = key_string
            self.setText(key_string)
            # Emit signal
            self.__emit_hotkey_changed_signal()

    def reset(self):
        """Reset the hotkey picker to the default state with no hotkey selected"""

        self.setText(self.default_text)
        self.selected_key_code = 0
        self.selected_key_string = ''

        # Emit signal
        self.__emit_hotkey_changed_signal()

    def get_default_text(self):
        """Get the default text"""

        return self.default_text

    def set_default_text(self, default_text):
        """Set the default text

        :param default_text: the new default text
        """

        self.default_text = default_text
        if not self.in_selection and self.selected_key_code == 0:
            self.setText(default_text)

    def get_selecting_text(self):
        """Get the selecting text"""

        return self.selecting_text

    def set_selecting_text(self, selecting_text):
        """Set the selecting text

        :param selecting_text: the new selecting text
        :return:
        """

        self.selecting_text = selecting_text
        if self.in_selection:
            self.setText(selecting_text)

    def get_cancel_key(self):
        """Get the cancel key"""

        return self.cancel_key

    def set_cancel_key(self, cancel_key):
        """Set the cancel key

        :param cancel_key: the new cancel key
        """

        self.cancel_key = cancel_key

    def get_filter_keys(self):
        """Get key filtering"""

        return self.filter_keys

    def set_filter_keys(self, filter_keys):
        """Set key filtering

        :param filter_keys: bool if keys should be filtered
        """

        self.filter_keys = filter_keys

    def get_allowed_keys(self):
        """Get allowed keys"""

        return self.allowed_keys

    def set_allowed_keys(self, allowed_keys):
        """Set allowed keys

        :param allowed_keys: the new allowed keys list
        """

        if allowed_keys and self.forbidden_keys:
            self.forbidden_keys = []
        self.allowed_keys = allowed_keys

    def get_forbidden_keys(self):
        """Get forbidden keys"""

        return self.forbidden_keys

    def set_forbidden_keys(self, forbidden_keys):
        """Set forbidden keys

        :param forbidden_keys: the new forbidden keys list
        """

        if forbidden_keys and self.allowed_keys:
            self.allowed_keys = []
        self.forbidden_keys = forbidden_keys

    def __emit_hotkey_changed_signal(self):
        """Emit a signal that the selected hotkey has changed"""

        self.hotkey_changed.emit(self.selected_key_code, self.selected_key_string)

    @staticmethod
    def key_code_to_string(key_code):
        """Get the key name from a key code

        :param key_code: the key you want to get the name of (e.g. 65 or Qt.Key_A)
        :return: name of the key as string
        """

        return HotkeyPicker.key_code_map.get(key_code)
