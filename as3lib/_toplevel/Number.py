import builtins
from as3lib._toplevel.Object import Object
from as3lib._toplevel.Constants import null, undefined
from as3lib._toplevel.Errors import TypeError
from ctypes import c_double


_NaN_value = 1e300000 / -1e300000
_NegInf_value = -1e300000
_PosInf_value = 1e300000


def _parseFloat(str_):
   # TODO: Make stop at second period
   if str_ is None:
      return _NaN_value
   str_ = str_.lstrip()
   if str_ == '':
      return 0
   if str_ == 'Infinity':
      return _PosInf_value
   if str_ == '-Infinity':
      return _NegInf_value
   size = len(str_)
   if size == 0:
      return _NaN_value
   if str_[0].isdigit() or str_[0] in '-+.':
      j = 0
      while str_[j] in '-+':
         j += 1
      if size > j + 1 and str_[j] == '0' and str_[j + 1] == 'x':
         j += 2
         if size == j:
            return _NaN_value
         while j != size and str_[j] in '0123456789abcdefABCDEF':
            j += 1
         return int(str_[:j], 16)
      while j != size and (str_[j].isdigit() or str_[j] == '.'):
         j += 1
      if j != size and str_[j] == 'e':
         if str_[j + 1] in '-+' and str_[j + 2].isdigit():
            j += 2
            while j != size and str_[j].isdigit():
               j += 1
         elif str_[j + 1].isdigit():
            j += 1
            while j != size and str_[j].isdigit():
               j += 1
      return float(str_[:j])
   return _NaN_value


class Number(Object):
   MAX_VALUE = 1.79e308
   MIN_VALUE = 5e-324

   @property
   def _value(self):
      return self._val.value

   @_value.setter
   def _value(self, value):
      self._val.value = value

   def _is_nan(self):
      return self._value.hex() == 'nan'

   def __init__(self, num=null):
      self._val = c_double()
      self._value = self._Number(num)

   def __str__(self):
      return self.toString()

   def __repr__(self):
      return 'as3lib.Number(%s)' % self

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

   def __eq__(self, value):
      return self._value == value

   def __lt__(self, value):
      return self._value < value

   def __gt__(self, value):
      return self._value > value

   def __neg__(self):
      if self._is_nan():
         return Number.NaN
      if self._value == _NegInf_value:
         return Number.POSITIVE_INFINITY
      if self._value == _PosInf_value:
         return Number.NEGATIVE_INFINITY
      return Number(-self._value)

   def __bool__(self):
      if self._is_nan():
         return False
      return self._value != 0

   def __abs__(self):
      if self._is_nan():
         return Number.NaN
      if self._value in {_NegInf_value, _PosInf_value}:
         return Number.POSITIVE_INFINITY
      return Number(self._value)

   def _Number(self, expression):
      if hasattr(expression, '_is_nan') and expression._is_nan():
         return _NaN_value
      if isinstance(expression, Object) and hasattr(expression, 'valueOf'):
         expression = expression.valueOf()
      if expression == _NegInf_value or expression == _PosInf_value or isinstance(expression, float):
         return expression
      if expression is _NaN_value or expression is undefined or expression is None:
         return _NaN_value
      if expression is null:
         return 0.0
      if hasattr(expression, '__float__'):
         return float(expression)
      if isinstance(expression, str):
         return _parseFloat(expression)
      if isinstance(expression, Object):
         return _NaN_value

   def toExponential(self):
      raise NotImplementedError

   def toFixed(self):
      raise NotImplementedError

   def toPrecision(self):
      raise NotImplementedError

   def toLocaleString(self):
      return self.toString()

   def toString(self, radix=10):
      # TODO: Radix
      if self._is_nan():
         return 'NaN'
      if self._value == _NegInf_value:
         return "-Infinity"
      if self._value == _PosInf_value:
         return "Infinity"
      if radix != 10:
         raise NotImplementedError
      if self._value.is_integer():
         return f'{int(self._value)}'
      return f'{self._value}'

   def valueOf(self):
      return self._value

Number.NaN = Number(_NaN_value)
Number.NEGATIVE_INFINITY = Number(_NegInf_value)
Number.POSITIVE_INFINITY = Number(_PosInf_value)
