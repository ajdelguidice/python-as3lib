from __future__ import annotations  # allow forward references
from as3lib import metaclasses
from as3lib.fl.core import UIComponent
from as3lib.fl.containers import BaseScrollPane
from as3lib.flash.events import EventDispatcher


class BaseButton(UIComponent):...


class Button(LabelButton):...


class ButtonLabelPlacement(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   BOTTOM = 'bottom'
   LEFT = 'left'
   RIGHT = 'right'
   TOP = 'top'


class CheckBox(LabelButton):...


class ColorPicker(UIComponent):...


class ComboBox(UIComponent):...


class DataGrid(SelectableList):...


class Label(UIComponent):...


class LabelButton(BaseButton):...


class List(SelectableList):...


class NumericStepper(UIComponent):...


class ProgressBar(UIComponent):...


class ProgressBarDirection(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   LEFT = 'left'
   RIGHT = 'right'


class ProgressBarMode(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   EVENT = 'event'
   MANUAL = 'manual'
   POLLED = 'polled'


class RadioButton(LabelButton):...


class RadioButtonGroup(EventDispatcher):...


class ScrollBar(UIComponent):...


class ScrollBarDirection(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   HORIZONTAL = 'horizontal'
   VERTICAL = 'vertical'


class ScrollPolicy(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   AUTO = 'auto'
   OFF = 'off'
   ON = 'on'


class SelectableList(BaseScrollPane):...


class Slider(UIComponent):...


class SliderDirection(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   HORIZONTAL = 'horizonal'
   VERTICAL = 'vertical'


class TextArea(UIComponent):...


class TextInput(UIComponent):...


class TileList(SelectableList):...


class UIScrollBar(ScrollBar):...
