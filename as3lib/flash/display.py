from as3lib import as3state, metaclasses
import as3lib as as3
import tkinter
from typing import Generator
from as3.flash.events import EventDispatcher

#Dummy classes
class InteractiveObject:...

def _winNameGen()-> Generator[int,None,None]:
   i = 0
   while True:
      yield i
      i += 1

_windowNameGenerator: Generator[int,None,None] = _winNameGen()

class as3totk:
   def anchors(flashalign:str):
      if flashalign == "B":
         return "s"
      if flashalign == "BL":
         return "sw"
      if flashalign == "BR":
         return "se"
      if flashalign == "L":
         return "w"
      if flashalign == "R":
         return "e"
      if flashalign == "T":
         return "n"
      if flashalign == "TL":
         return "nw"
      if flashalign == "TR":
         return "ne"

class ActionScriptVersion(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   ACTIONSCRIPT2 = 2
   ACTIONSCRIPT3 = 3
class AVLoader:...
class AVM1Movie:...
class Bitmap:...
class BitmapData:...
class BitmapDataChannel:...
class BitmapEncodingColorSpace(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   COLORSPACE_4_2_0 = "4:2:0"
   COLORSPACE_4_2_2 = "4:2:2"
   COLORSPACE_4_4_4 = "4:4:4"
   COLORSPACE_AUTO = "auto"
class BlendMode(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   ADD = "add"
   ALPHA = "alpha"
   DARKEN = "darken"
   DIFFERENCE = "difference"
   ERASE = "erase"
   HARDLIGHT = "hardlight"
   INVERT = "invert"
   LAYER = "layer"
   LIGHTEN = "lighten"
   MULTIPLY = "multiply"
   NORMAL = "normal"
   OVERLAY = "overlay"
   SCREEN = "screen"
   SHADER = "shader"
   SUBTRACT = "subtract"
class CapsStyle(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   NONE = "none"
   ROUND = "round"
   SQUARE = "square"
class ColorCorrection(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   DEFAULR = "default"
   OFF = "off"
   ON = "on"
class ColorCorrectionSupport(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   DEFAULT_OFF = "defaultOff"
   DEFAULT_ON = "defualtOn"
   UNSUPPORTED = "unsupported"
class DisplayObject(EventDispatcher):...
class DisplayObjectContainer(InteractiveObject):...
class FocusDirection(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   BOTTOM = "bottom"
   NONE = "none"
   TOP = "top"
class FrameLabel:...
class GradientType(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   LINEAR = "linear"
   RADIAL = "radial"
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
class InteractiveObject(DisplayObject):...
class InterpolationMethod(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   LINEAR_RGB = "linearRGB"
   RGB = "rgb"
class JointStyle(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   BEVEL = "bevel"
   MITER = "miter"
   ROUND = "round"
class JPEGEncoderOptions:...
class JPEGCREncoderOptions:...
class LineScaleMode(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   HORIZONTAL = "horizontal"
   NONE = "none"
   NORMAL = "normal"
   VERTICAL = "vertical"
class Loader:...
class LoderInfo:...
class MorphShape:...
class MovieClip:...
class NativeMenu:...
class NativeMenuItem:...
class NativeWindow:
   """
   Due to limitations in tkinter, any window that isn't the main window will not be able to start out inactive. It will instead start out minimized.
   """
   def _setActive(self,state:as3.allBoolean):
      self.__active = state
   def _getActive(self):
      return self.__active
   active = property(fget=_getActive,fset=_setActive)
   #alwaysInFront
   #bounds
   def _setClosed(self,state:as3.allBoolean):
      self.__closed = state
   def _getClosed(self):
      return self.__closed
   closed = property(fget=_getClosed,fset=_setClosed)
   #displayState
   #height
   #isSupported
   #maximizable
   #maxSize
   #menu
   #minimizable
   #minSize
   #owner
   #renderMode
   #resizable
   #stage
   #supportsMenu
   #supportsNotification
   #supportsTransparency
   #systemChrome
   #systemMaxSize
   #systemMinSize
   #title
   #transparent
   #type
   #visible
   #width
   #x
   #y
   def __init__(initOptions:NativeWindowInitOptions = NativeWindowInitOptions()):
      self.__mainwindow = len(as3state.windows) == 0:
      if self.__mainwindow == True:
         self.__windowObject = tkinter.Tk()
      else:
         self.__windowObject = tkinter.Toplevel()
         self.minimize()
      as3state.windows[next(_windowNameGenerator)] = self
   def activate():
      if self.active == False and self.closed == False:
         if self.__mainwindow == False:
            self.maximize()
         else:
            self.__windowObject.mainloop()
         self.active = True
   def close():
      self.__windowObject.destroy()
      self.closed = True
   def globalToScreen(globalPoint):... #accepts flash.geom.Point objects
   def listOwnedWindows():...
   def maximize():...
   def minimize():...
   def notifyUser(type):...
   def orderInBackOf(window:NativeWindow):...
   def orderInFrontOf(window:NativeWindow):...
   def orderToBack():...
   def orderToFront():...
   def restore():...
   def startMove():...
   def startResize(edgeOfCorner):...
class NativeWindowDisplayState(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   MAXIMIZED = "maximized"
   MINIMIZED = "minimized"
   NORMAL = "normal"
class NativeWindowInitOptions:
   #!Add restraints for properties and make them actual properties
   def __init__(self,**kwargs):
      self.maximizable:as3.allBoolean = kwargs.get('maximizable', True)
      self.minimizable:as3.allBoolean = kwargs.get('minimizable', True)
      self.owner:NativeWindow = kwargs.get('owner', as3.null)
      self.renderMode:str = kwargs.get('renderMode')
      self.resizable:as3.allBoolean = kwargs.get('resizable', True)
      self.systemChrome:str = kwargs.get('systemChrome', NativeWindowSystemChrome.STANDARD)
      self.transparent:as3.allBoolean = kwargs.get('transparent', False)
      self.type:str = kwargs.get('type', NativeWindowType.NORMAL)
class NativeWindowRenderMode(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   AUTO = "auto"
   CPU = "cpu"
   DIRECT = "direct"
   GPU = "gpu"
class NativeWindowResize(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   BOTTOM = "B"
   BOTTOM_LEFT = "BL"
   BOTTOM_RIGHT = "BR"
   LEFT = "L"
   RIGHT = "R"
   TOP = "T"
   TOP_LEFT = "TL"
   TOP_RIGHT = "TR"
class NativeWindowSystemChrome(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   ALTERNATE = "alternate"
   NONE = "none"
   STANDARD = "standard"
class NativeWindowType(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   LIGHTWEIGHT = "lightweight"
   NORMAL = "normal"
   UTILITY = "utility"
class PixelSnapping(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   ALWAYS = "always"
   AUTO = "auto"
   NEVER = "never"
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
   BOOL = "bool"
   BOOL2 = "bool2"
   BOOL3 = "bool3"
   BOOL4 = "bool4"
   FLOAT = "float"
   FLOAT2 = "float2"
   FLOAT3 = "float3"
   FLOAT4 = "float4"
   INT = "int"
   INT2 = "int2"
   INT3 = "int3"
   INT4 = "int4"
   MATRIX2X2 = "matrix2x2"
   MATRIX3X3 = "matrix3x3"
   MATRIX4X4 = "matrix4x4"
class ShaderPrecision(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   FAST = "fast"
   FULL = "full"
class Shape:...
class SimpleButtom:...
class SpreadMethod(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   PAD = "pad"
   REFLECT = "reflect"
   REPEAT = "repeat"
class Sprite:...
class Stage:...
class Stage3D:...
class StageAlign(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   BOTTOM = "B"
   BOTTOM_LEFT = "BL"
   BOTTOM_RIGHT = "BR"
   LEFT = "L"
   RIGHT = "R"
   TOP = "T"
   TOP_LEFT = "TL"
   TOP_RIGHT = "TR"
class StageAspectRatio(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   ANY = "any"
   LANDSCAPE = "landscape"
   PORTRAIT = "portrait"
class StageDisplayState(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   FULL_SCREEN = "fullScreen"
   FULL_SCREEN_INTERACTIVE = "fullScreenInteractive"
   NORMAL = "normal"
class StageOrientation(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   DEFAULT = "default"
   ROTATED_LEFT = "rotatedLeft"
   ROTATED_RIGHT = "rotatedRight"
   UNKNOWN = "unknown"
   UPSIDE_DOWN = "upsideDown"
class StageQuality(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   BEST = "best"
   HIGH = "high"
   HIGH_16X16 = "16x16"
   HIGH_16X16_LINEAR = "16x16linear"
   HIGH_8X8 = "8x8"
   HIGH_8X8_LINEAR = "8x8linear"
   LOW = "low"
   MEDIUM = "medium"
class StageScaleMode(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   EXACT_FIT = "exactFit"
   NO_BORDER = "noBorder"
   NO_SCALE = "noScale"
   SHOW_ALL = "showAll"
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
   NEGATIVE = "negative"
   NONE = "none"
   POSITIVE = "positive"
