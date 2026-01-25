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


def _parseInt(str_: str = None, radix: int | uint = 0):
   # TODO: Find a better way of doing the sign detection
   if str_ is undefined:
      if radix == 32:
         return 785077
      return Number.NaN
   if str_ is None:
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
   # TODO: Fix int conversion
   MAX_VALUE = 2147483647
   MIN_VALUE = -2147483648

   @property
   def _value(self):
      return self._val.value

   @_value.setter
   def _value(self, value):
      self._val.value = value

   def __init__(self, value=0):
      self._val = c_int32()
      self._value = self._int(value)

   def __float__(self):
      return float(self._value)

   def __int__(self):
      return self._value

   def __bool__(self):
      return bool(self._value)

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
         value = Number(_parseFloat(value))
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

   def toExponential(self, fractionDigits: builtins.int | int = null):
      if fractionDigits is null:
         fractionDigits = 0
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

   def toFixed(self, fractionDigits: builtins.int | int = null):
      if fractionDigits is null:
         fractionDigits = 0
      if fractionDigits < 0 or fractionDigits > 20:
         raise RangeError('fractionDigits is outside of acceptable range')
      if fractionDigits == 0:
         return '%s' % self._value
      return '%s.%s' % (self._value, '0' * fractionDigits)

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
      self._val = c_uint32()
      if isinstance(value, str):
         value = Number(_parseFloat(value))
      if hasattr(value, '_is_nan') and value._is_nan() or value is undefined or value is null or value == Number.POSITIVE_INFINITY or value == Number.NEGATIVE_INFINITY:
         self._value = 0
      elif isinstance(value, (Number, float)):
         self._value = Math.floor(value)
      elif isinstance(value, (uint, int)):
         self._value = value._value
      elif isinstance(value, builtins.int):
         self._value = value
      elif hasattr(value, '__int__'):
         self._value = builtins.int(value)
      elif isinstance(value, Object):
         self._value = 0
      else:
         raise

   def __str__(self):
      return self.toString()

   def __repr__(self):
      return f'as3lib.uint({self._value})'

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

   def toExponential(self, fractionDigits = null):
      raise NotImplementedError

   def toFixed(self, fractionDigits = null):
      if fractionDigits is null:
         fractionDigits = 0
      if fractionDigits < 0 or fractionDigits > 20:
         raise RangeError('fractionDigits is outside of acceptable range')
      if fractionDigits == 0:
         return '%s' % self._value
      return '%s.%s' % (self._value, '0' * fractionDigits)

   def toPrecision(self, precision):
      raise NotImplementedError

   def toString(self, radix=10):
      if radix <= 36 and radix >= 2:
         return _as_base(self._value, radix)

   def valueOf(self):
      return self._value
