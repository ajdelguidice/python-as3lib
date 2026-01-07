from __future__ import annotations
from as3lib._toplevel.Constants import undefined, null
from as3lib._toplevel.Errors import RangeError, TypeError
from as3lib._toplevel.Math import Math
from as3lib._toplevel.Number import Number
from as3lib._toplevel.Object import Object
import builtins
from numpy import base_repr


def _parseInt(str_: str = None, radix: int | uint = 0):
   # TODO: Find a better way of doing the sign detection
   if str_ is None or str_ is undefined:
      return Number.NaN
   str_ = str_.lstrip()
   zero = False
   minus = 0
   j1 = 0
   while j1 < len(str_) and str_[j1] in '-+':
      if str_[j1] == '-':
         minus += 1
      j1 += 1
   str_ = str_[j1:]
   if len(str_) >= 2 and str_.startswith('0x'):
      radix = 16
      str_ = str_[2:]
   elif radix < 2 or radix > 36:
      raise Error(f'parseInt; radix {radix} is outside of the acceptable range')
   if str_.startswith('0'):
      zero = True
      str_.lstrip("0")
   radixchars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:radix]
   str_ = str_.upper()
   j = 0
   while j < len(str_) and str_[j] in radixchars:
      j += 1
   if j == 0:
      return 0 if zero else Number.NaN
   return builtins.int(str_[:j], radix) * (-1 if minus % 2 else 1)


class int(Object):
   # TODO: Make this return a Number if the result is a float
   # TODO: Implement checks for max and min value
   # TODO: Fix int conversion
   __slots__ = ('_value')
   MAX_VALUE = 2147483647
   MIN_VALUE = -2147483648

   def __init__(self, value=0):
      self._value = self._int(value)

   def __repr__(self):
      return f'as3lib.int({self._value})'

   def __getitem__(self):
      return self._value

   def __setitem__(self, value):
      self._value = self._int(value)

   def __add__(self, value):
      return int(self._value + self._int(value))

   def __sub__(self, value):
      return int(self._value - self._int(value))

   def __mul__(self, value):
      return int(self._value * self._int(value))

   def __truediv__(self, value):
      value = self._int(value)
      if value == 0:
         if self._value == 0:
            return Number.NaN
         if self._value > 0:
            return Number.POSITIVE_INFINITY
         if self._value < 0:
            return Number.NEGATIVE_INFINITY
      try:
         return int(self._value / value)
      except Exception:
         raise TypeError(f'Can not divide int by {type(value)}')

   def __float__(self):
      return float(self._value)

   def __int__(self):
      return self._value

   def __bool__(self):
      return bool(self._value)

   def __eq__(self, value):
      return self._value == value

   def __lt__(self, value):
      return self._value < value

   def __gt__(self, value):
      return self._value > value

   @staticmethod
   def _upperBounds(value):
      v = int.MIN_VALUE + value
      if value > int.MAX_VALUE:
         v = int._upperBounds(v)
      return v

   @staticmethod
   def _lowerBounds(value):
      v = int.MAX_VALUE + value
      if value < int.MIN_VALUE:
         v = int._lowerBounds(v)
      return v

   @staticmethod
   def _boundsCheck(value):
      if value < int.MIN_VALUE:
         return int._lowerBounds(value)
      if value > int.MAX_VALUE:
         return int._upperBounds(value)
      return value

   def _int(self, value):
      # !It is unclear if most of this is included here, most is from the Number class
      if isinstance(value, str):
         value = _parseInt(value, 10)
      if value is Number.NaN or value == Number.POSITIVE_INFINITY or value == Number.NEGATIVE_INFINITY:
         return 0
      if isinstance(value, (builtins.int, int)):
         return self._boundsCheck(value)
      if isinstance(value, (float, Number)):
         return self._boundsCheck(Math.floor(value))
      if hasattr(value, '__int__'):
         return value.__int__()
      raise TypeError(f'Can not convert type {type(value)} to integer')

   def toExponential(self, fractionDigits: builtins.int | int):
      if fractionDigits < 0 and fractionDigits > 20:
         raise RangeError('fractionDigits is outside of acceptable range')
      temp = str(self._value)
      if temp[0] == '-':
         whole = temp[:2]
         temp = temp[2:]
      else:
         whole = temp[:1]
         temp = temp[1:]
      decpos = temp.find('.')
      if decpos == -1:
         exponent = len(temp)
      else:
         exponent = len(temp[:decpos])
      temp = temp.replace('.', '') + '0'*20
      if fractionDigits > 0:
         return f'{whole}.{"".join([temp[i] for i in range(fractionDigits)])}e+{exponent}'
      return f'{whole}e+{exponent}'

   def toFixed(self, fractionDigits: builtins.int | int):
      if fractionDigits < 0 or fractionDigits > 20:
         raise RangeError('fractionDigits is outside of acceptable range')
      if fractionDigits == 0:
         return f'{self._value}'
      return f'{self._value}.{"0"*fractionDigits}'

   def toPrecision(self, precision: builtins.int | int | uint):
      if precision < 1 or precision > 21:
         raise RangeError('fractionDigits is outside of acceptable range')
      temp = str(self._value)
      length = len(temp)
      if precision < length:
         return self.toExponential(precision-1)
      if precision == length:
         return temp
      return f'{temp}.{"0"*(precision-length)}'

   def toString(self, radix: builtins.int | int | uint = 10):
      if radix <= 36 and radix >= 2:
         return base_repr(self._value, base=radix)

   def valueOf(self):
      return self._value


class uint(Object):
   MAX_VALUE = 4294967295
   MIN_VALUE = 0

   @staticmethod
   def _upperBounds(value):
      return value % uint.MAX_VALUE - 1

   @staticmethod
   def _lowerBounds(value):
      v = uint.MAX_VALUE + value + 1
      if v < uint.MIN_VALUE:
         v = uint._lowerBounds(v)
      return v

   @staticmethod
   def _boundsCheck(value):
      if value < uint.MIN_VALUE:
         return uint._lowerBounds(value)
      if value > uint.MAX_VALUE:
         return uint._upperBounds(value)
      return value

   def __init__(self, value=undefined):
      if isinstance(value, str):
         value = _parseInt(value, 10)
      if value is undefined or value is null or value is Number.NaN or value == Number.POSITIVE_INFINITY or value == Number.NEGATIVE_INFINITY:
         self._value = 0
      elif isinstance(value, (Number, float)):
         self._value = uint._boundsCheck(Math.floor(value))
      elif isinstance(value, (builtins.int, uint, int)):
         self._value = uint._boundsCheck(value)
      elif hasattr(value, '__int__'):
         self._value = uint._boundsCheck(builtins.int(value))
      else:
         raise

   def __str__(self):
      return self.toString()

   def __eq__(self, value):
      return self._value == value

   def __lt__(self, value):
      return self._value < value

   def __gt__(self, value):
      return self._value > value

   def __truediv__(self, value):
      if value == 0:
         if self._value == 0:
            return Number.NaN
         if self._value > 0:
            return Number.POSITIVE_INFINITY
         raise  # Should not happen
      try:
         return uint(self._value / builtins.int(value))
      except Exception:
         raise TypeError(f'Can not divide uint by {type(value)}')

   def toExponential(self, fracionDigits):
      raise NotImplementedError

   def toFixed(self, fracionDigits):
      raise NotImplementedError

   def toPrecision(self, precision):
      raise NotImplementedError

   def toString(self, radix=10):
      if radix <= 36 and radix >= 2:
         return base_repr(self._value, base=radix).lower()

   def valueOf(self):
      return self._value
