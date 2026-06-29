from __future__ import annotations
from as3lib import (ArgumentError, Boolean, false, null, Number, Object,
                    String, uint)
from as3lib.flash.events import EventDispatcher


class TextJustifier(Object):
    @property
    def lineJustification(self):
        return self._lineJustification

    @lineJustification.setter
    def lineJustification(self, value):
        raise NotImplementedError

    @property
    def locale(self):
        return self._locale

    def __init__(self, locale: String, lineJustification: String):
        if self.__class__ is ContentElement:
            # This class is supposed to throw an ArgumentError if instantiated
            # but not from its children
            raise ArgumentError
        # TODO: Errors
        self._locale = String(locale)
        self._lineJustification = String(lineJustification)

    def clone(self):
        return TextJustifier(self.locale, self.lineJustification)

    @staticmethod
    def getJustifierForLocale(locale: String):
        raise NotImplementedError


class BreakOpportunity(Object):
    ALL = String('all')
    ANY = String('any')
    AUTO = String('auto')
    NONE = String('none')


class CFFHinting(Object):
    HORIZONTAL_STEM = String('horizontalStem')
    NONE = String('none')


class ContentElement(Object):
    GRAPHIC_ELEMENT = uint(0xfdef)

    @property
    def elementFormat(self):
        return self._elementFormat

    @elementFormat.setter
    def elementFormat(self, value):
        raise NotImplementedError

    @property
    def eventMirror(self):
        return self._eventMirror

    @eventMirror.setter
    def eventMirror(self, value):
        raise NotImplementedError

    @property
    def groupElement(self):
        raise NotImplementedError

    @property
    def rawText(self):
        raise NotImplementedError

    @property
    def text(self):
        raise NotImplementedError

    @property
    def textBlock(self):
        raise NotImplementedError

    @property
    def textBlockBeginIndex(self):
        raise NotImplementedError

    @property
    def textRotation(self):
        return self._textRotation

    @textRotation.setter
    def textRotation(self, value):
        self._textRotation = String(value)

    @property
    def userData(self):
        raise NotImplementedError

    @userData.setter
    def userData(self, value):
        raise NotImplementedError

    def __init__(self, elementFormat: ElementFormat = null,
                 eventMirror: EventDispatcher = null,
                 textRotation: String = 'rotate0'):
        if self.__class__ is ContentElement:
            # This class is supposed to throw an ArgumentError if instantiated
            # but not from its children
            raise ArgumentError
        self._elementFormat = elementFormat
        self._eventMirror = eventMirror
        self.textRotation = textRotation


class DigitCase(Object):
    DEFAULT = String('defualt')
    LINING = String('lining')
    OLD_STYLE = String('oldStyle')


class DigitWidth(Object):
    DEFAULT = String('defualt')
    PROPORTIONAL = String('proportional')
    TABULAR = String('tabular')


class EastAsianJustifier(TextJustifier):
    @property
    def composeTrailingIdeographicSpaces(self):
        return self._composeTrailingIdeographicSpaces

    @composeTrailingIdeographicSpaces.setter
    def composeTrailingIdeographicSpaces(self, value):
        self._composeTrailingIdeographicSpaces = Boolean(value)

    @property
    def justificationStyle(self):
        return self._justificationStyle

    @justificationStyle.setter
    def justificationStyle(self, value):
        self._justificationStyle = String(value)

    def __init__(self, locale: String = 'ja',
                 lineJustification: String = 'allButLast',
                 justificationStyle: String = 'pushInKinsoku'):
        super().__init__(locale, lineJustification)
        self.justificationStyle = justificationStyle
        self.composeTrailingIdeographicSpaces = false

    def clone(self):
        return EastAsianJustifier(self.locale, self.lineJustification, self.justificationStyle)


class ElementFormat:
    ...


class FontDescription:
    ...


class FontLookup(Object):
    DEVICE = String('device')
    EMBEDDED_CFF = String('embeddedCFF')


class FontMetrics:
    ...


class FontPosture(Object):
    ITALIC = String('italic')
    NORMAL = String('normal')


class FontWeight(Object):
    BOLD = String('bold')
    NORMAL = String('normal')


class GraphicElement(ContentElement):
    @property
    def elementHeight(self):
        return self._elementHeight

    @elementHeight.setter
    def elementHeight(self, value):
        self._elementHeight = Number(value)

    @property
    def elementWidth(self):
        return self._elementWidth

    @elementWidth.setter
    def elementWidth(self, value):
        self._elementWidth = Number(value)

    @property
    def graphic(self):
        return self._graphic

    @graphic.setter
    def graphic(self, value):
        raise NotImplementedError

    def __init__(self, graphic = null, elementWidth: Number = 15.0,
                 elementHeight: Number = 15.0,
                 elementFormat: ElementFormat = null,
                 eventMirror: EventDispatcher = null,
                 textRotation: String = 'rotate0'):
        super().__init__(elementFormat, eventMirror, textRotation)
        self._graphic = graphic
        self.elementWidth = elementWidth
        self.elementHeight = elementHeight


class GroupElement:
    ...


class JustificationStyle(Object):
    PRIORITIZE_LEAST_ADJUSTMENT = String('prioritizeLeastAdjustment')
    PUSH_IN_KINSOKU = String('pushInKinsoku')
    PUSH_OUT_ONLY = String('pushOutOnly')


class Kerning(Object):
    AUTO = String('auto')
    OFF = String('off')
    ON = String('on')


class LignatureLevel(Object):
    COMMON = String('common')
    EXOTIC = String('exotic')
    MINIMUM = String('minimum')
    NONE = String('none')
    UNCOMMON = String('uncommon')


class LineJustification(Object):
    ALL_BUT_LAST = String('allButLast')
    ALL_BUT_MANDATORY_BREAK = String('allButMandatoryBreak')
    ALL_INCLUDING_LAST = String('allIncludingLast')
    UNJUSTIFIED = String('unjustified')


class RenderingMode(Object):
    CFF = String('cff')
    NORMAL = String('normal')


class SpaceJustifier:
    ...


class TabAlignment(Object):
    CENTER = String('center')
    DECIMAL = String('decimal')
    END = String('end')
    START = String('start')


class TabStop(Object):
    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        self._alignment = String(value)

    @property
    def decimalAlignmentToken(self):
        return self._decimalAlignmentToken

    @decimalAlignmentToken.setter
    def decimalAlignmentToken(self, value):
        self._decimalAlignmentToken = String(value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = Number(value)

    def __init__(self, alignment: String = 'start', position: Number = 0.0,
                 decimalAlignmentToken: String = ''):
        self.alignment = alignment
        self.position = position
        self.decimalAlignmentToken = decimalAlignmentToken


class TextBaseline(Object):
    ASCENT = String('ascent')
    DESCENT = String('descent')
    IDEOGRAPHIC_BOTTOM = String('ideographicBottom')
    IDEOGRAPHIC_CENTER = String('ideographicCenter')
    IDEOGRAPHIC_TOP = String('ideographicTop')
    ROMAN = String('roman')
    USE_DOMINANT_BASELINE = String('useDominantBaseline')


class TextBlock:
    ...


class TextElement:
    ...


class TextLine:
    ...


class TextLineCreationResult(Object):
    COMPLETE = String('complete')
    EMERGENCY = String('emergency')
    INSUFFICIENT_WIDTH = String('insufficientWidth')
    SUCCESS = String('success')


class TextLineMirrorRegion:
    ...


class TextLineValidity(Object):
    INVALID = String('invalid')
    POSSIBLY_INVALID = String('possiblyInvalid')
    STATIC = String('static')
    VALID = String('valid')


class TextRotation(Object):
    AUTO = String('auto')
    ROTATE_0 = String('rotate0')
    ROTATE_180 = String('rotate180')
    ROTATE_270 = String('rotate270')
    ROTATE_90 = String('rotate90')


class TypographicCase(Object):
    CAPS = String('caps')
    CAPS_AND_SMALL_CAPS = String('capsAndSmallCaps')
    DEFAULT = String('default')
    LOWERCASE = String('lowercase')
    SMALL_CAPS = String('smallCaps')
    TITLE = String('title')
    UPPERCASE = String('uppercase')
