from as3lib import (Array, Boolean, false, int, null, Number, Object, String,
                    true, uint)
from as3lib.flash.events import ErrorEvent, Event


# Classes
class ListEvent(Event):
    ITEM_CLICK = String('itemClick')
    ITEM_DOUBLE_CLICK = String('itemDoubleClick')
    ITEM_ROLL_OUT = String('itemRollOut')
    ITEM_ROLL_OVER = String('itemRollOver')

    @property
    def columnIndex(self):
        return self._columnIndex

    @property
    def index(self):
        return self._index

    @property
    def item(self):
        return self._item

    @property
    def rowIndex(self):
        return self._rowIndex

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, columnIndex: int = -1,
                 rowIndex: int = -1, index: int = -1, item: Object = null):
        super().__init__(type, bubbles, cancelable)
        self._columnIndex = int(columnIndex)
        self._rowIndex = int(rowIndex)
        self._index = int(index)
        self._item = item

    def clone(self):
        return ListEvent(self.type, self.bubbles, self.cancelable,
                         self.columnIndex, self.rowIndex, self.index,
                         self.item)

    def toString(self):
        return self.formatToString('ListEvent', 'type', 'bubbles',
                                   'cancelable', 'columnIndex', 'rowIndex')


class ColorPickerEvent(Event):
    CHANGE = String('change')
    ENTER = String('enter')
    ITEM_ROLL_OUT = String('itemRollOut')
    ITEM_ROLL_OVER = String('itemRollOver')

    @property
    def color(self):
        return self._color

    def __init__(self, type: String, color: uint):
        super().__init__(type, true, true)
        self._color = uint(color)

    def clone(self):
        return ColorPickerEvent(self.type, self.color)

    def toString(self):
        return self.formatToString('ColorPickerEvent', 'type', 'bubbles',
                                   'cancelable', 'color')


class ComponentEvent(Event):
    BUTTON_DOWN = String('buttonDown')
    ENTER = String('enter')
    HIDE = String('hide')
    LABEL_CHANGE = String('labelChange')
    MOVE = String('move')
    RESIZE = String('resize')
    SHOW = String('show')

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false):
        super().__init__(type, bubbles, cancelable)

    def clone(self):
        return ComponentEvent(self.type, self.bubbles, self.cancelable)

    def toString(self):
        return self.formatToString('ComponentEvent', 'type', 'bubbles',
                                   'cancelable')


class DataChangeEvent(Event):
    DATA_CHANGE = String('dataChange')
    PRE_DATA_CHANGE = String('preDataChange')

    @property
    def changeType(self):
        return self._changeType

    @property
    def endIndex(self):
        return self._endIndex

    @property
    def items(self):
        return self._items

    @property
    def startIndex(self):
        return self._startIndex

    def __init__(self, eventType: String, changeType: String, items: Array,
                 startIndex: int = -1, endIndex: int = -1):
        super().__init__(eventType, false, false)
        self._changeType = String(changeType)
        self._items = items  # TODO: Coerce to Array
        self._startIndex = int(startIndex)
        self._endIndex = int(endIndex)

    def clone(self):
        return DataChangeEvent(self.type, self.changeType, self.items,
                               self.startIndex, self.endIndex)

    def toString(self):
        return self.formatToString('DataChangeEvent', 'type', 'changeType',
                                   'startIndex', 'endIndex', 'bubbles',
                                   'cancelable')


class DataChangeType(Object):
    ADD = String('add')
    CHANGE = String('change')
    INVALIDATE = String('invalidate')
    INVALIDATE_ALL = String('invalidateAll')
    REMOVE = String('remove')
    REMOVE_ALL = String('removeAll')
    REPLACE = String('replace')
    SORT = String('sort')


class DataGridEvent(ListEvent):
    COLUMN_STRETCH = String('columnStretch')
    HEADER_RELEASE = String('headerRelease')
    ITEM_EDIT_BEGIN = String('itemEditBegin')
    ITEM_EDIT_BEGINNING = String('itemEditBeginning')
    ITEM_EDIT_END = String('itemEditEnd')
    ITEM_FOCUS_IN = String('itemFocusIn')
    ITEM_FOCUS_OUT = String('itemFocusOut')

    @property
    def dataField(self):
        return self._dataField

    @dataField.setter
    def dataField(self, value):
        self._dataField = String(value)

    @property
    def itemRenderer(self):
        return self._itemRenderer

    @property
    def reason(self):
        return self._reason

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, columnIndex: int = -1,
                 rowIndex: int = -1, itemRenderer: Object = null,
                 dataField: String = null, reason: String = null):
        super().__init__(type, bubbles, cancelable, columnIndex, rowIndex)
        self._itemRenderer = itemRenderer
        self._dataField = String(dataField)
        self._reason = String(reason)

    def clone(self):
        return DataGridEvent(self.type, self.bubbles, self.cancelable,
                             self.columnIndex, self.rowIndex,
                             self.itemRenderer, self.dataField, self.reason)

    def toString(self):
        return self.formatToString('DataGridEvent', 'type', 'bubbles',
                                   'cancelable', 'columnIndex', 'rowIndex',
                                   'itemRenderer', 'dataField', 'reason')


class DataGridEventReason(Object):
    CANCELED = String('cancelled')
    NEW_COLUMN = String('newColumn')
    NEW_ROW = String('newRow')
    OTHER = String('other')


class InteractionInputType(Object):
    KEYBOARD = String('keyboard')
    MOUSE = String('mouse')


class RSLErrorEvent(ErrorEvent):
    RSL_LOAD_FAILED = String('rslLoadFailed')

    @property
    def failedURLs(self):
        return self._failedURLs

    @property
    def rslsFailed(self):
        return self._rslsFailed

    @property
    def rslsLoaded(self):
        return self._rslsLoaded

    @property
    def rslsTotal(self):
        return self._rslsTotal

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, rslsLoaded: int = 0,
                 rslsFailed: int = 0, rslsTotal: int = 0,
                 failedURLs: Array = null):
        super().__init__(type, bubbles, cancelable)
        # TODO: Coerce to Array
        self._rslsLoaded = int(rslsLoaded)
        self._rslsFailed = int(rslsFailed)
        self._rslsTotal = int(rslsTotal)
        self._failedURLs = Array() if failedURLs is null else failedURLs


class RSLEvent(Event):
    RSL_LOAD_COMPLETE = String('rslLoadComplete')
    RSL_PROGRESS = String('rslProgress')

    @property
    def bytesLoaded(self):
        return self._bytesLoaded

    @property
    def bytesTotal(self):
        return self._bytesTotal

    @property
    def rslsFailed(self):
        return self._rslsFailed

    @property
    def rslsLoaded(self):
        return self._rslsLoaded

    @property
    def rslsTotal(self):
        return self._rslsTotal

    def __init__(self, type: String, bubbles: Boolean = false,
                 cancelable: Boolean = false, rslsLoaded: int = 0,
                 rslsFailed: int = 0, rslsTotal: int = 0,
                 bytesLoaded: int = 0, bytesTotal: int = 0):
        super().__init__(type, bubbles, cancelable)
        self._rslsLoaded = int(rslsLoaded)
        self._rslsFailed = int(rslsFailed)
        self._rslsTotal = int(rslsTotal)
        self._bytesLoaded = int(bytesLoaded)
        self._bytesTotal = int(bytesTotal)


class ScrollEvent(Event):
    SCROLL = String('scroll')

    @property
    def delta(self):
        return self._delta

    @property
    def direction(self):
        return self._direction

    @property
    def position(self):
        return self._position

    def __init__(self, direction: String, delta: Number, position: Number):
        super().__init__('scroll', false, false)
        self._direction = String(direction)
        self._delta = Number(delta)
        self._position = Number(position)

    def clone(self):
        return ScrollEvent(self.direction, self.delta, self.position)

    def toString(self):
        return self.formatToString('ScrollEvent', 'type', 'bubbles',
                                   'cancelable', 'direction', 'delta',
                                   'position')


class SliderEvent(Event):
    CHANGE = String('change')
    THUMB_DRAG = String('thumbDrag')
    THUMB_PRESS = String('thumbPress')
    THUMB_RELEASE = String('thumbRelease')

    @property
    def clickTarget(self):
        return self._clickTarget

    @property
    def keyCode(self):
        return self._keyCode

    @property
    def triggerEvent(self):
        return self._triggerEvent

    @property
    def value(self):
        return self._value

    def __init__(self, type: String, value: Number, clickTarget: String,
                 triggerEvent: String, keyCode: int = 0):
        super().__init__(type, false, false)
        self._value = Number(value)
        self._clickTarget = String(clickTarget)
        self._triggerEvent = String(triggerEvent)
        self._keyCode = int(keyCode)

    def clone(self):
        return SliderEvent(self.type, self.value, self.clickTarget,
                           self.triggerEvent, self.keyCode)

    def toString(self):
        return self.formatToString('SliderEvent', 'type', 'value', 'bubbles',
                                   'cancelable', 'keyCode', 'triggerEvent',
                                   'clickTarget')


class SliderEventClickTarget(Object):
    THUMB = String('thumb')
    TRACK = String('track')
