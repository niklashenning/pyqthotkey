from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QPushButton


class HotkeyPicker(QPushButton):

    # Signal that hotkey has changed
    hotkeyChanged = Signal(int, str)

    # Key code map
    __key_code_map = {}
    for key, value in vars(Qt).items():
        if isinstance(value, Qt.Key):
            __key_code_map[value] = key.partition('_')[2]

    # Manually change name for some keys
    __key_code_map[Qt.Key.Key_Adiaeresis] = 'Ä'
    __key_code_map[Qt.Key.Key_Odiaeresis] = 'Ö'
    __key_code_map[Qt.Key.Key_Udiaeresis] = 'Ü'

    def __init__(self, parent=None, default_text: str = 'None', selection_text: str = '..',
                 cancel_key: Qt.Key = Qt.Key.Key_Escape, key_filter_enabled: bool = False,
                 allowed_keys: list[Qt.Key] = [], forbidden_keys: list[Qt.Key] = []):
        """Create a new HotkeyPicker instance

        :param parent: the parent widget
        :param default_text: the text shown when no hotkey is selected
        :param selection_text: the text shown when in selection
        :param cancel_key: the key that is used to exit the current key selection
        :param key_filter_enabled: if the hotkey picker should use a filter instead of accepting every key
        :param allowed_keys: list of keys that can be chosen (filter_keys must be enabled)
        :param forbidden_keys: list of keys that cannot be chosen (filter_keys must be enabled)
        """

        super(HotkeyPicker, self).__init__(parent)

        # Init arguments
        self.__default_text = default_text
        self.__selection_text = selection_text
        self.__cancel_key = cancel_key
        self.__key_filter_enabled = key_filter_enabled
        self.__allowed_keys = allowed_keys
        self.__forbidden_keys = forbidden_keys

        # Make sure either allowed_keys or forbidden_keys is emtpy
        if allowed_keys and forbidden_keys:
            self.__forbidden_keys = []

        # Init variables
        self.__selected_key_code = 0
        self.__selected_key_string = ''
        self.__in_selection = False

        self.setText(self.__default_text)

        # Prevent the hotkey picker from focusing automatically (e.g. if it is the only widget)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    def focusInEvent(self, event):
        """Set text to selection text

        :param event: event sent by PyQt
        """

        self.__in_selection = True
        self.setText(self.__selection_text)

    def focusOutEvent(self, event):
        """Unset selection text if focused out without new key being selected

        :param event: event sent by PyQt
        """

        # Focus out without a new key being selected
        if self.__selected_key_code == 0 and self.__in_selection:
            self.setText(self.__default_text)
            self.__in_selection = False
        elif self.__selected_key_code != 0 and self.__in_selection:
            self.setText(HotkeyPicker.keyCodeToString(self.__selected_key_code))
            self.__in_selection = False

    def keyPressEvent(self, event):
        """Get key from event and set it as the hotkey

        :param event: event sent by PyQt
        """

        key = event.key()
        key_string = HotkeyPicker.keyCodeToString(key)

        # Check if entered key is cancel key
        if key == self.__cancel_key:
            self.setText(self.__default_text)
            self.__selected_key_code = 0
            self.__selected_key_string = ''
        else:
            # Ignore key press if key is not in allowed_keys
            if self.__key_filter_enabled and self.__allowed_keys and key not in self.__allowed_keys:
                return
            # Ignore key press if key is in forbidden_keys
            elif self.__key_filter_enabled and self.__forbidden_keys and key in self.__forbidden_keys:
                return

            self.setText(key_string)
            self.__selected_key_code = key
            self.__selected_key_string = key_string

        # Clear selection and widget focus
        self.__in_selection = False
        self.clearFocus()

        # Emit signal
        self.__emit_hotkey_changed_signal()

    def getHotkey(self) -> Qt.Key | int:
        """Get the currently selected hotkey

        :return: key code, 0 if no hotkey is selected
        """

        return self.__selected_key_code

    def getHotkeyString(self) -> str:
        """Get the name of the currently selected hotkey

        :return: string with the key name, empty string if no hotkey is selected
        """

        return self.__selected_key_string

    def setHotkey(self, hotkey: Qt.Key | int):
        """Set the hotkey

        :param hotkey: the key code of the hotkey (e.g. 65 or Qt.Key_A)
        """

        key_string = HotkeyPicker.keyCodeToString(hotkey)

        # Ignore if filter is enabled and key code is not in allowed keys
        if self.__key_filter_enabled and self.__allowed_keys and hotkey not in self.__allowed_keys:
            return
        # Ignore if filter is enabled and key code is in forbidden keys
        elif self.__key_filter_enabled and self.__forbidden_keys and hotkey in self.__forbidden_keys:
            return

        # Input key code valid
        if key_string is not None:
            self.__selected_key_code = hotkey
            self.__selected_key_string = key_string
            self.setText(key_string)
            # Emit signal
            self.__emit_hotkey_changed_signal()

    def reset(self):
        """Reset the hotkey picker to the default state with no hotkey selected"""

        self.setText(self.__default_text)
        self.__selected_key_code = 0
        self.__selected_key_string = ''

        # Emit signal
        self.__emit_hotkey_changed_signal()

    def getDefaultText(self) -> str:
        """Get the default text"""

        return self.__default_text

    def setDefaultText(self, default_text: str):
        """Set the default text

        :param default_text: the new default text
        """

        self.__default_text = default_text
        if not self.__in_selection and self.__selected_key_code == 0:
            self.setText(default_text)

    def getSelectionText(self) -> str:
        """Get the selecting text"""

        return self.__selection_text

    def setSelectionText(self, selecting_text: str):
        """Set the selecting text

        :param selecting_text: the new selecting text
        """

        self.__selection_text = selecting_text
        if self.__in_selection:
            self.setText(selecting_text)

    def getCancelKey(self) -> Qt.Key:
        """Get the cancel key"""

        return self.__cancel_key

    def setCancelKey(self, cancel_key: Qt.Key | int):
        """Set the cancel key

        :param cancel_key: the new cancel key
        """

        self.__cancel_key = cancel_key

    def isKeyFilterEnabled(self) -> bool:
        """Get whether keys are being filtered"""

        return self.__key_filter_enabled

    def setKeyFilterEnabled(self, on: bool):
        """Enable or disable key filtering

        :param on: if keys should be filtered
        """

        self.__key_filter_enabled = on

    def getAllowedKeys(self) -> list[Qt.Key]:
        """Get allowed keys"""

        return self.__allowed_keys

    def setAllowedKeys(self, allowed_keys: list[Qt.Key | int]):
        """Set allowed keys

        :param allowed_keys: the new allowed keys list
        """

        if allowed_keys and self.__forbidden_keys:
            self.__forbidden_keys = []
        self.__allowed_keys = allowed_keys

    def getForbiddenKeys(self) -> list[Qt.Key]:
        """Get forbidden keys"""

        return self.__forbidden_keys

    def setForbiddenKeys(self, forbidden_keys: list[Qt.Key | int]):
        """Set forbidden keys

        :param forbidden_keys: the new forbidden keys list
        """

        if forbidden_keys and self.__allowed_keys:
            self.__allowed_keys = []
        self.__forbidden_keys = forbidden_keys

    def __emit_hotkey_changed_signal(self):
        """Emit a signal that the selected hotkey has changed"""

        self.hotkeyChanged.emit(self.__selected_key_code, self.__selected_key_string)

    @staticmethod
    def keyCodeToString(key_code: Qt.Key | int) -> str:
        """Get the key name from a key code

        :param key_code: the key you want to get the name of (e.g. 65 or Qt.Key_A)
        :return: name of the key as string
        """

        return HotkeyPicker.__key_code_map.get(key_code)
