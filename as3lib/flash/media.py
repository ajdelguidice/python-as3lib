from __future__ import annotations
from as3lib import as3state, Array, Boolean, Error, false, int, null, Number, Object, String, true, uint, Vector
from as3lib.flash.display import BitmapData, DisplayObject
from as3lib.flash.events import ErrorEvent, EventDispatcher
from as3lib.flash.filesystem import File
from as3lib.flash.geom import Rectangle
from as3lib.flash.net import NetStream, URLLoader, URLRequest, URLStream
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
    @property
    def data(self):
        raise NotImplementedError

    @property
    def localTime(self):
        raise NotImplementedError


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
    @property
    def echoPath(self):
        return self._echoPath

    @echoPath.setter
    def echoPath(self, value):
        self._echoPath = int(value)

    @property
    def isVoiceDetected(self):
        return self._isVoiceDetected

    @isVoiceDetected.setter
    def isVoiceDetected(self, value):
        self._isVoiceDetected = int(value)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        value = String(value)
        # if value not in MicrophoneEnhancedMode:
        if value not in {'fullDuplex', 'halfDuplex', 'headset', 'off', 'speakerMute'}:
            raise
        self._mode = value

    @property
    def nonLinearProcessing(self):
        return self._nonLinearProcessing

    @nonLinearProcessing.setter
    def nonLinearProcessing(self, value):
        self._nonLinearProcessing = Boolean(value)

    def __init__(self):
        self.echoPath = 128
        # TODO: isVoiceDetected
        # TODO: Default for non-usb microphone is FULL_DUPLEX
        #       Default for usb microphone is HALF_DUPLEX
        # self.mode
        self.nonLinearProcessing = true


class Sound(EventDispatcher):
    @property
    def bytesLoaded(self):
        raise NotImplementedError

    @property
    def bytesTotal(self):
        raise NotImplementedError

    @property
    def id3(self):
        raise NotImplementedError

    @property
    def isBuffering(self):
        raise NotImplementedError

    @property
    def isURLInaccessible(self):
        raise NotImplementedError

    @property
    def length(self):
        raise NotImplementedError

    @property
    def url(self):
        raise NotImplementedError

    def __init__(self, stream: URLRequest = null,
                 context: SoundLoaderContext = null):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def extract(self, target: ByteArray, length: Number,
                startPosition: Number = -1):
        raise NotImplementedError

    def load(self, stream: URLRequest, context: SoundLoaderContext = null):
        raise NotImplementedError

    def loadCompressedDataFromByteArray(self, bytes: ByteArray,
                                        bytesLength: uint):
        raise NotImplementedError

    def loadPCMFromByteArray(self, bytes: ByteArray, samples: uint,
                             format: String = 'float', stereo: Boolean = true,
                             sampleRate: Number = 44100.0):
        raise NotImplementedError

    def play(self, startTime: Number = 0, loops: int = 0, sndTransform: SoundTransform = null):
        raise NotImplementedError


class SoundChannel(EventDispatcher):
    @property
    def leftPeak(self):
        raise NotImplementedError

    @property
    def position(self):
        raise NotImplementedError

    @property
    def rightPeak(self):
        raise NotImplementedError

    @property
    def soundTransform(self):
        raise NotImplementedError

    @soundTransform.setter
    def soundTransform(self, value):
        raise NotImplementedError

    def __init__(self):
        super().__init__()

    def stop(self):
        raise NotImplementedError


class SoundCodec(Object):
    NELLYMOSER = String('NellyMoser')
    PCMA = String('pcma')
    PCMU = String('pcmu')
    SPEEX = String('Speex')


class SoundLoaderContext(Object):
    @property
    def bufferTime(self):
        return self._bufferTime

    @bufferTime.setter
    def bufferTime(self, value):
        self._bufferTime = Number(value)

    @property
    def checkPolicyFile(self):
        return self._checkPolicyFile

    @checkPolicyFile.setter
    def checkPolicyFile(self, value):
        self._checkPolicyFile = Boolean(value)

    def __init__(self, bufferTime: Number = 1000,
                 checkPolicyFile: Boolean = false):
        self.bufferTime = bufferTime
        self.checkPolicyFile = checkPolicyFile


class SoundMixer(Object):
    @staticproperty
    def audioPlaybackMode(cls):
        raise NotImplementedError

    @audioPlaybackMode.setter
    def audioPlaybackMode(cls, value):
        raise NotImplementedError

    @staticproperty
    def bufferTime(self):
        raise NotImplementedError

    @bufferTime.setter
    def bufferTime(self, value):
        raise NotImplementedError

    @staticproperty
    def soundTransform(self):
        raise NotImplementedError

    @soundTransform.setter
    def soundTransform(self, value):
        raise NotImplementedError

    @staticproperty
    def useSpeakerphoneForVoice(self):
        raise NotImplementedError

    @useSpeakerphoneForVoice.setter
    def useSpeakerphoneForVoice(self, value):
        raise NotImplementedError

    @staticmethod
    def areSoundsInaccessible():
        raise NotImplementedError

    @staticmethod
    def computeSpectrum(outputArray: ByteArray, FFTMode: Boolean = false,
                        stretchFactor: int = 0):
        raise NotImplementedError

    @staticmethod
    def stopAll():
        raise NotImplementedError


class SoundTransform(Object):
    @property
    def leftToLeft(self):
        raise NotImplementedError

    @leftToLeft.setter
    def leftToLeft(self, value):
        raise NotImplementedError

    @property
    def leftToRight(self):
        raise NotImplementedError

    @leftToRight.setter
    def leftToRight(self, value):
        raise NotImplementedError

    @property
    def pan(self):
        return self._pan

    @pan.setter
    def pan(self, value):
        value = Number(value)
        # TODO: Check if this is supposed to raises here
        if value > -1 or value < 1:
            raise
        self._pan = value

    @property
    def rightToLeft(self):
        raise NotImplementedError

    @rightToLeft.setter
    def rightToLeft(self, value):
        raise NotImplementedError

    @property
    def rightToRight(self):
        raise NotImplementedError

    @rightToRight.setter
    def rightToRight(self, value):
        raise NotImplementedError

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        value = Number(value)
        # TODO: Check if this is supposed to raises here
        if value < 0 or value > 1:
            raise
        self._volume = value

    def __init__(self, vol: Number = 1, panning: Number = 0):
        self.volume = vol
        self.pan = panning


class StageVideo(EventDispatcher):
    @property
    def colorSpaces(self):
        raise NotImplementedError

    @property
    def depth(self):
        raise NotImplementedError

    @depth.setter
    def depth(self, value):
        raise NotImplementedError

    @property
    def pan(self):
        raise NotImplementedError

    @pan.setter
    def pan(self, value):
        raise NotImplementedError

    @property
    def videoHeight(self):
        raise NotImplementedError

    @property
    def videoWidth(self):
        raise NotImplementedError

    @property
    def viewPort(self):
        raise NotImplementedError

    @viewPort.setter
    def viewPort(self, value):
        raise NotImplementedError

    @property
    def zoom(self):
        raise NotImplementedError

    @zoom.setter
    def zoom(self, value):
        raise NotImplementedError

    def __init__(self):
        super().__init__()

    def attachCamera(self, theCamera: Camera):
        raise NotImplementedError

    def attachNetStream(self, netStream: NetStream):
        raise NotImplementedError


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
    @property
    def deblocking(self):
        raise NotImplementedError

    @deblocking.setter
    def deblocking(self, value):
        raise NotImplementedError

    @property
    def smoothing(self):
        raise NotImplementedError

    @smoothing.setter
    def smoothing(self, value):
        raise NotImplementedError

    @property
    def videoHeight(self):
        raise NotImplementedError

    @property
    def videoWidth(self):
        raise NotImplementedError

    def __init__(self, width: int = 320, height: int = 240):
        super().__init__()
        # NOTE: width and height properties are defined by the parent
        width = int(width)
        if width == 0:
            width = 320
        self.width = width

        height = int(height)
        if height == 0:
            height = 240
        self.height = height
        raise NotImplementedError

    def attachCamera(self, camera: Camera):
        raise NotImplementedError

    def attachNetStream(self, netStream: NetStream):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError


class VideoCodec(Object):
    H264AVC = String('H264Avc')
    SORENSON = String('Sorenson')


class VideoStatus(Object):
    ACCELERATED = String('accelerated')
    SOFTWARE = String('software')
    UNAVAILABLE = String('unavailable')


class VideoStreamSettings(Object):
    @property
    def bandwidth(self):
        return self._bandwidth

    @property
    def codec(self):
        return self._codec

    @property
    def fps(self):
        return self._fps

    @property
    def height(self):
        return self._height

    @property
    def keyFrameInterval(self):
        return self._keyFrameInterval

    @property
    def quality(self):
        return self._quality

    @property
    def width(self):
        return self._width

    def __init__(self):
        self._keyFrameInterval = int(15)
        self._width = int(-1)
        self._height = int(-1)
        self._fps = int(-1)
        raise NotImplementedError

    def setKeyFrameInterval(self, keyFrameInterval: int):
        keyFrameInterval = int(keyFrameInterval)
        if keyFrameInterval != -1 and (keyFrameInterval < 1 or keyFrameInterval > 300):
            keyFrameInterval = int(15)
        self._keyFrameInterval = keyFrameInterval

    def setMode(self, width: int, height: int, fps: Number):
        raise NotImplementedError

    def setQuality(self, bandwidth: int, quality: int):
        raise NotImplementedError


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
