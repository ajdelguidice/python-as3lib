from __future__ import annotations
from as3lib._toplevel.Constants import undefined, null
from as3lib._toplevel.Errors import Error, RangeError, TypeError
from as3lib._toplevel.Math import Math
from as3lib._toplevel.Number import Number, _parseFloat
from as3lib._toplevel.Object import Object
import builtins
from ctypes import c_uint32, c_int32


_base_digits = '0123456789abcdefghijklmnopqrstuvwxyz'
def _as_base(num, radix):
   if num == 0:
      return '0'
   l = []
   temp = abs(num)
   while temp > 0:
      l.append(_base_digits[temp % radix])
      temp //= radix
   if num < 0:
      l.append('-')
   l.reverse()
   return ''.join(l)


def _exponentFix(value):
   if value.find('e') != -1:
      a, b = value.split('e')
      bi = int(b)
      if bi == 0:
         return a
      if b.startswith('+'):
         return '%se+%i' % (a, bi)
      return '%se%i' % (a, bi)
   return value


class int(Object):
   # TODO: Make this return a Number if the result is a float
   MAX_VALUE = 2147483647
   MIN_VALUE = -2147483648

   @property
   def _value(self):
      return self._val.value

   @_value.setter
   def _value(self, value):
      self._val.value = value

   def __init__(self, value=0):
      self._val = c_int32(self._int(value))

   def __float__(self):
      return float(self._value)

   def __int__(self):
      return self._value

   def __bool__(self):
      return bool(self._value)

   def __repr__(self):
      return 'as3lib.int(%s)' % self._value

   def __add__(self, value):
      return int(self._value + self._int(value))

   def __sub__(self, value):
      return int(self._value - self._int(value))

   def __mul__(self, value):
      return int(self._value * self._int(value))

   def __truediv__(self, value):
      value = self._int(value)
      if value == 0:
         if self._value > 0:
            return Number.POSITIVE_INFINITY
         if self._value < 0:
            return Number.NEGATIVE_INFINITY
         return Number.NaN
      return int(self._value / value)

   def __eq__(self, value):
      return self._value == value

   def __lt__(self, value):
      return self._value < value

   def __gt__(self, value):
      return self._value > value

   def __lshift__(self, value):
      return int(self._value << self._int(value))

   def __rshift__(self, value):
      return int(self._value >> self._int(value))

   def __xor__(self, value):
      return int(self._value ^ self._int(value))

   def __mod__(self, value):
      return int(self._value % self._int(value))

   def _int(self, value):
      if isinstance(value, str):
         value = _parseFloat(value)
      if hasattr(value, '_is_nan') and value._is_nan() or value == Number.POSITIVE_INFINITY or value == Number.NEGATIVE_INFINITY:
         return 0
      if isinstance(value, (int, uint, Number)):
         value = value._value
      if isinstance(value, (builtins.int)):
         return value
      if isinstance(value, float):
         return Math.floor(value)
      if hasattr(value, '__int__'):
         return builtins.int(value)
      if isinstance(value, Object):
         return 0
      raise TypeError(f'Can not convert type {type(value)} to integer')

   def toExponential(self, fractionDigits: uint = null):
      fractionDigits = uint(fractionDigits)
      if fractionDigits > 20:
         raise RangeError('fractionDigits is outside of acceptable range')
      if self == 0:
         if fractionDigits == 0:
            return '1e-15'
         return _exponentFix(('{:.%se}' % fractionDigits).format(self._value)) + 'e-16'
      return _exponentFix(('{:.%se}' % fractionDigits).format(self._value))

   def toFixed(self, fractionDigits: uint = null):
      fractionDigits = uint(fractionDigits)
      if fractionDigits > 20:
         raise RangeError('fractionDigits is outside of acceptable range')
      return ('{:.%sf}' % fractionDigits).format(self._value)

   def toPrecision(self, precision: builtins.int | int | uint):
      if precision < 1 or precision > 21:
         raise RangeError('fractionDigits is outside of acceptable range')
      temp = str(self._value)
      length = len(temp)
      if precision < length:
         return self.toExponential(precision-1)
      if precision == length:
         return temp
      return '%s.%s' % (temp, '0' * (precision - length))

   def toString(self, radix: builtins.int | int | uint = 10):
      if radix <= 36 and radix >= 2:
         return _as_base(self._value, radix)

   def valueOf(self):
      return self._value


class uint(Object):
   MAX_VALUE = 4294967295
   MIN_VALUE = 0

   @property
   def _value(self):
      return self._val.value

   @_value.setter
   def _value(self, value):
      self._val.value = value

   def __init__(self, value=undefined):
      self._val = c_uint32(self._uint(value))

   def __str__(self):
      return self.toString()

   def __repr__(self):
      return 'as3lib.uint(%s)' % self._value

   def __eq__(self, value):
      return self._value == value

   def __lt__(self, value):
      return self._value < value

   def __gt__(self, value):
      return self._value > value

   def __truediv__(self, value):
      value = self._uint(value)
      if value == 0:
         if self._value > 0:
            return Number.POSITIVE_INFINITY
         return Number.NaN
      return uint(self._value / value)

   _uint = int._int
   toExponential = int.toExponential
   toFixed = int.toFixed
   toPrecision = int.toPrecision
   toString = int.toString
   valueOf = int.valueOf
