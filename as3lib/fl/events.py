from as3lib.flash.events import _AS3_BASEEVENT


class ColorPickerEvent:...


class ComponentEvent(_AS3_BASEEVENT):
   BUTTON_DOWN = 'buttonDown'  # bubbles=False, cancelable=False
   ENTER = 'enter'  # bubbles=False, cancelable=False
   HIDE = 'hide'  # bubbles=False, cancelable=False
   LABEL_CHANGE = 'labelChange'  # bubbles=False, cancelable=False
   MOVE = 'move'  # bubbles=False, cancelable=False
   RESIZE = 'resize'  # bubbles=False, cancelable=False
   SHOW = 'show'  # bubbles=False, cancelable=False
   _INTERNAL_allowedTypes = {'buttonDown', 'enter', 'hide', 'labelChange', 'move', 'resize', 'show'}

   def toString(self):
      return f'[ComponentEvent type={self.type} bubbles={self.bubbles} cancelable={self.cancelable}]'


class DataChangeEvent:...


class DataChangeType:...


class DataGridEvent:...


class DataGridEventReason:...


class InteractionInputType:...


class ListEvent:...


class RSLErrorEvent:...


class RSLEvent:...


class ScrollEvent(_AS3_BASEEVENT):
   SCROLL = 'scroll'
   _INTERNAL_allowedTypes = {'scroll'}

   @property
   def delta(self):
      return self.__delta

   @property
   def direction(self):
      return self.__direction

   @property
   def position(self):
      return self.__position

   def __init__(self, direction, delta, position):
      super().__init__('scroll', False, False)
      self.__delta = delta
      self.__direction = direction
      self.__position = position

   def toString(self):
      return f'[ScrollEvent type={self.type} bubbles={self.bubbles} cancelable={self.cancelable} direction={self.direction} delta={self.delta} position={self.position}]'


class SliderEvent:...


class SliderEventClickTarget:...
