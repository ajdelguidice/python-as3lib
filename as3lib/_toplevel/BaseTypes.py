from __future__ import annotations
from as3lib._toplevel.Boolean import Boolean
from as3lib._toplevel.Errors import RangeError, Error, TypeError
from as3lib._toplevel.Math import Math
from as3lib._toplevel.Number import Number
from as3lib._toplevel.Object import Object
from as3lib._toplevel.trace import trace
from as3lib.helpers import textObject, recursionDepth
import builtins
from functools import cmp_to_key, partial
from inspect import isfunction
from io import StringIO
from multipledispatch import dispatch
from numpy import base_repr
from types import NoneType


from as3lib._toplevel.Functions import parseInt, parseFloat


# Constants
_NaN_value = 1e300000 / -1e300000
_NegInf_value = -1e300000
_PosInf_value = 1e300000


# Singleton Objects
class _undefined:
   __slots__ = ("value")

   def __init__(self):
      self.value = None

   def __int__(self):
      return 0

   def __str__(self):
      return self.toString()

   def __repr__(self):
      return self.toString()

   def toString(self):
      return 'undefined'


class _null:
   __slots__ = ("value")

   def __init__(self):
      self.value = None

   def __int__(self):
      return 0

   def __str__(self):
      return self.toString()

   def __repr__(self):
      return self.toString()

   def __bool__(self):
      return False

   def toString(self):
      return 'null'


undefined = _undefined()
null = _null()


# Data types
class Array(list, Object):
   # TODO: Arrays are sparse arrays, meaning there might be an element at index 0 and another at index 5, but nothing in the index positions between those two elements. In such a case, the elements in positions 1 through 4 are undefined, which indicates the absence of an element, not necessarily the presence of an element with the value undefined.
   # NOTE: Actionscript arrays seem to function like a python dictionary which can only uses ints as keys
   __slots__ = ('filler')
   CASEINSENSITIVE = 1
   DESCENDING = 2
   UNIQUESORT = 4
   RETURNINDEXEDARRAY = 8
   NUMERIC = 16

   def __init__(self, *args):
      if len(args) == 1 and isinstance(args[0], (Number, int, uint, builtins.int, float)):
         super().__init__([undefined for i in range(args[0])])
      else:
         super().__init__(args)

   def __getitem__(self, item):
      if isinstance(item, slice):
         return Array(*[self[i] for i in range(*item.indices(len(self)))])
      else:
         try:
            value = super().__getitem__(item)
            return value if value is not None else undefined
         except Exception:
            return undefined

   def __setitem__(self, item, value):
      if isinstance(item, (builtins.int, int, uint, Number)) and item+1 > self.length:
         '''
         When you assign a value to an array element (for example, my_array[index] = value), if index is a number, and index+1 is greater than the length property, the length property is updated to index+1.
         '''
         self.length = item+1
      super().__setitem__(item, value)

   @property
   def length(self):
      return len(self)

   @length.setter
   def length(self, value: builtins.int | int):
      if value < 0:
         raise RangeError(f'Array.length can not be negative. got {value}')
      elif value == 0:
         self.clear()
      elif len(self) > value:
         while len(self) > value:
            self.pop()
      elif len(self) < value:
         while len(self) < value:
            self.append(undefined)

   def __add__(self, item):
      return self.toString() + str(item)

   def __repr__(self):
      return f'as3lib.Array({self.toString()})'

   def __pos__(self):
      return Number(0)

   def __neg__(self):
      return -Number(0)

   def concat(self, *args):
      '''
      Concatenates the elements specified in the parameters with the elements in an array and creates a new array. If the parameters specify an array, the elements of that array are concatenated. If you don't pass any parameters, the new array is a duplicate (shallow clone) of the original array.
      Parameters:
         *args — A value of any data type (such as numbers, elements, or strings) to be concatenated in a new array.
      Returns:
         Array — An array that contains the elements from this array followed by elements from the parameters.
      '''
      newArr = Array(*self)
      for i in args:
         if isinstance(i, (list, tuple)):
            newArr.extend(i)
         else:
            newArr.append(i)
      return newArr

   def every(self, callback: callable):
      '''
      Executes a test function on each item in the array until an item is reached that returns False for the specified function. You use this method to determine whether all items in an array meet a criterion, such as having values less than a particular number.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple comparison (for example, item < 20) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Boolean — A Boolean value of True if all items in the array return True for the specified function; otherwise, False.
      '''
      if callback is null:
         return True
      for i in range(len(self)):
         if callback(self[i], i, self) is False:
            return False
      return True

   def filter(self, callback: callable):
      '''
      Executes a test function on each item in the array and constructs a new array for all items that return True for the specified function. If an item returns False, it is not included in the new array.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple comparison (for example, item < 20) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Array — A new array that contains all items from the original array that returned True.
      '''
      if callback is null:
         return
      tempArray = Array()
      for i in range(len(self)):
         if callback(self[i], i, self) is True:
            tempArray.push(self[i])
      return tempArray

   def forEach(self, callback: callable):
      '''
      Executes a function on each item in the array.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple command (for example, a trace() statement) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      '''
      if callback is null:
         return undefined
      for i in range(len(self)):
         callback(self[i], i, self)

   def indexOf(self, searchElement, fromIndex: builtins.int | int = 0):
      '''
      Searches for an item in an array using == and returns the index position of the item.
      Parameters:
         searchElement — The item to find in the array.
         fromIndex:int (default = 0) — The location in the array from which to start searching for the item.
      Returns:
         index:int — A zero-based index position of the item in the array. If the searchElement argument is not found, the return value is -1.
      '''
      if fromIndex < 0:
         fromIndex = 0
      for i in range(fromIndex, len(self)):
         if self[i] == searchElement:
            return i
      return -1

   def insertAt(self, index: builtins.int | int, element):
      '''
      Insert a single element into an array.
      Parameters
         index:int — An integer that specifies the position in the array where the element is to be inserted. You can use a negative integer to specify a position relative to the end of the array (for example, -1 is the last element of the array).
         element — The element to be inserted.
      '''
      self.insert(index, element)

   @staticmethod
   def _join(o, sep=None):
      if sep is None or sep is undefined:
         s = ','
      elif hasattr(sep, 'toString'):
         s = sep.toString()
      else:
         s = str(sep)
      with textObject() as out:
         n = o.length
         for i in range(n):
            x = o[i]
            if x is not None and x is not undefined and x is not null:
               out += str(x)
            if i + 1 < n:
               out += s
         return out.get()

   def join(self, sep: str = ','):
      '''
      Warining: Due to how this works, this will fail if you nest more Arrays than python's maximum recursion depth. If this becomes a problem, you should consider using a different programming language for your project.

      Converts the elements in an array to strings, inserts the specified separator between the elements, concatenates them, and returns the resulting string. A nested array is always separated by a comma (,), not by the separator passed to the join() method.
      Parameters:
         sep (default = ",") — A character or string that separates array elements in the returned string. If you omit this parameter, a comma is used as the default separator.
      Returns:
         String — A string consisting of the elements of an array converted to strings and separated by the specified parameter.

      Note: Mixing python objects with as3lib objects may not give the desired result.
      '''
      return Array._join(self, sep)

   def lastIndexOf(self, searchElement, fromIndex: builtins.int | int = None):
      '''
      Searches for an item in an array, working backward from the last item, and returns the index position of the matching item using ==.
      Parameters:
         searchElement — The item to find in the array.
         fromIndex:int (default = 99*10^99) — The location in the array from which to start searching for the item. The default is the maximum value allowed for an index. If you do not specify fromIndex, the search starts at the last item in the array.
      Returns:
         int — A zero-based index position of the item in the array. If the searchElement argument is not found, the return value is -1.
      '''
      if fromIndex is None:
         fromIndex = len(self)
      elif fromIndex < 0:
         raise RangeError(f'Array.lastIndexOf; fromIndex can not negative. got {fromIndex}')
      index = self[::-1].indexOf(searchElement, len(self)-1-fromIndex)
      return index if index == -1 else len(self)-1-index

   def map(self, callback: callable):
      '''
      Executes a function on each item in an array, and constructs a new array of items corresponding to the results of the function on each item in the original array.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple command (such as changing the case of an array of strings) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Array — A new array that contains the results of the function on each item in the original array.
      '''
      if callback is null:
         return
      return Array(*[callback(self[i], i, self) for i in range(len(self))])

   def pop(self):
      '''
      Removes the last element from an array and returns the value of that element.
      Returns:
         * — The value of the last element (of any data type) in the specified array.
      '''
      return super().pop(-1)

   def push(self, *args):
      '''
      Adds one or more elements to the end of an array and returns the new length of the array.
      Parameters:
         *args — One or more values to append to the array.
      '''
      self.extend(args)

   def removeAt(self, index: builtins.int | int):
      '''
      Remove a single element from an array. This method modifies the array without making a copy.
      Parameters:
         index:int — An integer that specifies the index of the element in the array that is to be deleted. You can use a negative integer to specify a position relative to the end of the array (for example, -1 is the last element of the array).
      Returns:
         * — The element that was removed from the original array.
      '''
      return super().pop(index)

   def reverse(self):
      '''
      Reverses the array in place.
      Returns:
         Array — The new array.
      '''
      super().reverse()
      return self

   def shift(self):
      '''
      Removes the first element from an array and returns that element. The remaining array elements are moved from their original position, i, to i-1.
      Returns:
         * — The first element (of any data type) in an array.
      '''
      return super().pop(0)

   def slice(self, startIndex: builtins.int | int = 0, endIndex: builtins.int | int = 99*10^99):
      '''
      Returns a new array that consists of a range of elements from the original array, without modifying the original array. The returned array includes the startIndex element and all elements up to, but not including, the endIndex element.
      If you don't pass any parameters, the new array is a duplicate (shallow clone) of the original array.
      Parameters:
         startIndex:int (default = 0) — A number specifying the index of the starting point for the slice. If startIndex is a negative number, the starting point begins at the end of the array, where -1 is the last element.
         endIndex:int (default = 99*10^99) — A number specifying the index of the ending point for the slice. If you omit this parameter, the slice includes all elements from the starting point to the end of the array. If endIndex is a negative number, the ending point is specified from the end of the array, where -1 is the last element.
      Returns:
         Array — An array that consists of a range of elements from the original array.
      '''
      if startIndex < 0:
         startIndex = len(self)+startIndex
      if endIndex < 0:
         endIndex = len(self)+endIndex
      return self[startIndex: endIndex]

   def some(self, callback: callable):
      '''
      Executes a test function on each item in the array until an item is reached that returns True. Use this method to determine whether any items in an array meet a criterion, such as having a value less than a particular number.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple comparison (for example item < 20) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Boolean — A Boolean value of True if any items in the array return True for the specified function; otherwise False.
      '''
      if callback is null:
         return False
      for i in range(len(self)):
         if callback(self[i], i, self) is True:
            return True
      return False

   def sort(self, *args):
      '''
      Warning: Maximum element length is 100000
      '''
      if len(args) == 0:
         '''
         Sorting is case-sensitive (Z precedes a).
         Sorting is ascending (a precedes b).
         The array is modified to reflect the sort order; multiple elements that have identical sort fields are placed consecutively in the sorted array in no particular order.
         All elements, regardless of data type, are sorted as if they were strings, so 100 precedes 99, because "1" is a lower string value than "9".
         '''
         def s(x, y):
            trace('Array.sort: BROKEN: Using Array.sort with no arguements doesn\'t work as intended because the documentation does not include the entire sort order')
            sortorder = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'  # 123456789 #!Where numbers and symbols?
            x, y = str(x), str(y)
            if sortorder.index(x[0]) > sortorder.index(y[0]):
               return 1
            if sortorder.index(x[0]) < sortorder.index(y[0]):
               return -1
            if sortorder.index(x[0]) == sortorder.index(y[0]):
               if len(x) > 1 and len(y) > 1:
                  return s(x[1:], y[1:])
               if len(x) > 1:
                  return 1
               if len(y) > 1:
                  return -1
               return 0
         with recursionDepth(100000):
            super().sort(key=cmp_to_key(s))
      elif len(args) == 1:
         if isinstance(args[0], (bool, Boolean)) and args[0] is True:
            super().sort()
         elif isfunction(args[0]):
            super().sort(key=lambda: cmp_to_key(args[0]))
         elif isinstance(args[0], (builtins.int, float, int, uint, Number)):
            if args[0] == 1:  # CASEINSENSITIVE
               raise NotImplementedError('Array.sort(1)')
            elif args[0] == 2:  # DESCENDING
               raise NotImplementedError('Array.sort(2)')
            elif args[0] == 4:  # UNIQUESORT
               raise NotImplementedError('Array.sort(4)')
            elif args[0] == 8:  # RETURNINDEXEDARRAY
               raise NotImplementedError('Array.sort(8)')
            elif args[0] == 16:  # NUMERIC
               def s(x, y):
                  try:
                     x, y = float(x), float(y)
                  except Exception:
                     raise Error('Array.sort; Can not use Array.NUMERIC (16) when array doesn\'t only contain numbers or strings that convert to numbers')
                  if x > y:
                     return 1
                  if x < y:
                     return -1
                  if x == y:
                     return 0
               super().sort(key=cmp_to_key(s))
            else:
               raise NotImplementedError(f'Array.sort({args[0]})')
         elif type(args[0]) in (tuple, list, Array):
            raise NotImplementedError('Array.sort with multiple sortOptions')
      else:
         raise NotImplementedError('Array.sort with more than one arguement')

   def sortOn():...

   def splice(self, startIndex: builtins.int | int, deleteCount: builtins.int | int, *values):
      '''
      Adds elements to and removes elements from an array. This method modifies the array without making a copy.
      Parameters:
         startIndex:int — An integer that specifies the index of the element in the array where the insertion or deletion begins. You can use a negative integer to specify a position relative to the end of the array (for example, -1 is the last element of the array).
         deleteCount:int — An integer that specifies the number of elements to be deleted. This number includes the element specified in the startIndex parameter. If you do not specify a value for the deleteCount parameter, the method deletes all of the values from the startIndex element to the last element in the array. If the value is 0, no elements are deleted.
         *values — An optional list of one or more comma-separated values to insert into the array at the position specified in the startIndex parameter. If an inserted value is of type Array, the array is kept intact and inserted as a single element. For example, if you splice an existing array of length three with another array of length three, the resulting array will have only four elements. One of the elements, however, will be an array of length three.
      Returns:
         Array — An array containing the elements that were removed from the original array.
      '''
      if startIndex < 0:
         startIndex = len(self) + startIndex
      if deleteCount < 0:
         raise RangeError(f'Array.splice; deleteCount can not negative. got {deleteCount}')
      removedValues = self[startIndex: startIndex+deleteCount]
      self[startIndex: startIndex+deleteCount] = values
      return removedValues

   def toList(self):
      return list(self)

   def toLocaleString(self):
      '''
      Returns a string that represents the elements in the specified array. Every element in the array, starting with index 0 and ending with the highest index, is converted to a concatenated string and separated by commas. In the ActionScript 3.0 implementation, this method returns the same value as the Array.toString() method.
      Returns:
         String — A string of array elements.
      '''
      with textObject() as out:
         n = self.length
         for i in range(n):
            x = self[i]
            if x is not None and x is not undefined and x is not null:
               if hasattr(x, 'toLocaleString'):
                  out += x.toLocaleString()
               else:
                  out += str(x)
            if i + 1 < n:
               out += ','
         return out.get()

   def toString(self):
      '''
      Returns a string that represents the elements in the specified array. Every element in the array, starting with index 0 and ending with the highest index, is converted to a concatenated string and separated by commas. To specify a custom separator, use the Array.join() method.
      Returns:
         String — A string of array elements.

      Note: Mixing python objects with as3lib objects may not give the desired result.
      '''
      return Array._join(self)

   def unshift(self, *args):
      '''
      Adds one or more elements to the beginning of an array and returns the new length of the array. The other elements in the array are moved from their original position, i, to i+1.
      Parameters:
         *args — One or more numbers, elements, or variables to be inserted at the beginning of the array.
      Returns:
         int — An integer representing the new length of the array.
      '''
      tempArray = [*args, *self]
      self.clear()
      self.extend(tempArray)
      return len(self)


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
      return int.MIN_VALUE + value % (int.MAX_VALUE + 1)

   @staticmethod
   def _lowerBounds(value):
      return value % int.MAX_VALUE + 1

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
      return value % (uint.MAX_VALUE + 1)

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
      elif isinstance(value, (uint, int)):
         self._value = uint._boundsCheck(value._value)
      elif isinstance(value, builtins.int):
         self._value = uint._boundsCheck(value)
      elif hasattr(value, '__int__'):
         self._value = uint._boundsCheck(builtins.int(value))
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

   def __lt__(self, value):
      return self._value < value

   def __gt__(self, value):
      return self._value > value

   def __neg__(self):
      if self._value is _NaN_value:
         return Number.NaN
      if self._value == _NegInf_value:
         return Number.NEGATIVE_INFINITY
      if self._value == _PosInf_value:
         return Number.POSITIVE_INFINITY
      return Number(-self._value)

   def __bool__(self):
      if self._value is _NaN_value:
         return False
      return self._value != 0

   def __abs__(self):
      if self._value is _NaN_value:
         return Number.NaN
      if self._value in {_NegInf_value, _PosInf_value}:
         return Number.POSITIVE_INFINITY
      return Number(self._value)

   def _Number(self, expression):
      if expression == _NegInf_value or expression == _PosInf_value or isinstance(expression, (float, Number)):
         return expression
      if expression is _NaN_value or expression is undefined or expression is None:
         return _NaN_value
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
            return _NaN_value

   def toExponential(self):...
   def toFixed(self):...
   def toPrecision():...

   def toLocaleString(self):
      return self.toString()

   def toString(self, radix=10):
      # TODO: Radix
      if self._value is _NaN_value:
         return 'NaN'
      if self._value == _NegInf_value:
         return "-Infinity"
      if self._value == _PosInf_value:
         return "Infinity"
      if self._value.is_integer():
         return f'{int(self._value)}'
      return f'{self._value}'

   def valueOf(self):
      return self._value


Number.NaN = Number(_NaN_value)
Number.NEGATIVE_INFINITY = Number(_NegInf_value)
Number.POSITIVE_INFINITY = Number(_PosInf_value)


class String(str, Object):
   def __init__(self, value=''):
      self.__init2(self._String(value))

   def __init2(self, value):
      super().__init__()

   def __str__(self):
      return self

   @property
   def length(self):
      return len(self)

   def _String(self, expression):
      if isinstance(expression, str):
         return expression
      if isinstance(expression, bool):
         return 'true' if expression else 'false'
      if hasattr(expression, 'toString'):
         return expression.toString()
      return f'{expression}'

   def __repr__(self):
      return f'as3lib.String({self})'

   def __getitem__(self, item):
      return String(super().__getitem__(item))

   def __add__(self, value):
      return String(f'{self}{self._String(value)}')

   def __bool__(self):
      return self.length > 0

   def __neg__(self):
      # TODO: Make sure that this is correct
      return -parseFloat(self)

   def __pos__(self):
      # TODO: Make sure that this is correct
      return parseFloat(self)

   def charAt(self, index: builtins.int | int = 0):
      if index < 0 or index > len(self) - 1:
         return ''
      return self[index]

   def charCodeAt(self, index: builtins.int | int = 0):
      if index < 0 or index > len(self) - 1:
         return Number.NaN
      return parseInt(r'{:04X}'.format(ord(self[index])), 16)

   def concat(self, *args):
      return self + ''.join([self._String(i) for i in args])

   def fromCharCode():...

   def indexOf(self, val, startIndex: builtins.int | int = 0):
      return self.find(val, startIndex)

   def lastIndexOf(self, val, startIndex: builtins.int | int = None):...
   def localeCompare():...
   def match():...
   def replace():...
   def search():...

   def slice(self, startIndex=0, endIndex=None):
      if endIndex is None:
         return self[startIndex:]
      if startIndex < 0:...
      return self[startIndex:endIndex]

   def split(self, delimiter=None, limit=0x7fffffff):
      if delimiter is undefined or delimiter is None:
         arr = Array(self)
      elif delimiter == '' or False:  # An empty string, an empty regular expression, or a regular expression that can match an empty string
         arr = Array(sourceArray=[i for i in self])
      elif False:...  # If the delimiter parameter is a regular expression, only the first match at a given position of the string is considered, even if backtracking could find a nonempty substring match at that position.
      elif False:...  # If the delimiter parameter is a regular expression containing grouping parentheses, then each time the delimiter is matched, the results (including any undefined results) of the grouping parentheses are spliced into the output array.
      if limit != 0x7fffffff:
         return arr[:limit]
      return arr

   def substr(self, startIndex: builtins.int | int = 0, len: builtins.int | int = None):
      if len < 0:
         len = 0
      if startIndex < 0:
         startIndex = self.length + startIndex
      if len is None:
         return self[startIndex:]
      return self[startIndex:startIndex+len]

   def substring(self, startIndex: builtins.int | int = 0, endIndex: builtins.int | int = None):
      if startIndex < 0:
         startIndex = 0
      if endIndex is None:
         endIndex = len(self)
      if endIndex < 0:
         endIndex = 0
      if startIndex > endIndex:
         return self[endIndex:startIndex]
      return self[startIndex:endIndex]

   def toLocaleLowerCase(self):
      return self.lower()

   def toLocaleUpperCase(self):
      return self.upper()

   def toLowerCase(self):
      return self.lower()

   def toUpperCase(self):
      return self.upper()

   def toString(self):
      return self

   def valueOf(self):
      return f"{self}"


class Vector(list, Object):
   '''
   AS3 Vector datatype.

   This class is not really a vector as I haven't found a way to do that in
   python. It is instead just a type locked list.

   I have not found a way to create a syntax similar to Vector.<T> so you
   currently have to declare it like Vector(..., type=T). The way this is
   currently handled also does not allow you to use Vector.<T> as a type.
   '''
   _mdspns = {}

   @staticmethod
   def coercePythonToAs3Object(obj, type_):
      # bool must go above int because bool isinstance of int
      if isinstance(obj, bool):
         return Boolean(obj)
      if isinstance(obj, builtins.int):
         if type_ is int:
            return int(obj)
         if type_ is uint:
            return uint(obj)
         return Number(obj)
      if isinstance(obj, float):
         return Number(obj)
      if isinstance(obj, str):
         return String(obj)

      # Could not coerce object or object already as3
      return obj

   @staticmethod
   def _checkTypeAll(arr, type_, superclass):
      # TODO: Implements/Implementer
      for i in arr:
         Vector._checkType(i, type_, superclass)

   @staticmethod
   def _checkType(value, type_, superclass):
      # TODO: Implements/Implementer
      if value is not null:
         if superclass:
            if not isinstance(value, type_):
               raise TypeError('%s is not %s or subclass of %s' % (type(value), type_, type_))
         else:
            if type(value) is not type_:
               raise TypeError('%s is not %s' % (type(value), type_))

   @dispatch(list, namespace=_mdspns)
   def __init__(self, sourceArray, **kwargs):
      # TODO: Make sure this works properly
      self._type = kwargs['type']
      self._fixed = False
      self._superclass = True
      if isinstance(sourceArray, Vector):
         self = sourceArray
      else:
         sourceArray = [Vector.coercePythonToAs3Object(i, self._type) for i in sourceArray]
         Vector._checkTypeAll(sourceArray, self._type, self._superclass)
         super().__init__(sourceArray)

   def _number_init(self, length, fixed, **kwargs):
      self._type = kwargs['type']
      self._superclass = False
      super().__init__((null for i in range(length)))
      self._fixed = fixed

   @dispatch(object, object, namespace=_mdspns)
   def __init__(self, length=0, fixed=False, **kwargs):
      self._number_init(length, fixed, **kwargs)

   @dispatch(object, namespace=_mdspns)
   def __init__(self, length=0, **kwargs):
      self._number_init(length, False, **kwargs)

   @dispatch(namespace=_mdspns)
   def __init__(self, **kwargs):
      self._number_init(0, False, **kwargs)

   @property
   def fixed(self):
      return self._fixed

   @fixed.setter
   def fixed(self, value):
      self._fixed = value

   @property
   def length(self):
      return len(self)

   @length.setter
   def length(self, value):
      if self.fixed:
         raise RangeError('Can not set vector length while fixed is set to true.')
      if value > 4294967296:
         raise RangeError('New length outside of accepted range (0-4294967296).')
      if len(self) > value:
         while len(self) > value:
            self.pop()
      elif len(self) < value:
         while len(self) < value:
            self.append(null)

   @staticmethod
   def _join(o, sep=None):
      if sep is None or sep is undefined:
         s = ','
      elif hasattr(sep, 'toString'):
         s = sep.toString()
      else:
         s = str(sep)
      with StringIO() as out:
         n = o.length
         for i in range(n):
            x = o[i]
            if x != None:
               out.write(str(x))
            if i + 1 < n:
               out.write(s)
         return out.getvalue()

   def __repr__(self):
      return 'as3lib.Vector.<%s>(%s)' % (self._type.__name__, self)

   def __getitem__(self, item):
      if isinstance(item, slice):...
      else:
         return super().__getitem__(item)

   def __setitem__(self, item, value):
      value = Vector.coercePythonToAs3Object(value, self._type)
      Vector._checkType(value, self._type, self._superclass)
      super().__setitem__(item, value)

   def concat(self, *args):
      temp = Vector([], type=self._type)
      temp.extend(self)
      if len(args) > 0:
         for i in args:
            if isinstance(i, Vector) and issubclass(i._type, self._type):
               temp.extend(i)
            elif not isinstance(i, Vector):
               raise TypeError('Vector.concat; One or more arguements are not of type Vector')
            else:
               raise TypeError('Vector.concat; One or more arguements do not have a base type that can be converted to the current base type.')
      temp.fixed = self.fixed
      return temp

   def every(self, callback, thisObject=null):
      if callback is null:
         return True
      for i, item in enumerate(self):
         if callback(item, i, self) is False:
            return False
      return True

   def filter(self, callback, thisObject=null):
      # TODO: Handle null callback
      tempVector = Vector(type=self._type)
      tempVector._superclass = self._superclass
      for i, item in enumerate(self):
         if callback(item, i, self) is True:
            tempVector.push(item)
      return tempVector

   def forEach(self, callback, thisObject=null):
      if callback is null:
         return undefined
      for i, item in enumerate(self):
         callback(item, i, self)

   def indexOf(self, searchElement, fromIndex=0):
      if fromIndex < 0:
         fromIndex = len(self) - fromIndex
      for i in range(fromIndex, len(self)):
         if self[i] == searchElement:
            return i
      return -1

   def insertAt(self, index, element):
      if self.fixed:
         raise RangeError('insertAt can not be called on a Vector with fixed set to true.')
      elif self._superclass:
         if element is null or isinstance(element, self._type):...
      else:...

   def join(self, sep: str = ','):
      return Vector._join(self, sep)

   def lastIndexOf(self, searchElement, fromIndex=None):
      if fromIndex is None:
         fromIndex = len(self)
      elif fromIndex < 0:
         fromIndex = len(self) - fromIndex
      ...
      # index = self[::-1].indexOf(searchElement,len(self)-1-fromIndex)
      # return index if index == -1 else len(self)-1-index

   def map(self, callback, thisObject=null):
      # TODO: Handle null callback
      tempVect = Vector(self.length, type=self._type)
      tempVect._superclass = self._superclass
      for i, item in enumerate(self):
         tempVect[i] = callback(item, i, self)
      return tempVect

   def pop(self):
      if self.fixed:
         raise RangeError('pop can not be called on a Vector with fixed set to true.')
      return super().pop(-1)

   def push(self, *args):
      if self.fixed:
         raise RangeError('push can not be called on a Vector with fixed set to true.')
      # !Check item types
      self.extend(args)
      return len(self)

   def removeAt(self, index):
      if self.fixed:
         raise RangeError('removeAt can not be called on a Vector with fixed set to true.')
      elif False:  # !Index out of bounds
         raise RangeError('index is out of bounds.')
      return super().pop(index)

   def reverse(self):
      super().reverse()
      return self

   def shift(self):
      if self.fixed:
         raise RangeError('shift can not be called on a Vector with fixed set to true.')
      return super().pop(0)

   def slice(self):
      raise NotImplementedError

   def some(self, callback, thisObject=null):
      if callback is null:
         return False
      for i, item in enumerate(self):
         if callback(item, i, self) is True:
            return True
      return False

   def sort(self):
      raise NotImplementedError

   def splice(self):
      raise NotImplementedError

   def toLocaleString(self):
      raise NotImplementedError

   def toString(self):
      return Vector._join(self)

   def unshift(self, *args):
      if self.fixed:
         raise RangeError('unshift can not be called on a Vector with fixed set to true.')
      argsOK = True
      if self._superclass:
         for i in args:
            if i is not null or not isinstance(i, self._type):
               argsOK = False
               break
      else:
         for i in args:
            if i is not null or type(i) is not self._type:
               argsOK = False
               break
      if not argsOK:
         raise TypeError('One or more args is not of the Vector\'s base type.')
      tempVect = (*args, *self)
      self.clear()
      self.extend(tempVect)
      return len(self)

# Temporary aliases. Remove when a syntax similar to Vector.<Type> is
# implemented.
Vector.Boolean = partial(Vector, type=Boolean)
Vector.int = partial(Vector, type=int)
Vector.Number = partial(Vector, type=Number)
Vector.uint = partial(Vector, type=uint)
Vector.String = partial(Vector, type=String)
