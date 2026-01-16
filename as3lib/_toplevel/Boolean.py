from as3lib._toplevel.Constants import undefined, null
from as3lib._toplevel.int import int, uint
from as3lib._toplevel.Number import Number
from as3lib._toplevel.Object import Object
import builtins


class Boolean(Object):
   __slots__ = ('_value')

   def __init__(self, expression=False):
      self._value = self._Boolean(expression)

   def __repr__(self):
      return f'as3lib.Boolean({self._value})'

   def __getitem__(self):
      return self._value

   def __setitem__(self, value):
      self._value = value

   def __bool__(self):
      return self._value

   def __float__(self):
      return float(self._value)

   def __int__(self):
      return builtins.int(self._value)

   def __eq__(self, value):
      return self._value == value

   def __abs__(self):
      return Number(self._value)

   def _Boolean(self, expression=None):
      if isinstance(expression, bool):
         return expression
      if expression is null or expression is undefined or expression is None:
         return False
      # NOTE: For some reason, python str does not have __bool__ but can be
      #       converted to one anyways
      if hasattr(expression, '__bool__') or isinstance(expression, str):
         return bool(expression)
      return False

   def toString(self):
      return str(self._value).lower()

   def valueOf(self):
      return self._value
