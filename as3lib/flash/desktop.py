from as3lib import (as3state, ArgumentError, Array, false, int, metaclasses,
                    null, true)
from as3lib.flash.events import EventDispatcher, InvokeEvent
import tkinter


# Interfaces
class IFilePromise:...


# Classes
class Clipboard:...
class ClipboardFormats:...
class ClipboardTransferMode:...
class DockIcon:...
class Icon:...
class InteractiveIcon:...
class InvokeEventReason(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
    LOGIN = 'login'
    NOTIFICATION = 'notification'
    OPEN_URL = 'openUrl'
    STANDARD = 'standard'


class NativeApplication(EventDispatcher):
    # TODO: dispatch InvokeEvent when application starts
    #       InvokeEvent('invoke', false, false, <directory>, sys.argv)
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
        raise NotImplementedError

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

    @property
    def nativeApplication(self=None):  # TODO: Make static
        return as3state.nativeApplication

    @property
    def openedWindows(self):
        return self._openedWindows

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
        # According to the documentation, this class is not supposed to be
        # instantiated. Instead, NativeApplication.nativeApplication is used to
        # retrieve the global NativeApplication instance
        # TODO: Ensure that raising is the right thing to do
        raise

    def __init__(self):
        super().__init__()
        self._autoExit = true
        self._execInBackground = false
        self._idleThreshold = int(300)
        self._openedWindows = Array()
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

    def exit(self):
        raise NotImplementedError

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

    def _close(self):
        # INTERNAL: closes the toolkit main object
        self._toolkitApplication.destroy()


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
