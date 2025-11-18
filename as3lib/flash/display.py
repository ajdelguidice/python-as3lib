from __future__ import annotations
import as3lib as as3
from as3lib import as3state, metaclasses
from as3lib.flash.errors import ArguementError, IllegalOperationError
from as3lib.flash.events import Event, EventDispatcher
from as3lib.flash.geom import Point, Rectangle
import tkinter


def _winNameGen():
   i = 0
   while True:
      yield i
      i += 1


_windowNameGenerator = _winNameGen()


class as3totk:
   def anchors(flashalign: str):
      if flashalign == 'B':
         return 's'
      if flashalign == 'BL':
         return 'sw'
      if flashalign == 'BR':
         return 'se'
      if flashalign == 'L':
         return 'w'
      if flashalign == 'R':
         return 'e'
      if flashalign == 'T':
         return 'n'
      if flashalign == 'TL':
         return 'nw'
      if flashalign == 'TR':
         return 'ne'


class DisplayObject(EventDispatcher):
   def __init__(self, target = None):
      super().__init__(target)
      self.added = Event('render', True)
      self.addedToStage = Event('addedToStage')
      self.enterFrame = Event('enterFrame')
      self.exitFrame = Event('exitFrame')
      self.frameConstructed = Event('frameConstructed')
      self.removed = Event('removed', True)
      self.removedFromStage = Event('removedFromStage')
      self.render = Event('render')
   def getBounds(self, targetCoordinateSpace):...
   def getRect(self, targetCoordinateSpace):...
   def globalToLocal(self, point: Point):...
   def globalToLocal3D(self, point: Point):...
   def hitTestObject(self, obj):...
   def hitTestPoint(self, x, y, shapeFlag):...
   def local3DToGlobal(self, point3d):...
   def localToGlobal(self, point: Point):...


class InteractiveObject(DisplayObject):...


class DisplayObjectContainer(InteractiveObject):...


class ActionScriptVersion(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   ACTIONSCRIPT2 = 2
   ACTIONSCRIPT3 = 3


class AVLoader:...


class AVM1Movie:...


class Bitmap:...


class BitmapData:...


class BitmapDataChannel:...


class BitmapEncodingColorSpace(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   COLORSPACE_4_2_0 = '4:2:0'
   COLORSPACE_4_2_2 = '4:2:2'
   COLORSPACE_4_4_4 = '4:4:4'
   COLORSPACE_AUTO = 'auto'


class BlendMode(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   ADD = 'add'
   ALPHA = 'alpha'
   DARKEN = 'darken'
   DIFFERENCE = 'difference'
   ERASE = 'erase'
   HARDLIGHT = 'hardlight'
   INVERT = 'invert'
   LAYER = 'layer'
   LIGHTEN = 'lighten'
   MULTIPLY = 'multiply'
   NORMAL = 'normal'
   OVERLAY = 'overlay'
   SCREEN = 'screen'
   SHADER = 'shader'
   SUBTRACT = 'subtract'


class CapsStyle(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   NONE = 'none'
   ROUND = 'round'
   SQUARE = 'square'


class ColorCorrection(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   DEFAULR = 'default'
   OFF = 'off'
   ON = 'on'


class ColorCorrectionSupport(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   DEFAULT_OFF = 'defaultOff'
   DEFAULT_ON = 'defualtOn'
   UNSUPPORTED = 'unsupported'


class FocusDirection(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   BOTTOM = 'bottom'
   NONE = 'none'
   TOP = 'top'


class FrameLabel:...


class GradientType(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   LINEAR = 'linear'
   RADIAL = 'radial'


class Graphics:...


class GraphicsBitmapFill:...


class GraphicsEndFill:...


class GraphicsGradientFill:...


class GraphicsPath:...


class GraphicsPathCommand:...


class GraphicsPathWinding:...


class GraphicsShaderFill:...


class GraphicsSolidFill:...


class GraphicsStroke:...


class GraphicsTrianglePath:...


class GraphicsObject:...


class InterpolationMethod(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   LINEAR_RGB = 'linearRGB'
   RGB = 'rgb'


class JointStyle(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   BEVEL = 'bevel'
   MITER = 'miter'
   ROUND = 'round'


class JPEGEncoderOptions:...


class JPEGCREncoderOptions:...


class LineScaleMode(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   HORIZONTAL = 'horizontal'
   NONE = 'none'
   NORMAL = 'normal'
   VERTICAL = 'vertical'


class Loader:...


class LoderInfo:...


class MorphShape:...


class MovieClip:...


class NativeMenu(EventDispatcher):
   @property
   def isSupported(self):...

   @property
   def items(self):
      return self._items

   @items.setter
   def items(self, value):
      self._items = value

   @property
   def numItems(self):
      return self._items.length

   @property
   def parent(self):
      return self._parent

   def __init__(self):
      super().__init__()
      self.displaying = Event('displaying')
      self.preparing = Event('preparing')
      self.select = Event('select')
      self._items = as3.Array()
      self._parent

   def addItem(self, item: NativeMenuItem):
      if item is None or item.menu is not None:
         raise ArguementError()
      self._items.append(item)

   def addItemAt(self, item: NativeMenuItem, index):
      # TODO: Add RangeError when index is out of bounds
      if item is None or item.menu is not None:
         raise ArguementError()
      self._items.insertAt(index, item)

   def addSubmenu(self, submenu: NativeMenu, label):
      item = NativeMenuItem(label)
      item.submenu = submenu
      self.addItem(item)
      return item

   def addSubmenuAt(self, submenu: NativeMenu, index, label):
      item = NativeMenuItem(label)
      item.submenu = submenu
      self.addItemAt(item, index)
      return item

   def clone(self):...

   def containsItem(self, item: NativeMenuItem):
      for i in self._items:
         if i is item:
            return True
      return False

   def display(self, stage: Stage, stageX, stageY):...

   def getItemAt(self, index):
      # TODO: Add RangeError when index is out of bounds
      return self._items[index]

   def getItemByName(self, name):
      for i in self._items:
         if i.name == name:
            return i

   def getItemIndex(self, item: NativeMenuItem):
      for index, i in enumerate(self._items):
         if i is item:
            return index
      return -1

   def removeAllItems(self):
      for i in range(self.numItems):
         self.removeItemAt(0)

   def removeItem(self, item: NativeMenuItem):
      self._items.remove(item)

   def removeItemAt(self, index):
      return self._items.removeAt(index)

   def setItemIndex(self, item: NativeMenuItem, index):
      # TODO: Add RangeError when index is out of bounds
      i = self.getItemIndex(item)
      if i == -1:
         self.addItemAt(item, index)
      else:
         self.removeItemAt(i)
         self.addItemAt(item, index)


class NativeMenuItem(EventDispatcher):
   @property
   def checked(self):...

   @checked.setter
   def checked(self, value):...

   @property
   def data(self):
      return self._data

   @data.setter
   def data(self, value):
      self._data = value

   @property
   def enabled(self):
      return self._enabled

   @enabled.setter
   def enabled(self, value):
      self._enabled = value

   @property
   def isSeparator(self):
      return self._isSep

   @property
   def keyEquivalent(self):...

   @keyEquivalent.setter
   def keyEquivalent(self, value):...

   @property
   def keyEquivalentModifiers(self):...

   @keyEquivalentModifiers.setter
   def keyEquivalentModifiers(self, value):...

   @property
   def label(self):
      return self._label

   @label.setter
   def label(self, value):
      self._label = value

   @property
   def menu(self):
      return self._menu

   @property
   def mnemonicIndex(self):...

   @mnemonicIndex.setter
   def mnemonicIndex(self, value):...

   @property
   def name(self):
      return self._name

   @name.setter
   def name(self, value):
      self._name = value

   @property
   def submenu(self):
      return self._subMenu

   @submenu.setter
   def submenu(self, value: NativeMenu):
      self._subMenu = value

   def __init__(self, label, isSeparator=False):
      super().__init__()
      self.displaying = Event('displaying')
      self.preparing = Event('preparing')
      self.select = Event('select')
      self._isSep = isSeparator
      self._label = label
      self._data = None
      self._enabled = True
      self._menu = None
      self._name = None
      self._subMenu = None

   def clone(self):...
   def toString(self):...


class NativeWindow:
   '''
   Due to limitations in tkinter, windows will not be able to start out inactive. They will instead start out minimized.
   '''
   @property
   def active(self):
      return self._active

   @property
   def alwaysInFront(self):
      return self._alwaysInFront

   @alwaysInFront.setter
   def alwaysInFront(self, value):
      if self._alwaysInFront != value:
         self._windowObject.attributes('-topmost', value)
         self._alwaysInFront = value

   @property
   def bounds(self):...

   @property
   def closed(self):
      return self._closed

   @property
   def displayState(self):
      if self.closed:
         raise IllegalOperationError()
      ...

   @property
   def height(self):...

   @property
   def isSupported(self):
      return True

   @property
   def maximizable(self):...

   @property
   def maxSize(self):...

   @property
   def menu(self):...

   @property
   def minimizable(self):...

   @property
   def minSize(self):...

   @property
   def owner(self):
      return self._owner

   @property
   def renderMode(self):...

   @property
   def resizable(self):...

   @property
   def stage(self):...

   @property
   def supportsMenu(self):...

   @property
   def supportsNotification(self):...

   @property
   def supportsTransparency(self):...

   @property
   def systemChrome(self):...

   @property
   def systemMaxSize(self):...

   @property
   def systemMinSize(self):...

   @property
   def title(self):
      if self.closed:
         raise IllegalOperationError()
      return self._title

   @title.setter
   def title(self, value):
      if self.closed:
         raise IllegalOperationError()
      self._windowObject.title(value)
      self._title = value

   @property
   def transparent(self):...

   @property
   def type(self):...

   @property
   def visible(self):
      if self.closed:
         raise IllegalOperationError()
      ...

   @visible.setter
   def visible(self, value):
      if self.closed:
         raise IllegalOperationError()
      ...

   @property
   def width(self):...

   @property
   def x(self):...

   @property
   def y(self):...

   def __init__(self, initOptions: NativeWindowInitOptions = None):
      self._closed = False
      self._active = False
      self._alwaysInFront = False
      if initOptions is None:
         initOptions = NativeWindowInitOptions()
      if not isinstance(initOptions, NativeWindowInitOptions):
         raise IllegalOperationError()
      if len(as3state.windows) == 0:
         as3state.windows['TkWorkaroundWindow'] = tkinter.Tk()
         as3state.windows['TkWorkaroundWindow'].iconify()
      self._windowObject = tkinter.Toplevel()
      self.minimize()
      self._winNum = next(_windowNameGenerator)
      as3state.windows[self._winNum] = self
      self.title = 'Flash Player'
      if initOptions.owner is not None:
         self._owner = initOptions.owner
         self._windowObject.transient(self._owner._windowObject)

   def activate(self):
      if not self.active and not self.closed:
         self.maximize()
         self._active = True

   def close(self):
      self._windowObject.destroy()
      self._closed = True

   def globalToScreen(self, globalPoint: Point):...

   def listOwnedWindows(self):...

   def maximize(self):
      if self.closed:
         raise IllegalOperationError()
      ...

   def minimize(self):
      if self.closed:
         raise IllegalOperationError()
      ...

   def notifyUser(self, type):...

   def orderInBackOf(self, window: NativeWindow):...

   def orderInFrontOf(self, window: NativeWindow):...

   def orderToBack(self):...

   def orderToFront(self):...

   def restore(self):
      if self.closed:
         raise IllegalOperationError()
      ...

   def startMove(self):
      if self.closed:
         raise IllegalOperationError()
      ...

   def startResize(self, edgeOrCorner):
      if self.closed:
         raise IllegalOperationError()
      ...


class NativeWindowDisplayState(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   MAXIMIZED = 'maximized'
   MINIMIZED = 'minimized'
   NORMAL = 'normal'


class NativeWindowInitOptions:
   # TODO: Add restraints for properties and make them actual properties
   def __init__(self, **kwargs):
      self.maximizable = bool(kwargs.get('maximizable', True))
      self.minimizable = bool(kwargs.get('minimizable', True))
      self.owner: NativeWindow = kwargs.get('owner', None)
      self.renderMode = str(kwargs.get('renderMode', ''))
      self.resizable = bool(kwargs.get('resizable', True))
      self.systemChrome = str(kwargs.get('systemChrome', NativeWindowSystemChrome.STANDARD))
      self.transparent = bool(kwargs.get('transparent', False))
      self.type = str(kwargs.get('type', NativeWindowType.NORMAL))


class NativeWindowRenderMode(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   AUTO = 'auto'
   CPU = 'cpu'
   DIRECT = 'direct'
   GPU = 'gpu'


class NativeWindowResize(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   BOTTOM = 'B'
   BOTTOM_LEFT = 'BL'
   BOTTOM_RIGHT = 'BR'
   LEFT = 'L'
   RIGHT = 'R'
   TOP = 'T'
   TOP_LEFT = 'TL'
   TOP_RIGHT = 'TR'


class NativeWindowSystemChrome(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   ALTERNATE = 'alternate'
   NONE = 'none'
   STANDARD = 'standard'


class NativeWindowType(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   LIGHTWEIGHT = 'lightweight'
   NORMAL = 'normal'
   UTILITY = 'utility'


class PixelSnapping(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   ALWAYS = 'always'
   AUTO = 'auto'
   NEVER = 'never'


class PNGEncoderOptions:...


class Scene:...


class SceneMode:...


class Screen:...


class ScreenMode(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   colorDepth = as3state.colordepth
   height = as3state.height
   refreshRate = as3state.refreshrate
   width = as3state.width


class Shader:...


class ShaderData:...


class ShaderInput:...


class ShaderJob:...


class ShaderParameter:...


class ShaderParameterType(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   BOOL = 'bool'
   BOOL2 = 'bool2'
   BOOL3 = 'bool3'
   BOOL4 = 'bool4'
   FLOAT = 'float'
   FLOAT2 = 'float2'
   FLOAT3 = 'float3'
   FLOAT4 = 'float4'
   INT = 'int'
   INT2 = 'int2'
   INT3 = 'int3'
   INT4 = 'int4'
   MATRIX2X2 = 'matrix2x2'
   MATRIX3X3 = 'matrix3x3'
   MATRIX4X4 = 'matrix4x4'


class ShaderPrecision(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   FAST = 'fast'
   FULL = 'full'


class Shape:...


class SimpleButtom:...


class SpreadMethod(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   PAD = 'pad'
   REFLECT = 'reflect'
   REPEAT = 'repeat'


class Sprite(DisplayObjectContainer):...


class Stage:...


class Stage3D:...


class StageAlign(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   BOTTOM = 'B'
   BOTTOM_LEFT = 'BL'
   BOTTOM_RIGHT = 'BR'
   LEFT = 'L'
   RIGHT = 'R'
   TOP = 'T'
   TOP_LEFT = 'TL'
   TOP_RIGHT = 'TR'


class StageAspectRatio(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   ANY = 'any'
   LANDSCAPE = 'landscape'
   PORTRAIT = 'portrait'


class StageDisplayState(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   FULL_SCREEN = 'fullScreen'
   FULL_SCREEN_INTERACTIVE = 'fullScreenInteractive'
   NORMAL = 'normal'


class StageOrientation(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   DEFAULT = 'default'
   ROTATED_LEFT = 'rotatedLeft'
   ROTATED_RIGHT = 'rotatedRight'
   UNKNOWN = 'unknown'
   UPSIDE_DOWN = 'upsideDown'


class StageQuality(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   BEST = 'best'
   HIGH = 'high'
   HIGH_16X16 = '16x16'
   HIGH_16X16_LINEAR = '16x16linear'
   HIGH_8X8 = '8x8'
   HIGH_8X8_LINEAR = '8x8linear'
   LOW = 'low'
   MEDIUM = 'medium'


class StageScaleMode(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   EXACT_FIT = 'exactFit'
   NO_BORDER = 'noBorder'
   NO_SCALE = 'noScale'
   SHOW_ALL = 'showAll'


class SWFVersion(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   FLASH1 = 1
   FLASH2 = 2
   FLASH3 = 3
   FLASH4 = 4
   FLASH5 = 5
   FLASH6 = 6
   FLASH7 = 7
   FLASH8 = 8
   FLASH9 = 9
   FLASH10 = 10
   FLASH11 = 11


class TriangleCulling(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   NEGATIVE = 'negative'
   NONE = 'none'
   POSITIVE = 'positive'
