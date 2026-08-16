from as3lib import as3state, false, int, Number, Object, String, true
from as3lib.helpers import staticproperty
from as3lib.flash.events import EventDispatcher
from functools import cache
import platform
import sys


class ApplicationDomain(Object):
    ...


class Capabilities(Object):
    # TODO: get actual values
    # TODO: document changes from original

    @staticproperty
    def avHardwareDisable(cls):
        # This is not needed so it is always True
        return true

    @staticproperty
    @cache
    def cpuAddressSize(cls):
        # returns 32 (32bit system) or 64 (64bit system)
        return Number(platform.architecture()[0][:-3])

    @staticproperty
    @cache
    def cpuArchitecture(cls):
        # returns 'PowerPC','x86','SPARC', or 'ARM'
        if platform.machine() in {'x86', 'x86_64', 'AMD64'}:
            return String('x86')
        if platform.machine() == 'PowerPC':
            return String('PowerPC')
        if platform.machine() in {'ARM', 'ARM64'}:
            return String('ARM')

    @staticproperty
    def hasAccessibility(cls):
        return false  # TODO: Placeholder

    @staticproperty
    def hasAudio(cls):
        raise NotImplementedError

    @staticproperty
    def hasAudioEncoder(cls):
        raise NotImplementedError

    @staticproperty
    def hasEmbeddedVideo(cls):
        raise NotImplementedError

    @staticproperty
    def hasIME(cls):
        raise NotImplementedError

    @staticproperty
    def hasMP3(cls):
        raise NotImplementedError

    @staticproperty
    def hasPrinting(cls):
        raise NotImplementedError

    @staticproperty
    def hasScreenBroadcast(cls):
        raise NotImplementedError

    @staticproperty
    def hasScreenPlayback(cls):
        raise NotImplementedError

    @staticproperty
    def hasStreamingAudio(cls):
        raise NotImplementedError

    @staticproperty
    def hasStreamingVideo(cls):
        raise NotImplementedError

    @staticproperty
    def hasTLS(cls):
        raise NotImplementedError

    @staticproperty
    def hasVideoEncoder(cls):
        raise NotImplementedError

    @staticproperty
    def isDebugger(cls):
        return as3state.as3DebugEnable

    @staticproperty
    def isEmbeddedInAcrobat(cls):
        # Always false because this is irelavant
        return false

    @staticproperty
    def language(cls):
        raise NotImplementedError

    @staticproperty
    def languages(cls):
        raise NotImplementedError

    @staticproperty
    def localFileReadDisable(cls):
        raise NotImplementedError

    @staticproperty
    @cache
    def manufacturer(cls):
        if as3state.platform == 'Windows':
            return String('Adobe Windows')
        if as3state.platform == 'Linux':
            return String('Adobe Linux')
        if as3state.platform == 'Darwin':
            return String('Adobe Macintosh')

    @staticproperty
    def maxLevelIDC(cls):
        raise NotImplementedError

    @staticproperty
    @cache
    def os(cls):
        # TODO: add others
        if as3state.platform == 'Windows':
            raise NotImplementedError
        if as3state.platform == 'Linux':
            return String(f'Linux {platform.release()}')
        if as3state.platform == 'Darwin':
            raise NotImplementedError

    @staticproperty
    def pixelAspectRatio(cls):
        raise NotImplementedError

    @staticproperty
    def playerType(cls):
        return String('StandAlone')

    @staticproperty
    def screenColor(cls):
        raise NotImplementedError

    @staticproperty
    def screenDPI(cls):
        raise NotImplementedError

    @staticproperty
    def screenResolutionX(cls):
        # Initial width of the display frame
        return Number(as3state.viewportWidth)

    @staticproperty
    def screenResolutionY(cls):
        # Initial height of the display frame
        return Number(as3state.viewportHeight)

    @staticproperty
    def serverString(cls):
        raise NotImplementedError

    @staticproperty
    def supports32BitProcesses(cls):
        raise NotImplementedError

    @staticproperty
    def supports64BitProcesses(cls):
        raise NotImplementedError

    @staticproperty
    def touchscreenType(cls):
        raise NotImplementedError

    @staticproperty
    @cache
    def version(cls):
        tempfv = as3state.flashVersion
        if as3state.platform == 'Windows':
            return String(f'Win {tempfv[0]},{tempfv[1]},{tempfv[2]},{tempfv[3]}')
        if as3state.platform == 'Linux':
            return String(f'LNX {tempfv[0]},{tempfv[1]},{tempfv[2]},{tempfv[3]}')
        if as3state.platform == 'Darwin':
            return String(f'MAC {tempfv[0]},{tempfv[1]},{tempfv[2]},{tempfv[3]}')
        if as3state.platform == 'Android':
            return String(f'AND {tempfv[0]},{tempfv[1]},{tempfv[2]},{tempfv[3]}')

    @staticmethod
    def hasMultiChannelAudio(type: str):
        raise NotImplementedError


def fscommand(command, args=''):
    raise NotImplementedError


class ImageDecodingPolicy(Object):
    ON_DEMAND = String('onDemand')
    ON_LOAD = String('onLoad')


class IME(EventDispatcher):
    ...


class IMEConversionMode(Object):
    ALPHANUMERIC_FULL = String('ALPHANUMERIC_FULL')
    ALPHANUMERIC_HALF = String('ALPHANUMERIC_HALF')
    CHINESE = String('CHINESE')
    JAPANESE_HIRAGANA = String('JAPANESE_HIRAGANA')
    JAPANESE_KATAKANA_FULL = String('JAPANESE_KATAKANA_FULL')
    JAPANESE_KATAKANA_HALF = String('JAPANESE_KATAKANA_HALF')
    KOREAN = String('KOREAN')
    UNKNOWN = String('UNKNOWN')


class LoaderContext(Object):
    ...


class JPEGLoaderContex(LoaderContext):
    ...


class MessageChannel(EventDispatcher):
    ...


class MessageChannelState(Object):
    CLOSED = String('closed')
    CLOSING = String('closing')
    OPEN = String('open')


class Security(Object):
    ...


class SecurityDomain(Object):
    ...


class SecurityPanel(Object):
    CAMERA = String('camera')
    DEFAULT = String('default')
    DISPLAY = String('display')
    LOCAL_STORAGE = String('localStorage')
    MICROPHONE = String('microphone')
    PRIVACY = String('privacy')
    SETTINGS_MANAGER = String('settingsManager')


class System(Object):
    @staticproperty
    def freeMemory(cls):
        raise NotImplementedError

    @staticproperty
    def ime(cls):
        raise NotImplementedError

    @staticproperty
    def privateMemory(cls):
        raise NotImplementedError

    @staticproperty
    def totalMemory(cls):
        raise NotImplementedError

    @staticproperty
    def totalMemoryNumber(cls):
        raise NotImplementedError

    @staticproperty
    def useCodePage(cls):
        raise NotImplementedError

    @useCodePage.setter
    def useCodePage(cls, value):
        raise NotImplementedError

    def disposeXML():
        raise NotImplementedError

    def exit(code: int = 0):
        sys.exit(int(code))

    def gc():
        raise NotImplementedError

    def pause():
        raise NotImplementedError

    def pauseForGCIfCollectionImminent():
        raise NotImplementedError

    def resume():
        raise NotImplementedError

    def setClipboard():
        raise NotImplementedError


class SystemUpdater(EventDispatcher):
    ...


class SystemUpdaterType(Object):
    DRM = String('drm')
    SYSTEM = String('system')


class TouchscreenType(Object):
    FINGER = String('finger')
    NONE = String('none')
    STYLUS = String('stylus')


class Worker(EventDispatcher):
    ...


class WorkerDomain(Object):
    ...


class WorkerState(Object):
    NEW = String('new')
    RUNNING = String('running')
    TERMINATED = String('terminated')
