from as3lib import Boolean, Number, Object, String, true
from as3lib.flash.display import MovieClip, Sprite


class ComponentShim(MovieClip):
    # This was included inside of every decompiled flash project I checked but
    # it isn't in the documentation. I have no clue how it's used
    ...


class InvalidationType(Object):
    All = 'all'
    DATA = 'data'
    RENDERER_STYLES = 'rendererStyles'
    SCROLL = 'scroll'
    SELECTED = 'selected'
    SIZE = 'size'
    STATE = 'state'
    STYLES = 'styles'


class UIComponent(Sprite):
    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = Boolean(value)

    @property
    def focusEnabled(self):
        return self._focusEnabled

    @focusEnabled.setter
    def focusEnabled(self, value):
        self._focusEnabled = Boolean(value)

    @property
    def focusManager(self):
        raise NotImplementedError

    @focusManager.setter
    def focusManager(self, value):
        raise NotImplementedError

    @property
    def height(self):
        raise NotImplementedError

    @height.setter
    def height(self, value):
        raise NotImplementedError

    @property
    def mouseFocusEnabled(self):
        return self._mouseFocuseEnabled

    @mouseFocusEnabled.setter
    def mouseFocusEnabled(self, value):
        self._mouseFocuseEnabled = Boolean(value)

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
    def visible(self):
        raise NotImplementedError

    @visible.setter
    def visible(self, value):
        raise NotImplementedError

    @property
    def width(self):
        raise NotImplementedError

    @width.setter
    def width(self, value):
        raise NotImplementedError

    @property
    def x(self):
        raise NotImplementedError

    @x.setter
    def x(self, value):
        raise NotImplementedError

    @property
    def y(self):
        raise NotImplementedError

    @y.setter
    def y(self, value):
        raise NotImplementedError

    def __init__(self):
        super().__init__()
        self._enabled = true
        self._focusEnabled = true

        self._mouseFocusEnabled = true
        ...

    def clearStyle(self, style: String):
        raise NotImplementedError

    def drawFocus(self, focused: Boolean):
        raise NotImplementedError

    def drawNow(self):
        raise NotImplementedError

    def getFocus(self):
        raise NotImplementedError

    def getStyle(self, style: String):
        raise NotImplementedError

    @staticmethod
    def getStyleDefinition():
        raise NotImplementedError

    def invalidate(self, property: String, callLater: Boolean = true):
        raise NotImplementedError

    @staticmethod
    def mergeStyles(*list):
        raise NotImplementedError

    def move(self, x: Number, y: Number):
        raise NotImplementedError

    def setFocus(self):
        raise NotImplementedError

    def setSize(self, width: Number, height: Number):
        raise NotImplementedError

    def setStyle(self, style: String, value: Object):
        raise NotImplementedError

    def validateNow(self):
        raise NotImplementedError

    def getStyleValue(self, name: String):
        # TODO: protected
        raise NotImplementedError
