from as3lib.flash.events import _AS3_BASEEVENT

class ColorPickerEvent:...
class ComponentEvent(_AS3_BASEEVENT):
	BUTTON_DOWN = "buttonDown" #bubbles=False, cancelable=False
	ENTER = "enter" #bubbles=False, cancelable=False
	HIDE = "hide" #bubbles=False, cancelable=False
	LABEL_CHANGE = "labelChange" #bubbles=False, cancelable=False
	MOVE = "move" #bubbles=False, cancelable=False
	RESIZE = "resize" #bubbles=False, cancelable=False
	SHOW = "show" #bubbles=False, cancelable=False
	_INTERNAL_allowedTypes = {"buttonDown","enter","hide","labelChange","move","resize","show"}
	def toString(self):
		return f"[ComponentEvent type={self.type} bubbles={self.bubbles} cancelable={self.cancelable}]"
class DataChangeEvent:...
class DataChangeType:...
class DataGridEvent:...
class DataGridEventReason:...
class InteractionInputType:...
class ListEvent:...
class RSLErrorEvent:...
class RSLEvent:...
class ScrollEvent(_AS3_BASEEVENT):
	SCROLL = "scroll"
	_INTERNAL_allowedTypes = {"scroll"}
	def _getDelta(self):
		return self.__delta
	delta = property(fget=_getDelta)
	def _getDirection(self):
		return self.__direction
	direction = property(fget=_getDirection)
	def _getPosition(self):
		return self.__position
	position = property(fget=_getPosition)
	def __init__(self,direction,delta,position,_target=None):
		super().__init__("scroll",False,False,_target)
		self.__delta = delta
		self.__direction = direction
		self.__position = position
	def toString(self):
		return return f"[ScrollEvent type={self.type} bubbles={self.bubbles} cancelable={self.cancelable} direction={self.direction} delta={self.delta} position={self.position}]"
class SliderEvent:...
class SliderEventClickTarget:...
