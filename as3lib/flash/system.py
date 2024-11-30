from as3lib import toplevel as as3
from as3lib import configmodule
import platform
from typing import Union
import sys
from functools import cache

class ApplicationDomain:
    pass
class Capabilities:
    #!get actual values later
    #!document changes from original
    #!use __slots__
    avHardwareDisable = True
    @cache
    def _getCPUBits():
        return as3.Number(platform.architecture()[0][:-3])
    cpuAddressSize = property(fget=_getCPUBits) #returns 32 (32bit system) or 64 (64bit system)
    @cache
    def _getCPUArch():
        #!support other architectures
        match platform.machine():
            case "x86" | "x86_64" | "AMD64":
                return "x86"
    cpuArchitecture = property(fget=_getCPUArch) #returns "PowerPC","x86","SPARC",or "ARM"
    #hasAccessibility
    hasAudio = True #value is always True
    #hasAudioEncoder
    #hasEmbeddedVideo
    #hasIME
    #hasMP3
    #hasPrinting
    #hasScreenBroadcast
    #hasScreenPlayback
    #hasStreamingAudio
    #hasStreamingVideo
    #hasTLS
    #hasVideoEncoder
    def _getDebug():
        return configmodule.as3DebugEnable
    isDebugger = property(fget=_getDebug)
    #isEmbeddedInAcrobat
    #language
    #languages
    #localFileReadDisable
    @cache
    def _getManuf():
        match configmodule.platform:
            case "Windows":
                return "Adobe Windows"
            case "Linux":
                return "Adobe Linux"
            case "Darwin":
                return "Adobe Macintosh"
    manufacturer = property(fget=_getManuf)
    #maxLevelIDC
    @cache
    def _getOS():
        #!add others
        match configmodule.platform:
            case "Windows":
                pass
            case "Linux":
                return f"Linux {platform.release()}"
            case "Darwin":
                pass
    os = property(fget=_getOS)
    #pixelAspectRatio
    #playerType
    #screenColor
    #screenDPI
    #screenResolutionX
    #screenResolutionY
    #serverString
    #supports32BitProcesses
    #supports64BitProcesses
    #touchscreenType
    @cache
    def _getVer():
        tempfv = configmodule.spoofedFlashVersion
        match configmodule.platform:
            case "Windows":
                return f"Win {tempfv[0]},{tempfv[1]},{tempfv[2]},{tempfv[3]}"
            case "Linux":
                return f"LNX {tempfv[0]},{tempfv[1]},{tempfv[2]},{tempfv[3]}"
            case "Darwin":
                return f"MAC {tempfv[0]},{tempfv[1]},{tempfv[2]},{tempfv[3]}"
            case "Android":
                return f"AND {tempfv[0]},{tempfv[1]},{tempfv[2]},{tempfv[3]}"
    version = property(fget=_getVer)
    def hasMultiChannelAudio(type:Union[str,as3.String]):
        pass
class ImageDecodingPolicy:
    ON_DEMAND = "onDemand"
    ON_LOAD = "onLoad"
class IME:
    pass
class IMEConversionMode:
    ALPHANUMERIC_FULL = "ALPHANUMERIC_FULL"
    ALPHANUMERIC_HALF = "ALPHANUMERIC_HALF"
    CHINESE = "CHINESE"
    JAPANESE_HIRAGANA = "JAPANESE_HIRAGANA"
    JAPANESE_KATAKANA_FULL = "JAPANESE_KATAKANA_FULL"
    JAPANESE_KATAKANA_HALF = "JAPANESE_KATAKANA_HALF"
    KOREAN = "KOREAN"
    UNKNOWN = "UNKNOWN"
class JPEGLoaderContex:
    pass
class LoaderContext:
    pass
class MessageChannel:
    pass
class MessageChannelState:
    CLOSED = "closed"
    CLOSING = "closing"
    OPEN = "open"
class Security:
    pass
class SecurityDomain:
    pass
class SecurityPanel:
    pass
class System:
    #freeMemory
    #ime
    #privateMemory
    #totalMemory
    #totalMemoryNumber
    #useCodePage
    def disposeXML():
        pass
    def exit(code:Union[int,as3.int,as3.uint]=0):
        sys.exit(int(code))
    def gc():
        pass
    def pause():
        pass
    def pauseForGCIfCollectionImminent():
        pass
    def resume():
        pass
    def setClipboard():
        pass
class SystemUpdater:
    pass
class SystemUpdaterType:
    DRM = "drm"
    SYSTEM = "system"
class TouchscreenType:
    FINGER = "finger"
    NONE = "none"
    STYLUS = "stylus"
class Worker:
    pass
class WorkerDomain:
    pass
class WorkerState:
    NEW = "new"
    RUNNING = "running"
    TERMINATED = "terminated"