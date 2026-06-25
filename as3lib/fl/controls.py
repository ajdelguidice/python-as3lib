from __future__ import annotations  # allow forward references
from as3lib import (Array, Boolean, false, int, null, Object, String, true,
                    uint)
from as3lib.fl.core import UIComponent
from as3lib.fl.containers import BaseScrollPane
from as3lib.fl.events import ComponentEvent
from as3lib.flash.events import EventDispatcher
from as3lib.flash.text import TextField


class ButtonLabelPlacement(Object):
    BOTTOM = 'bottom'
    LEFT = 'left'
    RIGHT = 'right'
    TOP = 'top'


class BaseButton(UIComponent):
    @property
    def autoRepeat(self):
        raise NotImplementedError

    @autoRepeat.setter
    def autoRepeat(self, value: Boolean):
        raise NotImplementedError

    @property
    def enabled(self):
        raise NotImplementedError

    @enabled.setter
    def enabled(self, value: Boolean):
        raise NotImplementedError

    @property
    def selected(self):
        raise NotImplementedError

    @selected.setter
    def selected(self, value: Boolean):
        raise NotImplementedError

    def __init__(self):
        super().__init__()

    @staticmethod
    def getStyleDefinition():
        raise NotImplementedError

    def setMouseState(self, state: String):
        raise NotImplementedError


class SelectableList(BaseScrollPane):
    ...


class LabelButton(BaseButton):
    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value: String):
        self._label = String(value)
        self.dispatchEvent(ComponentEvent('labelChange'))

    @property
    def labelPlacement(self):
        return self._labelPlacement

    @labelPlacement.setter
    def labelPlacement(self, value: String):
        if value not in {ButtonLabelPlacement.RIGHT, ButtonLabelPlacement.LEFT,
                         ButtonLabelPlacement.BOTTOM, ButtonLabelPlacement.TOP}:
            raise
        self._labelPlacement = String(value)

    @property
    def selected(self):
        raise NotImplementedError

    @selected.setter
    def selected(self, value: Boolean):
        raise NotImplementedError

    @property
    def textField(self):
        raise NotImplementedError

    @textField.setter
    def textField(self, value: TextField):
        raise NotImplementedError

    @property
    def toggle(self):
        raise NotImplementedError

    @toggle.setter
    def toggle(self, value: Boolean):
        raise NotImplementedError

    def __init__(self):
        super().__init__()
        self._label = String('Label')
        self._labelPlacement = ButtonLabelPlacement.RIGHT

    @staticmethod
    def getStyleDefinition():
        raise NotImplementedError


class Button(LabelButton):
    ...


class CheckBox(LabelButton):
    ...


class ColorPicker(UIComponent):
    ...


class ComboBox(UIComponent):
    ...


class DataGrid(SelectableList):
    ...


class Label(UIComponent):
    ...


class List(SelectableList):
    ...


class NumericStepper(UIComponent):
    ...


class ProgressBar(UIComponent):
    ...


class ProgressBarDirection(Object):
    LEFT = 'left'
    RIGHT = 'right'


class ProgressBarMode(Object):
    EVENT = 'event'
    MANUAL = 'manual'
    POLLED = 'polled'


class RadioButton(LabelButton):
    @property
    def autoRepeat(self):
        return false

    @autoRepeat.setter
    def autoRepeat(self, value: Boolean):
        # NOTE: This property should not change in a RadioButton
        raise NotImplementedError

    @property
    def group(self):
        raise NotImplementedError

    @group.setter
    def group(self, value: RadioButtonGroup):
        raise NotImplementedError

    @property
    def groupName(self):
        raise NotImplementedError

    @groupName.setter
    def groupName(self, value: String):
        raise NotImplementedError

    @property
    def selected(self):
        raise NotImplementedError

    @selected.setter
    def selected(self, value: Boolean):
        raise NotImplementedError

    @property
    def toggle(self):
        return true

    @toggle.setter
    def toggle(self, value: Boolean):
        # NOTE: This property should not change in a RadioButton
        raise NotImplementedError

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: Object):
        self._value = value

    def __init__(self):
        super().__init__()
        self._value = null

    def drawFocus(self, focused: Boolean):
        raise NotImplementedError

    @staticmethod
    def getStyleDefinition():
        raise NotImplementedError


class RadioButtonGroup(EventDispatcher):
    # TODO: Events
    @property
    def name(self):
        return self._name

    @property
    def numRadioButtons(self):
        return self._radioButtons.length

    @property
    def selectedData(self):
        raise NotImplementedError

    @selectedData.setter
    def selectedData(self, value: Object):
        raise NotImplementedError

    @property
    def selection(self):
        raise NotImplementedError

    @selection.setter
    def selection(self, value: RadioButton):
        if not isinstance(value, RadioButton):
            raise TypeError
        raise NotImplementedError

    def __init__(self, name: String = null):
        super().__init__()
        if name is null:
            self._name = String('RadioButtonGroup')
        else:
            self._name = String(name)
        self._radioButtons = Array()

    def addRadioButton(self, radioButton: RadioButton):
        self._radioButtons.push(radioButton)
        radioButton.group = self

    @staticmethod
    def getGroup(name: String):
        raise NotImplementedError

    def getRadioButtonAt(self, index: int):
        raise NotImplementedError

    def getRadioButtonIndex(self, radioButton: RadioButton):
        raise NotImplementedError

    def removeRadioButton(self, radioButton: RadioButton):
        raise NotImplementedError


class ScrollBar(UIComponent):
    ...


class ScrollBarDirection(Object):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'


class ScrollPolicy(Object):
    AUTO = 'auto'
    OFF = 'off'
    ON = 'on'


class Slider(UIComponent):
    ...


class SliderDirection(Object):
    HORIZONTAL = 'horizonal'
    VERTICAL = 'vertical'


class TextArea(UIComponent):
    ...


class TextInput(UIComponent):
    ...


class TileList(SelectableList):
    ...


class UIScrollBar(ScrollBar):
    ...


class listClasses:
    class CellRenderer(LabelButton):
        ...

    class ImageCell(CellRenderer):
        ...

    class ListData(Object):
        @property
        def column(self):
            return self._col

        @property
        def icon(self):
            return self._icon

        @property
        def index(self):
            return self._index

        @property
        def label(self):
            return self._label

        @property
        def owner(self):
            return self._owner

        @property
        def row(self):
            return self._row

        def __init__(self, label: String, icon: Object, owner: UIComponent,
                     index: uint, row: uint, col: uint = 0):
            self._label = String(label)
            self._icon = icon
            self._owner = owner
            self._index = uint(index)
            self._row = uint(row)
            self._col = uint(col)

    class TileListData(ListData):
        @property
        def source(self):
            return self._source

        def __init__(self, label: String, icon: Object, source: Object,
                     owner: UIComponent, index: uint, row: uint,
                     col: uint = 0):
            super().__init__(label, icon, owner, index, row, col)
            self._source = source
