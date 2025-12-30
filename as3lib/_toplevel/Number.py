import builtins
from as3lib._toplevel.Object import Object
from as3lib._toplevel.Constants import null, undefined
from as3lib._toplevel.Errors import TypeError


_NaN_value = 1e300000 / -1e300000
_NegInf_value = -1e300000
_PosInf_value = 1e300000

class Number(Object):
   __slots__ = ('_value')
   MAX_VALUE = 1.79e308
   MIN_VALUE = 5e-324

   def __init__(self, num=None):
      self._value = self._Number(num)

   def __str__(self):
      return self.toString()

   def __repr__(self):
      return f'as3lib.Number({self._value})'

   def __getitem__(self):
      return self._value

   def __setitem__(self, value):
      self._value = self._Number(value)

   def __add__(self, value):
      try:
         return Number(self._value + float(value))
      except Exception:
         raise TypeError(f'can not add {type(value)} to Number')

   def __sub__(self, value):
      try:
         return Number(self._value - float(value))
      except Exception:
         raise TypeError(f'can not subtract {type(value)} from Number')

   def __mul__(self, value):
      try:
         return Number(self._value * float(value))
      except Exception:
         raise TypeError(f'can not multiply Number by {type(value)}')

   def __truediv__(self, value):
      if value == 0:
         if self._value == 0:
            return Number.NaN
         if self._value > 0:
            return Number.POSITIVE_INFINITY
         if self._value < 0:
            return Number.NEGATIVE_INFINITY
      try:
         return Number(self._value / float(value))
      except Exception:
         raise TypeError(f'Can not divide Number by {type(value)}')

   def __float__(self):
      return float(self._value)

   def __int__(self):
      return builtins.int(self._value)

   def __bool__(self):
      bool(self._value)

   def __eq__(self, value):
      return self._value == value

   def __invert__(self):
      return Number(-self._value)

   def _Number(self, expression):
      if expression == _NegInf_value or expression == _PosInf_value or isinstance(expression, (float, Number)):
         return expression
      if expression is _NaN_value or expression is undefined or expression is None:
         return Number.NaN
      if expression is null:
         return 0.0
      if hasattr(expression, '__float__'):
         return float(expression)
      if isinstance(expression, str):
         if expression == "":
            return 0.0
         try:
            return float(expression)
         except Exception:
            return Number.NaN

   def toExponential(self):...
   def toFixed(self):...
   def toPrecision():...

   def toString(self, radix=10):
      # TODO: Radix
      if self._value is Number.NaN:
         return 'NaN'
      if self._value is Number.NEGATIVE_INFINITY:
         return "-Infinity"
      if self._value is Number.POSITIVE_INFINITY:
         return "Infinity"
      if self._value.is_integer():
         return f'{int(self._value)}'
      return f'{self._value}'

   def valueOf(self):
      return self._value

Number.NaN = Number(_NaN_value)
Number.NEGATIVE_INFINITY = Number(_NegInf_value)
Number.POSITIVE_INFINITY = Number(_PosInf_value)
