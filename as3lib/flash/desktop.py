from __future__ import annotations
from as3lib import (as3state, ArgumentError, Array, Boolean, false, int, null,
                    Number, Object, String, true, uint, Vector)
from as3lib.flash.display import NativeWindow
from as3lib.flash.events import (Event, EventDispatcher, InvokeEvent,
                                 KeyboardEvent, MouseEvent)
from as3lib.flash.filesystem import File
from as3lib.flash.ui import Keyboard, KeyLocation
from as3lib.helpers import staticproperty
import sys
import tkinter
import platform


class _TOOLKITEVENT:
    def TkGetKeyCode(event):
        # NOTE: Can't easily use keycode here because keycodes are
        #       platform specific. Using keysym, while incorrect for keyboards
        #       that aren't US_QWERTY, is still better than having a different
        #       conversion for each platform.
        # TODO: Make this work on all keyboard types. This will be a lot
        #       easier once tk is no longer used
        keysym_num = event.keysym_num
        if keysym_num == 65288:
            return Keyboard.BACKSPACE
        if keysym_num == 65289:
            return Keyboard.TAB

        if keysym_num == 65293:
            return Keyboard.ENTER
        if False:  # TODO
            return Keyboard.COMMAND
        if keysym_num in {65505, 65506}:
            return Keyboard.SHIFT
        if keysym_num in {65507, 65508}:
            return Keyboard.CONTROL
        if keysym_num in {65513, 65514}:
            return Keyboard.ALTERNATE

        if keysym_num == 65509:
            return Keyboard.CAPS_LOCK
        if False:  # TODO
            return Keyboard.NUMPAD

        if keysym_num == 65307:
            return Keyboard.ESCAPE
        if keysym_num == 32:
            return Keyboard.SPACE
        if keysym_num == 65365:
            return Keyboard.PAGE_UP
        if keysym_num == 65366:
            return Keyboard.PAGE_DOWN
        if keysym_num == 65367:
            return Keyboard.END
        if keysym_num == 65360:
            return Keyboard.HOME
        if keysym_num == 65361:
            return Keyboard.LEFT
        if keysym_num == 65362:
            return Keyboard.UP
        if keysym_num == 65363:
            return Keyboard.RIGHT
        if keysym_num == 65364:
            return Keyboard.DOWN

        if keysym_num == 65379:
            return Keyboard.INSERT
        if keysym_num == 65535:
            return Keyboard.DELETE

        if keysym_num in {41, 48}:  # ), 0
            return Keyboard.NUMBER_0
        if keysym_num in {33, 49}:  # !, 1
            return Keyboard.NUMBER_1
        if keysym_num in {64, 50}:  # @, 2
            return Keyboard.NUMBER_2
        if keysym_num in {35, 51}:  # #, 3
            return Keyboard.NUMBER_3
        if keysym_num in {36, 52}:  # $, 4
            return Keyboard.NUMBER_4
        if keysym_num in {37, 53}:  # %, 5
            return Keyboard.NUMBER_5
        if keysym_num in {94, 54}:  # ^, 6
            return Keyboard.NUMBER_6
        if keysym_num in {38, 55}:  # &, 7
            return Keyboard.NUMBER_7
        if keysym_num in {42, 56}:  # *, 8
            return Keyboard.NUMBER_8
        if keysym_num in {40, 57}:  # (, 9
            return Keyboard.NUMBER_9

        if keysym_num in {65, 97}:
            return Keyboard.A
        if keysym_num in {66, 98}:
            return Keyboard.B
        if keysym_num in {67, 99}:
            return Keyboard.C
        if keysym_num in {68, 100}:
            return Keyboard.D
        if keysym_num in {69, 101}:
            return Keyboard.E
        if keysym_num in {70, 102}:
            return Keyboard.F
        if keysym_num in {71, 103}:
            return Keyboard.G
        if keysym_num in {72, 104}:
            return Keyboard.H
        if keysym_num in {73, 105}:
            return Keyboard.I
        if keysym_num in {74, 106}:
            return Keyboard.J
        if keysym_num in {75, 107}:
            return Keyboard.K
        if keysym_num in {76, 108}:
            return Keyboard.L
        if keysym_num in {77, 109}:
            return Keyboard.M
        if keysym_num in {78, 110}:
            return Keyboard.N
        if keysym_num in {79, 111}:
            return Keyboard.O
        if keysym_num in {80, 112}:
            return Keyboard.P
        if keysym_num in {81, 113}:
            return Keyboard.Q
        if keysym_num in {82, 114}:
            return Keyboard.R
        if keysym_num in {83, 115}:
            return Keyboard.S
        if keysym_num in {84, 116}:
            return Keyboard.T
        if keysym_num in {85, 117}:
            return Keyboard.U
        if keysym_num in {86, 118}:
            return Keyboard.V
        if keysym_num in {87, 119}:
            return Keyboard.W
        if keysym_num in {88, 120}:
            return Keyboard.X
        if keysym_num in {89, 121}:
            return Keyboard.Y
        if keysym_num in {90, 122}:
            return Keyboard.Z

        if keysym_num in {65438, 65456}:
            return Keyboard.NUMPAD_0
        if keysym_num in {65436, 65457}:
            return Keyboard.NUMPAD_1
        if keysym_num in {65433, 65458}:
            return Keyboard.NUMPAD_2
        if keysym_num in {65435, 65459}:
            return Keyboard.NUMPAD_3
        if keysym_num in {65430, 65460}:
            return Keyboard.NUMPAD_4
        if keysym_num in {65437, 65461}:
            return Keyboard.NUMPAD_5
        if keysym_num in {65432, 65462}:
            return Keyboard.NUMPAD_6
        if keysym_num in {65429, 65463}:
            return Keyboard.NUMPAD_7
        if keysym_num in {65431, 65464}:
            return Keyboard.NUMPAD_8
        if keysym_num in {65434, 65465}:
            return Keyboard.NUMPAD_9
        if keysym_num == 65450:
            return Keyboard.NUMPAD_MULTIPLY
        if keysym_num == 65451:
            return Keyboard.NUMPAD_ADD
        if keysym_num == 65421:
            return Keyboard.NUMPAD_ENTER
        if keysym_num == 65453:
            return Keyboard.NUMPAD_SUBTRACT
        if keysym_num in {65454, 65439}:  # ., del
            return Keyboard.NUMPAD_DECIMAL
        if keysym_num == 65455:
            return Keyboard.NUMPAD_DIVIDE

        if keysym_num == 65470:
            return Keyboard.F1
        if keysym_num == 65471:
            return Keyboard.F2
        if keysym_num == 65472:
            return Keyboard.F3
        if keysym_num == 65473:
            return Keyboard.F4
        if keysym_num == 65474:
            return Keyboard.F5
        if keysym_num == 65475:
            return Keyboard.F6
        if keysym_num == 65476:
            return Keyboard.F7
        if keysym_num == 65477:
            return Keyboard.F8
        if keysym_num == 65478:
            return Keyboard.F9
        if keysym_num == 65479:
            return Keyboard.F10
        if keysym_num == 65480:
            return Keyboard.F11
        if keysym_num == 65481:
            return Keyboard.F12
        if False:  # TODO
            return Keyboard.F13
        if False:  # TODO
            return Keyboard.F14
        if False:  # TODO
            return Keyboard.F15

        if keysym_num == 65407:
            return uint(144)

        if keysym_num in {59, 58}:  # ;, :
            return Keyboard.SEMICOLON
        if keysym_num in {61, 43}:  # =, +
            return Keyboard.EQUAL
        if keysym_num in {44, 60}:  # ,, <
            return Keyboard.COMMA
        if keysym_num in {45, 95}:  # -, _
            return Keyboard.MINUS
        if keysym_num in {46, 62}:  # ., >
            return Keyboard.PERIOD
        if keysym_num in {47, 63}:  # /, ?
            return Keyboard.SLASH
        if keysym_num in {96, 126}:  # `, ~
            return Keyboard.BACKQUOTE

        if keysym_num in {91, 123}:  # [, {
            return Keyboard.LEFTBRACKET
        if keysym_num in {92, 124}:  # \, |
            return Keyboard.BACKSLASH
        if keysym_num in {93, 125}:  # ], }
            return Keyboard.RIGHTBRACKET
        if keysym_num in {39, 34}:  # ', "
            return Keyboard.QUOTE

        # TODO
        '''
        RED = uint(0x01000000)
        GREEN = uint(0x01000001)
        YELLOW = uint(0x01000002)
        BLUE = uint(0x01000003)
        CHANNEL_UP = uint(0x01000004)
        CHANNEL_DOWN = uint(0x01000005)
        RECORD = uint(0x01000006)
        PLAY = uint(0x01000007)
        PAUSE = uint(0x01000008)
        STOP = uint(0x01000009)
        FAST_FORWARD = uint(0x0100000A)
        REWIND = uint(0x0100000B)
        SKIP_FORWARD = uint(0x0100000C)
        SKIP_BACKWARD = uint(0x0100000D)
        NEXT = uint(0x0100000E)
        PREVIOUS = uint(0x0100000F)
        LIVE = uint(0x01000010)
        LAST = uint(0x01000011)
        MENU = uint(0x01000012)
        INFO = uint(0x01000013)
        GUIDE = uint(0x01000014)
        EXIT = uint(0x01000015)
        BACK = uint(0x01000016)
        AUDIO = uint(0x01000017)
        SUBTITLE = uint(0x01000018)
        DVR = uint(0x01000019)
        VOD = uint(0x0100001A)
        INPUT = uint(0x0100001B)
        SETUP = uint(0x0100001C)
        HELP = uint(0x0100001D)
        MASTER_SHELL = uint(0x0100001E)
        SEARCH = uint(0x0100001F)
        PLAY_PAUSE = uint(0x01000020)
        '''

        # Unknown keys get 0
        # TODO: Determine what flash player does here
        return 0

    def TkGetKeyboardEvent(event):
        # TODO
        charCode = 0  # TODO

        keyCode = _TOOLKITEVENT.TkGetKeyCode(event)

        keyLocation = KeyLocation.STANDARD  # TODO

        ctrlKey = false  # TODO

        altKey = false  # TODO

        shiftKey = false  # TODO

        controlKey = false  # TODO

        commandKey = false  # TODO

        if event.type == tkinter.EventType.KeyPress:
            return KeyboardEvent(KeyboardEvent.KEY_DOWN, true, true, charCode, keyCode, keyLocation, ctrlKey, altKey, shiftKey, controlKey, commandKey)
        if event.type == tkinter.EventType.KeyRelease:
            return KeyboardEvent(KeyboardEvent.KEY_UP, true, false, charCode, keyCode, keyLocation, ctrlKey, altKey, shiftKey, controlKey, commandKey)

    def MouseButtonToTk(name):
        if platform.system() in {'Linux', 'Windows'}:
            if name == MouseEvent.CLICK:
                return '<Button-1>'
            if name == MouseEvent.MIDDLE_CLICK:
                return '<Button-2>'
            if name == MouseEvent.RIGHT_CLICK:
                return '<Button-3>'
        elif platform.system() == 'Darwin':
            if name == MouseEvent.CLICK:
                return '<Button-1>'
            if name == MouseEvent.MIDDLE_CLICK:
                return '<Button-3>'
            if name == MouseEvent.RIGHT_CLICK:
                return '<Button-2>'

    def TkGetMouseButton(event):
        if platform.system() in {'Linux', 'Windows'}:
            if event.num == 1:
                return MouseEvent.CLICK
            if event.num == 2:
                return MouseEvent.MIDDLE_CLICK
            if event.num == 3:
                return MouseEvent.RIGHT_CLICK
        elif platform.system() == 'Darwin':
            if event.num == 1:
                return MouseEvent.CLICK
            if event.num == 2:
                return MouseEvent.RIGHT_CLICK
            if event.num == 3:
                return MouseEvent.MIDDLE_CLICK

    def TkGetMouseEvent(event):
        raise NotImplementedError

    def QtGetKeyCode(event):
        # TODO: If fully switching to PyQt, use PyQt6.QtCore.Qt.Key enum
        #       and PyQt6.QtCore.Qt.KeyboardModifier enum instead of
        #       hardcoding key values
        isDarwin = as3state.platform == 'Darwin'
        QtKeycode = event.key()
        QtModifiers = event.modifiers()
        shiftPressed = QtModifiers % 0x2000000
        #
        # KeyboardModifer.KeypadModifier
        if QtModifiers & 0x20000000:
            # Key.Key_0, Key.Key_Insert
            if QtKeycode in {48, 16777222}:
                return Keyboard.NUMPAD_0
            # Key.Key_1, Key.Key_End
            if QtKeycode in {49, 16777233}:
                return Keyboard.NUMPAD_1
            # Key.Key_2, Key.Key_Down
            if QtKeycode in {50, 16777237}:
                return Keyboard.NUMPAD_2
            # Key.Key_3, Key.Key_PageDown
            if QtKeycode in {51, 16777239}:
                return Keyboard.NUMPAD_3
            # Key.Key_4, Key.Key_Left
            if QtKeycode in {52, 16777234}:
                return Keyboard.NUMPAD_4
            # Key.Key_5, Key.Key_Clear
            # TODO: Check darwin, check other keyboards
            if QtKeycode in {53, 16777227}:
                return Keyboard.NUMPAD_5
            # Key.Key_6, Key.Key_Right
            if QtKeycode in {54, 16777236}:
                return Keyboard.NUMPAD_6
            # Key.Key_7, Key.Key_Home
            if QtKeycode in {55, 16777232}:
                return Keyboard.NUMPAD_7
            # Key.Key_8, Key.Key_Up
            if QtKeycode in {56, 16777235}:
                return Keyboard.NUMPAD_8
            # Key.Key_9, Key.Key_PageUp
            if QtKeycode in {57, 16777238}:
                return Keyboard.NUMPAD_9
            # Key.Key_Asterisk
            if QtKeycode == 42:
                return Keyboard.NUMPAD_MULTIPLY
            # Key.Key_Plus
            if QtKeycode == 43:
                return Keyboard.NUMPAD_ADD
            # Key.Key_Enter
            if QtKeycode == 16777221:
                return Keyboard.NUMPAD_ENTER
            # Key.Key_Minus
            if QtKeycode == 45:
                return Keyboard.NUMPAD_SUBTRACT
            # Key.Key_Period, Key.Key_Delete
            if QtKeycode in {46, 16777223}:
                return Keyboard.NUMPAD_DECIMAL
            # Key.Key_Slash
            if QtKeycode == 47:
                return Keyboard.NUMPAD_DIVIDE

        # Key.Key_Backspace
        if QtKeycode == 16777219:
            return Keyboard.BACKSPACE
        # Key.Key_Tab
        if QtKeycode == 16777217:
            return Keyboard.TAB

        # Key.Key_Enter
        if QtKeycode == 16777221:
            return Keyboard.ENTER
        # Darwin: Key.Key_Control, TODO: Other platforms
        if isDarwin and QtKeycode == 16777249:
            return Keyboard.COMMAND
        # Key.Key_Shift
        if QtKeycode == 16777248:
            return Keyboard.SHIFT
        # Darwin: Key.Key_Meta, Other: Key.Key_Control
        if isDarwin and QtKeycode == 16777250 or not isDarwin and QtKeycode == 16777249:
            return Keyboard.CONTROL
        # Key.Key_Alt
        if QtKeycode == 16777251:
            return Keyboard.ALTERNATE

        # Key.Key_CapsLock
        if QtKeycode == 16777252:
            return Keyboard.CAPS_LOCK
        # TODO
        if False:
            return Keyboard.NUMPAD

        # Key.Key_Escape
        if QtKeycode == 16777216:
            return Keyboard.ESCAPE
        # Key.Key_Space
        if QtKeycode == 32:
            return Keyboard.SPACE
        # Key.Key_PageUp
        if QtKeycode == 16777238:
            return Keyboard.PAGE_UP
        # Key.Key_PageDown
        if QtKeycode == 16777239:
            return Keyboard.PAGE_DOWN
        # Key.Key_End
        if QtKeycode == 16777233:
            return Keyboard.END
        # Key.Key_Home
        if QtKeycode == 16777232:
            return Keyboard.HOME
        # Key.Key_Left
        if QtKeycode == 16777234:
            return Keyboard.LEFT
        # Key.Key_Up
        if QtKeycode == 16777235:
            return Keyboard.UP
        # Key.Key_Right
        if QtKeycode == 16777236:
            return Keyboard.RIGHT
        # Key.Key_Down
        if QtKeycode == 16777237:
            return Keyboard.DOWN

        # Key.Key_Insert
        if QtKeycode == 16777222:
            return Keyboard.INSERT
        # Key.Key_Delete
        if QtKeycode == 16777223:
            return Keyboard.DELETE

        # Key.Key_0, shiftPressed: Key.Key_ParenRight
        if not shiftPressed and QtKeycode == 48 or shiftPressed and QtKeycode == 41:
            return Keyboard.NUMBER_0
        # Key.Key_1, shiftPressed: Key.Key_Exclam
        if not shiftPressed and QtKeycode == 49 or shiftPressed and QtKeycode == 33:
            return Keyboard.NUMBER_1
        # Key.Key_2, shiftPressed: Key.Key_At
        if not shiftPressed and QtKeycode == 50 or shiftPressed and QtKeycode == 64:
            return Keyboard.NUMBER_2
        # Key.Key_3, shiftPressed: Key.Key_NumberSign
        if not shiftPressed and QtKeycode == 51 or shiftPressed and QtKeycode == 35:
            return Keyboard.NUMBER_3
        # Key.Key_4, shiftPressed: Key.Key_Dollar
        if not shiftPressed and QtKeycode == 52 or shiftPressed and QtKeycode == 36:
            return Keyboard.NUMBER_4
        # Key.Key_5, shiftPressed: Key.Key_Percent
        if not shiftPressed and QtKeycode == 53 or shiftPressed and QtKeycode == 37:
            return Keyboard.NUMBER_5
        # Key.Key_6, shiftPressed: Key.Key_AsciiCircum
        if not shiftPressed and QtKeycode == 54 or shiftPressed and QtKeycode == 94:
            return Keyboard.NUMBER_6
        # Key.Key_7, shiftPressed: Key.Key_Ampersand
        if not shiftPressed and QtKeycode == 55 or shiftPressed and QtKeycode == 38:
            return Keyboard.NUMBER_7
        # Key.Key_8, shiftPressed: Key.Key_Asterisk
        if not shiftPressed and QtKeycode == 56 or shiftPressed and QtKeycode == 42:
            return Keyboard.NUMBER_8
        # Key.Key_9, shiftPressed: Key.Key_ParenLeft
        if not shiftPressed and QtKeycode == 57 or shiftPressed and QtKeycode == 40:
            return Keyboard.NUMBER_9

        # Key.Key_A
        if QtKeycode == 65:
            return Keyboard.A
        # Key.Key_B
        if QtKeycode == 66:
            return Keyboard.B
        # Key.Key_C
        if QtKeycode == 67:
            return Keyboard.C
        # Key.Key_D
        if QtKeycode -- 68:
            return Keyboard.D
        # Key.Key_E
        if QtKeycode == 69:
            return Keyboard.E
        # Key.Key_F
        if QtKeycode == 70:
            return Keyboard.F
        # Key.Key_G
        if QtKeycode == 71:
            return Keyboard.G
        # Key.Key_H
        if QtKeycode == 72:
            return Keyboard.H
        # Key.Key_I
        if QtKeycode == 73:
            return Keyboard.I
        # Key.Key_J
        if QtKeycode == 74:
            return Keyboard.J
        # Key.Key_K
        if QtKeycode == 75:
            return Keyboard.K
        # Key.Key_L
        if QtKeycode == 76:
            return Keyboard.L
        # Key.Key_M
        if QtKeycode == 77:
            return Keyboard.M
        # Key.Key_N
        if QtKeycode == 78:
            return Keyboard.N
        # Key.Key_O
        if QtKeycode == 79:
            return Keyboard.O
        # Key.Key_P
        if QtKeycode == 80:
            return Keyboard.P
        # Key.Key_Q
        if QtKeycode == 81:
            return Keyboard.Q
        # Key.Key_R
        if QtKeycode == 82:
            return Keyboard.R
        # Key.Key_S
        if QtKeycode == 83:
            return Keyboard.S
        # Key.Key_T
        if QtKeycode == 84:
            return Keyboard.T
        # Key.Key_U
        if QtKeycode == 85:
            return Keyboard.U
        # Key.Key_V
        if QtKeycode == 86:
            return Keyboard.V
        # Key.Key_W
        if QtKeycode == 87:
            return Keyboard.W
        # Key.Key_X
        if QtKeycode == 88:
            return Keyboard.X
        # Key.Key_Y
        if QtKeycode == 89:
            return Keyboard.Y
        # Key.Key_Z
        if QtKeycode == 90:
            return Keyboard.Z

        # Key.Key_F1
        if QtKeycode == 16777264:
            return Keyboard.F1
        # Key.Key_F2
        if QtKeycode == 16777265:
            return Keyboard.F2
        # Key.Key_F3
        if QtKeycode == 16777266:
            return Keyboard.F3
        # Key.Key_F4
        if QtKeycode == 16777267:
            return Keyboard.F4
        # Key.Key_F5
        if QtKeycode == 16777268:
            return Keyboard.F5
        # Key.Key_F6
        if QtKeycode == 16777269:
            return Keyboard.F6
        # Key.Key_F7
        if QtKeycode == 16777270:
            return Keyboard.F7
        # Key.Key_F8
        if QtKeycode == 16777271:
            return Keyboard.F8
        # Key.Key_F9
        if QtKeycode == 16777272:
            return Keyboard.F9
        # Key.Key_F10
        if QtKeycode == 16777273:
            return Keyboard.F10
        # Key.Key_F11
        if QtKeycode == 16777274:
            return Keyboard.F11
        # Key.Key_F12
        if QtKeycode == 16777275:
            return Keyboard.F12
        # Key.Key_F13
        if QtKeycode == 16777276:
            return Keyboard.F13
        # Key.Key_F14
        if QtKeycode == 16777277:
            return Keyboard.F14
        # Key.Key_F15
        if QtKeycode == 16777278:
            return Keyboard.F15

        # Key.Key_NumLock
        if QtKeycode == 16777253:
            return uint(144)  # Numlock

        # Key.Key_Semicolon, Key.Key_Colon
        if QtKeycode in {59, 58}:
            return Keyboard.SEMICOLON
        # Key.Key_Equal, Key.Key_Plus
        if QtKeycode in {61, 43}:
            return Keyboard.EQUAL
        # Key.Key_Comma, Key.Key_Less
        if QtKeycode in {44, 60}:
            return Keyboard.COMMA
        # Key.Key_Minus, Key.Key_Underscore
        if QtKeycode in {45, 95}:
            return Keyboard.MINUS
        # Key.Key_Period, Key.Key_Greater
        if QtKeycode in {46, 62}:
            return Keyboard.PERIOD
        # Key.Key_Slash, Key.Key_Question
        if QtKeycode in {47, 63}:
            return Keyboard.SLASH
        # Key.Key_QuoteLeft, Key.Key_AsciiTilde
        if QtKeycode in {96, 126}:
            return Keyboard.BACKQUOTE

        # Key.Key_BracketLeft, Key.Key_BraceLeft
        if QtKeycode in {91, 123}:
            return Keyboard.LEFTBRACKET
        # Key.Key_Backslash, Key.Key_Bar
        if QtKeycode in {92, 124}:
            return Keyboard.BACKSLASH
        # Key.Key_BracketRight, Key.Key_BraceRight
        if QtKeycode in {93, 125}:
            return Keyboard.RIGHTBRACKET
        # Key.Key_Apostraphe, Key.Key_QuoteDbl
        if QtKeycode in {39, 34}:  # ', "
            return Keyboard.QUOTE

        # Key.Key_Red
        if QtKeycode == 0x01000114:
            return Keyboard.RED
        # Key.Key_Green
        if QtKeycode == 0x01000115:
            return Keyboard.GREEN
        # Key.Key_Yellow
        if QtKeycode == 0x01000116:
            return Keyboard.YELLOW
        # Key.Key_Blue
        if QtKeycode == 0x01000117:
            return Keyboard.BLUE
        # Key.Key_ChannelUp
        if QtKeycode == 0x01000118:
            return Keyboard.CHANNEL_UP
        # Key.Key_ChannelDown
        if QtKeycode == 0x01000119:
            return Keyboard.CHANNEL_DOWN
        # Key.Key_MediaRecord
        if QtKeycode == 0x01000084:
            return Keyboard.RECORD
        # TODO: Should this be Key.Key_Play instead?
        # Key.Key_MediaPlay
        if QtKeycode == 0x01000080:
            return Keyboard.PLAY
        # Key.Key_MediaPause
        if QtKeycode == 0x01000085:
            return Keyboard.PAUSE
        # TODO: Should this be Key.Key_Stop instead?
        # Key.Key_MediaStop
        if QtKeycode == 0x01000081:
            return Keyboard.STOP
        # TODO
        # FAST_FORWARD = uint(0x0100000A)
        # REWIND = uint(0x0100000B)
        # SKIP_FORWARD = uint(0x0100000C)
        # SKIP_BACKWARD = uint(0x0100000D)
        # NEXT = uint(0x0100000E)
        # PREVIOUS = uint(0x0100000F)
        # LIVE = uint(0x01000010)
        # LAST = uint(0x01000011)
        # MENU = uint(0x01000012)
        # Key.Key_Info
        if QtKeycode == 0x0100011b:
            return Keyboard.INFO
        # Key.Key_Guide
        if QtKeycode == 0x0100011a:
            return Keyboard.GUIDE
        # Key.Key_Exit
        if QtKeycode == 0x0102000a:
            return Keyboard.EXIT
        # BACK = uint(0x01000016)
        # AUDIO = uint(0x01000017)
        # Key.Key_Subtitle
        if QtKeycode == 0x01000105:
            return Keyboard.SUBTITLE
        # TODO
        # DVR = uint(0x01000019)
        # VOD = uint(0x0100001A)
        # INPUT = uint(0x0100001B)
        # SETUP = uint(0x0100001C)
        # HELP = uint(0x0100001D)
        # MASTER_SHELL = uint(0x0100001E)
        # Key.Key_Search
        if QtKeycode == 0x01000092:
            return Keyboard.SEARCH
        # Key.Key_MediaTogglePlayPause
        if QtKeycode == 0x01000086:
            return Keyboard.PLAY_PAUSE

        # Unknown keys get 0
        # TODO: Determine what flash player does here
        return 0

    def QtGetKeyboardEvent(event):
        QtEventType = event.type()
        QtModifiers = event.modifiers()
        isDarwin = as3state.platform == 'Darwin'

        charCode = 0  # TODO

        keyCode = _TOOLKITEVENT.QtGetKeyCode(event)

        if False:  # TODO
            keyLocation = KeyLocation.LEFT
        elif False:  # TODO
            keyLocation = KeyLocation.RIGHT
        elif QtModifiers & 0x20000000:  # KeyboardModifer.KeypadModifier
            keyLocation = KeyLocation.NUM_PAD
        elif False:  # TODO
            keyLocation = KeyLocation.D_PAD
        else:
            keyLocation = KeyLocation.STANDARD

        if keyCode == 0:
            # TODO
            return

        # Darwin: Ctrl or Command, Other: Ctrl
        if isDarwin:
            # KeyboardModifier.ControlModifier or KeyboardModifier.MetaModifier
            ctrlKey = Boolean(QtModifiers & 67108864) or Boolean(QtModifiers & 268435456)
        else:
            # KeyboardModifier.ControlModifier
            ctrlKey = Boolean(QtModifiers & 67108864)

        # Not Darwin: Alt
        if isDarwin:
            altKey = false
        else:
            altKey = Boolean(QtModifiers & 134217728)  # KeyboardModifier.AltModifier

        shiftKey = Boolean(QtModifiers & 33554432)  # KeyboardModifier.ShiftModifier

        if isDarwin:
            controlKey = Boolean(QtModifiers & 268435456)  # KeyboardModifier.MetaModifier
        else:
            controlKey = Boolean(QtModifiers & 67108864)  # KeyboardModifier.ControlModifier

        # Darwin only: Command
        if isDarwin:
            commandKey = Boolean(QtModifiers & 67108864)  # KeyboardModifier.ControlModifier
        else:
            commandKey = false

        if QtEventType == 6:
            return KeyboardEvent(KeyboardEvent.KEY_DOWN, true, true, charCode, keyCode, keyLocation, ctrlKey, altKey, shiftKey, controlKey, commandKey)
        if QtEventType == 7:
            return KeyboardEvent(KeyboardEvent.KEY_UP, true, false, charCode, keyCode, keyLocation, ctrlKey, altKey, shiftKey, controlKey, commandKey)

    def QtGetMouseEvent(event):
        raise NotImplementedError


# Interfaces
class IFilePromise:
    ...


# Classes
class Clipboard(Object):
    ...


class ClipboardFormats(Object):
    BITMAP_FORMAT = String('air:bitmap')
    FILE_LIST_FORMAT = String('air:file list')
    FILE_PROMISE_LIST_FORMAT = String('air:file promise list')
    HTML_FORMAT = String('air:html')
    RICH_TEXT_FORMAT = String('air:rtf')
    TEXT_FORMAT = String('air:text')
    URL_FORMAT = String('air:url')


class ClipboardTransferMode(Object):
    CLONE_ONLY = String('cloneOnly')
    CLONE_PREFERRED = String('clonePreferred')
    ORIGINAL_ONLY = String('originalOnly')
    ORIGINAL_PREFERRED = String('originalPreferred')


class Icon(EventDispatcher):
    ...


class InteractiveIcon(Icon):
    ...


class DockIcon(InteractiveIcon):
    ...


class InvokeEventReason(Object):
    LOGIN = String('login')
    NOTIFICATION = String('notification')
    OPEN_URL = String('openUrl')
    STANDARD = String('standard')


class _as3lib_AboutWindow:
    @property
    def isOpen(self):
        return self._isOpen

    def __init__(self):
        self._isOpen = False

    def open(self, *e):
        if self._isOpen:
            self.toplevel.lift()
            return

        self.toplevel = tkinter.Toplevel()
        self.toplevel.geometry('350x155')
        self.toplevel.resizable(False, False)
        self.toplevel.transient(as3state.nativeApplication._toolkitApplication)
        self.toplevel.bind('<Destroy>', self._close)
        self.label = tkinter.Label(self.toplevel, font=('TkTextFont', 9), anchor='w', justify='left', text=f'as3lib version: {as3state.__version__}\nReported flash version: {as3state.flashVersion}\nDebug mode: {as3state.as3DebugEnable}')
        self.label.place(x=7, y=9, anchor='nw')
        self.okButton = tkinter.Button(self.toplevel, text='OK', command=self.close)
        self.okButton.place(x=299, y=115, width=29, height=29, anchor='nw')
        self._isOpen = True

    def _close(self, *e):
        self._isOpen = False

    def close(self, *e):
        if self._isOpen:
            self.toplevel.destroy()
        self._close()


class NativeApplication(EventDispatcher):
    # TODO: Event.ACTIVATE
    # TODO: Event.EXITING
    # TODO: Event.INVOKE
    # TODO: Event.NETWORK_CHANGE
    # TODO: Event.SUSPEND
    # TODO: Event.USER_IDLE
    # TODO: Event.USER_PRESENT

    # These events seem to originate from the NativeApplication and then make
    # their way down to other things.
    # TODO: Event.KEY_DOWN
    # TODO: Event.KEY_UP

    @property
    def activeWindow(self):
        raise NotImplementedError

    @property
    def applicationDescription(self):
        raise NotImplementedError

    @property
    def applicationID(self):
        raise NotImplementedError

    @property
    def autoExit(self):
        return self._autoExit

    @autoExit.setter
    def autoExit(self, value):
        self._autoExit = Boolean(value)

    @property
    def executeInBackground(self):
        return self._execInBackground

    @executeInBackground.setter
    def executeInBackground(self, value):
        raise NotImplementedError

    @property
    def icon(self):
        raise NotImplementedError

    @property
    def idleThreshold(self):
        return self._idleThreshold

    @idleThreshold.setter
    def idleThreshold(self, value):
        # TODO: Type coersion
        value = int(value)
        if value < 5 or value > 86400:
            raise ArgumentError('value must be between 5 and 86400 (inclusive).')
        self._idleThreshold = value

    @property
    def isCompiledAOT(self):
        # Only returns true on iOS
        return false

    @property
    def menu(self):
        raise NotImplementedError

    @menu.setter
    def menu(self, value):
        raise NotImplementedError

    @staticproperty
    def nativeApplication(cls):
        return as3state.nativeApplication

    @property
    def openedWindows(self):
        return Array(*self._openedWindows.values())

    @property
    def publisherID(self):
        raise NotImplementedError

    @property
    def runtimePatchLevel(self):
        raise NotImplementedError

    @property
    def runtimeVersion(self):
        raise NotImplementedError

    @property
    def startAtLogin(self):
        raise NotImplementedError

    @startAtLogin.setter
    def startAtLogin(self, value):
        raise NotImplementedError

    @property
    def supportsDefaultApplication(self):
        raise NotImplementedError

    @property
    def supportsDockIcon(self):
        raise NotImplementedError

    @property
    def supportsMenu(self):
        raise NotImplementedError

    @property
    def supportsStartAtLogin(self):
        raise NotImplementedError

    @property
    def supportsSystemTrayIcon(self):
        raise NotImplementedError

    @property
    def systemIdleMode(self):
        raise NotImplementedError

    @systemIdleMode.setter
    def systemIdleMode(self, value):
        raise NotImplementedError

    @property
    def timeSinceLastUserInput(self):
        raise NotImplementedError

    def __new__(cls):
        # This class is a singleton
        if as3state.nativeApplication is None:
            return super().__new__(cls)
        # TODO: Ensure that raising is the right thing to do
        raise

    def __init__(self):
        super().__init__()
        self._autoExit = true
        self._execInBackground = false
        self._idleThreshold = int(300)

        # Using a dictionary is fine here because the public property is
        # readonly
        self._openedWindows = {}

        self._timeSinceUserInput = int(0)

        self._toolkitApplication = None
        self._aboutwindow = _as3lib_AboutWindow()

    def activate(self, window=null):
        raise NotImplementedError

    def addEventListener(type, listener, useCapture=False, priority=0, useWeakReference=False):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError

    def cut(self):
        raise NotImplementedError

    def dispatchEvent(self, event):
        # TODO: This is overriden. Figure out what it does differently
        super().dispatchEvent(event)

    def exit(self, errorCode: int = 0):
        # TODO: Make sure this is accurate
        # TODO: Allow finishing current events before executing this one
        # NOTE: This will not work properly until everything is using NativeWindow
        exitPrevented = false
        for i in self._openedWindows.values():
            if not isinstance(i, NativeWindow):
                # Skip this for non NativeWindow windows (ex: interface_tk.itk_window)
                continue

            e = Event(Event.CLOSING, false, true)
            i.dispatch(e)
            if e.isDefaultPrevented():
                exitPrevented = true
                break
        if not exitPrevented:
            for i in self._openedWindows.copy().values():
                i.close()

        self._toolkitApplication.destroy()
        sys.exit(int(errorCode))

    def getDefaultApplication(self, extension):
        raise NotImplementedError

    def isSetAsDefaultApplication(self, extension):
        # TODO: Stub
        return false

    def paste(self):
        raise NotImplementedError

    def removeAsDefaultApplication(self, extension):
        raise NotImplementedError

    def removeEventListener(self, type, listener, useCapture=False):
        raise NotImplementedError

    def selectAll(self):
        raise NotImplementedError

    def setAsDefaultApplication(self, extension):
        raise NotImplementedError

    def _temp_handle_keys(self, event):
        print(_TOOLKITEVENT.TkGetKeyCode(event))

    def _guiInit(self):
        # INTERNAL: Creates the base gui object if it does not yet exist.
        #           ex: tkinter.Tk, QApplication
        if not self._toolkitApplication:
            self._toolkitApplication = tkinter.Tk()
            self._toolkitApplication.withdraw()
            # self._toolkitApplication.bind_all('<KeyPress>', self._temp_handle_keys)

    def _invokeApplication(self):
        # TODO: do this when application starts
        self.dispatchEvent(InvokeEvent(Event.INVOKE, false, false, File(as3state.appdatadirectory), sys.argv, InvokeEventReason.STANDARD))

    def _addWindow(self, id, window):
        # Temporary internal function to add a window to openedWindows
        self._openedWindows[id] = window

    def _removeWindow(self, id):
        del self._openedWindows[id]
        if self.autoExit and not self.openedWindows.length:
            e = Event(Event.EXITING, false, true)
            self.dispatchEvent(e)

            # Canceling this event prevents the application from closing
            if not e.isDefaultPrevented():
                self.exit()


class NativeDragActions(Object):
    COPY = String('copy')
    LINK = String('link')
    MOVE = String('move')
    NONE = String('none')


class NativeDragManager(Object):
    ...


class NativeDragOptions(Object):
    ...


class NativeProcess(EventDispatcher):
    @staticproperty
    def isSupported(self):
        raise NotImplementedError

    @property
    def running(self):
        raise NotImplementedError

    @property
    def standardError(self):
        raise NotImplementedError

    @property
    def standardInput(self):
        raise NotImplementedError

    @property
    def standardOutput(self):
        raise NotImplementedError

    def __init__(self):
        raise NotImplementedError

    def closeInput(self):
        raise NotImplementedError

    def exit(self, force: Boolean = false):
        raise NotImplementedError

    def start(self, info: NativeProcessStartupInfo):
        raise NotImplementedError


class NativeProcessStartupInfo(Object):
    @property
    def arguments(self):
        return self._arguments

    @arguments.setter
    def arguments(self, value):
        self._arguments = Vector[String](value)

    @property
    def executable(self):
        return self._executable

    @executable.setter
    def executable(self, value):
        if value is null:
            raise ArgumentError
        if not isinstance(value, File):
            value = File(value)
        if value.isDirectory or not value.exists:
            raise ArgumentError
        self._executable = value

    @property
    def workingDirectory(self):
        return self._workingDirectory

    @workingDirectory.setter
    def workingDirectory(self, value):
        if not isinstance(value, File):
            value = File(value)
        if not (value.isDirectory and value.exists):
            raise ArgumentError
        self._workingDirectory = value

    def __init__(self):
        self._arguments = null
        self._executable = null
        self._workingDirectory = null


class NotificationType(Object):
    CRITICAL = String('critical')
    INFORMATION = String('information')


class SystemIdleMode(Object):
    KEEP_AWAKE = String('keepAwake')
    NORMAL = String('normal')


class SystemTrayIcon(InteractiveIcon):
    MAX_TIP_LENGTH = Number(63)
    ...


class Updater(Object):
    ...
