from as3lib import metaclasses
import as3lib as as3
from copy import copy


# BaseEvent
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

   def __init__(self, type, bubbles=False, cancelable=False):
      if type not in self._INTERNAL_allowedTypes:
         raise Exception('Provided event type is not valid for this object')
      self._type = type
      self._bubbles = bubbles
      self._cancelable = cancelable
      self._currentTarget = None
      self._target = None
      self._eventPhase = None
      self._preventDefault = False

   def __eq__(self, value):
      return self.type == value

   def __str__(self):
      return self.type

   def getEventProperties(self):
      return (self.type, self.bubbles, self.cancelable, self.currentTarget, self.eventPhase, self.target)

   def clone(self):
      return copy(self)

   def formatToString(self, className, *arguements):...

   def isDefaultPrevented(self):
      return self._preventDefault

   def preventDefault(self):
      if self.cancelable:
         self._preventDefault = True

   def stopImmediatePropagation(self):...

   def stopPropagation(self):...

   def toString(self):
      return f'[Event type={self.type} bubbles={self.bubbles} cancelable={self.cancelable}]'


# Dummy classes
class Event(_AS3_BASEEVENT):...


class EventDispatcher:...


class TextEvent:...


class ErrorEvent:...


# Interfaces
class IEventDispatcher:
   def __init__(self):
      self.eventobjects = {}

   def addEventListener(self, type, listener, useCapture=False, priority=0, useWeakReference=False):...

   def dispatchEvent(self, event):...

   def hasEventListener(self, type):...

   def removeEventListener(self, type, listener, useCapture=False):...

   def willTrigger(self, type):...


# Classes
class AccelerometerEvent:...


class ActivityEvent:...


class AsyncErrorEvent:...


class AudioOutputChangeEvent:...


class AVDictionaryDataEvent:...


class AVHTTPStatusEvent:...


class AVPauseAtPeriodEndEvent:...


class BrowserInvokeEvent:...


class ContextMenuEvent(_AS3_BASEEVENT):
   MENU_ITEM_SELECT = 'menuItemSelect'
   MENU_SELECT = 'menuSelect'
   _INTERNAL_allowedTypes = {'menuItemSelect', 'menuSelect'}

   @property
   def contextMenuOwner(self):
      return self._cmOwner

   @property
   def isMouseTargetInaccessible(self):
      return self._mTarget is None

   @property
   def mouseTarget(self):
      return self._mTarget

   def __init__(self, type, bubbles=False, cancelable=False, mouseTarget=None, contextMenuOwner=None):
      self._cmOwner = contextMenuOwner
      self._mTarget = mouseTarget
      super().__init__(type, bubbles, cancelable)

   def toString(self):
      return f'[ContextMenuEvent type={self.type} bubbles={self.bubbles} cancelable={self.cancelable} mouseTarget={self.mouseTarget} isMouseTargetInaccessible={self.isMouseTargetInaccessible}contextMenuOwner={self.contextMenuOwner}]'


class DataEvent(TextEvent):
   DATA = 'data'
   UPLOAD_COMPLETE_DATA = 'uploadCompleteData'
   _INTERNAL_allowedTypes = {'data', 'uploadCompleteData'}

   @property
   def data(self):
      return self._data

   @data.setter
   def data(self, value):
      self._data = value

   def __init__(self, type, bubbles=False, cancelable=False, data=''):
      self._data = data
      super().__init__(type, bubbles, cancelable)

   def toString(self):
      return f'[DataEvent type={self.type} bubbles={self.bubbles} cancelable={self.cancelable} data={self.data}]'


class DatagramSocketDataEvent:...


class DeviceRotationEvent:...


class DNSResolverEvent:...


class DRMAuthenticateEvent:...


class DRMAuthenticateCompleteEvent:...


class DRMAuthenticateErrorEvent:...


class DRMDeviceGroupErrorEvent:...


class DRMErrorEvent:...


class DRMLicenseRequestEvent:...


class DRMMetadataEvent:...


class DRMReturnVoucherCompleteEvent:...


class DRMStatusEvent:...


class ErrorEvent(TextEvent):
   ERROR = 'error'
   _INTERNAL_allowedTypes = set('error')

   @property
   def errorID(self):
      return self._errorID

   def __init__(self, type, bubbles=False, cancelable=False, text='', id=0):
      self._errorID = id
      super().__init__(type, bubbles, cancelable, text)

   def toString(self):
      return f'[ErrorEvent type={self.type} bubbles={self.bubbles} cancelable={self.cancelable} text={self.text} errorID={self.errorID}]'


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
   _INTERNAL_allowedTypes = {'activate', 'added', 'addedToStage', 'browerZoomChange', 'cancel', 'change', 'channelMessage', 'channelState', 'clear', 'close', 'closing', 'complete', 'connect', 'context3DCreate', 'copy', 'cut', 'deactivate', 'displaying', 'enterFrame', 'exitFrame', 'exiting', 'frameConstructed', 'frameLabel', 'fullscreen', 'htmlBoundsChange', 'htmlDOMInitialize', 'htmlRender', 'id3', 'init', 'locationChange', 'mouseLeave', 'networkChange', 'open', 'paste', 'preparing', 'removed', 'removeFromStage', 'render', 'resize', 'scroll', 'select', 'selectAll', 'soundComplete', 'standardErrorClose', 'standardInputClose', 'standardOutputClose', 'suspend', 'tabChildrenChange', 'tabEnableChange', 'tabIndexChange', 'textInteractionModeChange', 'textureReady', 'unload', 'userIdle', 'userPresent', 'videoFrame', 'workerState'}


class EventDispatcher:
   # TODO: Implement priority, weakReference

   def __init__(self, target: IEventDispatcher = None):
      # TODO: Implement target
      self.activate = Event('activate', False, False)
      self.deactivate = Event('deactivate', False, False)
      self._events = {}
      self._eventsCapture = {}

   def addEventListener(self, type: str, listener, useCapture: as3.allBoolean = False, priority: as3.allInt = 0, useWeakReference: as3.allBoolean = False):
      # TODO: Add error
      if useCapture is False:
         if self._events.get(type) is None:
            self._events[type] = [listener]
         elif listener not in self._events[type]:
            self._events[type].append(listener)
      else:
         if self._eventsCapture.get(type) is None:
            self._eventsCapture[type] = [listener]
         elif listener not in self._eventsCapture[type]:
            self._eventsCapture[type].append(listener)

   def dispatchEvent(self, event):
      # TODO: Implement useCapture
      # TODO: Implement bubbles
      if not event.isDefaultPrevented():
         if self._events.get(event.type) is not None:
            e = event.clone()
            for i in self._events[event.type]:
               e._currentTarget = i
               i(e)
            return True
      return False

   def hasEventListener(self, type):
      return self._events.get(type) is not None or self._eventsCapture.get(type) is not None

   def removeEventListener(self, type: str, listener, useCapture: as3.allBoolean = False):
      if useCapture is False:
         if self._events.get(type) is not None:
            try:
               self._events[type].remove(listener)
            except Exception:
               pass
      else:
         if self._eventsCapture.get(type) is not None:
            try:
               self._eventsCapture[type].remove(listener)
            except Exception:
               pass

   def willTrigger(self, type: str):...


class EventPhase(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   AT_TARGET = 2
   BUBBLING_PHASE = 3
   CAPTURING_PHASE = 1


class FileListEvent:...


class FocusEvent:...


class FullScreenEvent:...


class GameInputEvent:...


class GeolocationEvent:...


class GestureEvent:...


class GesturePhase:...


class HTMLUncaughtScriptExceptionEvent:...


class HTTPStatusEvent(_AS3_BASEEVENT):...


class IMEEvent:...


class InvokeEvent:...


class IOErrorEvent(ErrorEvent):...


class KeyboardEvent:...


class LocationChangeEvent:...


class MediaEventEvent:...


class MouseEventEvent:...


class NativeDragEvent:...


class NativeProcessExitEvent:...


class NativeWindowBoundsEvent:...


class NativeWindowDisplayStateEvent:...


class NetDataEvent:...


class NetMonitorEvent:...


class NetStatusEvent:...


class OutputProgressEvent:...


class PermissionEvent(_AS3_BASEEVENT):...


class PressAndTapGestureEvent:...


class ProgressEvent(_AS3_BASEEVENT):...


class RemoteNotificationEvent:...


class SampleDataEvent:...


class ScreenMouseEvent:...


class SecurityErrorEvent(ErrorEvent):...


class ServerSocketConnectEvent:...


class ShaderEvent:...


class SoftKeyboardEvent:...


class SoftKeyboardTrigger:...


class SQLEvent:...


class SQLUpdateEvent:...


class StageOrientationEvent:...


class StageVideoAvailabilityEvent:...


class StageVideoEventEvent:...


class StatusEvent:...


class StorageVolumeChangeEvent:...


class SyncEvent:...


class TextEvent(_AS3_BASEEVENT):
   LINK = 'link'  # bubbles=True, cancelable=False
   TEXT_INPUT = 'textInput'  # bubbles=True, cancelable=True
   _INTERNAL_allowedTypes = {'link', 'textInput'}

   @property
   def text(self):
      return self._text

   @text.setter
   def text(self, value):
      self._text = value

   def __init__(self, type, bubbles=False, cancelable=False, text=''):
      self._text = text
      super().__init__(type, bubbles, cancelable)

   def toString(self):
      return f'[TextEvent type={self.type} bubbles={self.bubbles} cancelable={self.cancelable} text={self.text}]'


class ThrottleEvent:...


class ThrottleType:...


class TimerEvent(_AS3_BASEEVENT):
   TIMER = 'timer'  # bubbles=False, cancelable=False
   TIMER_COMPLETE = 'timerComplete'  # bubbles=False, cancelable=False
   _INTERNAL_allowedTypes = {'timer', 'timerComplete'}

   def __init__(self, type, bubbles=False, cancelable=False):
      super().__init__(type, bubbles, cancelable)

   def toString(self):
      return f'[TimerEvent type={self.type} bubbles={self.bubbles} cancelable={self.cancelable}]'

   def updateAfterEvent(self):...


class TouchEvent:...


class TouchEventIntent:...


class TransformGestureEvent:...


class UncaughtErrorEvent:...


class UncaughtErrorEvents:...


class VideoEvent:...


class VideoTextureEvent:...


class VsyncStateChangeAvailabilityEvent:...
