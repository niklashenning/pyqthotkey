from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QFormLayout, QWidget
from pyqthotkey import HotkeyPicker


class Window(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)

        # Window settings
        self.setWindowTitle('Hotkey Picker Demo')
        self.resize(360, 150)

        # Define variables to store selected hotkeys in
        self.selected_hotkey_1 = 0
        self.selected_hotkey_1_name = ''
        self.selected_hotkey_2 = 0
        self.selected_hotkey_2_name = ''

        # Add first hotkey picker
        self.hotkey_picker_1 = HotkeyPicker(self)
        self.hotkey_picker_1.hotkeyChanged.connect(self.hotkey_picker_1_changed)
        self.hotkey_picker_1.setHotkey(Qt.Key.Key_F5)

        # Add second hotkey picker
        self.hotkey_picker_2 = HotkeyPicker(self)
        self.hotkey_picker_2.hotkeyChanged.connect(self.hotkey_picker_2_changed)

        # Set size constraints
        self.hotkey_picker_1.setFixedHeight(32)
        self.hotkey_picker_2.setFixedHeight(32)

        # Form layout
        form_layout = QFormLayout()
        form_layout.addRow('Hotkey 1:', self.hotkey_picker_1)
        form_layout.addRow('Hotkey 2:', self.hotkey_picker_2)
        form_layout.setSpacing(25)
        form_layout.setContentsMargins(25, 25, 25, 25)

        # Set layout
        central_widget = QWidget()
        central_widget.setLayout(form_layout)
        self.setCentralWidget(central_widget)

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
