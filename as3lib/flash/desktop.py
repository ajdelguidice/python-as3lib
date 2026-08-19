from __future__ import annotations
from as3lib import (as3state, ArgumentError, Array, each, false, int, null,
                    Number, Object, String, true, Vector)
from as3lib.flash.display import NativeWindow
from as3lib.flash.events import Event, EventDispatcher, InvokeEvent
from as3lib.flash.filesystem import File
from as3lib.helpers import staticproperty
import sys
import tkinter


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
    # TODO: Event.KEY_DOWN
    # TODO: Event.KEY_UP
    # TODO: Event.NETWORK_CHANGE
    # TODO: Event.SUSPEND
    # TODO: Event.USER_IDLE
    # TODO: Event.USER_PRESENT

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

    def _guiInit(self):
        # INTERNAL: Creates the base gui object if it does not yet exist.
        #           ex: tkinter.Tk, QApplication
        if not self._toolkitApplication:
            self._toolkitApplication = tkinter.Tk()
            self._toolkitApplication.withdraw()

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
