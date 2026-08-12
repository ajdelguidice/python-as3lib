from __future__ import annotations
from as3lib import (Array, ArgumentError, as3state, Boolean, false, null,
                    Object, String, true)
from as3lib.flash.accessibility import AccessibilityImplementation, AccessibilityProperties
from as3lib.flash.errors import IllegalOperationError
from as3lib.flash.events import Event, EventDispatcher, KeyboardEvent
from as3lib.flash.geom import Matrix, Point, Rectangle, Vector3D
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
    @property
    def accessibilityProperties(self):
        return self._accessProps

    @accessibilityProperties.setter
    def accessibilityProperties(self, value: AccessibilityProperties):
        self._accessProps = value

    @property
    def alpha(self):
        raise NotImplementedError

    @alpha.setter
    def alpha(self, value):
        raise NotImplementedError

    @property
    def blendMode(self):
        raise NotImplementedError

    @blendMode.setter
    def blendMode(self, value):
        raise NotImplementedError

    @property
    def blendShader(self):  # Write only
        raise

    @blendShader.setter
    def blendShader(self, value):
        raise NotImplementedError

    @property
    def cacheAsBitmap(self):
        raise NotImplementedError

    @cacheAsBitmap.setter
    def cacheAsBitmap(self, value):
        raise NotImplementedError

    @property
    def cacheAsBitmapMatrix(self):
        raise NotImplementedError

    @cacheAsBitmapMatrix.setter
    def cacheAsBitmapMatrix(self, value):
        raise NotImplementedError

    @property
    def filters(self):
        raise NotImplementedError

    @filters.setter
    def filters(self, value):
        raise NotImplementedError

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def loaderInfo(self):
        raise NotImplementedError

    @property
    def mask(self):
        raise NotImplementedError

    @mask.setter
    def mask(self, value):
        raise NotImplementedError

    @property
    def metaData(self):
        raise NotImplementedError

    @metaData.setter
    def metaData(self, value):
        raise NotImplementedError

    @property
    def mouseX(self):
        raise NotImplementedError

    @property
    def mouseY(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    @name.setter
    def name(self, value):
        raise NotImplementedError

    @property
    def opaqueBackground(self):
        raise NotImplementedError

    @opaqueBackground.setter
    def opaqueBackground(self, value):
        raise NotImplementedError

    @property
    def parent(self):
        raise NotImplementedError

    @property
    def root(self):
        raise NotImplementedError

    @property
    def rotation(self):
        raise NotImplementedError

    @rotation.setter
    def rotation(self, value):
        raise NotImplementedError

    @property
    def rotationX(self):
        raise NotImplementedError

    @rotationX.setter
    def rotationX(self, value):
        raise NotImplementedError

    @property
    def rotationY(self):
        raise NotImplementedError

    @rotationY.setter
    def rotationY(self, value):
        raise NotImplementedError

    @property
    def rotationZ(self):
        raise NotImplementedError

    @rotationZ.setter
    def rotationZ(self, value):
        raise NotImplementedError

    @property
    def scale9Grid(self):
        raise NotImplementedError

    @scale9Grid.setter
    def scale9Grid(self, value):
        raise NotImplementedError

    @property
    def scaleX(self):
        raise NotImplementedError

    @scaleX.setter
    def scaleX(self, value):
        raise NotImplementedError

    @property
    def scaleY(self):
        raise NotImplementedError

    @scaleY.setter
    def scaleY(self, value):
        raise NotImplementedError

    @property
    def scaleZ(self):
        raise NotImplementedError

    @scaleZ.setter
    def scaleZ(self, value):
        raise NotImplementedError

    @property
    def scrollRect(self):
        raise NotImplementedError

    @scrollRect.setter
    def scrollRect(self, value):
        raise NotImplementedError

    @property
    def stage(self):
        raise NotImplementedError

    @stage.setter
    def stage(self, value):
        raise NotImplementedError

    @property
    def transform(self):
        raise NotImplementedError

    @transform.setter
    def transform(self, value):
        raise NotImplementedError

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    def __init__(self, target = None):
        super().__init__(target)
        self._accessProps = AccessibilityProperties()

        self._height = 0

        self._visible = True
        self._width = 0
        self._x = 0
        self._y = 0
        self._z = 0

    def getBounds(self, targetCoordinateSpace: DisplayObject) -> Rectangle:
        raise NotImplementedError

    def getRect(self, targetCoordinateSpace: DisplayObject) -> Rectangle:
        raise NotImplementedError

    def globalToLocal(self, point: Point) -> Point:
        raise NotImplementedError

    def globalToLocal3D(self, point: Point) -> Vector3D:
        raise NotImplementedError

    def hitTestObject(self, obj: DisplayObject):
        raise NotImplementedError

    def hitTestPoint(self, x, y, shapeFlag=False):
        raise NotImplementedError

    def local3DToGlobal(self, point3d: Vector3D) -> Point:
        raise NotImplementedError

    def localToGlobal(self, point: Point) -> Point:
        raise NotImplementedError


class InteractiveObject(DisplayObject):
    @property
    def accessibilityImplementation(self):
        return self._accessImpl

    @accessibilityImplementation.setter
    def accessibilityImplementation(self, value: AccessibilityImplementation):
        self._accessImpl = value

    @property
    def contextMenu(self):
        return self._contextMenu

    @contextMenu.setter
    def contextMenu(self, value: NativeMenu):
        self._contextMenu = value

    @property
    def doubleClickEnabled(self):
        return self._doubleClickEnabled

    @doubleClickEnabled.setter
    def doubleClickEnabled(self, value):
        self._doubleClickEnabled = value

    @property
    def focusRect(self):
        return self._focusRect

    @focusRect.setter
    def focusRect(self, value):
        self._focusRect = value

    @property
    def mouseEnabled(self):
        return self._mouseEnabled

    @mouseEnabled.setter
    def mouseEnabled(self, value):
        self._mouseEnabled = value

    @property
    def needsSoftKeyboard(self):
        return self._needsSoftKeyboard

    @needsSoftKeyboard.setter
    def needsSoftKeyboard(self, value):
        self._needsSoftKeyboard = value

    @property
    def softKeyboard(self):
        return self._softKeyboard

    @softKeyboard.setter
    def softKeyboard(self, value):
        self._softKeyboard = value

    @property
    def softKeyboardInputAreaOfInterest(self):
        return self._softKeyboardAOI

    @softKeyboardInputAreaOfInterest.setter
    def softKeyboardInputAreaOfInterest(self, value):
        self._softKeyboardAOI = value

    @property
    def tabEnabled(self):
        return self._tabEnabled

    @tabEnabled.setter
    def tabEnabled(self, value):
        self._tabEnabled = value

    @property
    def tabIndex(self):
        return self._tabIndex

    @tabIndex.setter
    def tabIndex(self, value):
        self._tabIndex = value

    def _TOOLKITKEYDOWNEVENTHANDLER(self, event):
        # TODO: Bind function to toolkit key_down event
        # TODO: Convert toolkit key_down event into flash key_down event
        # TODO: Fill in the placeholder values
        # NOTE: cancelable in AIR but not in flash player
        self.dispatchEvent(KeyboardEvent('keyDown', true, true, 'charCode', 'keyCode', 'keyLocation', 'ctrlKey', 'altKey', 'shiftKey', 'controlKey', 'commandKey'))

    def _TOOLKITKEYUPEVENTHANDLER(self, event):
        # TODO: Bind function to toolkit key_up event
        # TODO: Convert toolkit key_up event into flash key_up event
        # TODO: Fill in the placeholder values
        self.dispatchEvent(KeyboardEvent('keyUp', true, false, 'charCode', 'keyCode', 'keyLocation', 'ctrlKey', 'altKey', 'shiftKey', 'controlKey', 'commandKey'))

    def __init__(self):
        super().__init__()
        self._accessImpl = AccessibilityImplementation()
        self._contextMenu = None
        self._doubleClickEnabled = False
        self._focusRect = None
        self._mouseEnabled = None
        self._needsSoftKeyboard = None
        self._softKeyboard = None
        self._softKeyboardAOI = None
        self._tabEnabled = True
        self._tabIndex = None

    def requestSoftKeyboard(self):
        return False  # Placeholder. This tells applications that access was denied


class DisplayObjectContainer(InteractiveObject):
    @property
    def mouseChildren(self):
        raise NotImplementedError

    @mouseChildren.setter
    def mouseChildren(self, value):
        raise NotImplementedError

    @property
    def numChildren(self):
        return self._children.length

    @property
    def tabChildren(self):
        return self._tabChilren

    @tabChildren.setter
    def tabChildren(self, value):
        if value != self._tabChilren:
            raise NotImplementedError
            for i in self._children:
                ...  # TODO: Set tabbing behavior
        self._tabChilren = value

    @property
    def textSnapshot(self):
        raise NotImplementedError

    def __init__(self):
        super().__init__()
        self._children = Array()
        self._tabChilren = True

    def addChild(self, child: DisplayObject):
        raise NotImplementedError

    def addChildAt(self, child: DisplayObject, index):
        raise NotImplementedError

    def areInaccessibleObjectsUnderPoint(self, point: Point):
        raise NotImplementedError

    def contains(self, child: DisplayObject):
        raise NotImplementedError

    def getChildAt(self, index):
        raise NotImplementedError

    def getChildByName(self, name):
        raise NotImplementedError

    def getChildIndex(self, child: DisplayObject):
        raise NotImplementedError

    def getObjectsUnderPoint(self, point: Point):
        raise NotImplementedError

    def removeChild(self, child: DisplayObject):
        raise NotImplementedError

    def removeChildAt(self, index):
        raise NotImplementedError

    def removeChildren(self, beginIndex, endIndex):
        raise NotImplementedError

    def setChildIndex(self, child: DisplayObject, index):
        raise NotImplementedError

    def stopAllMovieClips(self):
        raise NotImplementedError

    def swapChildren(self, child1: DisplayObject, child2: DisplayObject):
        raise NotImplementedError

    def swapChildrenAt(self, index1, index2):
        raise NotImplementedError


class Sprite(DisplayObjectContainer):
    @property
    def buttonMode(self):
        return self._buttonMode

    @buttonMode.setter
    def buttonMode(self, value):
        self._buttonMode = value

    @property
    def dropTarget(self):
        raise NotImplementedError

    @property
    def graphics(self):
        return self._graphics

    @property
    def hitArea(self):
        return self._hitArea

    @hitArea.setter
    def hitArea(self, value: Graphics):
        self._hitArea = value

    @property
    def soundTransform(self):
        raise NotImplementedError

    @soundTransform.setter
    def soundTransform(self, value):
        raise NotImplementedError

    @property
    def useHandCursor(self):
        return self._useHandCursor

    @useHandCursor.setter
    def useHandCursor(self, value):
        self._useHandCursor = value

    def __init__(self):
        super().__init__()
        self._buttonMode = False
        self._graphics = Graphics()  # Don't know if this is correct
        self._hitArea = None  # self is used as hit area if this is not set
        self._useHandCursor = True

    def startDrag(self, lockCenter=False, bounds: Rectangle = None):
        raise NotImplementedError

    def startTouchDrag(self, touchPointID, lockCenter=False, bounds: Rectangle = None):
        raise NotImplementedError

    def stopDrag(self):
        raise NotImplementedError

    def stopTouchDrag(self, touchPointID):
        raise NotImplementedError


class ActionScriptVersion(Object):
    ACTIONSCRIPT2 = 2
    ACTIONSCRIPT3 = 3


class AVLoader:
    ...


class AVM1Movie:
    ...


class Bitmap:
    ...


class BitmapData:
    ...


class BitmapDataChannel:
    ...


class BitmapEncodingColorSpace(Object):
    COLORSPACE_4_2_0 = '4:2:0'
    COLORSPACE_4_2_2 = '4:2:2'
    COLORSPACE_4_4_4 = '4:4:4'
    COLORSPACE_AUTO = 'auto'


class BlendMode(Object):
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


class CapsStyle(Object):
    NONE = 'none'
    ROUND = 'round'
    SQUARE = 'square'


class ColorCorrection(Object):
    DEFAULR = 'default'
    OFF = 'off'
    ON = 'on'


class ColorCorrectionSupport(Object):
    DEFAULT_OFF = 'defaultOff'
    DEFAULT_ON = 'defualtOn'
    UNSUPPORTED = 'unsupported'


class FocusDirection(Object):
    BOTTOM = 'bottom'
    NONE = 'none'
    TOP = 'top'


class FrameLabel(EventDispatcher):
    @property
    def frame(self):
        return self._frame

    @property
    def name(self):
        return self._name

    def __init__(self, name, frame):
        # TODO: Dispatch Event('frameLabel')
        super().__init__()
        self._name = name
        self._frame = frame


class GradientType(Object):
    LINEAR = 'linear'
    RADIAL = 'radial'


class Graphics(Object):
    # TODO: Make class 'final'
    def __init__(self, **kwargs):
        # Only internal things are supposed to be able to instantiate this but
        # there is no way to implement access restrictions like that in python
        # so an argument will have to do.
        noerr = kwargs.get('__as3Internal_constructorErrorOverride', False)
        if not noerr:
            raise
        ...

    def beginBitmapFill(self, bitmap: BitmapData, matrix: Matrix = None, repeat=True, smooth=False):
        raise NotImplementedError

    def beginFill(self, color, alpha=1.0):
        raise NotImplementedError

    def beginGradientFill(self, type, colors, alphas, ratios, matrix: Matrix = None, spreadMethod='pad', interpolationMethod='rgb', focalPointRatio=0):
        raise NotImplementedError

    def beginShaderFill(self, shader: Shader, matrix: Matrix = None):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def copyFrom(self, sourceGraphics: Graphics):
        raise NotImplementedError

    def cubicCurveTo(self, controlX1, controlY1, controlX2, controlY2, anchorX, anchorY):
        raise NotImplementedError

    def drawCircle(self, x, y, radius):
        raise NotImplementedError

    def drawEllipse(self, x, y, width, height):
        raise NotImplementedError

    def drawGraphicsData(self, graphicsData):
        raise NotImplementedError

    def drawPath(self, commands, data, winding='evenOdd'):
        raise NotImplementedError

    def drawRect(self, x, y, width, height):
        raise NotImplementedError

    def drawRoundRect(self, x, y, width, height, ellipseWidth, ellipseHeight):
        raise NotImplementedError

    def drawTriangles(self, vertices, indicies=None, uvtData=None, culling='none'):
        raise NotImplementedError

    def endFill(self):
        raise NotImplementedError

    def lineBitmapStyle(self, bitmap: BitmapData, matrix: Matrix = None, repeat=True, smooth=False):
        raise NotImplementedError

    def lineGradientStyle(self, type, colors, alphas, ratios, matrix: Matrix = None, spreadMethod='pad', interpolationMethod='rgb', focalPointRatio=0):
        raise NotImplementedError

    def lineShaderStyle(self, shader: Shader, matrix: Matrix = None):
        raise NotImplementedError

    def lineStyle(self, thickness, color=0, alpha=1.0, pixelHinting=False, scaleMode='normal', caps=None, joints=None, miterLimit=3):
        raise NotImplementedError

    def lineTo(self, x, y):
        raise NotImplementedError

    def moveTo(self, x, y):
        raise NotImplementedError

    def readGraphicsData(self, recurse=True):
        raise NotImplementedError


class GraphicsBitmapFill:
    ...


class GraphicsEndFill:
    ...


class GraphicsGradientFill:
    ...


class GraphicsPath:
    ...


class GraphicsPathCommand(Object):
    NO_OP = 0
    MOVE_TO = 1
    LINE_TO = 2
    CURVE_TO = 3
    WIDE_MOVE_TO = 4
    WIDE_LINE_TO = 5
    CUBIC_CURVE_TO = 6


class GraphicsPathWinding:
    ...


class GraphicsShaderFill:
    ...


class GraphicsSolidFill:
    ...


class GraphicsStroke:
    ...


class GraphicsTrianglePath:
    ...


class InterpolationMethod(Object):
    LINEAR_RGB = 'linearRGB'
    RGB = 'rgb'


class JointStyle(Object):
    BEVEL = 'bevel'
    MITER = 'miter'
    ROUND = 'round'


class JPEGEncoderOptions:
    ...


class JPEGCREncoderOptions:
    ...


class LineScaleMode(Object):
    HORIZONTAL = 'horizontal'
    NONE = 'none'
    NORMAL = 'normal'
    VERTICAL = 'vertical'


class Loader:
    ...


class LoderInfo:
    ...


class MorphShape:
    ...


class MovieClip(Sprite):
    @property
    def currentFrame(self):
        return self._currentFrame

    @property
    def currentFrameLabel(self):
        return self._currentFrameLabel

    @property
    def currentLabel(self):
        return self._currentLabel

    @property
    def currentLabels(self):
        return self._currentLabels

    @property
    def currentScene(self):
        return self._currentScene

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def framesLoaded(self):
        return self._framesLoaded

    @property
    def isPlaying(self):
        return self._isPlaying

    @property
    def scenes(self):
        return self._scenes

    @property
    def totalFrames(self):
        return self._totalFrames

    @property
    def trackAsMenu(self):
        return self._trackAsMenu

    @trackAsMenu.setter
    def trackAsMenu(self, value):
        self._trackAsMenu = value

    def __init__(self):
        super().__init__()
        # Most of these are placeholder values
        self._currentFrame = 0
        self._currentFrameLabel = None
        self._currentLabel = None
        self._currentLabels = Array()
        self._currentScene = 0
        self._enabled = True
        self._framesLoaded = None
        self._isPlaying = False
        self._scenes = Array()
        self._totalFrames = None
        self._trackAsMenu = False

    def gotoAndPlay(self, frame, scene=None):
        raise NotImplementedError

    def gotoAndStop(self, frame, scene):
        raise NotImplementedError

    def nextFrame(self):
        raise NotImplementedError

    def nextScene(self):
        raise NotImplementedError

    def play(self):
        raise NotImplementedError

    def prevFrame(self):
        raise NotImplementedError

    def prevScene(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError


class NativeMenu(EventDispatcher):
    @property
    def isSupported(self):
        raise NotImplementedError

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
        self._items = Array()
        self._parent

    def addItem(self, item: NativeMenuItem):
        if item is None or item.menu is not None:
            raise ArgumentError()
        self._items.append(item)

    def addItemAt(self, item: NativeMenuItem, index):
        # TODO: Add RangeError when index is out of bounds
        if item is None or item.menu is not None:
            raise ArgumentError()
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

    def clone(self):
        raise NotImplementedError

    def containsItem(self, item: NativeMenuItem):
        for i in self._items:
            if i is item:
                return True
        return False

    def display(self, stage: Stage, stageX, stageY):
        raise NotImplementedError

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
    def checked(self):
        raise NotImplementedError

    @checked.setter
    def checked(self, value):
        raise NotImplementedError

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
    def keyEquivalent(self):
        raise NotImplementedError

    @keyEquivalent.setter
    def keyEquivalent(self, value):
        raise NotImplementedError

    @property
    def keyEquivalentModifiers(self):
        raise NotImplementedError

    @keyEquivalentModifiers.setter
    def keyEquivalentModifiers(self, value):
        raise NotImplementedError

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
    def mnemonicIndex(self):
        raise NotImplementedError

    @mnemonicIndex.setter
    def mnemonicIndex(self, value):
        raise NotImplementedError

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
        self._isSep = isSeparator
        self._label = label
        self._data = None
        self._enabled = True
        self._menu = None
        self._name = None
        self._subMenu = None

    def clone(self):
        raise NotImplementedError

    def toString(self):
        raise NotImplementedError


class NativeWindow(EventDispatcher):
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
    def bounds(self):
        raise NotImplementedError

    @property
    def closed(self):
        return false if self._windowObject else true

    @property
    def displayState(self):
        if self.closed:
            raise IllegalOperationError()
        raise NotImplementedError

    @property
    def height(self):
        raise NotImplementedError

    @property
    def isSupported(self):
        return True

    @property
    def maximizable(self):
        raise NotImplementedError

    @property
    def maxSize(self):
        raise NotImplementedError

    @property
    def menu(self):
        raise NotImplementedError

    @property
    def minimizable(self):
        raise NotImplementedError

    @property
    def minSize(self):
        raise NotImplementedError

    @property
    def owner(self):
        return self._owner

    @property
    def renderMode(self):
        raise NotImplementedError

    @property
    def resizable(self):
        raise NotImplementedError

    @property
    def stage(self):
        raise NotImplementedError

    @property
    def supportsMenu(self):
        raise NotImplementedError

    @property
    def supportsNotification(self):
        raise NotImplementedError

    @property
    def supportsTransparency(self):
        raise NotImplementedError

    @property
    def systemChrome(self):
        raise NotImplementedError

    @property
    def systemMaxSize(self):
        raise NotImplementedError

    @property
    def systemMinSize(self):
        raise NotImplementedError

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
    def transparent(self):
        raise NotImplementedError

    @property
    def type(self):
        raise NotImplementedError

    @property
    def visible(self):
        if self.closed:
            raise IllegalOperationError()
        raise NotImplementedError

    @visible.setter
    def visible(self, value):
        if self.closed:
            raise IllegalOperationError()
        raise NotImplementedError

    @property
    def width(self):
        raise NotImplementedError

    @property
    def x(self):
        raise NotImplementedError

    @property
    def y(self):
        raise NotImplementedError

    def __init__(self, initOptions: NativeWindowInitOptions = None):
        self._active = False
        self._alwaysInFront = False
        if initOptions is None:
            initOptions = NativeWindowInitOptions()
        if not isinstance(initOptions, NativeWindowInitOptions):
            raise IllegalOperationError()
        as3state.nativeApplication._guiInit()
        self._windowObject = tkinter.Toplevel()
        self.minimize()
        self._winNum = next(_windowNameGenerator)
        as3state.nativeApplication._addWindow(self._winNum, self)
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
        self._windowObject = None
        e = Event('close')
        e._target = self
        self.dispatchEvent(e)
        as3state.nativeApplication._removeWindow(self._id)

    def globalToScreen(self, globalPoint: Point):
        raise NotImplementedError

    def listOwnedWindows(self):
        raise NotImplementedError

    def maximize(self):
        if self.closed:
            raise IllegalOperationError()
        raise NotImplementedError

    def minimize(self):
        if self.closed:
            raise IllegalOperationError()
        raise NotImplementedError

    def notifyUser(self, type):
        raise NotImplementedError

    def orderInBackOf(self, window: NativeWindow):
        raise NotImplementedError

    def orderInFrontOf(self, window: NativeWindow):
        raise NotImplementedError

    def orderToBack(self):
        raise NotImplementedError

    def orderToFront(self):
        raise NotImplementedError

    def restore(self):
        if self.closed:
            raise IllegalOperationError()
        raise NotImplementedError

    def startMove(self):
        if self.closed:
            raise IllegalOperationError()
        raise NotImplementedError

    def startResize(self, edgeOrCorner):
        if self.closed:
            raise IllegalOperationError()
        raise NotImplementedError


class NativeWindowDisplayState(Object):
    MAXIMIZED = 'maximized'
    MINIMIZED = 'minimized'
    NORMAL = 'normal'


class NativeWindowInitOptions:
    # TODO: Add restraints for properties and make them actual properties
    def __init__(self, **kwargs):
        self.maximizable = Boolean(kwargs.get('maximizable', True))
        self.minimizable = Boolean(kwargs.get('minimizable', True))
        self.owner: NativeWindow = kwargs.get('owner', null)
        self.renderMode = String(kwargs.get('renderMode', ''))
        self.resizable = Boolean(kwargs.get('resizable', True))
        self.systemChrome = String(kwargs.get('systemChrome', NativeWindowSystemChrome.STANDARD))
        self.transparent = Boolean(kwargs.get('transparent', False))
        self.type = String(kwargs.get('type', NativeWindowType.NORMAL))


class NativeWindowRenderMode(Object):
    AUTO = 'auto'
    CPU = 'cpu'
    DIRECT = 'direct'
    GPU = 'gpu'


class NativeWindowResize(Object):
    BOTTOM = 'B'
    BOTTOM_LEFT = 'BL'
    BOTTOM_RIGHT = 'BR'
    LEFT = 'L'
    RIGHT = 'R'
    TOP = 'T'
    TOP_LEFT = 'TL'
    TOP_RIGHT = 'TR'


class NativeWindowSystemChrome(Object):
    ALTERNATE = 'alternate'
    NONE = 'none'
    STANDARD = 'standard'


class NativeWindowType(Object):
    LIGHTWEIGHT = 'lightweight'
    NORMAL = 'normal'
    UTILITY = 'utility'


class PixelSnapping(Object):
    ALWAYS = 'always'
    AUTO = 'auto'
    NEVER = 'never'


class PNGEncoderOptions:
    ...


class Scene:
    ...


class SceneMode:
    ...


class Screen(EventDispatcher):
    ...


class ScreenMode(Object):
    ...


class Shader:
    ...


class ShaderData:
    ...


class ShaderInput:
    ...


class ShaderJob:
    ...


class ShaderParameter:
    ...


class ShaderParameterType(Object):
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


class ShaderPrecision(Object):
    FAST = 'fast'
    FULL = 'full'


class Shape(DisplayObject):
    @property
    def graphics(self):
        return self._graphics

    def __init__(self):
        super().__init__(self)
        self._graphics = Graphics(__as3Internal_constructorErrorOverride=True)
        raise NotImplementedError


class SimpleButtom:
    ...


class SpreadMethod(Object):
    PAD = 'pad'
    REFLECT = 'reflect'
    REPEAT = 'repeat'


class Stage:
    ...


class Stage3D:
    ...


class StageAlign(Object):
    BOTTOM = 'B'
    BOTTOM_LEFT = 'BL'
    BOTTOM_RIGHT = 'BR'
    LEFT = 'L'
    RIGHT = 'R'
    TOP = 'T'
    TOP_LEFT = 'TL'
    TOP_RIGHT = 'TR'


class StageAspectRatio(Object):
    ANY = 'any'
    LANDSCAPE = 'landscape'
    PORTRAIT = 'portrait'


class StageDisplayState(Object):
    FULL_SCREEN = 'fullScreen'
    FULL_SCREEN_INTERACTIVE = 'fullScreenInteractive'
    NORMAL = 'normal'


class StageOrientation(Object):
    DEFAULT = 'default'
    ROTATED_LEFT = 'rotatedLeft'
    ROTATED_RIGHT = 'rotatedRight'
    UNKNOWN = 'unknown'
    UPSIDE_DOWN = 'upsideDown'


class StageQuality(Object):
    BEST = 'best'
    HIGH = 'high'
    HIGH_16X16 = '16x16'
    HIGH_16X16_LINEAR = '16x16linear'
    HIGH_8X8 = '8x8'
    HIGH_8X8_LINEAR = '8x8linear'
    LOW = 'low'
    MEDIUM = 'medium'


class StageScaleMode(Object):
    EXACT_FIT = 'exactFit'
    NO_BORDER = 'noBorder'
    NO_SCALE = 'noScale'
    SHOW_ALL = 'showAll'


class SWFVersion(Object):
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


class TriangleCulling(Object):
    NEGATIVE = 'negative'
    NONE = 'none'
    POSITIVE = 'positive'
