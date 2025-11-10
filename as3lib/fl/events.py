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
      return self.formatToString('ComponentEvent', 'type', 'bubbles', 'cancelable')


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
   _INTERNAL_allowedTypes = {'scroll',}

   @property
   def delta(self):
      return self._delta

   @property
   def direction(self):
      return self._direction

   @property
   def position(self):
      return self._position

   def __init__(self, direction, delta, position):
      super().__init__('scroll', False, False)
      self._delta = delta
      self._direction = direction
      self._position = position

   def toString(self):
      return self.formatToString('ScrollEvent', 'type', 'bubbles', 'cancelable', 'direction', 'delta', 'position')


class SliderEvent:...


class SliderEventClickTarget:...
