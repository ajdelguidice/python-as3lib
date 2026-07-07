from __future__ import annotations
from as3lib import (ArgumentError, Boolean, false, int, null, Number, Object,
                    String, true, uint)
from as3lib.flash.display import DisplayObjectContainer
from as3lib.flash.errors import IllegalOperationError
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


class ElementFormat(Object):
    ...


class FontDescription(Object):
    @property
    def cffHinting(self):
        return self._cffHinting

    @cffHinting.setter
    def cffHinting(self, value):
        if self.locked:
            raise IllegalOperationError
        if value not in {CFFHinting.HORIZONTAL_STEM, CFFHinting.NONE}:
            # TODO: Use "value not in CFFHinting" on in is implemented correctly
            raise ArgumentError
        self._cffHinting = String(value)

    @property
    def fontLookup(self):
        return self._fontLookup

    @fontLookup.setter
    def fontLookup(self, value):
        if self.locked:
            raise IllegalOperationError
        if value not in {FontLookup.DEVICE, FontLookup.EMBEDDED_CFF}:
            ...
        self._fontLookup = String(value)

    @property
    def fontName(self):
        return self._fontName

    @fontName.setter
    def fontName(self, value):
        if self.locked:
            raise IllegalOperationError
        self._fontName = String(value)

    @property
    def fontPosture(self):
        return self._fontPosture

    @fontPosture.setter
    def fontPosture(self, value):
        if self.locked:
            raise IllegalOperationError
        if value not in {FontPosture.ITALIC, FontPosture.NORMAL}:
            # TODO: Use "value not in FontPosture" on in is implemented correctly
            raise ArgumentError
        self._fontPosture = String(value)

    @property
    def fontWeight(self):
        return self._fontWeight

    @fontWeight.setter
    def fontWeight(self, value):
        if self.locked:
            raise IllegalOperationError
        if value not in {FontWeight.BOLD, FontWeight.NORMAL}:
            # TODO: Use "value not in FontWeight" on in is implemented correctly
            raise ArgumentError
        self._fontWeight = String(value)

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        if self.locked:
            raise IllegalOperationError
        self._locked = Boolean(value)

    @property
    def renderingMode(self):
        return self._renderingMode

    @renderingMode.setter
    def renderingMode(self, value):
        if self.locked:
            raise IllegalOperationError
        if value not in {RenderingMode.CFF, RenderingMode.NORMAL}:
            # TODO: Use "value not in RenderingMode" on in is implemented correctly
            raise ArgumentError
        self._renderingMode = String(value)

    def __init__(self, fontName: String = '_serif',
                 fontWeight: String = 'normal',
                 fontPosture: String = 'normal',
                 fontLookup: String = 'device', renderingMode: String = 'cff',
                 cffHinting: String = 'horizontalStem'):
        self._locked = false
        self.fontName = fontName
        self.fontWeight = fontWeight
        self.fontPosture = fontPosture
        self.fontLookup = fontLookup
        self.renderingMode = renderingMode
        self.cffHinting = cffHinting

    def clone(self):
        return FontDescription(self.fontName, self.fontWeight,
                               self.fontPosture, self.fontLookup,
                               self.renderingMode, self.cffHinting)

    @staticmethod
    def isDeviceFontCompatible(fontName: String, fontWeight: String,
                               fontPosture: String):
        # TODO: Return true if a device font is found with the specified
        #       properties. Can only use OpenType and TrueType fonts
        fontName = String(fontName)
        fontWeight = String(fontWeight)
        fontPosture = String(fontPosture)
        if fontWeight not in {FontWeight.BOLD, FontWeight.NORMAL}:
            # TODO: Use "fontWeight not in FontWeight" on in is implemented correctly
            raise ArgumentError
        if fontPosture not in {FontPosture.ITALIC, FontPosture.NORMAL}:
            # TODO: Use "fontPosture not in FontPosture" on in is implemented correctly
            raise ArgumentError
        raise NotImplementedError

    @staticmethod
    def isFontCompatible(fontName: String, fontWeight: String,
                         fontPosture: String):
        fontName = String(fontName)
        fontWeight = String(fontWeight)
        fontPosture = String(fontPosture)
        if fontWeight not in {FontWeight.BOLD, FontWeight.NORMAL}:
            # TODO: Use "fontWeight not in FontWeight" on in is implemented correctly
            raise ArgumentError
        if fontPosture not in {FontPosture.ITALIC, FontPosture.NORMAL}:
            # TODO: Use "fontPosture not in FontPosture" on in is implemented correctly
            raise ArgumentError
        raise NotImplementedError


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


class GroupElement(ContentElement):
    @property
    def elementCount(self):
        return self._elements.length

    def __init__(self, elements = null, elementFormat: ElementFormat = null,
                 eventMirror: EventDispatcher = null,
                 textRotation: String = 'rotate0'):
        # TODO: Errors
        super().__init__(elementFormat, eventMirror, textRotation)
        self._elements = elements

    def getElementAt(self, index: int):
        raise NotImplementedError

    def getElementAtCharIndex(self, charIndex: int):
        raise NotImplementedError

    def getElementIndex(self, element: ContentElement):
        raise NotImplementedError

    def groupElements(self, beginIndex: int, endIndex: int):
        raise NotImplementedError

    def mergeTextElements(self, beginIndex: int, endIndex: int):
        raise NotImplementedError

    def replaceElements(self, beginIndex: int, endIndex: int, newElements):
        raise NotImplementedError

    def setElements(self, value):
        raise NotImplementedError

    def splitTextElement(self, elementIndex: int, splitIndex: int):
        raise NotImplementedError

    def ungroupElements(self, groupIndex: int):
        raise NotImplementedError


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


class SpaceJustifier(TextJustifier):
    @property
    def letterSpacing(self):
        return self._letterSpacing

    @letterSpacing.setter
    def letterSpacing(self, value):
        self._letterSpacing = Boolean(value)

    @property
    def maximumSpacing(self):
        return self._maximumSpacing

    @maximumSpacing.setter
    def maximumSpacing(self, value):
        self._maximumSpacing = Number(value)

    @property
    def minimumSpacing(self):
        return self._minimumSpacing

    @minimumSpacing.setter
    def minimumSpacing(self, value):
        self._minimumSpacing = Number(value)

    @property
    def optimumSpacing(self):
        return self._optimumSpacing

    @optimumSpacing.setter
    def optimumSpacing(self, value):
        self._optimumSpacing = Number(value)

    def __init__(self, locale: String = 'em',
                 lineJustification: String = 'unjustified',
                 letterSpacing: Boolean = false):
        super().__init__(locale, lineJustification)
        self.letterSpacing = letterSpacing

        # TODO: Find out where these values come from
        self.maximumSpacing = 1.5
        self.minimumSpacing = 0.5
        self.optimumSpacing = 1.0

    def clone(self):
        raise NotImplementedError


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


class TextElement(ContentElement):
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value if value is null else String(value)

    def __init__(self, text: String = null,
                 elementFormat: ElementFormat = null,
                 eventMirror: EventDispatcher = null,
                 textRotation: String = 'rotate0'):
        super().__init__(elementFormat, eventMirror, textRotation)
        self.text = text

    def replaceText(self, beginIndex: int, endIndex: int, newText: String):
        raise NotImplementedError


class TextLine(DisplayObjectContainer):
    ...


class TextLineCreationResult(Object):
    COMPLETE = String('complete')
    EMERGENCY = String('emergency')
    INSUFFICIENT_WIDTH = String('insufficientWidth')
    SUCCESS = String('success')


class TextLineMirrorRegion(Object):
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
