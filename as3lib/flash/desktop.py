from __future__ import annotations
from as3lib import (as3state, ArgumentError, Array, each, false, int, null,
                    Number, Object, String, true, uint, Vector)
from as3lib.flash.display import NativeWindow
from as3lib.flash.events import Event, EventDispatcher, InvokeEvent
from as3lib.flash.filesystem import File
from as3lib.flash.ui import Keyboard
from as3lib.helpers import staticproperty
import sys
import tkinter


class _TOOLKITEVENT:
    def TKGetKeyCode(event):
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
        return Array(*list(each(self._openedWindows)))

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
        for i in each(self._openedWindows):
            if not isinstance(i, NativeWindow):
                # Skip this for non NativeWindow windows (ex: interface_tk.itk_window)
                continue

            e = Event(Event.CLOSING, false, true)
            i.dispatch(e)
            if e.isDefaultPrevented():
                exitPrevented = true
                break
        if not exitPrevented:
            for i in each(self._openedWindows.copy()):
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

    def _TOOLKITHANDLER_keyDown(self, event):
        # TODO: Bind function to toolkit key_down event
        # TODO: Convert toolkit key_down event into flash key_down event
        # TODO: Fill in the placeholder values
        # NOTE: cancelable in AIR but not in flash player
        keyCode = _TOOLKITEVENT.TKGetKeyCode(event)
        self.dispatchEvent(KeyboardEvent('keyDown', true, true, 'charCode', keyCode, 'keyLocation', 'ctrlKey', 'altKey', 'shiftKey', 'controlKey', 'commandKey'))

    def _TOOLKITHANDLER_keyUp(self, event):
        # TODO: Bind function to toolkit key_up event
        # TODO: Convert toolkit key_up event into flash key_up event
        # TODO: Fill in the placeholder values
        keyCode = _TOOLKITEVENT.TKGetKeyCode(event)
        self.dispatchEvent(KeyboardEvent('keyUp', true, false, 'charCode', keyCode, 'keyLocation', 'ctrlKey', 'altKey', 'shiftKey', 'controlKey', 'commandKey'))

    def _temp_handle_keys(self, event):
        print(_TOOLKITEVENT.TKGetKeyCode(event))

    def _guiInit(self):
        # INTERNAL: Creates the base gui object if it does not yet exist.
        #           ex: tkinter.Tk, QApplication
        if not self._toolkitApplication:
            self._toolkitApplication = tkinter.Tk()
            self._toolkitApplication.withdraw()
            #self._toolkitApplication.bind_all('<KeyPress>', self._temp_handle_keys)

    def _invokeApplication(self):
        # TODO: do this when application starts
        self.dispatchEvent(InvokeEvent(Event.INVOKE, false, false, File(as3lib.appdatadirectory), sys.argv, InvokeEventReason.STANDARD))

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
