from as3lib._toplevel.Constants import null, undefined
from as3lib._toplevel.Errors import RangeError, TypeError
from as3lib._toplevel.Object import Object
import builtins
from ctypes import c_double
import math


_NaN_value = 1e300000 / -1e300000
_NegInf_value = -1e300000
_PosInf_value = 1e300000


def _parseFloat(str_):
   # TODO: Make stop at second period
   # TODO: '100a' should return NaN
   if str_ is undefined:
      return Number.NaN
   str_ = str_.lstrip()
   if str_ == '':
      return Number(0)
   if str_ == 'Infinity':
      return Number.POSITIVE_INFINITY
   if str_ == '-Infinity':
      return Number.NEGATIVE_INFINITY
   size = len(str_)
   if size == 0:
      return Number.NaN
   if str_[0].isdigit() or str_[0] in '-+.':
      j = 0
      while str_[j] in '-+':
         j += 1
      if size > j + 1 and str_[j] == '0' and str_[j + 1] == 'x':
         j += 2
         if size == j:
            return Number.NaN
         while j != size and str_[j] in '0123456789abcdefABCDEF':
            j += 1
         return Number(int(str_[:j], 16))
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
      return Number(float(str_[:j]))
   return Number.NaN


def _exponentFix(value):
   if value.find('e') != -1:
      a, b = value.split('e')
      return ('%se{:+d}' % a).format(int(b))
   return value


class Number(Object):
   __slots__ = '_val'
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
      self._val = c_double(self._Number(num))

   def __str__(self):
      return self.toString()

   def __repr__(self):
      return 'as3lib.Number(%s)' % self

   def __hash__(self):
      return hash(self._value)

   def __add__(self, value):
      return Number(self._value + self._Number(value))

   def __sub__(self, value):
      return Number(self._value - self._Number(value))

   def __mul__(self, value):
      return Number(self._value * self._Number(value))

   def __truediv__(self, value):
      value = self._Number(value)
      if value == 0:
         if self._value > 0:
            return Number.POSITIVE_INFINITY
         if self._value < 0:
            return Number.NEGATIVE_INFINITY
         return Number.NaN
      return Number(self._value / value)

   def __float__(self):
      return self._value

   def __int__(self):
      return builtins.int(self._value)

   def __index__(self):
      return math.floor(self._value)

   def __eq__(self, value):
      return self._value == value

   def __lt__(self, value):
      return self._value < value

   def __gt__(self, value):
      return self._value > value

   def __neg__(self):
      return Number(-self._value)

   def __bool__(self):
      return self._value != 0 and not self._is_nan()

   def __abs__(self):
      return Number(abs(self._value))

   def __pow__(self, value):
      return self._value ** value

   def __round__(self, places=null):
      if places is null:
         if self._value % 1 >= 0.5:
            return Number(math.ceil(self._value))
         return Number(math.floor(self._value))
      return Number(round(self._value, places))

   def _Number(self, expression):
      if hasattr(expression, '_is_nan') and expression._is_nan() or expression is _NaN_value:
         return _NaN_value
      if isinstance(expression, Object) and hasattr(expression, 'valueOf'):
         expression = expression.valueOf()
      if expression == _NegInf_value or expression == _PosInf_value or isinstance(expression, float):
         return expression
      if expression is undefined or expression is None:
         return Number.NaN
      if expression is null:
         return 0.0
      if hasattr(expression, '__float__'):
         return float(expression)
      if isinstance(expression, str):
         return _parseFloat(expression)
      if isinstance(expression, Object):
         return Number.NaN

   def toExponential(self, fractionDigits=null):
      # TODO: Cast fractionDigits to uint
      if fractionDigits is null:
         fractionDigits = 0
      if self._value == 0:
         if fractionDigits == 0:
            return '1e-15'
         return ('{:.%if}e-16' % fractionDigits).format(0)
      if self._is_nan() or self == Number.NEGATIVE_INFINITY or self == Number.POSITIVE_INFINITY:
         return self.toString()
      return _exponentFix(('{:.%ie}' % fractionDigits).format(self._value))

   def toFixed(self, fractionDigits=null):
      # TODO: Cast fractionDigits to uint
      if fractionDigits is null:
         fractionDigits = 0
      return ('{:.%if}' % fractionDigits).format(self._value)

   def toPrecision(self, precision):
      # TODO: Cast precision to uint
      raise NotImplementedError

   def toLocaleString(self):
      return self.toString()

   def toString(self, radix=10):
      # TODO: Radix
      if self._is_nan():
         return 'NaN'
      if self._value == Number.NEGATIVE_INFINITY:
         return "-Infinity"
      if self._value == Number.POSITIVE_INFINITY:
         return "Infinity"
      if radix != 10:
         return str(math.floor(self._value))
      if self._value.is_integer():
         return _exponentFix('%i' % self._value)
      return _exponentFix('%s' % self._value)

   def valueOf(self):
      return self._value

Infinity = Number.POSITIVE_INFINITY = Number(_PosInf_value)
NaN = Number.NaN = Number(_NaN_value)
Number.NEGATIVE_INFINITY = Number(_NegInf_value)
