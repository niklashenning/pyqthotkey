import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QPushButton
from src.hotkey_picker import HotkeyPicker


class Window(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)

        # Define variables to store selected hotkeys in
        self.selected_hotkey_1 = 0
        self.selected_hotkey_1_name = ''
        self.selected_hotkey_2 = 0
        self.selected_hotkey_2_name = ''
        self.selected_hotkey_3 = 0
        self.selected_hotkey_3_name = ''

        # Needed for window drag functionality
        self.offset = None

        # Frameless transparent window
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(360, 190)

        # Widget as window so everything can be customized
        self.window = QWidget(self)
        self.window.setFixedSize(360, 190)
        self.window.setObjectName('window')

        # Window title bar
        self.window_bar = QWidget(self)
        self.window_bar.setFixedSize(360, 32)
        self.window_bar.move(0, 1)
        self.window_bar.setObjectName('window_bar')

        # Window title
        self.window_title = QLabel(self)
        self.window_title.setText('Hotkey Picker Demo')
        self.window_title.setFixedSize(150, 20)
        self.window_title.move(125, 6)  # Using fixed position for simplicity
        self.window_title.setObjectName('window_title')

        # Close button
        self.close_button = QPushButton(self)
        self.close_button.setText('✕')
        self.close_button.setFixedSize(23, 23)
        self.close_button.move(331, 5)
        self.close_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_button.setObjectName('close_button')
        self.close_button.clicked.connect(self.close_button_pressed)

        # Labels for hotkey pickers
        self.label_1 = QLabel(self)
        self.label_1.setText('Hotkey 1:')
        self.label_1.move(70, 55)
        self.label_1.setObjectName('label_1')

        self.label_2 = QLabel(self)
        self.label_2.setText('Hotkey 2:')
        self.label_2.move(70, 95)
        self.label_2.setObjectName('label_2')

        self.label_3 = QLabel(self)
        self.label_3.setText('Hotkey 3:')
        self.label_3.move(70, 135)
        self.label_3.setObjectName('label_3')

        # F1-F12 keys
        f_keys = [Qt.Key_F1, Qt.Key_F2, Qt.Key_F3, Qt.Key_F4, Qt.Key_F5, Qt.Key_F6,
                  Qt.Key_F7, Qt.Key_F8, Qt.Key_F9, Qt.Key_F10, Qt.Key_F11, Qt.Key_F12]

        # First hotkey picker (custom text when in selection and custom cancel key)
        self.hotkey_picker_1 = HotkeyPicker(self, selecting_text='Selecting..', cancel_key=Qt.Key_Return)
        self.hotkey_picker_1.setFixedWidth(140)
        self.hotkey_picker_1.move(150, 55)
        self.hotkey_picker_1.setObjectName('hotkey_picker_1')
        self.hotkey_picker_1.hotkey_changed.connect(self.hotkey_picker_1_changed)
        self.hotkey_picker_1.set_hotkey(Qt.Key_F5)

        # Second hotkey picker (only F1-F12 can be picked)
        self.hotkey_picker_2 = HotkeyPicker(self, filter_keys=True, forbidden_keys=f_keys)
        self.hotkey_picker_2.setFixedWidth(140)
        self.hotkey_picker_2.move(150, 95)
        self.hotkey_picker_2.setObjectName('hotkey_picker_2')
        self.hotkey_picker_2.hotkey_changed.connect(self.hotkey_picker_2_changed)

        # Third hotkey picker (everything except for F1-F12 keys can be picked)
        self.hotkey_picker_3 = HotkeyPicker(self, default_text='Not selected..',
                                            filter_keys=True, allowed_keys=f_keys)
        self.hotkey_picker_3.setFixedWidth(140)
        self.hotkey_picker_3.move(150, 135)
        self.hotkey_picker_3.setObjectName('hotkey_picker_3')
        self.hotkey_picker_3.hotkey_changed.connect(self.hotkey_picker_3_changed)

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

    def hotkey_picker_3_changed(self, key, key_name):
        # Handle change of hotkey 3
        self.selected_hotkey_3 = key
        self.selected_hotkey_3_name = key_name
        print([key, key_name])

    def keyPressEvent(self, event):
        # React to a selected hotkey being pressed
        if event.key() == self.selected_hotkey_1:
            print('Selected hotkey 1 (' + self.selected_hotkey_1_name + ') has been pressed')
        if event.key() == self.selected_hotkey_2:
            print('Selected hotkey 2 (' + self.selected_hotkey_2_name + ') has been pressed')
        if event.key() == self.selected_hotkey_3:
            print('Selected hotkey 3 (' + self.selected_hotkey_3_name + ') has been pressed')

    def close_button_pressed(self):
        # Exit application on close button press
        sys.exit()

    def mousePressEvent(self, event):
        # Window drag functionality
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # Window drag functionality
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # Window drag functionality
        self.offset = None
        super().mouseReleaseEvent(event)
