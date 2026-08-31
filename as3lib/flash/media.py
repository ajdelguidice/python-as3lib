from __future__ import annotations
from as3lib import as3state, Array, Boolean, Error, false, int, null, Number, Object, String, true, uint, Vector
from as3lib.flash.display import BitmapData, DisplayObject
from as3lib.flash.events import ErrorEvent, EventDispatcher
from as3lib.flash.filesystem import File
from as3lib.flash.geom import Rectangle
from as3lib.flash.net import URLLoader, URLRequest, URLStream
from as3lib.flash.utils import ByteArray
from as3lib.helpers import staticproperty


# Classes
class AudioDecoder(Object):
    DOLBY_DIGITAL = String('DolbyDigital')
    DOLBY_DIGITAL_PLUS = String('DolbyDigitalPlus')
    DTS = String('DTS')
    DTS_EXPRESS = String('DTSExpress')
    DTS_HD_HIGH_RESOLUTION_AUDIO = String('DTSHDHighResolutionAudio')
    DTS_HD_MASTER_AUDIO = String('DTSHDMasterAudio')


class AudioDeviceManager(EventDispatcher):
    # TODO: Initialise this singleton
    # TODO: AudioOutputChangeEvent

    @staticproperty
    def audioDeviceManager(cls):
        return as3state.audioDeviceManager

    @property
    def deviceNames(self):
        return self._deviceNames

    @staticproperty
    def isSupported(self):
        return true  # TODO: Placeholder

    @property
    def selectedDeviceIndex(self):
        return self._selectedDevice

    @selectedDeviceIndex.setter
    def selectedDeviceIndex(self, value):
        raise NotImplementedError

    def __new__(cls):
        # This class is a singleton
        if as3state.audioDeviceManager is None:
            return super().__new__(cls)
        # TODO: Ensure that raising is the right thing to do
        raise

    def __init__(self):
        super().__init__()

        # TODO: These values are placeholders
        self._deviceNames = Array()
        self._selectedDevice = int(0)


class AudioOutputChangeReason(Object):
    DEVICE_CHANGE = String('deviceChange')
    USER_SELECTION = String('userSelection')


class AudioPlaybackMode(Object):
    AMBIENT = String('ambient')
    MEDIA = String('media')
    VOICE = String('voice')


class AVNetworkingParams(Object):
    # TODO: Determine if these properties should be writeable
    @property
    def appendRandomQueryParameter(self):
        raise NotImplementedError

    @appendRandomQueryParameter.setter
    def appendRandomQueryParameter(self, value):
        raise NotImplementedError

    @property
    def forceNativeNetworking(self):
        return self._forceNativeNetworking

    @forceNativeNetworking.setter
    def forceNativeNetworking(self, value):
        self._forceNativeNetworking = Boolean(value)

    @property
    def networkDownVerificationUrl(self):
        return self._networkDownVerificationUrl

    @networkDownVerificationUrl.setter
    def networkDownVerificationUrl(self, value):
        self._networkDownVerificationUrl = String(value)

    @property
    def readSetCookieHeader(self):
        return self._readSetCookieHeader

    @readSetCookieHeader.setter
    def readSetCookieHeader(self, value):
        self._readSetCookieHeader = Boolean(value)

    @property
    def useCookieHeaderForAllRequests(self):
        return self._useCookieHeaderForAllRequests

    @useCookieHeaderForAllRequests.setter
    def useCookieHeaderForAllRequests(self, value):
        self._useCookieHeaderForAllRequests = Boolean(value)

    def __init__(self, init_forceNativeNetworking: Boolean = false,
                 init_readSetCookieHeader: Boolean = true,
                 init_useCookieHeaderForAllRequests: Boolean = false,
                 init_networkDownVerificationUrl: String = ''):
        self.forceNativeNetworking = init_forceNativeNetworking
        self.readSetCookieHeader = init_readSetCookieHeader
        self.useCookieHeaderForAllRequests = init_useCookieHeaderForAllRequests
        self.networkDownVerificationUrl = init_networkDownVerificationUrl


class AVTagData(Object):
    ...


class AVURLLoader(URLLoader):
    # cookieHeader

    def __init__(self, request: URLRequest = null):
        raise NotImplementedError

    def addEventListener(self, type: String, listener: callable,
                         useCapture: Boolean = false, priority: int = 0,
                         useWeakReference: Boolean = false):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def load(self, request: URLRequest):
        raise NotImplementedError


class AVURLStream(URLStream):
    # cookieHeader

    def load(self, request: URLRequest):
        raise NotImplementedError


class Camera(EventDispatcher):
    @property
    def activityLevel(self):
        raise NotImplementedError

    @property
    def bandwidth(self):
        raise NotImplementedError

    @property
    def currentFPS(self):
        raise NotImplementedError

    @property
    def fps(self):
        raise NotImplementedError

    @property
    def height(self):
        raise NotImplementedError

    @property
    def index(self):
        raise NotImplementedError

    @staticproperty
    def isSupported(cls):
        raise NotImplementedError

    @property
    def keyFrameInterval(self):
        raise NotImplementedError

    @property
    def loopback(self):
        raise NotImplementedError

    @property
    def motionLevel(self):
        raise NotImplementedError

    @property
    def motionTimeout(self):
        raise NotImplementedError

    @property
    def muted(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    @staticproperty
    def names(cls):
        raise NotImplementedError

    @staticproperty
    def permissionStatus(cls):
        raise NotImplementedError

    @property
    def position(self):
        raise NotImplementedError

    @property
    def quality(self):
        raise NotImplementedError

    @property
    def width(self):
        raise NotImplementedError

    def __init__(self):
        raise NotImplementedError
        super().__init__()

    def copyToByteArray(self, rect: Rectangle, destination: ByteArray):
        raise NotImplementedError

    def copyToVector(self, rect: Rectangle, destination: Vector[uint]):
        raise NotImplementedError

    def drawToBitmapData(self, destination: BitmapData):
        raise NotImplementedError

    @staticmethod
    def getCamera(name: String = null):
        raise NotImplementedError

    def requestPermission(self):
        raise NotImplementedError

    def setKeyFrameInterval(keyFrameInterval: int):
        raise NotImplementedError

    def setLoopback(self, compress: Boolean = false):
        raise NotImplementedError

    def setMode(self, width: int, height: int, fps: Number,
                favorArea: Boolean = true):
        raise NotImplementedError

    def setMotionLevel(self, motionLevel: int, timeout: int = 2000):
        raise NotImplementedError

    def setQuality(self, bandwidth: int, quality: int):
        raise NotImplementedError


class CameraPosition(Object):
    BACK = String('back')
    FRONT = String('front')
    UNKNOWN = String('unknown')


class CameraRoll(EventDispatcher):
    @staticproperty
    def permissionStatus(cls):
        raise NotImplementedError

    @staticproperty
    def supportsAddBitmapData(cls):
        raise NotImplementedError

    @staticproperty
    def supportsBrowseForImage(cls):
        raise NotImplementedError

    def __init__(self):
        raise NotImplementedError
        super().__init__()

    def addBitmapData(self, bitmapData: BitmapData):
        raise NotImplementedError

    def browseForImage(self, value: CameraRollBrowseOptions = null):
        raise NotImplementedError

    def requestPermission(self):
        raise NotImplementedError


class CameraRollBrowseOptions(Object):
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = Number(value)

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        raise NotImplementedError

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = Number(value)

    def __init__(self):
        super().__init__()
        self._width = Number(0)
        self._height = Number(0)
        self._origin = Rectangle(0, 0, 0, 0)


class CameraUI(EventDispatcher):
    @staticproperty
    def isSupported(cls):
        raise NotImplementedError

    @staticproperty
    def permissionStatus(cls):
        raise NotImplementedError

    def __init__(self):
        super().__init__()

    def launch(self, requestedMediaType: String):
        raise NotImplementedError

    def requestPermission(self):
        raise NotImplementedError


class H264Level(Object):
    LEVEL_1 = String('1')
    LEVEL_1_1 = String('1.1')
    LEVEL_1_2 = String('1.2')
    LEVEL_1_3 = String('1.3')
    LEVEL_1B = String('1b')
    LEVEL_2 = String('2')
    LEVEL_2_1 = String('2.1')
    LEVEL_2_2 = String('2.2')
    LEVEL_3 = String('3')
    LEVEL_3_1 = String('3.1')
    LEVEL_3_2 = String('3.2')
    LEVEL_4 = String('4')
    LEVEL_4_1 = String('4.1')
    LEVEL_4_2 = String('4.2')
    LEVEL_5 = String('5')
    LEVEL_5_1 = String('5.1')


class H264Profile(Object):
    BASELINE = String('baseline')
    MAIN = String('main')


class ID3Info(Object):
    @property
    def album(self):
        raise NotImplementedError

    @album.setter
    def album(self, value):
        raise NotImplementedError

    @property
    def artist(self):
        raise NotImplementedError

    @artist.setter
    def artist(self, value):
        raise NotImplementedError

    @property
    def comment(self):
        raise NotImplementedError

    @comment.setter
    def comment(self, value):
        raise NotImplementedError

    @property
    def genre(self):
        raise NotImplementedError

    @genre.setter
    def genre(self, value):
        raise NotImplementedError

    @property
    def songName(self):
        raise NotImplementedError

    @songName.setter
    def songName(self, value):
        raise NotImplementedError

    @property
    def track(self):
        raise NotImplementedError

    @track.setter
    def track(self, value):
        raise NotImplementedError

    @property
    def year(self):
        raise NotImplementedError

    @year.setter
    def year(self, value):
        raise NotImplementedError

    def __init__(self):
        raise NotImplementedError


# TODO: Implements flash.desktop.IFilePromise
class MediaPromise(EventDispatcher):
    @property
    def file(self):
        raise NotImplementedError

    @property
    def isAsync(self):
        raise NotImplementedError

    @property
    def mediaType(self):
        raise NotImplementedError

    @property
    def relativePath(self):
        raise NotImplementedError

    def __init__(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def open(self):
        raise NotImplementedError

    def reportError(self, e: ErrorEvent):
        raise NotImplementedError


class MediaType(Object):
    IMAGE = String('image')
    VIDEO = String('video')


class Microphone(EventDispatcher):
    @property
    def activityLevel(self):
        raise NotImplementedError

    @property
    def codec(self):
        raise NotImplementedError

    @codec.setter
    def codec(self):
        raise NotImplementedError

    @property
    def enableVAD(self):
        raise NotImplementedError

    @enableVAD.setter
    def enableVAD(self):
        raise NotImplementedError

    @property
    def encodeQuality(self):
        raise NotImplementedError

    @encodeQuality.setter
    def encodeQuality(self):
        raise NotImplementedError

    @property
    def enhancedOptions(self):
        raise NotImplementedError

    @enhancedOptions.setter
    def enhancedOptions(self):
        raise NotImplementedError

    @property
    def framesPerPacket(self):
        raise NotImplementedError

    @framesPerPacket.setter
    def framesPerPacket(self):
        raise NotImplementedError

    @property
    def gain(self):
        raise NotImplementedError

    @gain.setter
    def gain(self):
        raise NotImplementedError

    @property
    def index(self):
        raise NotImplementedError

    @staticproperty
    def isSupported(self):
        raise NotImplementedError

    @property
    def muted(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    @property
    def names(self):
        raise NotImplementedError

    @property
    def noiseSuppressionLevel(self):
        raise NotImplementedError

    @noiseSuppressionLevel.setter
    def noiseSuppressionLevel(self):
        raise NotImplementedError

    @property
    def noiseSuppressionStatus(self):
        raise NotImplementedError

    @property
    def rate(self):
        raise NotImplementedError

    @rate.setter
    def rate(self):
        raise NotImplementedError

    @property
    def silenceLevel(self):
        raise NotImplementedError

    @property
    def silenceTimeout(self):
        raise NotImplementedError

    @property
    def soundTransform(self):
        raise NotImplementedError

    @soundTransform.setter
    def soundTransform(self):
        raise NotImplementedError

    @property
    def useEchoSuppression(self):
        raise NotImplementedError

    def __init__(self):
        raise NotImplementedError
        super().__init__()

    @staticmethod
    def getEnhancedMicrophone(index: int = -1):
        raise NotImplementedError

    @staticmethod
    def getMicrophone(index: int = -1):
        raise NotImplementedError

    def requestPermission(self):
        raise NotImplementedError

    def setLoopBack(self, state: Boolean = true):
        raise NotImplementedError

    def setSilenceLevel(self, silenceLevel: Number, timeout: int = -1):
        raise NotImplementedError

    def setUseEchoSuppression(self, useEchoSuppression: Boolean):
        raise NotImplementedError


class MicrophoneEnhancedMode(Object):
    FULL_DUPLEX = String('fullDuplex')
    HALF_DUPLEX = String('halfDuplex')
    HEADSET = String('headset')
    OFF = String('off')
    SPEAKER_MUTE = String('speakerMute')


class MicrophoneEnhancedOptions(Object):
    ...


class SoundChannel(EventDispatcher):
    ...


class SoundCodec(Object):
    NELLYMOSER = String('NellyMoser')
    PCMA = String('pcma')
    PCMU = String('pcmu')
    SPEEX = String('Speex')


class SoundLoaderContext(Object):
    ...


class SoundMixer(Object):
    ...


class SoundTransform(Object):
    ...


class StageVideo(EventDispatcher):
    ...


class StageVideoAvailability(Object):
    AVAILABLE = String('available')
    UNAVAILABLE = String('unavailable')


class StageVideoAvailabilityReason(Object):
    DRIVER_TOO_OLD = String('driverTooOld')
    NO_ERROR = String('noError')
    UNAVAILABLE = String('unavailable')
    USER_DISABLED = String('userDisabled')
    WMODE_INCOMPATIBLE = String('wModeIncompatible')


class StageWebView(EventDispatcher):
    ...


class Video(DisplayObject):
    ...


class VideoCodec(Object):
    H264AVC = String('H264Avc')
    SORENSON = String('Sorenson')


class VideoStatus(Object):
    ACCELERATED = String('accelerated')
    SOFTWARE = String('software')
    UNAVAILABLE = String('unavailable')


class VideoStreamSettings(Object):
    ...


class H264VideoStreamSettings(VideoStreamSettings):
    @property
    def codec(self):
        raise NotImplementedError

    @property
    def level(self):
        return self._level

    @property
    def profile(self):
        return self._profile

    def __init__(self):
        raise NotImplementedError
        super().__init__()

        # TODO: Check what these are supposed to be
        self._level = H264Level.LEVEL_1
        self._profile = H264Profile.BASELINE

    def setProfileLevel(self, profile: String, level: String):
        profile = String(profile)
        level = String(level)
        raise NotImplementedError
        if profile not in H264Profile:
            raise Error()
        if level not in H264Level:
            raise Error()
        self._profile = profile
        self._level = level


# Functions
def avSentToURL(auth, request: URLRequest, cookieHeader: String = null):
    raise NotImplementedError


def scanHardware():
    raise NotImplementedError
