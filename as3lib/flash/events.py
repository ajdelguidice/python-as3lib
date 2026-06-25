from as3lib import (Array, as3state, Boolean, Error, false, int, metaclasses,
                    Number, null, Object, String, true, TypeError, uint)
from as3lib.flash.errors import SQLError
from as3lib.flash.geom import Rectangle


_ERRCONSTAllowedChars = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                         'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                         'U', 'V', 'W', 'X', 'Y', 'Z', '_', '0', '1', '2',
                         '3', '4', '5', '6', '7', '8', '9'}


def _HELPER_GetEventConstants(cls):
    # TODO: Make child classes able to have the same constants defined as the
    #       parents
    consts = set()
    for i in (i for i in dir(cls) if not i.startswith('_')):
        valid = True
        for j in i:
            if j not in _ERRCONSTAllowedChars:
                valid = False
                break
        if valid:
            consts.add(getattr(cls, i))
    if cls.__base__ != object:
        return consts - _HELPER_GetEventConstants(cls.__base__)
    return consts


# Interfaces
class IEventDispatcher:
    def __init__(self):
        self.eventobjects = {}

    def addEventListener(self, type, listener, useCapture=False, priority=0, useWeakReference=False):
        raise NotImplementedError

    def dispatchEvent(self, event):
        raise NotImplementedError

    def hasEventListener(self, type):
        raise NotImplementedError

    def removeEventListener(self, type, listener, useCapture=False):
        raise NotImplementedError

    def willTrigger(self, type):
        raise NotImplementedError


# Classes
class Event(Object):
    # TODO: Find a way to not pollute children with constants
    ACTIVATE = 'activate'  # bubbles=False, cancelable=False
    ADDED = 'added'  # bubbles=True, cancelable=False
    ADDED_TO_STAGE = 'addedToStage'  # bubbles=False, cancelable=False
    BROWSER_ZOOM_CHANGE = 'browerZoomChange'  # bubbles=False, cancelable=False
    CANCEL = 'cancel'  # bubbles=False, cancelable=False
    CHANGE = 'change'  # bubbles=True, cancelable=False
    CHANNEL_MESSAGE = 'channelMessage'  # bubbles=False, cancelable=False
    CHANNEL_STATE = 'channelState'  # bubbles=False, cancelable=False
    CLEAR = 'clear'  # bubbles=False, cancelable=False
    CLOSE = 'close'  # bubbles=False, cancelable=False
    CLOSING = 'closing'  # bubbles=False, cancelable=True
    COMPLETE = 'complete'  # bubbles=False, cancelable=False
    CONNECT = 'connect'  # bubbles=False, cancelable=False
    CONTEXT3D_CREATE = 'context3DCreate'  # ?
    COPY = 'copy'  # bubbles=False, cancelable=False
    CUT = 'cut'  # bubbles=False, cancelable=False
    DEACTIVATE = 'deactivate'  # bubbles=False, cancelable=False
    DISPLAYING = 'displaying'  # bubbles=False, cancelable=False
    ENTER_FRAME = 'enterFrame'  # bubbles=False, cancelable=False
    EXIT_FRAME = 'exitFrame'  # bubbles=False, cancelable=False
    EXITING = 'exiting'  # bubbles=False, cancelable=True
    FRAME_CONSTRUCTED = 'frameConstructed'  # bubbles=False, cancelable=False
    FRAME_LABEL = 'frameLabel'  # bubbles=False, cancelable=False
    FULLSCREEN = 'fullscreen'  # bubbles=False, cancelable=False
    HTML_BOUNDS_CHANGE = 'htmlBoundsChange'  # bubbles=False, cancelable=False
    HTML_DOM_INITIALIZE = 'htmlDOMInitialize'  # bubbles=False, cancelable=False
    HTML_RENDER = 'htmlRender'  # bubbles=False, cancelable=False
    ID3 = 'id3'  # bubbles=False, cancelable=False
    INIT = 'init'  # bubbles=False, cancelable=False
    LOCATION_CHANGE = 'locationChange'  # bubbles=False, cancelable=False
    MOUSE_LEAVE = 'mouseLeave'  # bubbles=False, cancelable=False
    NETWORK_CHANGE = 'networkChange'  # bubbles=False, cancelable=False
    OPEN = 'open'  # bubbles=False, cancelable=False
    PASTE = 'paste'  # bubbles=(platformDependant), cancelable=False
    PREPARING = 'preparing'  # bubbles=False, cancelable=False
    REMOVED = 'removed'  # bubbles=True, cancelable=False
    REMOVED_FROM_STAGE = 'removeFromStage'  # bubbles=False, cancelable=False
    RENDER = 'render'  # bubbles=False, cancelable=False
    RESIZE = 'resize'  # bubbles=False, cancelable=False
    SCROLL = 'scroll'  # bubbles=False, cancelable=False
    SELECT = 'select'  # bubbles=False, cancelable=False
    SELECT_ALL = 'selectAll'  # bubbles=False, cancelable=False
    SOUND_COMPLETE = 'soundComplete'  # bubbles=False, cancelable=False
    STANDARD_ERROR_CLOSE = 'standardErrorClose'  # bubbles=False, cancelable=False
    STANDARD_INPUT_CLOSE = 'standardInputClose'  # bubbles=False, cancelable=False
    STANDARD_OUTPUT_CLOSE = 'standardOutputClose'  # bubbles=False, cancelable=False
    SUSPEND = 'suspend'  # bubbles=False, cancelable=False
    TAB_CHILDREN_CHANGE = 'tabChildrenChange'  # bubbles=True, cancelable=False
    TAB_ENABLE_CHANGE = 'tabEnableChange'  # bubbles=True, cancelable=False
    TAB_INDEX_CHANGE = 'tabIndexChange'  # bubbles=True, cancelable=False
    TEXT_INTERACTION_MODE_CHANGE = 'textInteractionModeChange'  # bubbles=False, cancelable=False
    TEXTURE_READY = 'textureReady'  # ?
    UNLOAD = 'unload'  # bubbles=False, cancelable=False
    USER_IDLE = 'userIdle'  # bubbles=False, cancelable=False
    USER_PRESENT = 'userPresent'  # bubbles=False, cancelable=False
    VIDEO_FRAME = 'videoFrame'  # bubbles=False, cancelable=False
    WORKER_STATE = 'workerState'  # bubbles=False, cancelable=False

    @property
    def _propagation(self):
        # 0 - continue, 1 - stop, 2 - stopimmediate
        return self._propagationState

    @property
    def bubbles(self):
        return self._bubbles

    @property
    def cancelable(self):
        return self._cancelable

    @property
    def currentTarget(self):
        return self._currentTarget

    @property
    def eventPhase(self):
        return self._eventPhase

    @property
    def target(self):
        return self._target

    @property
    def type(self):
        return self._type

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false):
        self._type = String(type)
        self._bubbles = Boolean(bubbles)
        self._cancelable = Boolean(cancelable)
        self._currentTarget = null
        self._target = null
        self._eventPhase = 2
        self._preventDefault = false
        self._propagationState = 0
        self._eventDispatched = false

    def clone(self):
        return Event(self.type, self.bubbles, self.cancelable)

    @staticmethod
    def _formatToString_formatAttr(attr):
        if isinstance(attr, (String, str)):
            return f'"{attr}"'
        return attr

    def formatToString(self, className, *arguements):
        return String(''.join(['[', className] + [f' {i}={self._formatToString_formatAttr(getattr(self, i))}' for i in arguements] + [']']))

    def isDefaultPrevented(self):
        return self._preventDefault

    def preventDefault(self):
        if self.cancelable:
            self._preventDefault = true

    def stopImmediatePropagation(self):
        self._propagationState = 2

    def stopPropagation(self):
        self._propagationState = 1

    def toString(self):
        return self.formatToString('Event', 'type', 'bubbles', 'cancelable', 'eventPhase')


class EventDispatcher(Object):
    # TODO: Implement priority, weakReference

    def __init__(self, target: IEventDispatcher = null):
        self._events = {}
        self._eventsCapture = {}
        self._target = self if target is null else target

    def addEventListener(self, type: String, listener, useCapture: Boolean = false, priority: int = 0, useWeakReference: Boolean = false):
        # TODO: Add error
        # TODO: Implement priority
        type = String(type)
        useCapture = Boolean(useCapture)
        priority = int(priority)
        useWeakReference = Boolean(useWeakReference)
        if useCapture == false:
            if type not in self._events:
                self._events[type] = [listener]
            elif listener not in self._events[type]:
                self._events[type].append(listener)
        else:
            if type not in self._eventsCapture:
                self._eventsCapture[type] = [listener]
            elif listener not in self._eventsCapture[type]:
                self._eventsCapture[type].append(listener)

    def dispatchEvent(self, event):
        # TODO: Implement useCapture
        # TODO: Implement bubbles
        # TODO: stopPropagation
        if event.isDefaultPrevented() or not len(self._events.get(event.type, set())):
            return false
        event._currentTarget = self  # TODO: Make sure that this is correct
        if not event._eventDispatched:
            event._target = self._target
            event._eventDispatched = true
            e = event
        else:
            e = event.clone()
        for i in self._events.get(event.type, set()):
            i(e)
            if e.isDefaultPrevented():
                return false
            if e._propagation == 2:  # Stop Immediate
                # TODO: Make sure this is correct
                break
        return true

    def hasEventListener(self, type: String):
        type = String(type)
        return (type in self._events and len(self._events[type]) or
                type in self._eventsCapture and len(self._eventsCapture[type]))

    def removeEventListener(self, type: String, listener, useCapture: Boolean = false):
        type = String(type)
        useCapture = Boolean(useCapture)
        if useCapture == false:
            if type in self._events:
                try:
                    self._events[type].remove(listener)
                except Exception:
                    pass
        else:
            if type in self._eventsCapture:
                try:
                    self._eventsCapture[type].remove(listener)
                except Exception:
                    pass

    def willTrigger(self, type: String):
        # TODO: Also check ancestors
        return self.hasEventListener(type)


class TextEvent(Event):
    LINK = 'link'  # bubbles=True, cancelable=False
    TEXT_INPUT = 'textInput'  # bubbles=True, cancelable=True

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = String(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, text: String = ''):
        super().__init__(type, bubbles, cancelable)
        self.text = text

    def clone(self):
        return TextEvent(self.type, self.bubbles, self.cancelable, self.text)

    def toString(self):
        return self.formatToString('TextEvent', 'type', 'bubbles',
                                   'cancelable', 'text')


class ErrorEvent(TextEvent):
    ERROR = 'error'

    @property
    def errorID(self):
        return self._errorID

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, text: String = '', id: int = 0):
        super().__init__(type, bubbles, cancelable, text)
        self._errorID = int(id)

    def clone(self):
        return ErrorEvent(self.type, self.bubbles, self.cancelable, self.text,
                          self.errorID)

    def toString(self):
        return self.formatToString('ErrorEvent', 'type', 'bubbles',
                                   'cancelable', 'text', 'errorID')


class AccelerometerEvent(Event):
    UPDATE = 'update'

    @property
    def accelerationX(self):
        return self._accelX

    @accelerationX.setter
    def accelerationX(self, value):
        self._accelX = Number(value)

    @property
    def accelerationY(self):
        return self._accelY

    @accelerationY.setter
    def accelerationY(self, value):
        self._accelY = Number(value)

    @property
    def accelerationZ(self):
        return self._accelZ

    @accelerationZ.setter
    def accelerationZ(self, value):
        self._accelZ = Number(value)

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = Number(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, timestamp: Number = 0,
                 accelerationX: Number = 0, accelerationY: Number = 0,
                 accelerationZ: Number = 0):
        super().__init__(type, bubbles, cancelable)
        self.accelerationX = accelerationX
        self.accelerationY = accelerationY
        self.accelerationZ = accelerationZ
        self.timestamp = timestamp

    def clone(self):
        return AccelerometerEvent(self.type, self.bubbles, self.cancelable,
                                  self.timestamp, self.accelerationX,
                                  self.accelerationY, self.accelerationZ)

    def toString(self):
        return self.formatToString('AccelerometerEvent', 'type', 'bubbles',
                                   'cancelable', 'timestamp', 'accelerationX',
                                   'accelerationY', 'accelerationZ')


class ActivityEvent(Event):
    ACTIVITY = 'activity'

    @property
    def activating(self):
        return self.activating

    @activating.setter
    def activating(self, value):
        self._activating = Boolean(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, activating: Boolean = false):
        super().__init__(type, bubbles, cancelable)
        self.activating = activating

    def clone(self):
        return ActivityEvent(self.type, self.bubbles, self.cancelable,
                             self.activating)

    def toString(self):
        return self.formatToString('ActivityEvent', 'type', 'bubbles',
                                   'cancelable', 'activating')


class AsyncErrorEvent(ErrorEvent):
    ASYNC_ERROR = 'asyncError'

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, text: String = '',
                 error: Error = null):
        id = 0 if error is null else error.errorID
        super().__init__(type, bubbles, cancelable, text, id)
        self._error = error

    def clone(self):
        return AsyncErrorEvent(self.type, self.bubbles, self.cancelable,
                               self.text, self.error)

    def toString(self):
        return self.formatToString('AsyncErrorEvent', 'type', 'bubbles',
                                   'cancelable', 'text', 'error', 'errorID')


class AudioOutputChangeEvent(Event):
    AUDIO_OUTPUT_CHANGE = 'audioOutputChange'

    @property
    def reason(self):
        return self._reason

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, reason: String = null):
        super().__init__(type, bubbles, cancelable)
        self._reason = String(reason)


class AVDictionaryDataEvent(Event):
    # TODO: Make _dictionary init as a flash.utils.Dictionary object
    AV_DICTIONARY_DATA = 'avDictionaryData'

    @property
    def dictionary(self):
        return self._dictionary

    @property
    def time(self):
        return self._time

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, init_dictionary = null,
                 init_dataTime: Number = 0):
        super().__init__(type, bubbles, cancelable)
        self._dictionary = {} if init_dictionary is null else init_dictionary
        self._time = Number(init_dataTime)


class AVHTTPStatusEvent(Event):
    AV_HTTP_RESPONSE_STATUS = 'avHttpResponseStatus'

    @property
    def responseHeaders(self):
        return self._responseHeaders

    @responseHeaders.setter
    def responseHeaders(self, value):
        self._responseHeaders = value

    @property
    def responseUrl(self):
        return self._responseUrl

    @responseUrl.setter
    def responseUrl(self, value):
        self._responseUrl = String(value)

    @property
    def status(self):
        return self._status

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, status: int = 0,
                 responseUrl: String = null, responseHeaders: Array = null):
        super().__init__(type, bubbles, cancelable)
        self._status = int(status)
        self.responseUrl = responseUrl
        self.responseHeaders = responseHeaders

    def clone(self):
        return AVHTTPStatusEvent(self.type, self.bubbles, self.cancelable,
                                 self.status, self.responseUrl,
                                 self.responseHeaders)

    def toString(self):
        return self.formatToString('AVHTTPStatusEvent', 'type', 'bubbles',
                                   'cancelable', 'status')


class AVPauseAtPeriodEndEvent(Event):
    AV_PAUSE_AT_PERIOD_END = 'avPauseAtPeriodEnd'

    @property
    def userData(self):
        return self._userData

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, userData: int = 0):
        super().__init__(type, bubbles, cancelable)
        self._userData = int(userData)


class BrowserInvokeEvent(Event):
    BROWSER_INVOKE = 'browserInvoke'

    @property
    def arguments(self):
        return self._arguements

    @property
    def isHTTPS(self):
        return self._isHTTPS

    @property
    def isUserEvent(self):
        return self._isUserEvent

    @property
    def sandboxType(self):
        return self._sandboxType

    @property
    def securityDomain(self):
        return self._securityDomain

    def __init__(self, type: String, bubbles: Boolean, cancelable: Boolean,
                 arguments: Array, sandboxType: String,
                 securityDomain: String, isHTTPS: Boolean):
        super().__init__(type, bubbles, cancelable)
        self._arguments = arguments
        self._isHTTPS = Boolean(isHTTPS)
        self._isUserEvent = false
        self._sandboxType = String(sandboxType)
        self._securityDomain = String(securityDomain)

    def clone(self):
        return BrowserInvokeEvent(self.type, self.bubbles, self.cancelable,
                                  self.arguments, self.sandboxType,
                                  self.securityDomain, self.isHTTPS)


class ContextMenuEvent(Event):
    MENU_ITEM_SELECT = 'menuItemSelect'
    MENU_SELECT = 'menuSelect'

    @property
    def contextMenuOwner(self):
        return self._cmOwner

    @property
    def isMouseTargetInaccessible(self):
        return self._mTarget is null

    @property
    def mouseTarget(self):
        return self._mTarget

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, mouseTarget = null,
                 contextMenuOwner = null):
        super().__init__(type, bubbles, cancelable)
        self._cmOwner = contextMenuOwner
        self._mTarget = mouseTarget

    def clone(self):
        return ContextMenuEvent(self.type, self.bubbles, self.cancelable,
                                self.mouseTarget, self.contextMenuOwner)

    def toString(self):
        return self.formatToString('ContextMenuEvent', 'type', 'bubbles',
                                   'cancelable', 'mouseTarget',
                                   'isMouseTargetInaccessible',
                                   'contextMenuOwner')


class DataEvent(TextEvent):
    DATA = 'data'
    UPLOAD_COMPLETE_DATA = 'uploadCompleteData'

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = String(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, data: String = ''):
        super().__init__(type, bubbles, cancelable)
        self.data = data

    def clone(self):
        return DataEvent(self.type, self.bubbles, self.cancelable, self.data)

    def toString(self):
        return self.formatToString('DataEvent', 'type', 'bubbles',
                                   'cancelable', 'data')


class DatagramSocketDataEvent(Event):
    DATA = 'data'

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        raise NotImplementedError

    @property
    def dstAddress(self):
        return self._dstAddress

    @dstAddress.setter
    def dstAddress(self, value):
        self._dstAddress = String(value)

    @property
    def dstPort(self):
        return self._dstPort

    @dstPort.setter
    def dstPort(self, value):
        self._dstPort = int(value)

    @property
    def srcAddress(self):
        return self._srcAddress

    @srcAddress.setter
    def srcAddress(self, value):
        self._srcAddress = String(value)

    @property
    def srcPort(self):
        return self._srcPort

    @srcPort.setter
    def srcPort(self, value):
        self._srcPort = int(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, srcAddress: String = '',
                 srcPort: int = 0, dstAddress: String = '', dstPort: int = 0,
                 data = null):
        super().__init__(type, bubbles, cancelable)
        self.srcAddress = srcAddress
        self.srcPort = srcPort
        self.dstAddress = dstAddress
        self.dstPort = dstPort
        self._data = data

    def clone(self):
        return DatagramSocketDataEvent(self.type, self.bubbles,
                                       self.cancelable, self.srcAddress,
                                       self.srcPort, self.dstAddress,
                                       self.dstPort, self.data)

    def toString(self):
        return self.formatToString('DatagramSocketDataEvent', 'type',
                                   'bubbles', 'cancelable', 'srcAddress',
                                   'srcPort', 'dstAddress', 'dstPort', 'data')


class DeviceRotationEvent(Event):
    UPDATE = 'update'

    @property
    def pitch(self):
        return self._pitch

    @pitch.setter
    def pitch(self, value):
        self._pitch = Number(value)

    @property
    def quaternion(self):
        return self._quaternion

    @quaternion.setter
    def quaternion(self, value):
        raise NotImplementedError

    @property
    def roll(self):
        return self._roll

    @roll.setter
    def roll(self, value):
        self._roll = Number(value)

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = Number(value)

    @property
    def yaw(self):
        return self._yaw

    @yaw.setter
    def yaw(self, value):
        self._yaw = Number(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, timestamp: Number = 0,
                 roll: Number = 0, pitch: Number = 0, yaw: Number = 0,
                 quaternion: Array = null):
        super().__init__(type, bubbles, cancelable)
        self.timestamp = timestamp
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
        self._quaternion = quaternion

    def clone(self):
        return DeviceRotationEvent(self.type, self.bubbles, self.cancelable,
                                   self.timestamp, self.roll, self.pitch,
                                   self.yaw, self.quaternion)

    def toString(self):
        return self.formatToString('DeviceRotationEvent', 'type', 'bubbles',
                                   'cancelable', 'timestamp', 'roll', 'pitch',
                                   'yaw', 'quaternion')


class DNSResolverEvent(Event):
    LOOKUP = 'lookup'

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = String(value)

    @property
    def resourceRecords(self):
        return self._resourceRecords

    @resourceRecords.setter
    def resourceRecords(self, value):
        raise NotImplementedError

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, host: String = '',
                 resourceRecords: Array = null):
        super().__init__(type, bubbles, cancelable)
        self.host = host
        self._resourceRecords = resourceRecords

    def clone(self):
        return DNSResolverEvent(self.type, self.bubbles, self.cancelable,
                                self.host, self.resourceRecords)

    def toString(self):
        return self.formatToString('DNSResolverEvent', 'type', 'bubbles',
                                   'cancelable', 'host', 'resourceRecords')


class DRMAuthenticateEvent:
    ...


class DRMAuthenticateCompleteEvent:
    ...


class DRMAuthenticateErrorEvent:
    ...


class DRMDeviceGroupErrorEvent:
    ...


class DRMErrorEvent:
    ...


class DRMLicenseRequestEvent:
    ...


class DRMMetadataEvent:
    ...


class DRMReturnVoucherCompleteEvent:
    ...


class DRMStatusEvent:
    ...


class EventPhase(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
    AT_TARGET = 2
    BUBBLING_PHASE = 3
    CAPTURING_PHASE = 1


class FileListEvent(Event):
    DIRECTORY_LISTING = 'directoryListing'
    SELECT_MULTIPLE = 'selectMultiple'

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        self._files = value

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, files: Array = null):
        super().__init__(type, bubbles, cancelable)
        self.files = Array() if files is null else files


class FocusEvent(Event):
    # TODO: Implement isRelatedObjectInaccessible
    FOCUS_IN = 'focusIn'
    FOCUS_OUT = 'focusOut'
    KEY_FOCUS_CHANGE = 'keyFocusChange'
    MOUSE_FOCUS_CHANGE = 'mouseFocusChange'

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = String(value)

    @property
    def isRelatedObjectInaccessible(self):
        raise NotImplementedError

    @isRelatedObjectInaccessible.setter
    def isRelatedObjectInaccessible(self, value):
        raise NotImplementedError

    @property
    def keyCode(self):
        return self._keyCode

    @keyCode.setter
    def keyCode(self, value):
        self._keyCode = uint(value)

    @property
    def relatedObject(self):
        return self._relatedObject

    @relatedObject.setter
    def relatedObject(self, value):
        self._relatedObject = value

    @property
    def shiftKey(self):
        return self._shiftKey

    @shiftKey.setter
    def shiftKey(self, value):
        self._shiftKey = Boolean(value)

    def __init__(self, type: String, bubbles: Boolean = true,
                 cancelable: Boolean = false, relatedObject = null,
                 shiftKey: Boolean = false, keyCode: uint = 0,
                 direction: String = 'none'):
        super().__init__(type, bubbles, cancelable)
        self.direction = direction
        self.keyCode = keyCode
        self.relatedObject = relatedObject
        self.shiftKey = shiftKey

    def clone(self):
        return FocusEvent(self.type, self.bubbles, self.cancelable,
                          self.relatedObject, self.shiftKey, self.keyCode,
                          self.direction)

    def toString(self):
        return self.formatToString('FocusEvent', 'type', 'bubbles',
                                   'cancelable', 'relatedObject', 'shiftKey',
                                   'keyCode')


class FullScreenEvent(ActivityEvent):
    FULL_SCREEN = 'fullScreen'
    FULL_SCREEN_INTERACTIVE_ACCEPTED = 'fullScreenInteractiveAccepted'

    @property
    def fullScreen(self):
        return self._fullscreen

    @property
    def interactive(self):
        return self._interactive

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, fullScreen: Boolean = false,
                 interactive: Boolean = false):
        super().__init__(type, bubbles, cancelable, false)
        self._fullscreen = Boolean(fullScreen)
        self._interactive = Boolean(interactive)

    def clone(self):
        return FullScreenEvent(self.type, self.bubbles, self.cancelable,
                               self.fullScreen, self.interactive)

    def toString(self):
        return self.formatToString('FullScreenEvent', 'type', 'bubbles',
                                   'cancelable', 'activating')


class GameInputEvent(ActivityEvent):
    DEVICE_ADDED = 'deviceAdded'
    DEVICE_REMOVED = 'deviceRemoved'
    DEVICE_UNUSABLE = 'deviceUnusable'

    @property
    def device(self):
        return self._device

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, device = null):
        super().__init__(type, bubbles, cancelable)
        self._device = device


class GeolocationEvent(Event):
    UPDATE = 'update'

    @property
    def altitude(self):
        return self._altitude

    @altitude.setter
    def altitude(self, value):
        self._altitude = Number(value)

    @property
    def heading(self):
        return self._heading

    @heading.setter
    def heading(self, value):
        self._heading = Number(value)

    @property
    def horizontalAccuracy(self):
        return self._horizontalAccuracy

    @horizontalAccuracy.setter
    def horizontalAccuracy(self, value):
        self._horizontalAccuracy = Number(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = Number(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = Number(value)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = Number(value)

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = Number(value)

    @property
    def verticalAccuracy(self):
        return self._verticalAccuracy

    @verticalAccuracy.setter
    def verticalAccuracy(self, value):
        self._verticalAccuracy = Number(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, latitude: Number = 0,
                 longitude: Number = 0, altitude: Number = 0,
                 hAccuracy: Number = 0, vAccuracy: Number = 0,
                 speed: Number = 0, heading: Number = 0,
                 timestamp: Number = 0):
        super().__init__(type, bubbles, cancelable)
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.horizontalAccuracy = hAccuracy
        self.verticalAccuracy = vAccuracy
        self.speed = speed
        self.heading = heading
        self.timestamp = timestamp

    def clone(self):
        return GeolocationEvent(self.type, self.bubbles, self.cancelable,
                                self.latitude, self.longitude, self.altitude,
                                self.horizontalAccuracy,
                                self.verticalAccuracy, self.speed,
                                self.heading, self.timestamp)

    def toString(self):
        return self.formatToString('GeolocationEvent', 'type', 'bubbles',
                                   'cancelable', 'latitude', 'longitude',
                                   'altitude', 'horizontalAccuracy',
                                   'verticalAccuracy', 'speed', 'heading',
                                   'timestamp')


class GestureEvent(Event):
    GESTURE_TWO_FINGER_TAP = 'gestureTwoFingerTap'

    @property
    def altKey(self):
        return self._altKey

    @altKey.setter
    def altKey(self, value):
        self._altKey = Boolean(value)

    @property
    def commandKey(self):
        return self._commandKey

    @commandKey.setter
    def commandKey(self, value):
        self._commandKey = Boolean(value)

    @property
    def controlKey(self):
        return self._controlKey

    @controlKey.setter
    def controlKey(self, value):
        self._controlKey = Boolean(value)

    @property
    def ctrlKey(self):
        return self._ctrlKey

    @ctrlKey.setter
    def ctrlKey(self, value):
        self._ctrlKey = Boolean(value)

    @property
    def localX(self):
        return self._localX

    @localX.setter
    def localX(self, value):
        self._localX = Number(value)

    @property
    def localY(self):
        return self._localY

    @localY.setter
    def localY(self, value):
        self._localY = Number(value)

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        # TODO: Use "value not in GesturePhase" once "in" is implemented
        #       properly for Object and _AS3_CONSTANTSOBJECT
        if value not in {'all', 'begin', 'end', 'update'}:
            raise
        self._phase = String(value)

    @property
    def shiftKey(self):
        return self._shiftKey

    @shiftKey.setter
    def shiftKey(self, value):
        self._shiftKey = Boolean(value)

    @property
    def stageX(self):
        raise NotImplementedError

    @property
    def stageY(self):
        raise NotImplementedError

    def __init__(self, type: String, bubbles: Boolean = true,
                 cancelable: Boolean = false, phase: String = null,
                 localX: Number = 0, localY: Number = 0,
                 ctrlKey: Boolean = false, altKey: Boolean = false,
                 shiftKey: Boolean = false, commandKey: Boolean = false,
                 controlKey: Boolean = false):
        super().__init__(type, bubbles, cancelable)
        self.phase = phase
        self.localX = localX
        self.localY = localY
        self.ctrlKey = ctrlKey
        self.altKey = altKey
        self.shiftKey = shiftKey
        self.commandKey = commandKey
        self.controlKey = controlKey

    def clone(self):
        raise NotImplementedError

    def toString(self):
        return self.formatToString('GestureEvent', 'phase', 'localX',
                                   'localY', 'ctrlKey', 'altKey', 'shiftKey',
                                   'commandKey', 'controlKey')

    def updateAfterEvent(self):
        raise NotImplementedError


class GesturePhase(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
    ALL = 'all'
    BEGIN = 'begin'
    END = 'end'
    UPDATE = 'update'


class HTMLUncaughtScriptExceptionEvent(Event):
    UNCAUGHT_SCRIPT_EXCEPTION = ''  # TODO

    @property
    def exceptionValue(self):
        return self._exceptionValue

    @exceptionValue.setter
    def exceptionValue(self, value):
        self._exceptionValue = value

    @property
    def stackTrace(self):
        return self._stackTrace

    @stackTrace.setter
    def stackTrace(self, value):
        raise NotImplementedError

    def __init__(self, exceptionValue):  # TODO
        super().__init__('', false, false)
        raise NotImplementedError

    def clone(self):
        raise NotImplementedError


class HTTPStatusEvent(Event):
    HTTP_RESPONSE_STATUS = 'httpResponseStatus'
    HTTP_STATUS = 'httpStatus'

    @property
    def redirected(self):
        return self._redirected

    @redirected.setter
    def redirected(self, value):
        self._redirected = Boolean(value)

    @property
    def responseHeaders(self):
        return self._responseHeaders

    @responseHeaders.setter
    def responseHeaders(self, value: list):
        self._responseHeaders = value

    @property
    def responseURL(self):
        return self._responseURL

    @responseURL.setter
    def responseURL(self, value):
        self._responseURL = String(value)

    @property
    def status(self):
        return self._status

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, status: int = 0,
                 redirected: Boolean = false):
        super().__init__(type, bubbles, cancelable)
        self._status = int(status)
        self.redirected = redirected
        self.responseHeaders = Array()
        self.responseURL = ''

    def clone(self):
        return HTTPStatusEvent(self.type, self.bubbles, self.cancelable,
                               self.status, self.redirected)

    def toString(self):
        return self.formatToString('HTTPStatusEvent', 'type', 'bubbles',
                                   'cancelable', 'status')


class IMEEvent(TextEvent):
    IME_COMPOSITION = 'imeComposition'
    IME_START_COMPOSITION = 'imeStartComposition'

    @property
    def imeClient(self):
        return self._imeClient

    @imeClient.setter
    def imeClient(self, value):
        self._imeClient = value

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, text: String = '',
                 imeClient = null):
        super().__init__(type, bubbles, cancelable, text)
        self.imeClient = imeClient

    def clone(self):
        return IMEEvent(self.type, self.bubbles, self.cancelable, self.text,
                        self.imeClient)

    def toString(self):
        return self.formatToString('IMEEvent', 'type', 'bubbles',
                                   'cancelable', 'text')  # imeClient


class InvokeEvent(Event):
    INVOKE = 'invoke'

    @property
    def arguments(self):
        return self._argv

    @property
    def currentDirectory(self):
        return self._dir

    @property
    def reason(self):
        return self._reason

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, dir = null, argv: Array = null,
                 reason: String = 'standard'):
        super().__init__(type, bubbles, cancelable)
        self._dir = dir
        self._argv = argv
        self._reason = reason

    def clone(self):
        return InvokeEvent(self.type, self.bubbles, self.cancelable,
                           self.currentDirectory, self.arguements,
                           self.reason)


class IOErrorEvent(ErrorEvent):
    IO_ERROR = 'ioError'
    STANDARD_ERROR_IO_ERROR = 'standardErrorIoError'
    STANDARD_INPUT_IO_ERROR = 'standardInputIoError'
    STANDARD_OUTPUT_IO_ERROR = 'standardOutputIoError'

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, text: String = '', id: int = 0):
        super().__init__(type, bubbles, cancelable, text, id)

    def clone(self):
        return IOErrorEvent(self.type, self.bubbles, self.cancelable,
                            self.text, self.errorID)

    def toString(self):
        return self.formatToString('IOErrorEvent', 'type', 'bubbles',
                                   'cancelable', 'text', 'errorID')


class KeyboardEvent(Event):
    KEY_DOWN = 'keyDown'
    KEY_UP = 'keyUp'

    @property
    def altKey(self):
        return self._altKey

    @altKey.setter
    def altKey(self, value):
        self._altKey = Boolean(value)

    @property
    def charCode(self):
        return self._charCode

    @charCode.setter
    def charCode(self, value):
        self._charCode = uint(value)

    @property
    def commandKey(self):
        return self._commandKey

    @commandKey.setter
    def commandKey(self, value):
        self._commandKey = Boolean(value)

    @property
    def controlKey(self):
        return self._controlKey

    @controlKey.setter
    def controlKey(self, value):
        self._controlKey = Boolean(value)

    @property
    def ctrlKey(self):  # TODO
        raise NotImplementedError
        #if as3state.platform == 'Darwin':
        #   return self.commandKey or self.controlKey
        #return self.controlKey

    @ctrlKey.setter
    def ctrlKey(self, value):
        raise NotImplementedError

    @property
    def keyCode(self):
        return self._keyCode

    @keyCode.setter
    def keyCode(self, value):
        self._keyCode = uint(value)

    @property
    def keyLocation(self):
        return self._keyLocation

    @keyLocation.setter
    def keyLocation(self, value):
        self._keyLocation = uint(value)

    @property
    def shiftKey(self):
        return self._shiftKey

    @shiftKey.setter
    def shiftKey(self, value):
        self._shiftKey = Boolean(value)

    def __init__(self, type: String, bubbles: Boolean = true,
                 cancelable: Boolean = false, charCodeValue: uint = 0,
                 keyCodeValue: uint = 0, keyLocationValue: uint = 0,
                 ctrlKeyValue: Boolean = false, altKeyValue: Boolean = false,
                 shiftKeyValue: Boolean = false,
                 controlKeyValue: Boolean = false,
                 commandKeyValue: Boolean = false):
        super().__init__(type, bubbles, cancelable)
        self.altKey = altKeyValue
        self.charCode = charCodeValue
        self.commandKey = commandKeyValue
        self._controlKey = controlKeyValue  # TODO
        self.ctrlKey = ctrlKeyValue
        self.keyCode = keyCodeValue
        self.keyLocation = keyLocationValue
        self.shiftKey = shiftKeyValue

    def clone(self):
        return KeyboardEvent(self.type, self.bubbles, self.cancelable,
                             self.charCode, self.keyCode, self.keyLocation,
                             self.ctrlKey, self.altKey, self.shiftKey,
                             self.controlKey, self.commandKey)

    def toString(self):
        return self.formatToString('KeyboardEvent', 'type', 'bubbles',
                                   'cancelable', 'altKey', 'charCode',
                                   'commandKey', 'controlKey', 'ctrlKey',
                                   'keyCode', 'keyLocation', 'shiftKey')

    def updateAfterEvent(self):
        raise NotImplementedError


class LocationChangeEvent(Event):
    LOCATION_CHANGE = 'locationChange'
    LOCATION_CHANGING = 'locationChanging'

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = String(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, location: String = null):
        super().__init__(type, bubbles, cancelable)
        self.location = location

    def clone(self):
        return LocationChangeEvent(self.type, self.bubbles, self.cancelable,
                                   self.location)

    def toString(self):
        return self.formatToString('LocationChangeEvent', 'type', 'bubbles',
                                   'cancelable', 'location')


class MediaEvent(Event):
    COMPLETE = String('complete')
    SELECT = String('select')

    @property
    def data(self):
        return self._data

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, data = null):
        super().__init__(type, bubbles, cancelable)
        self._data = data

    def clone(self):
        return MediaEvent(self.type, self.bubbles, self.cancelable, self.data)

    def toString(self):
        return self.formatToString('MediaEvent', 'type', 'bubbles',
                                   'cancelable', 'data'))


class MouseEvent(Event):
    CLICK = String('click')
    CONTEXT_MENU = String('contextMenu')
    DOUBLE_CLICK = String('doubleClick')
    MIDDLE_CLICK = String('middleClick')
    MIDDLE_MOUSE_DOWN = String('middleMouseDown')
    MIDDLE_MOUSE_UP = String('middleMouseUp')
    MOUSE_DOWN = String('mouseDown')
    MOUSE_MOVE = String('mouseMove')
    MOUSE_OUT = String('mouseOut')
    MOUSE_OVER = String('mouseOver')
    MOUSE_UP = String('mouseUp')
    MOUSE_WHEEL = String('mouseWheel')
    RELEASE_OUTSIDE = String('releaseOutside')
    RIGHT_CLICK = String('rightClick')
    RIGHT_MOUSE_DOWN = String('rightMouseDown')
    RIGHT_MOUSE_UP = String('rightMouseUp')
    ROLL_OUT = String('rollOut')
    ROLL_OVER = String('rollOver')

    @property
    def altKey(self):
        return self._altKey

    @altKey.setter
    def altKey(self, value):
        self._altKey = Boolean(value)

    @property
    def buttonDown(self):
        return self._buttonDown

    @buttonDown.setter
    def buttonDown(self, value):
        self._buttonDown = Boolean(value)

    @property
    def clickCount(self):
        return self._clickCount

    @property
    def commandKey(self):
        return self._commandKey

    @commandKey.setter
    def commandKey(self, value):
        self._commandKey = Boolean(value)

    @property
    def controlKey(self):
        return self._controlKey

    @controlKey.setter
    def controlKey(self, value):
        self._controlKey = Boolean(value)

    @property
    def ctrlKey(self):
        return self._ctrlKey

    @ctrlKey.setter
    def ctrlKey(self, value):
        self._ctrlKey = Boolean(value)

    @property
    def delta(self):
        return self._delta

    @delta.setter
    def delta(self, value):
        self._delta = int(value)

    @property
    def isRelatedObjectInaccessible(self):
        raise NotImplementedError

    @isRelatedObjectInaccessible.setter
    def isRelatedObjectInaccessible(self, value):
        raise NotImplementedError

    @property
    def localX(self):
        return self._localX

    @localX.setter
    def localX(self, value):
        self._localX = Number(value)

    @property
    def localY(self):
        return self._localY

    @localY.setter
    def localY(self, value):
        self._localY = Number(value)

    @property
    def movementX(self):
        return self._movementX

    @movementX.setter
    def movementX(self, value):
        self._movementX = Number(value)

    @property
    def movementY(self):
        return self._movementY

    @movementY.setter
    def movementY(self, value):
        self._movementY = Number(value)

    @property
    def relatedObject(self):
        return self._relatedObject

    @relatedObject.setter
    def relatedObject(self, value):
        raise NotImplementedError

    @property
    def shiftKey(self):
        return self._shiftKey

    @shiftKey.setter
    def shiftKey(self, value):
        self._shiftKey = Boolean(value)

    @property
    def stageX(self):
        raise NotImplementedError

    @property
    def stageY(self):
        raise NotImplementedError

    def __init__(self, type: String, bubbles: Boolean = true,
                 cancelable: Boolean = false, localX: Number = NaN,
                 localY: Number = NaN, relatedObject = null,
                 ctrlKey: Boolean = false, altKey: Boolean = false,
                 shiftKey: Boolean = false, buttonDown: Boolean = false,
                 delta: int = 0, commandKey: Boolean = false,
                 controlKey: Boolean = false, clickCount: int = 0):
        super().__init__(type, bubbles, cancelable)
        self.localX = localX
        self.localY = localY
        self._relatedObject = relatedObject
        self.ctrlKey = ctrlKey
        self.altKey = altKey
        self.shiftKey = shiftKey
        self.buttonDown = buttonDown
        self.delta = delta
        self.commandKey = commandKey
        self.controlKey = controlKey
        self._clickCount = int(clickCount)

    def clone(self):
        return MouseEvent(self.type, self.bubbles, self.cancelable,
                          self.localX, self.localY, self.relatedObject,
                          self.ctrlKey, self.altKey, self.shiftKey,
                          self.buttonDown, self.delta, self.commandKey,
                          self.controlKey, self.clickCount)

    def toString(self):
        raise NotImplementedError

    def updateAfterEvent(self):
        raise NotImplementedError


class NativeDragEvent(MouseEvent):
    NATIVE_DRAG_COMPLETE =  String('')
    NATIVE_DRAG_DROP = String('')
    NATIVE_DRAG_ENTER = String('')
    NATIVE_DRAG_EXIT = String('')
    NATIVE_DRAG_OVER = String('')
    NATIVE_DRAG_START = String('')
    NATIVE_DRAG_UPDATE = String('')

    @property
    def allowedActions(self):
        return self._allowedActions

    @allowedActions.setter
    def allowedActions(self, value):
        self._allowedActions = value

    @property
    def clipboard(self):
        return self._clipboard

    @clipboard.setter
    def clipboard(self, value):
        self._clipboard = value

    @property
    def dropAction(self):
        return self._dropAction

    @dropAction.setter
    def dropAction(self, value):
        self._dropAction = String(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = true, localX: Number = NaN,
                 localY: Number = NaN, relatedObject = null, clipboard = null,
                 allowedActions = null, dropAction: String = null,
                 controlKey: Boolean = false, altKey: Boolean = false,
                 shiftKey: Boolean = false, commandKey: Boolean = false):
        super().__init__(type, bubbles, cancelable, localX, localY,
                         relatedObject, false, altKey, shiftKey, false, 0,
                         commandKey, controlKey, 0)
        self.allowedActions = allowedActions
        self.dropAction = dropAction
        self.clipboard = clipboard

    def clone(self):
        return NativeDragEvent(self.type, self.bubbles, self.cancelable,
                               self.localX, self.localY, self.relatedObject,
                               self.clipboard, self.allowedActions,
                               self.dropAction, self.controlKey, self.altKey,
                               self.shiftKey, self.commandKey)

    def toString(self):
        return self.formatToString('NativeDragEvent', 'type', 'bubbles',
                                   'cancelable', 'localX', 'localY',
                                   'relatedObject', 'clipboard',
                                   'allowedActions', 'dropAction',
                                   'controlKey', 'altKey', 'shiftKey',
                                   'commandKey')


class NativeProcessExitEvent(Event):
    EXIT = String('exit')

    @property
    def exitCode(self):
        return self._exitCode

    @exitCode.setter
    def exitCode(self, value):
        self._exitCode = Number(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, exitCode: Number = NaN):
        super().__init__(type, bubbles, cancelable)
        self.exitCode = exitCode

    def clone(self):
        return NativeProcessExitEvent(self.type, self.bubbles,
                                      self.cancelable, self.exitCode)

    def toString(self):
        return self.formatToString('NativeProcessExitEvent', 'type',
                                   'bubbles', 'cancelable', 'exitCode')


class NativeWindowBoundsEvent(Event):
    MOVE = String('move')
    MOVING = String('moving')
    RESIZE = String('resize')
    RESIZING = String('resizing')

    @property
    def afterBounds(self):
        return self._afterBounds

    @property
    def beforeBounds(self):
        return self._beforeBounds

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, beforeBounds: Rectangle = null,
                 afterBounds: Rectangle = null):
        super().__init__(type, bubbles, cancelable)
        # TODO: Type checks
        self._beforeBounds = beforeBounds
        self._afterBounds = afterBounds

    def clone(self):
        return NativeWindowBoundsEvent(self.type, self.bubbles,
                                       self.cancelable, self.beforeBounds,
                                       self.afterBounds)

    def toString(self):
        return f'[NativeWindowBoundsEvent type={self.type} bubbles={self.bubbles} cancelable={self.cancelable} previousDisplayState={self.beforeBounds} currentDisplayState={self.afterBounds}]'


class NativeWindowDisplayStateEvent(Event):
    DISPLAY_STATE_CHANGE = String('displayStateChange')
    DISPLAY_STATE_CHANGING = String('displayStateChanging')

    @property
    def afterDisplayState(self):
        return self._afterDisplayState

    @property
    def beforeDisplayState(self):
        return self._beforeDisplayState

    def __init__(self, type: String, bubbles: Boolean = true,
                 cancelable: Boolean = false, beforeDisplayState: String = '',
                 afterDisplayState: String = ''):
        super().__init__(type, bubbles, cancelable)
        self._beforeDisplayState = String(beforeDisplayState)
        self._afterDisplayState = String(afterDisplayState)

    def clone(self):
        return NativeWindowDisplayStateEvent(self.type, self.bubbles,
                                             self.cancelable,
                                             self.beforeDisplayState,
                                             self.afterDisplayState)

    def toString(self):
        return self.formatToString('NativeWindowDisplayStateEvent', 'type',
                                   'bubbles', 'cancelable',
                                   'beforeDisplayState', 'afterDisplayState')


class NetDataEvent(Event):
    MEDIA_TYPE_DATA = String('mediaTypeData')

    @property
    def info(self):
        return self._info

    @property
    def timestamp(self):
        return self._timestamp

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, timestamp: Number = 0,
                 info: Object = null):
        super().__init__(type, bubbles, cancelable)
        self._timestamp = Number(timestamp)
        self._info = info

    def clone(self):
        return NetDataEvent(self.type, self.bubbles, self.cancelable,
                            self.timestamp, self.info)

    def toString(self):
        return self.formatToString('NetDataEvent', 'type', 'bubbles',
                                   'cancelable', 'timestamp')


class NetMonitorEvent(Event):
    NET_STREAM_CREATE = String('netStreamCreate')

    @property
    def netStream(self):
        return self._netStream

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, netStream = null):
        super().__init__(type, bubbles, cancelable)
        self._netStream = netSteam

    def clone(self):
        return NetMonitorEvent(self.type, self.bubbles, self.cancelable,
                               self.netStream)

    def toString(self):
        return self.formatToString('NetMonitorEvent', 'type', 'bubbles',
                                   'cancelable', 'netStream')


class NetStatusEvent(Event):
    NET_STATUS = String('netStatus')

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, value):
        self._info = value

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, info: Object = null):
        super().__init__(type, bubbles, cancelable)
        self.info = info

    def clone(self):
        return NetStatusEvent(self.type, self.bubbles, self.cancelable,
                              self.info)

    def toString(self):
        return self.formatToString('NetStatusEvent', 'type', 'bubbles',
                                   'cancelable', 'info')


class OutputProgressEvent(Event):
    OUTPUT_PROGRESS = String('outputProgress')

    @property
    def bytesPending(self):
        return self._bytesPending

    @bytesPending.setter
    def bytesPending(self, value):
        self._bytesPending = Number(value)

    @property
    def bytesTotal(self):
        return self._bytesTotal

    @bytesTotal.setter
    def bytesTotal(self, value):
        self._bytesTotal = Number(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, bytesPending: Number = 0,
                 bytesTotal: Number = 0):
        super().__init__(type, bubbles, cancelable)
        self.bytesPending = bytesPending
        self.bytesTotal = bytesTotal

    def clone(self):
        return OutputProgressEvent(self.type, self.bubbles, self.cancelable,
                                   self.bytesPending, self.bytesTotal)

    def toString(self):
        return self.formatToString('OutputProgressEvent', 'type', 'bubbles',
                                   'cancelable', 'bytesPending', 'bytesTotal')


class PermissionEvent(Event):
    # TODO: figure out where permission information is stored
    PERMISSION_STATUS = 'permissionStatus'

    @property
    def status(self):
        return self._status

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, status: String = 'denied'):
        super().__init__(type, bubbles, cancelable)
        self._status = String(status)

    def clone(self):
        return PermissionEvent(self.type, self.bubbles, self.cancelable,
                               self.status)

    def toString(self):
        return String(f'[PermissionEvent type={self.type} bubbles={self.bubbles} cancelable={self.cancelable} permission= status={self.status}]')


class PressAndTapGestureEvent(GestureEvent):
    GESTURE_PRESS_AND_TAP = String('gesturePressAndTap')

    @property
    def tapLocalX(self):
        return self._tapLocalX

    @tapLocalX.setter
    def tapLocalX(self, value):
        self._tapLocalX = Number(value)

    @property
    def tapLocalY(self):
        return self._tapLocalY

    @tapLocalY.setter
    def tapLocalY(self, value):
        self._tapLocalY = Number(value)

    @property
    def tapStageX(self):
        raise NotImplementedError

    @property
    def tapStageY(self):
        raise NotImplementedError

    def __init__(self, type: String, bubbles: Boolean = true,
                 cancelable: Boolean = false, phase: String = null,
                 localX: Number = 0, localY: Number = 0,
                 tapLocalX: Number = 0, tapLocalY: Number = 0,
                 ctrlKey: Boolean = false, altKey: Boolean = false,
                 shiftKey: Boolean = false, commandKey: Boolean = false,
                 controlKey: Boolean = false):
        super().__init__(type, bubbles, cancelable, phase, localX, localY,
                         ctrlKey, altKey, shiftKey, commandKey, controlKey)
        self.tapLocalX = tapLocalX
        self.tapLocalY = tapLocalY

    def clone(self):
        return PressAndTapGestureEvent(self.type, self.bubbles,
                                       self.cancelable, self.phase,
                                       self.localX, self.localY,
                                       self.tapLocalX, self.tapLocalY,
                                       self.ctrlKey, self.altKey,
                                       self.shiftKey, self.commandKey,
                                       self.controlKey)

    def toString(self):
        raise NotImplementedError


class ProgressEvent(Event):
    PROGRESS = 'progress'
    SOCKET_DATA = 'socketData'
    STANDARD_ERROR_DATA = 'standardErrorData'
    STANDARD_INPUT_PROGRESS = 'standardInputProgress'
    STANDARD_OUTPUT_DATA = 'standardOutputData'

    @property
    def bytesLoaded(self):
        return self._bytesLoaded

    @bytesLoaded.setter
    def bytesLoaded(self, value):
        self._bytesLoaded = Number(value)

    @property
    def bytesTotal(self):
        return self._bytesTotal

    @bytesTotal.setter
    def bytesTotal(self, value):
        self._bytesTotal = Number(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, bytesLoaded: Number = 0,
                 bytesTotal: Number = 0):
        super().__init__(type, bubbles, cancelable)
        self.bytesLoaded = bytesLoaded
        self.bytesTotal = bytesTotal

    def clone(self):
        return ProgressEvent(self.type, self.bubbles, self.cancelable,
                             self.bytesLoaded, self.bytesTotal)

    def toString(self):
        return self.formatToString('ProgressEvent', 'type', 'bubbles',
                                   'cancelable', 'bytesLoaded', 'bytesTotal')


class RemoteNotificationEvent(Event):
    NOTIFICATION + String('notification')
    TOKEN = String('token')

    @property
    def data(self):
        return self._data

    @property
    def tokenId(self):
        return self._tokenId

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, data: Object = null,
                 tokenId: String = null):
        super().__init__(type, bubbles, cancelable)
        self._data = data
        self._tokenId = String(tokenId)


class SampleDataEvent(Event):
    SAMPLE_DATA = String('sampleData')

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        raise NotImplementedError

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = Number(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, theposition: Number = 0,
                 thedata = null):
        super().__init__(type, bubbles, cancelable)
        self.position = theposition
        self._data = thedata

    def clone(self):
        return SampleDataEvent(self.type, self.bubbles, self.cancelable,
                               self.position, self.data)

    def toString(self):
        raise NotImplementedError


class ScreenMouseEvent(MouseEvent):
    CLICK = String('click')
    MOUSE_DOWN = String('mouseDown')
    MOUSE_UP = String('mouseUp')
    RIGHT_CLICK = String('rightClick')
    RIGHT_MOUSE_DOWN = String('rightMouseDown')
    RIGHT_MOUSE_UP = String('rightMouseUp')

    @property
    def screenX(self):
        return self._screenX

    @property
    def screenY(self):
        return self._screenY

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, screenX: Number = NaN,
                 screenY: Number = NaN, ctrlKey: Boolean = false,
                 altKey: Boolean = false, shiftKey: Boolean = false,
                 buttonDown: Boolean = false, commandKey: Boolean = false,
                 controlKey: Boolean = false):
        super().__init__(type, bubbles, cancelable, NaN, NaN, null, ctrlKey,
                         altKey, shiftKey, buttonDown, 0, commandKey,
                         controlKey, 0)
        self._screenX = Number(screenX)
        self._screenY = Number(screenY)

    def clone(self):
        return ScreenMouseEvent(self.type, self.bubbles, self.cancelable,
                                self.screenX, self.screenY, self.ctrlKey,
                                self.altKey, self.shiftKey, self.buttonDown,
                                self.commandKey, self.controlKey)

    def toString(self):
        return self.formatToString('ScreenMouseEvent', 'type', 'bubbles',
                                   'cancelable', 'screenX', 'screenY',
                                   'ctrlKey', 'altKey', 'shiftKey',
                                   'buttonDown', 'commandKey', 'controlKey')


class SecurityErrorEvent(ErrorEvent):
    SECURITY_ERROR = 'securityError'

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, text: String = '', id: int = 0):
        super().__init__(type, bubbles, cancelable, text, id)

    def clone(self):
        return SecurityErrorEvent(self.type, self.bubbles, self.cancelable,
                                  self.text, self.errorID)

    def toString(self):
        return self.formatToString('SecurityErrorEvent', 'type', 'bubbles',
                                   'cancelable', 'text', 'errorID')


class ServerSocketConnectEvent(Event):
    CONNECT = String('connect')

    @property
    def socket(self):
        return self._sockeet

    @socket.setter
    def socket(self, value):
        self._socket = String(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, socket: String = null):
        super().__init__(type, bubbles, cancelable)
        self.socket = socket

    def clone(self):
        return ServerSocketConnectEvent(self.type, self.bubbles,
                                        self.cancelable, self.socket)

    def toString(self):
        return self.formatToString('ServerSocketConnectEvent', 'type',
                                   'bubbles', 'cancelable', 'socket')


class ShaderEvent(Event):
    COMPLETE = String('complete')

    @property
    def bitmapData(self):
        return self._bitmapData

    @bitmapData.setter
    def bitmapData(self, value):
        raise NotImplementedError

    @property
    def byteArray(self):
        return self._byteArray

    @byteArray.setter
    def byteArray(self, value):
        raise NotImplementedError

    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, value):
        raise NotImplementedError

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, bitmap = null, array = null,
                 vector = null):
        super().__init__(type, bubbles, cancelable)
        self._bitmapData = bitmap
        self._byteArray = array
        self._vector = vector

    def clone(self):
        return ShaderEvent(self.type, self.bubbles, self.cancelable,
                           self.bitmapData, self.byteArray, self.vector)

    def toString(self):
        return self.formatToString('ShaderEvent', 'type', 'bubbles',
                                   'cancelable', 'bitmapData', 'byteArray',
                                   'vector')


class SoftKeyboardEvent(Event):
    SOFT_KEYBOARD_ACTIVATE = String('softKeyboardActivate')
    SOFT_KEYBOARD_ACTIVATING = String('softKeyboardActivating')
    SOFT_KEYBOARD_DEACTIVATE = String('softKeyboardDeactivate')

    @property
    def relatedObject(self):
        return self._relatedObject

    @relatedObject.setter
    def relatedObject(self, value):
        self._relatedObject = value

    @property
    def triggerType(self):
        return self._triggerType

    def __init__(self, type: String, bubbles: Boolean, cancelable: Boolean,
                 relatedObjectVal, triggerTypeVal: String):
        super().__init__(type, bubbles, cancelable)
        self.relatedObject = relatedObjectVal
        self._triggerType = triggerTypeVal

    def clone(self):
        return SoftKeyboardEvent(self.type, self.bubbles, self.cancelable,
                                 self.relatedObject, self.triggerType)

    def toString(self):
        raise NotImplementedError


class SoftKeyboardTrigger(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
    CONTENT_TRIGGERED = 'contentTriggered'
    USER_TRIGGERED = 'userTriggered'


class SQLErrorEvent(ErrorEvent):
    ERROR = 'error'

    @property
    def error(self):
        return self._error

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, error: SQLError = null):
        if not isinstance(error, SQLError):
            raise TypeError
        # TODO: Determine if text and ID are taken from error
        super().__init__(type, bubbles, error)  # <text>, <ID>
        self._error = error

    def clone(self):
        return SQLErrorEvent(self.type, self.bubbles, self.cancelable,
                             self.error)

    def toString(self):
        return self.formatToString('SQLErrorEvent', 'type', 'bubbles',
                                   'cancelable', 'error')


class SQLEvent(Event):
    ANALYZE = 'analyze'
    ATTACH = 'attach'
    BEGIN = 'begin'
    CANCEL = 'cancel'
    CLOSE = 'close'
    COMMIT = 'commit'
    COMPACT = 'compact'
    DEANALYZE = 'deanalyze'
    DETACH = 'detach'
    OPEN = 'open'
    REENCRYPT = 'reencrypt'
    RELEASE_SAVEPOINT = 'releaseSavepoint'
    RESULT = 'result'
    ROLLBACK = 'rollback'
    ROLLBACK_TO_SAVEPOINT = 'rollbackToSavepoint'
    SCHEMA = 'schema'
    SET_SAVEPOINT = 'setSavepoint'

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false):
        super().__init__(type, bubbles, cancelable)

    def clone(self):
        return SQLEvent(self.type, self.bubbles, self.cancelable)


class SQLUpdateEvent(Event):
    DELETE = 'delete'
    INSERT = 'insert'
    UPDATE = 'update'

    @property
    def rowID(self):
        return self._rowID

    @property
    def table(self):
        return self._table

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, table: String = null,
                 rowID: Number = 0):
        super().__init__(type, bubbles, cancelable)
        self._table = table
        self._rowID = rowID

    def clone(self):
        return SQLUpdateEvent(self.type, self.bubbles, self.cancelable,
                              self.table, self.rowID)


class StageOrientationEvent(Event):
    ORIENTATION_CHANGE = 'orientationChange'
    ORIENTATION_CHANGING = 'orientationChanging'

    @property
    def afterOrientation(self):
        return self._afterOrientation

    @property
    def beforeOrientation(self):
        return self._beforeOrientation

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false,
                 beforeOrientation: String = null,
                 afterOrientation: String = null):
        super().__init__(type, bubbles, cancelable)
        self._afterOrientation = String(afterOrientation)
        self._beforeOrientation = String(beforeOrientation)

    def clone(self):
        return StageOrientationEvent(self.type, self.bubbles, self.cancelable,
                                     self.beforeOrientation,
                                     self.afterOrientation)

    def toString(self):
        raise NotImplementedError


class StageVideoAvailabilityEvent(Event):
    driver = ''  # TODO
    reason = ''  # TODO
    STAGE_VIDEO_AVAILABILITY = 'stageVideoAvailability'

    @property
    def availability(self):
        return self._availability

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, availability: String = null):
        super().__init__(type, bubbles, cancelable)
        self._availability = String(availability)


class StageVideoEvent(Event):
    codecInfo = ''  # TODO
    RENDER_STATE = 'renderState'
    RENDER_STATUS_ACCELERATED = 'accelerated'
    RENDER_STATUS_SOFTWARE = 'software'
    RENDER_STATUS_UNAVAILABLE = 'unavailable'

    @property
    def colorSpace(self):
        return self._colorSpace

    @property
    def status(self):
        return self._status

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, status: String = null,
                 colorSpace: String = null):
        super().__init__(type, bubbles, cancelable)
        self._colorSpace = String(colorSpace)
        self._status = String(status)


class StatusEvent(Event):
    STATUS = 'status'

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = String(value)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = String(value)

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, code: String = '',
                 level: String = ''):
        super().__init__(type, bubbles, cancelable)
        self.code = code
        self.level = level

    def clone(self):
        return StatusEvent(self.type, self.bubbles, self.cancelable,
                           self.code, self.level)

    def toString(self):
        return self.formatToString('StatusEvent', 'type', 'bubbles',
                                   'cancelable', 'code', 'level')


class StorageVolumeChangeEvent(Event):
    STORAGE_VOLUME_MOUNT = String('storageVolumeMount')
    STORAGE_VOLUME_UNMOUNT = String('storageVolumeUnmount')

    @property
    def rootDirectory(self):
        if self.type == StorageVolumeChangeEvent.STORAGE_VOLUME_UNMOUNT:
            return null
        raise NotImplementedError

    @property
    def storageVolume(self):
        if self.type == StorageVolumeChangeEvent.STORAGE_VOLUME_UNMOUNT:
            return null
        raise NotImplementedError

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, path = null, volume = null):
        super().__init__(type, bubbles, cancelable)
        self._path = path
        self._volume = volume

    def clone(self):
        return StorageVolumeChangeEvent(self.type, self.bubbles,
                                        self.cancelable, self.path,
                                        self.volume)

    def toString(self):
        raise NotImplementedError


class SyncEvent(Event):
    SYNC = 'sync'

    @property
    def changeList(self):
        return self._changeList

    @changeList.setter
    def changeList(self, value):
        raise NotImplementedError

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, changeList: Array = null):
        super().__init__(type, bubbles, cancelable)
        self._changeList = changeList

    def clone(self):
        return SyncEvent(self.type, self.bubbles, self.cancelable,
                         self.changeList)

    def toString(self):
        return f'[SynceEvent type={self.type} bubbles={self.bubbles} cancelable={self.cancelable} list={self.changeList}]'


class ThrottleEvent(Event):
    THROTTLE = 'throttle'

    @property
    def state(self):
        return self._state

    @property
    def targetFrameRate(self):
        return self._targetFrameRate

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, state: String = null,
                 targetFrameRate: Number = 0):
        super().__init__(type, bubbles, cancelable)
        self._state = String(state)
        self._targetFrameRate = Number(targetFrameRate)

    def clone(self):
        return ThrottleEvent(self.type, self.bubbles, self.cancelable,
                             self.state, self.targetFrameRate)

    def toString(self):
        return self.formatToString('ThrottleEvent', 'type', 'bubbles',
                                   'cancelable', 'state', 'targetFrameRate')


class ThrottleType(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
    PAUSE = 'pause'
    RESUME = 'resume'
    THROTTLE = 'throttle'


class TimerEvent(Event):
    TIMER = 'timer'  # bubbles=False, cancelable=False
    TIMER_COMPLETE = 'timerComplete'  # bubbles=False, cancelable=False

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false):
        super().__init__(type, bubbles, cancelable)

    def clone(self):
        return TimerEvent(self.type, self.bubbles, self.cancelable)

    def toString(self):
        return self.formatToString('TimerEvent', 'type', 'bubbles',
                                   'cancelable')

    def updateAfterEvent(self):
        raise NotImplementedError


class TouchEvent(Event):
    def __init__(self):
        raise NotImplementedError

    def clone(self):
        raise NotImplementedError

    def getSamples(self):
        raise NotImplementedError

    def isToolButtonDown(self):
        raise NotImplementedError

    def toString(self):
        raise NotImplementedError

    def updateAfterEvent(self):
        raise NotImplementedError


class TouchEventIntent(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
    ERASER = 'eraser'
    PEN = 'pen'
    UNKNOWN = 'unknown'


class TransformGestureEvent(GestureEvent):
    GESTURE_DIRECTION_TAP = String('gestureDirectionTap')
    GESTURE_PAN = String('gesturePan')
    GESTURE_ROTATE = String('gestureRotate')
    GESTURE_SWIPE = String('gestureSwipe')
    GESTURE_ZOOM = String('gestureZoom')

    def __init__(self):
        raise NotImplementedError

    def clone(self):
        raise NotImplementedError

    def toString(self):
        raise NotImplementedError


class UncaughtErrorEvent(ErrorEvent):
    UNCAUGHT_ERROR = 'uncaughtError'

    @property
    def error(self):
        return self._error

    def __init__(self, type: String, bubbles: Boolean = true,
                 cancelable: Boolean = true, error_in = null):
        # TODO: Check to see if text and errorID are retrieved from error_in
        super().__init__(type, bubbles, cancelable)  # , <text>, <ID>
        self._error = error_in

    def clone(self):
        return UncaughtErrorEvent(self.type, self.bubbles, self.cancelable,
                                  self.error)

    def toString(self):
        raise NotImplementedError


class UncaughtErrorEvents(EventDispatcher):
    def __init__(self):
        raise NotImplementedError


class VideoEvent(Event):
    codecInfo = String()  # TODO
    RENDER_STATE = 'renderState'
    RENDER_STATUS_ACCELERATED = 'accelerated'
    RENDER_STATUS_SOFTWARE = 'software'
    RENDER_STATUS_UNAVAILABLE = 'unavailable'

    @property
    def status(self):
        return self._status

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, status: String = null):
        super().__init__(type, bubbles, cancelable)
        self._status = String(status)


class VideoTextureEvent(Event):
    RENDER_STATE = 'renderState'

    @property
    def colorSpace(self):
        return self._colorSpace

    @property
    def status(self):
        return self._status

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, status: String = null,
                 colorSpace: String = null):
        super().__init__(type, bubbles, cancelable)
        self._status = String(status)
        self._colorSpace = String(colorSpace)


class VsyncStateChangeAvailabilityEvent:
    VSYNC_STATE_CHANGE_AVAILABILITY = 'vSyncStateChangeAvailability'

    @property
    def available(self):
        return self._available

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, available: Boolean = false):
        super().__init__(type, bubbles, cancelable)
        self._available = Boolean(available)

    def clone(self):
        return VsyncStateChangeAvailabilityEvent(self.type, self.bubbles,
                                                 self.cancelable,
                                                 self.available)

    def toString(self):
        return self.formatToString('VsyncStateChangeAvailabilityEvent',
                                   'type', 'bubbles', 'cancelable',
                                   'available')
