from as3lib import (Array, as3state, Boolean, Error, false, int, metaclasses,
                    Number, null, Object, String, true, TypeError, uint)
from as3lib.flash.errors import SQLError
from copy import copy


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


# BaseEvent
# TODO: Find a way to combine _AS3_BASEEVENT with Event without polluting
#       child classes with inherited constants
class _AS3_BASEEVENT:
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

   def __init__(self, type, bubbles=false, cancelable=false):
      if type not in _HELPER_GetEventConstants(self.__class__):
         raise Exception('Provided event type is not valid for this object')
      self._type = String(type)
      self._bubbles = Boolean(bubbles)
      self._cancelable = Boolean(cancelable)
      self._currentTarget = null
      self._target = null
      self._eventPhase = null
      self._preventDefault = false

   def __eq__(self, value):
      return self.type == value

   def __str__(self):
      return self.toString()

   def clone(self):
      return copy(self)

   def formatToString(self, className, *arguements):
      return String(''.join(['[', className] + [f' {i}={getattr(self, i)}' for i in arguements] + [']']))

   def isDefaultPrevented(self):
      return self._preventDefault

   def preventDefault(self):
      if self.cancelable:
         self._preventDefault = true

   def stopImmediatePropagation(self):
      raise NotImplementedError

   def stopPropagation(self):
      raise NotImplementedError

   def toString(self):
      return self.formatToString('Event', 'type', 'bubbles', 'cancelable')


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
class Event(_AS3_BASEEVENT):
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


class EventDispatcher(Object):
   # TODO: Implement priority, weakReference

   def __init__(self, target: IEventDispatcher = null):
      # TODO: Implement target
      self._events = {}
      self._eventsCapture = {}

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
      if not event.isDefaultPrevented() and event.type in self._events:
         e = event.clone()
         e._target = self
         for i in self._events[event.type]:
            i(e)
         return True
      return False

   def hasEventListener(self, type: String):
      type = String(type)
      return type in self._events.get(type) or type in self._eventsCapture

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
      raise NotImplementedError


class TextEvent(_AS3_BASEEVENT):
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
      return self.formatToString('TextEvent', 'type', 'bubbles', 'cancelable', 'text')


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
      return self.formatToString('ErrorEvent', 'type', 'bubbles', 'cancelable', 'text', 'errorID')


class AccelerometerEvent(_AS3_BASEEVENT):
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
      return self.formatToString('AccelerometerEvent', 'type', 'bubbles', 'cancelable', 'timestamp', 'accelerationX', 'accelerationY', 'accelerationZ')


class ActivityEvent(_AS3_BASEEVENT):
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
      return self.formatToString('ActivityEvent', 'type', 'bubbles', 'cancelable', 'activating')


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
      return AsyncErrorEvent(self.type, self.bubbles, self.cancelable, self.text,
                       self.error)

   def toString(self):
      return self.formatToString('AsyncErrorEvent', 'type', 'bubbles', 'cancelable', 'text', 'error', 'errorID')


class AudioOutputChangeEvent(_AS3_BASEEVENT):
   AUDIO_OUTPUT_CHANGE = 'audioOutputChange'

   @property
   def reason(self):
      return self._reason

   def __init__(self, type: String, bubbles: Boolean = false,
                cancelable: Boolean = false, reason: String = null):
      super().__init__(type, bubbles, cancelable)
      self._reason = String(reason)


class AVDictionaryDataEvent(_AS3_BASEEVENT):
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


class AVHTTPStatusEvent(_AS3_BASEEVENT):
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
      return self.formatToString('AVHTTPStatusEvent', 'type', 'bubbles', 'cancelable', 'status')


class AVPauseAtPeriodEndEvent(_AS3_BASEEVENT):
   AV_PAUSE_AT_PERIOD_END = 'avPauseAtPeriodEnd'

   @property
   def userData(self):
      return self._userData

   def __init__(self, type: String, bubbles: Boolean = false,
                cancelable: Boolean = false, userData: int = 0):
      super().__init__(type, bubbles, cancelable)
      self._userData = int(userData)


class BrowserInvokeEvent(_AS3_BASEEVENT):
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


class ContextMenuEvent(_AS3_BASEEVENT):
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
      return self.formatToString('ContextMenuEvent', 'type', 'bubbles', 'cancelable', 'mouseTarget', 'isMouseTargetInaccessible', 'contextMenuOwner')


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
      return self.formatToString('DataEvent', 'type', 'bubbles', 'cancelable', 'data')


class DatagramSocketDataEvent(_AS3_BASEEVENT):
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
      return DatagramSocketDataEvent(self.type, self.bubbles, self.cancelable,
                                     self.srcAddress, self.srcPort,
                                     self.dstAddress, self.dstPort, self.data)

   def toString(self):
      return self.formatToString('DatagramSocketDataEvent', 'type', 'bubbles',
                                 'cancelable', 'srcAddress', 'srcPort',
                                 'dstAddress', 'dstPort', 'data')


class DeviceRotationEvent(_AS3_BASEEVENT):
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
                cancelable: Boolean = false, timestamp: Number = 0, roll: Number = 0, pitch: Number = 0, yaw: Number = 0, quaternion: Array = null):
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


class DNSResolverEvent(_AS3_BASEEVENT):
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


class DRMAuthenticateEvent:...


class DRMAuthenticateCompleteEvent:...


class DRMAuthenticateErrorEvent:...


class DRMDeviceGroupErrorEvent:...


class DRMErrorEvent:...


class DRMLicenseRequestEvent:...


class DRMMetadataEvent:...


class DRMReturnVoucherCompleteEvent:...


class DRMStatusEvent:...


class EventPhase(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   AT_TARGET = 2
   BUBBLING_PHASE = 3
   CAPTURING_PHASE = 1


class FileListEvent(_AS3_BASEEVENT):
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


class FocusEvent(_AS3_BASEEVENT):
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

   def __init__(self, type: String, bubbles: Boolean = false,
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
      return self.formatToString('FocusEvent', 'type', 'bubbles', 'cancelable', 'relatedObject', 'shiftKey', 'keyCode')


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
      return FullScreenEventEvent(self.type, self.bubbles, self.cancelable,
                                  self.fullScreen, self.interactive)

   def toString(self):
      return self.formatToString('FullScreenEvent', 'type', 'bubbles', 'cancelable', 'activating')


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



class GeolocationEvent(_AS3_BASEEVENT):
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
                lonitude: Number = 0, altitude: Number = 0,
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
                              self.horizontalAccuracy, self.verticalAccuracy,
                              self.speed, self.heading, self.timestamp)

   def toString(self):
      return self.formatToString('GeolocationEvent', 'type', 'bubbles',
                                 'cancelable', 'latitude', 'longitude',
                                 'altitude', 'horizontalAccuracy',
                                 'verticalAccuracy', 'speed', 'heading',
                                 'timestamp')


class GestureEvent(_AS3_BASEEVENT):
   # TODO
   GESTURE_TWO_FINGER_TAP = 'gestureTwoFingerTap'

   def __init__(self, type: String, bubbles: Boolean = false,
                cancelable: Boolean = false, phase: String = null,
                localX: Number = 0, localY: Number = 0,
                ctrlKey: Boolean = false, altKey: Boolean = false,
                commandKey: Boolean = false, controlKey: Boolean = false):
      super().__init__(type, bubbles, cancelable)
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError

   def updateAfterEvent(self):
      raise NotImplementedError


class GesturePhase(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   ALL = 'all'
   BEGIN = 'begin'
   END = 'end'
   UPDATE = 'update'


class HTMLUncaughtScriptExceptionEvent(_AS3_BASEEVENT):
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


class HTTPStatusEvent(_AS3_BASEEVENT):
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
      return self.formatToString('HTTPStatusEvent', 'type', 'bubbles', 'cancelable', 'status')


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
      return self.formatToString('IMEEvent', 'type', 'bubbles', 'cancelable',
                                 'text')  # imeClient


class InvokeEvent(_AS3_BASEEVENT):
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
                         self.currentDirectory, self.arguements, self.reason)


class IOErrorEvent(ErrorEvent):
   IO_ERROR = 'ioError'
   STANDARD_ERROR_IO_ERROR = 'standardErrorIoError'
   STANDARD_INPUT_IO_ERROR = 'standardInputIoError'
   STANDARD_OUTPUT_IO_ERROR = 'standardOutputIoError'

   def clone(self):
      return IOErrorEvent(self.type, self.bubbles, self.cancelable, self.text,
                          self.errorID)

   def toString(self):
      return self.formatToString('IOErrorEvent', 'type', 'bubbles', 'cancelable', 'text', 'errorID')


class KeyboardEvent(_AS3_BASEEVENT):
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

   def __init__(self, type: String, bubbles: Boolean = false,
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
      return self.formatToString('KeyboardEvent', 'type', 'bubbles', 'cancelable', 'altKey', 'charCode', 'commandKey', 'controlKey', 'ctrlKey', 'keyCode', 'keyLocation', 'shiftKey')

   def updateAfterEvent(self):
      raise NotImplementedError


class LocationChangeEvent(_AS3_BASEEVENT):
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


class MediaEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class MouseEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError

   def updateAfterEvent(self):
      raise NotImplementedError


class NativeDragEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class NativeProcessExitEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class NativeWindowBoundsEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class NativeWindowDisplayStateEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class NetDataEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class NetMonitorEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class NetStatusEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class OutputProgressEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class PermissionEvent(_AS3_BASEEVENT):
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
      return PermissionEvent(self.type, self.bubbles, self.cancelable, self.status)

   def toString(self):
      return String(f'[PermissionEvent type={self.type} bubbles={self.bubbles} cancelable={self.cancelable} permission= status={self.status}]')


class PressAndTapGestureEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class ProgressEvent(_AS3_BASEEVENT):
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
      return self.formatToString('ProgressEvent', 'type', 'bubbles', 'cancelable', 'bytesLoaded', 'bytesTotal')


class RemoteNotificationEvent:...


class SampleDataEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class ScreenMouseEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class SecurityErrorEvent(ErrorEvent):
   SECURITY_ERROR = 'securityError'

   def clone(self):
      return SecurityErrorEvent(self.type, self.bubbles, self.cancelable,
                                self.text, self.errorID)

   def toString(self):
      return self.formatToString('SecurityErrorEvent', 'type', 'bubbles', 'cancelable', 'text', 'errorID')


class ServerSocketConnectEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class ShaderEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class SoftKeyboardEvent:
   def __init__(self):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

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


class SQLEvent:
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


class SQLUpdateEvent(_AS3_BASEEVENT):
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


class StageOrientationEvent(_AS3_BASEEVENT):
   ORIENTATION_CHANGE = 'orientationChange'
   ORIENTATION_CHANGING = 'orientationChanging'

   @property
   def afterOrientation(self):
      return self._afterOrientation

   @property
   def beforeOrientation(self):
      return self._beforeOrientation

   def __init__(self, type: String, bubbles: Boolean = false,
                cancelable: Boolean = false, beforeOrientation: String = null,
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


class StageVideoAvailabilityEvent(_AS3_BASEEVENT):
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


class StageVideoEvent(_AS3_BASEEVENT):
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


class StatusEvent(_AS3_BASEEVENT):
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
      return StatusEvent(self.type, self.bubbles, self.cancelable, self.code,
                         self.level)

   def toString(self):
      return self.formatToString('StatusEvent', 'type', 'bubbles',
                                 'cancelable', 'code', 'level')


class StorageVolumeChangeEvent(_AS3_BASEEVENT):
   STORAGE_VOLUME_MOUNT = String('storageVolumeMount')
   STORAGE_VOLUME_UNMOUNT = String('storageVolumeUnmount')

   @property
   def rootDirectory(self):
      if self.type == STORAGE_VOLUME_UNMOUNT:
         return null
      raise NotImplementedError

   @property
   def storageVolume(self):
      if self.type == STORAGE_VOLUME_UNMOUNT:
         return null
      raise NotImplementedError

   def __init__(self, type: String, bubbles: Boolean = false,
                cancelable: Boolean = false, path = null, volume = null):
      super().__init__(type, bubbles, cancelable)
      self._path = path
      self._volume = volume

   def clone(self):
      return StorageVolumeChangeEvent(self.type, self.bubbles, self.cancelable, self.path, self.volume)

   def toString(self):
      raise NotImplementedError


class SyncEvent(_AS3_BASEEVENT):
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


class ThrottleEvent(_AS3_BASEEVENT):
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
      return self.formatToString('ThrottleEvent', 'type', 'bubbles', 'cancelable', 'state', 'targetFrameRate')


class ThrottleType(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   PAUSE = 'pause'
   RESUME = 'resume'
   THROTTLE = 'throttle'


class TimerEvent(_AS3_BASEEVENT):
   TIMER = 'timer'  # bubbles=False, cancelable=False
   TIMER_COMPLETE = 'timerComplete'  # bubbles=False, cancelable=False

   def __init__(self, type: String, bubbles: Boolean = false,
                cancelable: Boolean = false):
      super().__init__(type, bubbles, cancelable)

   def clone(self):
      return TimerEvent(self.type, self.bubbles, self.cancelable)

   def toString(self):
      return self.formatToString('TimerEvent', 'type', 'bubbles', 'cancelable')

   def updateAfterEvent(self):
      raise NotImplementedError


class TouchEvent(_AS3_BASEEVENT):
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

   def __init__(self, type: String, bubbles: Boolean = false,
                cancelable: Boolean = false, error_in = null):
      # TODO: Check to see if text and errorID are retrieved from error_in
      super().__init__(type, bubbles, cancelable)  #, <text>, <ID>
      self._error = error_in

   def clone(self):
      return UncaughtErrorEvent(self.type, self.bubbles, self.cancelable,
                                self.error)

   def toString(self):
      raise NotImplementedError


class UncaughtErrorEvents(EventDispatcher):
   def __init__(self):
      raise NotImplementedError


class VideoEvent(_AS3_BASEEVENT):
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



class VideoTextureEvent(_AS3_BASEEVENT):
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
      return self.formatToString('VsyncStateChangeAvailabilityEvent', 'type',
                                 'bubbles', 'cancelable', 'available')
