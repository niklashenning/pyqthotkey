from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel
from src.hotkey_picker import HotkeyPicker


class Window(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)

        self.setWindowTitle('Hotkey Picker Demo')
        self.setFixedSize(360, 150)

        # Define variables to store selected hotkeys in
        self.selected_hotkey_1 = 0
        self.selected_hotkey_1_name = ''
        self.selected_hotkey_2 = 0
        self.selected_hotkey_2_name = ''

        # Add labels for the hotkey pickers
        self.label_1 = QLabel(self)
        self.label_1.setText('Hotkey 1:')
        self.label_1.move(80, 32)  # Using fixed positions for simplicity

        self.label_2 = QLabel(self)
        self.label_2.setText('Hotkey 2:')
        self.label_2.move(80, 78)

        # Add first hotkey picker with default settings
        self.hotkey_picker_1 = HotkeyPicker(self)
        self.hotkey_picker_1.move(170, 32)
        self.hotkey_picker_1.hotkey_changed.connect(self.hotkey_picker_1_changed)
        self.hotkey_picker_1.setHotkey(Qt.Key_F5)

        # Add second hotkey picker with default settings
        self.hotkey_picker_2 = HotkeyPicker(self)
        self.hotkey_picker_2.move(170, 78)
        self.hotkey_picker_2.hotkey_changed.connect(self.hotkey_picker_2_changed)

    def hotkey_picker_1_changed(self, key, key_name):
        # Handle change of hotkey 1
        self.selected_hotkey_1 = key
        self.selected_hotkey_1_name = key_name
        print([key, key_name])

    def hotkey_picker_2_changed(self, key, key_name):
        # Handle change of hotkey 2
        self.selected_hotkey_2 = key
        self.selected_hotkey_2_name = key_name
        print([key, key_name])

    def keyPressEvent(self, event):
        # React to a selected hotkey being pressed
        if event.key() == self.selected_hotkey_1:
            print('Selected hotkey 1 (' + self.selected_hotkey_1_name + ') has been pressed')
        if event.key() == self.selected_hotkey_2:
            print('Selected hotkey 2 (' + self.selected_hotkey_2_name + ') has been pressed')
