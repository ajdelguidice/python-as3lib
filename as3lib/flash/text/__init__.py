from __future__ import annotations
from as3lib import Boolean, false, Number, Object, String
from as3lib.flash.events import EventDispatcher
from as3lib.flash.display import DisplayObject, InteractiveObject
from . import engine, ime


class AntiAliasType(Object):
    ADVANCED = String('advanced')
    NORMAL = String('normal')


class AutoCapitalize(Object):
    ALL = String('all')
    NONE = String('none')
    SENTENCE = String('sentence')
    WORD = String('word')


class CSMSettings(Object):
    @property
    def fontSize(self):
        return self._fontSize

    @fontSize.setter
    def fontSize(self, value):
        self._fontSize = Number(value)

    @property
    def insideCutoff(self):
        return self._insideCutoff

    @insideCutoff.setter
    def insideCutoff(self, value):
        self._insideCutoff = Number(value)

    @property
    def outsideCutoff(self):
        return self._outsideCutoff

    @outsideCutoff.setter
    def outsideCutoff(self, value):
        self._outsideCutoff = Number(value)

    def __init__(self, fontSize: Number, insideCutoff: Number,
                 outsideCutoff: Number):
        self.fontSize = fontSize
        self.insideCutoff = insideCutoff
        self.outsideCutoff = outsideCutoff


class Font(Object):
    # TODO: Properties
    def __init__(self):
        # NOTE: From the swf files that I've seen, flash seems to register the font without a manual call to registerFont. I'm unsure if it is done here.
        Font.registerFont(self)

    @staticmethod
    def enumerateFonts(enumerateDeviceFonts: Boolean = false):
        raise NotImplementedError

    def hasGlyphs(self, str: String):
        raise NotImplementedError

    @staticmethod
    def registerFont(font):
        raise NotImplementedError


class FontStyle(Object):
    BOLD = String('bold')
    BOLD_ITALIC = String('boldItalic')
    ITALIC = String('italic')
    REGULAR = String('regular')


class FontType(Object):
    DEVICE = String('device')
    EMBEDDED = String('embedded')
    EMBEDDED_CFF = String('embeddedCFF')


class GridFitType(Object):
    NONE = String('none')
    PIXEL = String('pixel')
    SUBPIXEL = String('subpixel')


class ReturnKeyLabel(Object):
    DEFAULT = String('default')
    DONE = String('done')
    GO = String('go')
    NEXT = String('next')
    SEARCH = String('search')


class SoftKeyboardType(Object):
    CONTACT = String('contact')
    DECIMAL = String('decimal')
    DEFAULT = String('default')
    EMAIL = String('email')
    NUMBER = String('number')
    PHONE = String('phone')
    PUNCTUATION = String('punctuation')
    URL = String('url')


class StageText(EventDispatcher):
    ...


class StageTextClearButtonMode(Object):
    ALWAYS = String('always')
    NEVER = String('never')
    UNLESS_EDITING = String('unlessEditing')
    WHILE_EDITING = String('whileEditing')


class StageTextInitOptions(Object):
    @property
    def multiline(self):
        return self._multiline

    @multiline.setter
    def multiline(self, value):
        self._multiline = Boolean(value)

    def __init__(self, multiline: Boolean = false):
        self.multiline = multiline


class StaticText(DisplayObject):
    ...


class StyleSheet(EventDispatcher):
    ...


class TextColorType(Object):
    DARK_COLOR = String('darkColor')
    LIGHT_COLOR = String('lightColor')


class TextDisplayMode(Object):
    CRT = String('crt')
    DEFAULT = String('default')
    LCD = String('lcd')


class TextField(InteractiveObject):
    ...


class TextFieldAutoSize(Object):
    CENTER = String('center')
    LEFT = String('left')
    NONE = String('none')
    RIGHT = String('right')


class TextFieldType(Object):
    DYNAMIC = String('dynamic')
    INPUT = String('input')


class TextFormat(Object):
    ...


class TextFormatAlign(Object):
    CENTER = String('center')
    END = String('end')
    JUSTIFY = String('justify')
    LEFT = String('left')
    RIGHT = String('right')
    START = String('start')


class TextInteractionMode(Object):
    NORMAL = String('normal')
    SELECTION = String('selection')


class TextLineMetrics(Object):
    ...


class TextRenderer(Object):
    ...


class TextSnapshot(Object):
    ...
