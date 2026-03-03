from as3lib._toplevel import int, uint, Number
import builtins


def isEven(num: builtins.int | float | int | Number | uint):
   num = Number(num)
   if not isFinite(num):
      return False
   if num.valueOf().is_integer():
      return num % 2 == 0
   ...


def isOdd(num: builtins.int | float | int | Number | uint):
   num = Number(num)
   if not isFinite(num):
      return False
   if num.valueOf().is_integer():
      return num % 2 != 0
   ...


def objIsChildClass(obj, cls):
   '''
   Checks both isinstance and issubclass for (obj,cls)
   '''
   return isinstance(obj, cls) or issubclass(obj, cls)
