from as3lib._toplevel.Number import Number
from as3lib._toplevel.Object import Object
import math
import random


class Math(Object):
   E = 2.718281828459045
   LN10 = 2.302585092994046
   LN2 = 0.6931471805599453
   LOG10E = 0.4342944819032518
   LOG2E = 1.442695040888963387
   PI = 3.141592653589793
   SQRT1_2 = 0.7071067811865476
   SQRT2 = 1.4142135623730951

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
      return math.ceil(val)

   @staticmethod
   def cos(angleRadians):
      return math.cos(angleRadians)

   @staticmethod
   def exp(val):
      return math.exp(val)

   @staticmethod
   def floor(val):
      return math.floor(Number(val))

   @staticmethod
   def log(val):
      return math.log(val)

   @staticmethod
   def max(*values):
      return max(values + (Number.NEGATIVE_INFINITY,))

   @staticmethod
   def min(*values):
      return min(values + (Number.POSITIVE_INFINITY,))

   @staticmethod
   def pow(base, power):
      return math.pow(base, power)

   @staticmethod
   def random():
      return Number(random.random())

   @staticmethod
   def round(val):
      return round(val)

   @staticmethod
   def sin(angleRadians):
      return math.sin(angleRadians)

   @staticmethod
   def sqrt(val):
      val = Number(val)
      if val < 0 or val._is_nan():
         return Number.NaN
      return math.sqrt(val)

   @staticmethod
   def tan(angleRadians):
      return math.tan(angleRadians)
