from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QFocusEvent
from PyQt6.QtTest import QTest
from pytestqt.qt_compat import qt_api
from src.pyqthotkey import HotkeyPicker


def test_initial_values(qtbot):
    """Test initial values of the hotkey picker"""

    hotkey_picker = HotkeyPicker()
    qtbot.addWidget(hotkey_picker)

    assert hotkey_picker.getHotkey() is None
    assert hotkey_picker.getHotkeyString() is None
    assert hotkey_picker.getDefaultText() == 'None'
    assert hotkey_picker.getSelectionText() == '..'
    assert hotkey_picker.getCancelKey() == Qt.Key.Key_Escape
    assert hotkey_picker.isKeyFilterEnabled() == False
    assert hotkey_picker.getWhitelistedKeys() == []
    assert hotkey_picker.getBlacklistedKeys() == []


def test_set_hotkey(qtbot):
    """Test setting the selected hotkey of the hotkey picker"""

    hotkey_picker = HotkeyPicker()
    qtbot.addWidget(hotkey_picker)

    # Test setting hotkey without filter
    hotkey_picker.setHotkey(Qt.Key.Key_F8)
    assert hotkey_picker.getHotkey() == Qt.Key.Key_F8
    hotkey_picker.setHotkey(-1)
    assert hotkey_picker.getHotkey() == Qt.Key.Key_F8

    # Test setting hotkey with custom whitelisted keys
    hotkey_picker.setKeyFilterEnabled(True)
    hotkey_picker.setWhitelistedKeys([Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Control])
    hotkey_picker.setHotkey(Qt.Key.Key_A)
    assert hotkey_picker.getHotkey() == Qt.Key.Key_F8
    hotkey_picker.setHotkey(Qt.Key.Key_Control)
    assert hotkey_picker.getHotkey() == Qt.Key.Key_Control

    # Test setting hotkey with blacklisted keys
    hotkey_picker.setBlacklistedKeys([Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Control])
    hotkey_picker.setHotkey(Qt.Key.Key_A)
    assert hotkey_picker.getHotkey() == Qt.Key.Key_A
    hotkey_picker.setHotkey(Qt.Key.Key_Control)
    assert hotkey_picker.getHotkey() == Qt.Key.Key_A


def test_reset(qtbot):
    """Test resetting the hotkey picker"""

    hotkey_picker = HotkeyPicker()
    qtbot.addWidget(hotkey_picker)

    hotkey_picker.setHotkey(Qt.Key.Key_F5)
    hotkey_picker.reset()
    assert hotkey_picker.getHotkey() is None


def test_set_default_text(qtbot):
    """Test setting the default text of the hotkey picker"""

    hotkey_picker = HotkeyPicker()
    qtbot.addWidget(hotkey_picker)

    hotkey_picker.setDefaultText('nothing')
    assert hotkey_picker.getDefaultText() == 'nothing'
    assert hotkey_picker.text() == 'nothing'


def test_set_selection_text(qtbot):
    """Test setting the selection text of the hotkey picker"""

    hotkey_picker = HotkeyPicker()
    qtbot.addWidget(hotkey_picker)

    hotkey_picker.setSelectionText('selecting..')
    assert hotkey_picker.getSelectionText() == 'selecting..'

    qt_api.QtWidgets.QApplication.sendEvent(hotkey_picker, QFocusEvent(QEvent.Type.FocusIn))
    assert hotkey_picker.text() == 'selecting..'

    hotkey_picker.setSelectionText('press key..')
    assert hotkey_picker.text() == 'press key..'

    qt_api.QtWidgets.QApplication.sendEvent(hotkey_picker, QFocusEvent(QEvent.Type.FocusOut))
    assert hotkey_picker.text() == hotkey_picker.getDefaultText()


def test_set_cancel_key(qtbot):
    """Test setting the cancel key of the hotkey picker"""

    hotkey_picker = HotkeyPicker()
    qtbot.addWidget(hotkey_picker)

    hotkey_picker.setCancelKey(Qt.Key.Key_Return)
    assert hotkey_picker.getCancelKey() == Qt.Key.Key_Return

    qt_api.QtWidgets.QApplication.sendEvent(hotkey_picker, QFocusEvent(QEvent.Type.FocusIn))
    assert hotkey_picker.text() == hotkey_picker.getSelectionText()

    QTest.keyEvent(QTest.KeyAction.Click, hotkey_picker, Qt.Key.Key_Return)
    assert hotkey_picker.text() == hotkey_picker.getDefaultText()


def test_key_event(qtbot):
    """Test a key event on the hotkey picker"""

    hotkey_picker = HotkeyPicker()
    qtbot.addWidget(hotkey_picker)

    QTest.keyEvent(QTest.KeyAction.Click, hotkey_picker, Qt.Key.Key_F8)
    assert hotkey_picker.getHotkey() == Qt.Key.Key_F8


def test_key_filter_whitelist(qtbot):
    """Test the hotkey picker with a key filter
     and whitelist enabled"""

    hotkey_picker = HotkeyPicker(key_filter_enabled=True,
                                 whitelisted_keys=[Qt.Key.Key_F1, Qt.Key.Key_F2, Qt.Key.Key_F3])
    qtbot.addWidget(hotkey_picker)

    QTest.keyEvent(QTest.KeyAction.Click, hotkey_picker, Qt.Key.Key_F8)
    assert hotkey_picker.getHotkey() is None

    QTest.keyEvent(QTest.KeyAction.Click, hotkey_picker, Qt.Key.Key_F2)
    assert hotkey_picker.getHotkey() == Qt.Key.Key_F2


def test_key_filter_blacklist(qtbot):
    """Test the hotkey picker with a key filter
     and blacklist enabled"""

    hotkey_picker = HotkeyPicker(key_filter_enabled=True,
                                 blacklisted_keys=[Qt.Key.Key_F1, Qt.Key.Key_F2, Qt.Key.Key_F3])
    qtbot.addWidget(hotkey_picker)

    QTest.keyEvent(QTest.KeyAction.Click, hotkey_picker, Qt.Key.Key_F8)
    assert hotkey_picker.getHotkey() == Qt.Key.Key_F8

    QTest.keyEvent(QTest.KeyAction.Click, hotkey_picker, Qt.Key.Key_F2)
    assert hotkey_picker.getHotkey() == Qt.Key.Key_F8


def test_key_filter_both(qtbot):
    """Test the hotkey picker with a key filter enabled
     and both a key whitelist and a key blacklist passed"""

    hotkey_picker = HotkeyPicker(key_filter_enabled=True,
                                 whitelisted_keys=[Qt.Key.Key_F1, Qt.Key.Key_F2, Qt.Key.Key_F3],
                                 blacklisted_keys=[Qt.Key.Key_F4, Qt.Key.Key_F5, Qt.Key.Key_F6])
    qtbot.addWidget(hotkey_picker)

    # Test setting both whitelisted keys and blacklisted keys in constructor
    assert hotkey_picker.getWhitelistedKeys() == [Qt.Key.Key_F1, Qt.Key.Key_F2, Qt.Key.Key_F3]
    assert hotkey_picker.getBlacklistedKeys() == []

    # Test setting blacklisted keys while whitelisted keys are already set
    hotkey_picker.setBlacklistedKeys([Qt.Key.Key_A, Qt.Key.Key_B, Qt.Key.Key_C])
    assert hotkey_picker.getWhitelistedKeys() == []
    assert hotkey_picker.getBlacklistedKeys() == [Qt.Key.Key_A, Qt.Key.Key_B, Qt.Key.Key_C]

    # Test setting whitelisted keys while blacklisted keys are already set
    hotkey_picker.setWhitelistedKeys([Qt.Key.Key_D, Qt.Key.Key_E, Qt.Key.Key_F])
    assert hotkey_picker.getWhitelistedKeys() == [Qt.Key.Key_D, Qt.Key.Key_E, Qt.Key.Key_F]
    assert hotkey_picker.getBlacklistedKeys() == []


def test_focus_out_with_selected_key(qtbot):
    """Test a focus out event while in selection
     and a key selected before"""

    hotkey_picker = HotkeyPicker()
    qtbot.addWidget(hotkey_picker)

    hotkey_picker.setHotkey(Qt.Key.Key_F3)
    qt_api.QtWidgets.QApplication.sendEvent(hotkey_picker, QFocusEvent(QEvent.Type.FocusIn))
    assert hotkey_picker.text() == hotkey_picker.getSelectionText()

    qt_api.QtWidgets.QApplication.sendEvent(hotkey_picker, QFocusEvent(QEvent.Type.FocusOut))
    assert hotkey_picker.text() == 'F3'


def test_key_to_string(qtbot):
    """Test the static keyToString() method"""

    assert HotkeyPicker.keyToString(Qt.Key.Key_A) == 'A'
    assert HotkeyPicker.keyToString(65) == 'A'
    assert HotkeyPicker.keyToString(Qt.Key.Key_Escape) == 'Escape'
    assert HotkeyPicker.keyToString(Qt.Key.Key_Control) == 'Control'
    assert HotkeyPicker.keyToString(Qt.Key.Key_F12) == 'F12'
    assert HotkeyPicker.keyToString(-1) is None


def test_set_key_name(qtbot):
    """Test the static setKeyName() method"""

    HotkeyPicker.setKeyName(Qt.Key.Key_Control, 'Ctrl custom name')
    hotkey_picker = HotkeyPicker()
    qtbot.addWidget(hotkey_picker)

    QTest.keyEvent(QTest.KeyAction.Click, hotkey_picker, Qt.Key.Key_Control)
    assert hotkey_picker.getHotkeyString() == 'Ctrl custom name'
