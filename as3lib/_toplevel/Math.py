from as3lib._toplevel.Number import Number
from as3lib._toplevel.Object import Object
import math
import random


class Math(Object):
   E = Number(2.718281828459045)
   LN10 = Number(2.302585092994046)
   LN2 = Number(0.6931471805599453)
   LOG10E = Number(0.4342944819032518)
   LOG2E = Number(1.442695040888963387)
   PI = Number(3.141592653589793)
   SQRT1_2 = Number(0.7071067811865476)
   SQRT2 = Number(1.4142135623730951)

   @staticmethod
   def abs(val):
      val = Number(val)
      return abs(val)

   @staticmethod
   def acos(val):
      return math.acos(val)

   @staticmethod
   def asin(val):
      return math.asin(val)

   @staticmethod
   def atan(val):
      val = Number(val)
      return Number(math.atan(val))

   @staticmethod
   def atan2(y, x):
      x, y = Number(x), Number(y)
      return Number(math.atan2(y, x))

   @staticmethod
   def ceil(val):
      val = Number(val)
      if val == Number.POSITIVE_INFINITY or val == Number.NEGATIVE_INFINITY or val._is_nan():
         return val
      return math.ceil(val)

   @staticmethod
   def cos(angleRadians):
      a = Number(angleRadians)
      if a == Number.POSITIVE_INFINITY or a == Number.NEGATIVE_INFINITY or a._is_nan():
         return Number.NaN
      return Number(math.cos(a))

   @staticmethod
   def exp(val):
      return math.exp(val)

   @staticmethod
   def floor(val):
      val = Number(val)
      if val == Number.POSITIVE_INFINITY or val == Number.NEGATIVE_INFINITY or val._is_nan():
         return val
      return math.floor(val)

   @staticmethod
   def log(val):
      return math.log(val)

   @staticmethod
   def max(*values):
      v = [Number.NEGATIVE_INFINITY]
      for i in values:
         n = Number(i)
         if n._is_nan():
            return Number.NaN
         v.append(n)
      return max(v)

   @staticmethod
   def min(*values):
      v = [Number.POSITIVE_INFINITY]
      for i in values:
         n = Number(i)
         if n._is_nan():
            return Number.NaN
         v.append(n)
      return min(v)

   @staticmethod
   def pow(base, power):
      return math.pow(base, power)

   @staticmethod
   def random():
      return Number(random.random())

   @staticmethod
   def round(val):
      val = Number(val)
      if val == Number.POSITIVE_INFINITY or val == Number.NEGATIVE_INFINITY or val._is_nan():
         return val
      return round(val)

   @staticmethod
   def sin(angleRadians):
      a = Number(angleRadians)
      if a == Number.POSITIVE_INFINITY or a == Number.NEGATIVE_INFINITY or a._is_nan():
         return Number.NaN
      return Number(math.sin(a))

   @staticmethod
   def sqrt(val):
      val = Number(val)
      if val < 0 or val._is_nan():
         return Number.NaN
      return math.sqrt(val)

   @staticmethod
   def tan(angleRadians):
      a = Number(angleRadians)
      if a == Number.POSITIVE_INFINITY or a == Number.NEGATIVE_INFINITY or a._is_nan():
         return Number.NaN
      return math.tan(a)
