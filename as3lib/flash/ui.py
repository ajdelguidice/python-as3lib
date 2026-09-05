from __future__ import annotations
from as3lib import Array, Boolean, Error, false, int, null, Number, Object, String, true, uint, Vector
from as3lib.flash.display import BitmapData, NativeMenu, NativeMenuItem, Stage
from as3lib.flash.events import EventDispatcher
from as3lib.flash.geom import Point
from as3lib.helpers import staticproperty


class ContextMenu(NativeMenu):
    @property
    def builtInItems(self):
        raise NotImplementedError

    @builtInItems.setter
    def builtInItems(self, value: ContextMenuBuiltInItems):
        raise NotImplementedError

    @property
    def clipboardItems(self):
        raise NotImplementedError

    @clipboardItems.setter
    def clipboardItems(self, value: ContextMenuClipboardItems):
        raise NotImplementedError

    @property
    def clipboardMenu(self):
        raise NotImplementedError

    @clipboardMenu.setter
    def clipboardMenu(self, value):
        raise NotImplementedError

    @property
    def customItems(self):
        raise NotImplementedError

    @customItems.setter
    def customItems(self, value):
        raise NotImplementedError

    @property
    def isSupported(self):
        raise NotImplementedError

    @property
    def items(self):
        raise NotImplementedError

    @items.setter
    def items(self, value):
        raise NotImplementedError

    @property
    def link(self):
        raise NotImplementedError

    @link.setter
    def link(self, value):
        raise NotImplementedError

    @property
    def numItems(self):
        raise NotImplementedError

    def __init__(self):
        raise NotImplementedError

    def addItemAt(self, item: NativeMenuItem, index):
        raise NotImplementedError

    def clone(self):
        raise NotImplementedError

    def containsItem(self, item: NativeMenuItem):
        raise NotImplementedError

    def display(self, stage: Stage, stageX, stageY):
        raise NotImplementedError

    def getItemAt(self, index):
        raise NotImplementedError

    def getItemIndex(self, item: NativeMenuItem):
        raise NotImplementedError

    def hideBuiltInItems(self):
        raise NotImplementedError

    def removeAllItems(self):
        raise NotImplementedError

    def removeItemsAt(self, index):
        raise NotImplementedError


class ContextMenuBuiltInItems(Object):
    @property
    def forwardAndBack(self):
        return self._forwardAndBack

    @forwardAndBack.setter
    def forwardAndBack(self, value: Boolean):
        self._forwardAndBack = Boolean(value)

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: Boolean):
        self._loop = Boolean(value)

    @property
    def play(self):
        return self._play

    @play.setter
    def play(self, value: Boolean):
        self._play = Boolean(value)

    @property
    def print(self):
        return self._print

    @print.setter
    def print(self, value: Boolean):
        self._print = Boolean(value)

    @property
    def quality(self):
        return self._quality

    @quality.setter
    def quality(self, value: Boolean):
        self._quality = Boolean(value)

    @property
    def rewind(self):
        return self._rewind

    @rewind.setter
    def rewind(self, value: Boolean):
        self._rewind = Boolean(value)

    @property
    def save(self):
        return self._save

    @save.setter
    def save(self, value: Boolean):
        self._save = Boolean(value)

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value: Boolean):
        self._zoom = Boolean(value)

    def __init__(self):
        # TODO: Validate these values
        self.forwardAndBack = true
        self.loop = true
        self.play = true
        self.print = true
        self.quality = true
        self.rewind = true
        self.save = true
        self.zoom = true


class ContextMenuClipboardItems(Object):
    @property
    def clear(self):
        return self._clear

    @clear.setter
    def clear(self, value: Boolean):
        self._clear = Boolean(value)

    @property
    def copy(self):
        return self._copy

    @copy.setter
    def copy(self, value: Boolean):
        self._copy = Boolean(value)

    @property
    def cut(self):
        return self._cut

    @cut.setter
    def cut(self, value: Boolean):
        self._cutm = Boolean(value)

    @property
    def paste(self):
        return self._paste

    @paste.setter
    def paste(self, value: Boolean):
        self._paste = Boolean(value)

    @property
    def selectAll(self):
        return self._selectAll

    @selectAll.setter
    def selectAll(self, value: Boolean):
        self._selectAll = Boolean(value)

    def __init__(self):
        # TODO: Validate these values
        self.clear = true
        self.copy = true
        self.cut = true
        self.paste = true
        self.selectAll = true


class ContextMenuItem(NativeMenuItem):
    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, value: String):
        '''
        TODO:
        Each caption must contain at least one visible character.
        Control characters, newlines, and other white space characters are ignored.
        Captions that are identical to any built-in menu item, or to another custom item, are ignored, whether the matching item is visible or not. Menu captions are compared to built-in captions or existing custom captions without regard to case, punctuation, or white space.
        '''
        # Captions can not be more than 100 characters long.
        value = str(String(value))
        if len(value) > 100:
            raise Error('Captions can not be more than 100 characters long.')
        # Restricted captions
        if value in {'Save', 'Zoom In', 'Zoom Out', '100%', 'Show All', 'Quality', 'Play', 'Loop', 'Rewind', 'Forward', 'Back', 'Movie not loaded', 'About', 'Print', 'Show Redraw Regions', 'Debugger', 'Undo', 'Cut', 'Copy', 'Paste', 'Delete', 'Select All', 'Open', 'Open in new window', 'Copy link'}:
            raise Error(f'Caption "{value}" is not allowed.')
        # Restricted phrases
        if value.find('Adobe') != -1 or value.find('Macromedia') != -1 or value.find('Flash Player') != -1 or value.find('Settings') != -1:
            raise Error(f'Caption {value} contains a restricted phrase.')
        self._caption = String(value)

    @property
    def separatorBefore(self):
        return self._separatorBefore

    @separatorBefore.setter
    def separatorBefore(self, value: Boolean):
        self._separatorBefore = Boolean(value)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value: Boolean):
        self._visible = Boolean(value)

    def __init__(self, caption: String, separatorBefore: Boolean = false,
                 enabled: Boolean = true, visible: Boolean = true):
        super().__init__('')
        self.caption = caption
        self.separatorBefore = separatorBefore
        self.enabled = enabled  # Handled by NativeMenuItem
        self.visible = visible

    def clone(self):
        raise NotImplementedError

    @staticmethod
    def systemClearMenuItem():
        raise NotImplementedError

    @staticmethod
    def systemCopyLinkMenuItem():
        raise NotImplementedError

    @staticmethod
    def systemCopyMenuItem():
        raise NotImplementedError

    @staticmethod
    def systemCutMenuItem():
        raise NotImplementedError

    @staticmethod
    def systemOpenLinkMenuItem():
        raise NotImplementedError

    @staticmethod
    def systemPasteMenuItem():
        raise NotImplementedError

    @staticmethod
    def systemSelectAllMenuItem():
        raise NotImplementedError


class GameInput(EventDispatcher):
    ...


class GameInputControl(EventDispatcher):
    ...


class GameInputDevice(Object):
    MAX_BUFFER_SIZE = int(32000)
    ...


class Keyboard(Object):
    BACKSPACE = uint(8)
    TAB = uint(9)

    ENTER = uint(13)

    COMMAND = uint(15)
    SHIFT = uint(16)
    CONTROL = uint(17)
    ALTERNATE = uint(18)  # Alt/Option

    CAPS_LOCK = uint(20)
    NUMPAD = uint(21)  # Numpad pseudo-key (whatever that means)

    ESCAPE = uint(27)

    SPACE = uint(32)
    PAGE_UP = uint(33)
    PAGE_DOWN = uint(34)
    END = uint(35)
    HOME = uint(36)
    LEFT = uint(37)
    UP = uint(38)
    RIGHT = uint(39)
    DOWN = uint(40)

    INSERT = uint(45)
    DELETE = uint(46)

    NUMBER_0 = uint(48)
    NUMBER_1 = uint(49)
    NUMBER_2 = uint(50)
    NUMBER_3 = uint(51)
    NUMBER_4 = uint(52)
    NUMBER_5 = uint(53)
    NUMBER_6 = uint(54)
    NUMBER_7 = uint(55)
    NUMBER_8 = uint(56)
    NUMBER_9 = uint(57)

    A = uint(65)
    B = uint(66)
    C = uint(67)
    D = uint(68)
    E = uint(69)
    F = uint(70)
    G = uint(71)
    H = uint(72)
    I = uint(73)
    J = uint(74)
    K = uint(75)
    L = uint(76)
    M = uint(77)
    N = uint(78)
    O = uint(79)
    P = uint(80)
    Q = uint(81)
    R = uint(82)
    S = uint(83)
    T = uint(84)
    U = uint(85)
    V = uint(86)
    W = uint(87)
    X = uint(88)
    Y = uint(89)
    Z = uint(90)

    NUMPAD_0 = uint(96)
    NUMPAD_1 = uint(97)
    NUMPAD_2 = uint(98)
    NUMPAD_3 = uint(99)
    NUMPAD_4 = uint(100)
    NUMPAD_5 = uint(101)
    NUMPAD_6 = uint(102)
    NUMPAD_7 = uint(103)
    NUMPAD_8 = uint(104)
    NUMPAD_9 = uint(105)
    NUMPAD_MULTIPLY = uint(106)
    NUMPAD_ADD = uint(107)
    NUMPAD_ENTER = uint(108)
    NUMPAD_SUBTRACT = uint(109)
    NUMPAD_DECIMAL = uint(110)
    NUMPAD_DIVIDE = uint(111)
    F1 = uint(112)
    F2 = uint(113)
    F3 = uint(114)
    F4 = uint(115)
    F5 = uint(116)
    F6 = uint(117)
    F7 = uint(118)
    F8 = uint(119)
    F9 = uint(120)
    F10 = uint(121)
    F11 = uint(122)
    F12 = uint(123)
    F13 = uint(124)
    F14 = uint(125)
    F15 = uint(126)

    SEMICOLON = uint(186)
    EQUAL = uint(187)
    COMMA = uint(188)
    MINUS = uint(189)
    PERIOD = uint(190)
    SLASH = uint(191)
    BACKQUOTE = uint(192)

    LEFTBRACKET = uint(219)
    BACKSLASH = uint(220)
    RIGHTBRACKET = uint(221)
    QUOTE = uint(222)

    RED = uint(0x01000000)
    GREEN = uint(0x01000001)
    YELLOW = uint(0x01000002)
    BLUE = uint(0x01000003)
    CHANNEL_UP = uint(0x01000004)
    CHANNEL_DOWN = uint(0x01000005)
    RECORD = uint(0x01000006)
    PLAY = uint(0x01000007)
    PAUSE = uint(0x01000008)
    STOP = uint(0x01000009)
    FAST_FORWARD = uint(0x0100000A)
    REWIND = uint(0x0100000B)
    SKIP_FORWARD = uint(0x0100000C)
    SKIP_BACKWARD = uint(0x0100000D)
    NEXT = uint(0x0100000E)
    PREVIOUS = uint(0x0100000F)
    LIVE = uint(0x01000010)
    LAST = uint(0x01000011)
    MENU = uint(0x01000012)
    INFO = uint(0x01000013)
    GUIDE = uint(0x01000014)
    EXIT = uint(0x01000015)
    BACK = uint(0x01000016)
    AUDIO = uint(0x01000017)
    SUBTITLE = uint(0x01000018)
    DVR = uint(0x01000019)
    VOD = uint(0x0100001A)
    INPUT = uint(0x0100001B)
    SETUP = uint(0x0100001C)
    HELP = uint(0x0100001D)
    MASTER_SHELL = uint(0x0100001E)
    SEARCH = uint(0x0100001F)
    PLAY_PAUSE = uint(0x01000020)

    # TODO: KEYNAME_*
    # TODO: STRING_*

    CharCodeStrings = Array()  # TODO

    @staticproperty
    def capsLock(cls):
        raise NotImplementedError

    @staticproperty
    def hasVirtualKeyboard(cls):
        raise NotImplementedError

    @staticproperty
    def numLock(cls):
        raise NotImplementedError

    @staticproperty
    def physicalKeyboardType(cls):
        raise NotImplementedError

    @staticmethod
    def isAccessible():
        raise NotImplementedError


class KeyboardType(Object):
    ALPHANUMERIC = String('alphanumeric')
    KEYPAD = String('keypad')
    NONE = String('none')


class KeyLocation(Object):
    STANDARD = uint(0)
    LEFT = uint(1)
    RIGHT = uint(2)
    NUM_PAD = uint(3)
    D_PAD = uint(4)


class MouseCursorData(Object):
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: Vector[BitmapData]):
        # TODO: Proper type check
        if not isinstance(value, Vector):
            raise
        self._data = value

    @property
    def frameRate(self):
        return self._frameRate

    @frameRate.setter
    def frameRate(self, value: Number):
        self._frameRate = Number(value)

    @property
    def hotSpot(self):
        return self._hotSpot

    @hotSpot.setter
    def hotSpot(self, value: Point):
        if not isinstance(value, Point):
            raise
        self._hotSpot = value

    def __init__(self):
        self._data = null
        self.frameRate = 0
        self.hotSpot = Point(0, 0)


class Mouse(Object):
    @staticproperty
    def cursor(cls):
        raise NotImplementedError

    @cursor.setter
    def cursor(cls, value: String):
        raise NotImplementedError

    @staticproperty
    def supportsCursor(cls):
        raise NotImplementedError

    @staticproperty
    def supportsNativeCursor(cls):
        raise NotImplementedError

    @staticmethod
    def hide():
        raise NotImplementedError

    @staticmethod
    def registerCursor(name: String, cursor: MouseCursorData):
        raise NotImplementedError

    @staticmethod
    def show():
        raise NotImplementedError

    @staticmethod
    def unregisterCursor(name: String):
        raise NotImplementedError


class MouseCursor(Object):
    ARROW = String('arrow')
    AUTO = String('auto')
    BUTTON = String('button')
    HAND = String('hand')
    IBEAM = String('ibeam')


class Multitouch(Object):
    ...


class MultitouchInputMode(Object):
    GESTURE = String('gesture')
    NONE = String('none')
    TOUCH_POINT = String('touchPoint')
