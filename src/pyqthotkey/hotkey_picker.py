from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QPushButton


class HotkeyPicker(QPushButton):

    # Signal that hotkey has changed
    hotkeyChanged = Signal(object, object)

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
                 whitelisted_keys: list[Qt.Key] = [], blacklisted_keys: list[Qt.Key] = []):
        """Create a new HotkeyPicker instance

        :param parent: the parent widget
        :param default_text: the text shown when no hotkey is selected
        :param selection_text: the text shown when in selection
        :param cancel_key: the key that is used to exit the current key selection
        :param key_filter_enabled: if the hotkey picker should use a filter instead of accepting every key
        :param whitelisted_keys: list of keys that can be chosen (key_filter_enabled must be True)
        :param blacklisted_keys: list of keys that cannot be chosen (key_filter_enabled must be True)
        """

        super(HotkeyPicker, self).__init__(parent)

        # Init arguments
        self.__default_text = default_text
        self.__selection_text = selection_text
        self.__cancel_key = cancel_key
        self.__key_filter_enabled = key_filter_enabled
        self.__whitelisted_keys = whitelisted_keys
        self.__blacklisted_keys = blacklisted_keys

        # Make sure either whitelisted_keys or blacklisted_keys is emtpy
        if whitelisted_keys and blacklisted_keys:
            self.__blacklisted_keys = []

        # Init variables
        self.__selected_key = None
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
        if self.__selected_key is None and self.__in_selection:
            self.setText(self.__default_text)
            self.__in_selection = False
        elif self.__selected_key is not None and self.__in_selection:
            self.setText(HotkeyPicker.keyCodeToString(self.__selected_key))
            self.__in_selection = False

    def keyPressEvent(self, event):
        """Get key from event and set it as the hotkey

        :param event: event sent by PyQt
        """

        key = event.key()

        # Check if entered key is cancel key
        if key == self.__cancel_key:
            self.setText(self.__default_text)
            self.__selected_key = None
        else:
            # Ignore key press if key is not in whitelisted_keys
            if self.__key_filter_enabled and self.__whitelisted_keys and key not in self.__whitelisted_keys:
                return
            # Ignore key press if key is in blacklisted_keys
            elif self.__key_filter_enabled and self.__blacklisted_keys and key in self.__blacklisted_keys:
                return

            self.setText(HotkeyPicker.keyCodeToString(key))
            self.__selected_key = key

        # Clear selection and widget focus
        self.__in_selection = False
        self.clearFocus()

        # Emit signal
        self.__emit_hotkey_changed_signal()

    def getHotkey(self) -> Qt.Key | None:
        """Get the currently selected hotkey

        :return: key code, 0 if no hotkey is selected
        """

        return self.__selected_key

    def getHotkeyString(self) -> str:
        """Get the name of the currently selected hotkey

        :return: string with the key name, empty string if no hotkey is selected
        """

        return HotkeyPicker.keyCodeToString(self.__selected_key)

    def setHotkey(self, hotkey: Qt.Key | int):
        """Set the hotkey

        :param hotkey: the key code of the hotkey (e.g. 65 or Qt.Key_A)
        """

        # Ignore if filter is enabled and key code is not in whitelisted_keys
        if (self.__key_filter_enabled and self.__whitelisted_keys
                and hotkey not in self.__whitelisted_keys):
            return
        # Ignore if filter is enabled and key code is in blacklisted_keys
        elif (self.__key_filter_enabled and self.__blacklisted_keys
              and hotkey in self.__blacklisted_keys):
            return

        # Set hotkey if input key valid
        key_string = HotkeyPicker.keyCodeToString(hotkey)

        if key_string is not None:
            self.__selected_key = int(hotkey)
            self.setText(key_string)
            # Emit signal
            self.__emit_hotkey_changed_signal()

    def reset(self):
        """Reset the hotkey picker to the default state with no hotkey selected"""

        self.setText(self.__default_text)
        self.__selected_key = None

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
        if not self.__in_selection and self.__selected_key is None:
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
        """Get whether keys are being filtered

        :return: whether keys are being filtered
        """

        return self.__key_filter_enabled

    def setKeyFilterEnabled(self, on: bool):
        """Enable or disable key filtering

        :param on: if keys should be filtered
        """

        self.__key_filter_enabled = on

    def getWhitelistedKeys(self) -> list[Qt.Key]:
        """Get list of whitelisted keys

        :return: whitelisted keys
        """

        return self.__whitelisted_keys

    def setWhitelistedKeys(self, whitelisted_keys: list[Qt.Key | int]):
        """Set whitelisted keys (keys that can be selected)

        :param whitelisted_keys: the new list of whitelisted keys
        """

        if whitelisted_keys and self.__blacklisted_keys:
            self.__blacklisted_keys = []
        self.__whitelisted_keys = whitelisted_keys

    def getBlacklistedKeys(self) -> list[Qt.Key]:
        """Get list of blacklisted keys

        :return: blacklisted keys
        """

        return self.__blacklisted_keys

    def setBlacklistedKeys(self, blacklisted_keys: list[Qt.Key | int]):
        """Set blacklisted keys (keys that cannot be selected)

        :param blacklisted_keys: the new list of blacklisted keys
        """

        if blacklisted_keys and self.__whitelisted_keys:
            self.__whitelisted_keys = []
        self.__blacklisted_keys = blacklisted_keys

    def __emit_hotkey_changed_signal(self):
        """Emit a signal that the selected hotkey has changed"""

        self.hotkeyChanged.emit(self.__selected_key,
                                HotkeyPicker.keyCodeToString(self.__selected_key))

    @staticmethod
    def keyCodeToString(key_code: Qt.Key | int) -> str:
        """Get the key name from a key code

        :param key_code: the key you want to get the name of (e.g. 65 or Qt.Key_A)
        :return: name of the key as string
        """

        return HotkeyPicker.__key_code_map.get(key_code)
