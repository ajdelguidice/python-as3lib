from as3lib import as3state, false, int, metaclasses, Number, String, true
from as3lib.helpers import staticproperty
from functools import cache
import platform
import sys


class ApplicationDomain:
    ...


class Capabilities:
    # TODO: get actual values
    # TODO: document changes from original

    @staticproperty
    def avHardwareDisable(cls):
        # This is not needed so it is always True
        return true

    @staticproperty
    @cache
    def cpuAddressSize(cls):  # returns 32 (32bit system) or 64 (64bit system)
        return Number(platform.architecture()[0][:-3])

    @staticproperty
    @cache
    def cpuArchitecture(cls):  # returns 'PowerPC','x86','SPARC',or 'ARM'
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

    @property
    def playerType():
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


class ImageDecodingPolicy(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
    ON_DEMAND = 'onDemand'
    ON_LOAD = 'onLoad'


class IME:
    ...


class IMEConversionMode(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
    ALPHANUMERIC_FULL = 'ALPHANUMERIC_FULL'
    ALPHANUMERIC_HALF = 'ALPHANUMERIC_HALF'
    CHINESE = 'CHINESE'
    JAPANESE_HIRAGANA = 'JAPANESE_HIRAGANA'
    JAPANESE_KATAKANA_FULL = 'JAPANESE_KATAKANA_FULL'
    JAPANESE_KATAKANA_HALF = 'JAPANESE_KATAKANA_HALF'
    KOREAN = 'KOREAN'
    UNKNOWN = 'UNKNOWN'


class JPEGLoaderContex:
    ...


class LoaderContext:
    ...


class MessageChannel:
    ...


class MessageChannelState(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
    CLOSED = 'closed'
    CLOSING = 'closing'
    OPEN = 'open'


class Security:
    ...


class SecurityDomain:
    ...


class SecurityPanel:
    ...


class System:
    #freeMemory
    #ime
    #privateMemory
    #totalMemory
    #totalMemoryNumber
    #useCodePage

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


class SystemUpdater:
    ...


class SystemUpdaterType(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
    DRM = 'drm'
    SYSTEM = 'system'


class TouchscreenType(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
    FINGER = 'finger'
    NONE = 'none'
    STYLUS = 'stylus'


class Worker:
    ...


class WorkerDomain:
    ...


class WorkerState(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
    NEW = 'new'
    RUNNING = 'running'
    TERMINATED = 'terminated'
