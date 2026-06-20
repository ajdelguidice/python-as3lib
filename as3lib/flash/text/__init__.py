from __future__ import annotations
from as3lib.metaclasses import _AS3_CONSTANTSOBJECT
from as3lib import Object
from . import engine, ime


class AntiAliasType:
    ...


class AutoCapitalize:
    ...


class CSMSettings:
    ...


class Font(Object):
    def __init__(self):
        # From the swf files that I've seen, flash seems to register the font without a manual call to registerFont. I'm unsure if it is done here.
        Font.registerFont(self)

    @staticmethod
    def enumerateFonts(enumerateDeviceFonts=False):
        raise NotImplementedError

    def hasGlyphs(self, str):
        raise NotImplementedError

    @staticmethod
    def registerFont(font):
        raise NotImplementedError


class FontStyle(_AS3_CONSTANTSOBJECT):
    BOLD = 'bold'
    BOLD_ITALIC = 'boldItalic'
    ITALIC = 'italic'
    REGULAR = 'regular'


class FontType(_AS3_CONSTANTSOBJECT):
    DEVICE = 'device'
    EMBEDDED = 'embedded'
    EMBEDDED_CFF = 'embeddedCFF'


class GridFitType:
    ...


class ReturnKeyLabel:
    ...


class SoftKeyboardType:
    ...


class StageText:
    ...


class StageTextClearButtonMode:
    ...


class StageTextInitOptions:
    ...


class StaticText:
    ...


class StyleSheet:
    ...


class TextColorType:
    ...


class TextDisplayMode:
    ...


class TextField:
    ...


class TextFieldAutoSize:
    ...


class TextFieldType:
    ...


class TextFormat:
    ...


class TextFormatAlign:
    ...


class TextInteractionMode:
    ...


class TextLineMetrics:
    ...


class TextRenderer:
    ...


class TextSnapshot:
    ...
