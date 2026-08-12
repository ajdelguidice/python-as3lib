from as3lib import (as3state, ArgumentError, Array, each, false, int, null,
                    Object, true)
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
class Clipboard:
    ...


class ClipboardFormats:
    ...


class ClipboardTransferMode:
    ...


class DockIcon:
    ...


class Icon:
    ...


class InteractiveIcon:
    ...


class InvokeEventReason(Object):
    LOGIN = 'login'
    NOTIFICATION = 'notification'
    OPEN_URL = 'openUrl'
    STANDARD = 'standard'


class NativeApplication(EventDispatcher):
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
        raise NotImplementedError

    def exit(self, errorCode: int = 0):
        # TODO: Make sure this is accurate
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
        self.dispatchEvent(InvokeEvent('invoke', false, false, File(as3lib.appdatadirectory), sys.argv, InvokeEventReason.STANDARD))

    def _addWindow(self, id, window):
        # Temporary internal function to add a window to openedWindows
        self._openedWindows[id] = window

    def _removeWindow(self, id):
        del self._openedWindows[id]
        if self.autoExit and not self.openedWindows.length:
            self.exit()


class NativeDragActions:
    ...


class NativeDragManager:
    ...


class NativeDragOptions:
    ...


class NativeProcess:
    ...


class NativeProcessStartupInfo:
    ...


class NotificationType:
    ...


class SystemIdleMode:
    ...


class SystemTrayIcon:
    ...


class Updater:
    ...
