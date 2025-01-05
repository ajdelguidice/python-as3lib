import math as m
import random as r
from textwrap import wrap
from pathlib import Path
from . import configmodule, helpers
import builtins
from typing import overload, TypeVar, Callable
try:
   from warnings import deprecated
except:
   from .py_backports import deprecated
from functools import cmp_to_key
from inspect import isfunction

from numpy import nan, inf, base_repr

#Static values
true = True
false = False

#Dummy Classes (Here so python doesn't complain)
class Array:...
class Boolean:...
class int:...
class Number:...
class String:...
class uint:...
class Vector:...

#Objects with set values
class NInfinity:
   __slots__ = ("__value")
   def __init__(self):
      self.__value = -inf
   def __str__(self):
      return "-Infinity"
   def __repr__(self):
      return self.__value
   def __lt__(self, value):
      if typeName(value) == "NInfinity":
         return False
      else:
         return True
   def __le__(self, value):
      if typeName(value) == "NInfinity":
         return True
      else:
         return False
   def __eq__(self, value):
      if typeName(value) == "NInfinity":
         return True
      else:
         return False
   def __ne__(self, value):
      if typeName(value) == "NInfinity":
         return False
      else:
         return True
   def __gt__(self, value):
      return False
   def __ge__(self, value):
      if typeName(value) == "NInfinity":
         return True
      else:
         return False
   def __bool__(self):
      return True
   def __getattr__(self, value):
      return "NInfinity"
   def __getattribute__(self, value):
      return "NInfinity"
   def __setattr__(self, *value):
      pass
   def __add__(self, value):
      return self
   def __radd__(self, value):
      return self
   def __iadd__(self, value):
      return self
   def __sub__(self, value):
      return self
   def __mul__(self, value):
      return self
   def __matmul__(self, value):
      return self
   def __truediv__(self, value):
      return self
   def __floordiv__(self, value):
      return self
   def __mod__(self, value):
      return self
   def __divmod__(self, value):
      return self
   def __pow__(self, value):
      return self
   def __lshift__(self, value):
      return self
   def __rshift__(self, value):
      return self
   def __and__(self, value):
      if bool(value) == True:
         return True
      else:
         return False
   def __or__(self, value):
      return True
   def __xor__(self, value):
      if bool(value) == True:
         return False
      else:
         return True
   def __neg__(self):
      return self
   def __pos__(self):
      return NInfinity()
   def __abs__(self):
      return Infinity()
   def __invert__(self):
      return Infinity()
   def __complex__(self):
      return self
   def __int__(self):
      return self
   def __float__(self):
      return self
   def __round__(self):
      return self
   def __floor__(self):
      return self
   def __ceil__(self):
      return self
class Infinity:
   __slots__ = ("__value")
   def __init__(self):
      self.__value = inf
   def __str__(self):
      return "Infinity"
   def __repr__(self):
      return self.__value
   def __lt__(self, value):
      return False
   def __le__(self, value):
      if typeName(value) == "Infinity":
         return True
      else:
         return False
   def __eq__(self, value):
      if typeName(value) == "Infinity":
         return True
      else:
         return False
   def __ne__(self, value):
      if typeName(value) == "Infinity":
         return False
      else:
         return True
   def __gt__(self, value):
      if typeName(value) == "Infinity":
         return False
      else:
         return True
   def __ge__(self, value):
      return True
   def __bool__(self):
      return True
   def __getattr__(self, value):
      return "Infinity"
   def __getattribute__(self, value):
      return "Infinity"
   def __setattr__(self, *value):
      pass
   def __add__(self, value):
      return self
   def __radd__(self, value):
      return self
   def __iadd__(self, value):
      return self
   def __sub__(self, value):
      return self
   def __mul__(self, value):
      return self
   def __matmul__(self, value):
      return self
   def __truediv__(self, value):
      return self
   def __floordiv__(self, value):
      return self
   def __mod__(self, value):
      return self
   def __divmod__(self, value):
      return self
   def __pow__(self, value):
      return self
   def __lshift__(self, value):
      return self
   def __rshift__(self, value):
      return self
   def __and__(self, value):
      if bool(value) == True:
         return True
      else:
         return False
   def __or__(self, value):
      return True
   def __xor__(self, value):
      if bool(value) == True:
         return False
      else:
         return True
   def __neg__(self):
      return NInfinity()
   def __pos__(self):
      return self
   def __abs__(self):
      return self
   def __invert__(self):
      return NInfinity()
   def __complex__(self):
      return self
   def __int__(self):
      return self
   def __float__(self):
      return self
   def __round__(self):
      return self
   def __floor__(self):
      return self
   def __ceil__(self):
      return self
class NaN:
   __slots__ = ("__value")
   def __init__(self):
      self.__value = nan
   def __str__(self):
      return "NaN"
   def __repr__(self):
      return f"{self.__value}"
   def __lt__(self, value):
      return False
   def __le__(self, value):
      return False
   def __eq__(self, value):
      return False
   def __ne__(self, value):
      return True
   def __gt__(self, value):
      return False
   def __ge__(self, value):
      return False
   def __bool__(self):
      return False
   def __getattr__(self, value):
      return "NaN"
   def __getattribute__(self, value):
      return "NaN"
   def __setattr__(self, *value):
      pass
   def __contains__(self, value):
      return False
   def __add__(self, value):
      return self
   def __radd__(self, value):
      return self
   def __iadd__(self, value):
      return self
   def __sub__(self, value):
      return self
   def __mul__(self, value):
      return self
   def __matmul__(self, value):
      return self
   def __truediv__(self, value):
      return self
   def __floordiv__(self, value):
      return self
   def __mod__(self, value):
      return self
   def __divmod__(self, value):
      return self
   def __pow__(self, value):
      return self
   def __lshift__(self, value):
      return self
   def __rshift__(self, value):
      return self
   def __and__(self, value):
      return False
   def __xor__(self, value):
      return False
   def __or__(self, value):
      return False
   def __neg__(self):
      return self
   def __pos__(self):
      return self
   def __abs__(self):
      return self
   def __invert__(self):
      return
   def __complex__(self):
      return self
   def __int__(self):
      return self
   def _uint(self):
      return 0
   def __float__(self):
      return self
   def __round__(self):
      return self
   def __trunc__(self):
      return self
   def __floor__(self):
      return self
   def __ceil__(self):
      return self
class undefined:
   __slots__ = ("value")
   def __init__(self):
      self.value = None
   def __str__(self):
      return "undefined"
   def __repr__(self):
      return "None"
class null:
   __slots__ = ("value")
   def __init__(self):
      self.value = None
   def __str__(self):
      return "null"
   def __repr__(self):
      return "None"

#TypeVars
allNumber = TypeVar("allNumber",builtins.int,float,int,uint,Number)
allString = TypeVar("allString",str,String)
allArray = TypeVar("allArray",list,tuple,Array)
allBoolean = TypeVar("allBoolean",bool,Boolean)
allNone = TypeVar("allNone",undefined,null)

#Classes
class ArgumentError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
class Array(list):
   __slots__ = ("filler")
   CASEINSENSITIVE = 1
   DESCENDING = 2
   UNIQUESORT = 4
   RETURNINDEXEDARRAY =  8
   NUMERIC = 16
   def __init__(self,*args,numElements:builtins.int|int=None):
      self.filler = undefined()
      if numElements == None:
         super().__init__(args)
      else:
         if numElements < 0:
            RangeError(f"Array; numElements can not be less than 0. numElements is {numElements}")
         else:
            super().__init__([self.filler for i in range(numElements)])
   def __getitem__(self, item):
      if isinstance(item, slice):
         indices = range(*item.indices(len(self)))
         return Array(*[self[i] for i in indices])
      else:
         try:
            value = super().__getitem__(item)
            return value if value != None else undefined()
         except:
            return ""
   def __setitem__(self,item,value):
      if type(item) in (builtins.int,int,uint,Number) and item+1 > self.length:
         """
         When you assign a value to an array element (for example, my_array[index] = value), if index is a number, and index+1 is greater than the length property, the length property is updated to index+1.
         """
         self.length = item+1
      super().__setitem__(item,value)
   def _getLength(self):
      return len(self)
   def _setLength(self,value:builtins.int|int):
      if value < 0:
         trace("RangeError",f"Array; new length {value} is below zero",isError=True)
      elif value == 0:
         self.clear()
      elif len(self) > value:
         while len(self) > value:
            self.pop()
      elif len(self) < value:
         while len(self) < value:
            self.append(self.filler)
   def __add__(self,item):
      if type(item) not in (list,tuple,Array):
         return Array(*super().__add__([item]))
      return Array(*super().__add__(item))
   def __iadd__(self,item):
      if type(item) not in (list,tuple,Array):
         self.push(item)
      else:
         self.extend(item)
   def __str__(self):
      return self.toString()
   def __repr__(self):
      return f"as3lib.toplevel.Array({self.toString()})"
   length = property(fget=_getLength,fset=_setLength)
   def setFiller(self,newFiller):
      self.filler = newFiller
   def concat(self,*args):
      """
      Concatenates the elements specified in the parameters with the elements in an array and creates a new array. If the parameters specify an array, the elements of that array are concatenated. If you don't pass any parameters, the new array is a duplicate (shallow clone) of the original array.
      Parameters:
         *args — A value of any data type (such as numbers, elements, or strings) to be concatenated in a new array.
      Returns:
         Array — An array that contains the elements from this array followed by elements from the parameters.
      """
      if len(args) == 0:
         return Array(*self)
      elif len(args) == 1 and type(args[0]) in (list,tuple,Array): #!check whether this should be "if any element is array" or if it is only one
         return self+list(args[0])
      else:
         return self+list(args)
   def every(self, callback:callable):
      """
      Executes a test function on each item in the array until an item is reached that returns False for the specified function. You use this method to determine whether all items in an array meet a criterion, such as having values less than a particular number.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple comparison (for example, item < 20) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Boolean — A Boolean value of True if all items in the array return True for the specified function; otherwise, False.
      """
      for i in range(len(self)):
         if callback(self[i], i, self) == False:
            return False
      return True
   def filter(self, callback:callable):
      """
      Executes a test function on each item in the array and constructs a new array for all items that return True for the specified function. If an item returns False, it is not included in the new array.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple comparison (for example, item < 20) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Array — A new array that contains all items from the original array that returned True. 
      """
      tempArray = Array()
      for i in range(len(self)):
         if callback(self[i], i, self) == True:
            tempArray.push(self[i])
      return tempArray
   def forEach(self, callback:callable):
      """
      Executes a function on each item in the array.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple command (for example, a trace() statement) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      """
      for i in range(len(self)):
         callback(self[i], i, self)
   def indexOf(self, searchElement, fromIndex:builtins.int|int=0):
      """
      Searches for an item in an array using == and returns the index position of the item.
      Parameters:
         searchElement — The item to find in the array.
         fromIndex:int (default = 0) — The location in the array from which to start searching for the item.
      Returns:
         index:int — A zero-based index position of the item in the array. If the searchElement argument is not found, the return value is -1.
      """
      if fromIndex < 0:
         fromIndex = 0
      for i in range(fromIndex,len(self)):
         if self[i] == searchElement:
            return i
      return -1
   def insertAt(self, index:builtins.int|int, element):
      """
      Insert a single element into an array.
      Parameters
	      index:int — An integer that specifies the position in the array where the element is to be inserted. You can use a negative integer to specify a position relative to the end of the array (for example, -1 is the last element of the array).
	      element — The element to be inserted.
      """
      #can possibly be replaced with just self.insert(index,element) but this is slightly different than current
      #current inserts from end if negative while insert acts like the array is reversed
      if index < 0:
         self.insert((len(self) + index), element)
      else:
         self.insert(index, element)
   def join(self, sep:str|String=",", interpretation:int|builtins.int=0, _Array=None):
      """
      Warining: Due to how this works, this will fail if you nest more Arrays than python's maximum recursion depth. If this becomes a problem, you should consider using a different programming language for your project.

      Converts the elements in an array to strings, inserts the specified separator between the elements, concatenates them, and returns the resulting string. A nested array is always separated by a comma (,), not by the separator passed to the join() method.
      Parameters:
	      sep (default = ",") — A character or string that separates array elements in the returned string. If you omit this parameter, a comma is used as the default separator.
         interpretation (default = 0) — Which interpretation of the documentation you choose to use. This is an addition parameter added in as3lib because the original documentation isn't clear
               0 — [1,2,3,[4,5,6],7,8,9], sep(+) -> "1+2+3+4,5,6+7+8+9"
               1 — [1,2,3,[4,5,6],7,8,9], sep(+) -> "1+2+3,4,5,6,7+8+9"
      Returns:
	      String — A string consisting of the elements of an array converted to strings and separated by the specified parameter.
      """
      lsep = len(sep)
      result = ""
      if _Array == None:
         _Array = self
      if interpretation == 0:
         for i in _Array:
            if type(i) in (list,tuple,Array):
               result += f"{self.join(_Array=i)}{sep}"
            elif type(i) in (type(undefined()),type(None)):
               result += sep
            else:
               result += f"{i}{sep}"
      elif interpretation == 1:
         for i in _Array:
            if type(i) in (list,tuple,Array):
               if result[-lsep:] == sep:
                  result = result[:-lsep] + f","
               result += f"{self.join(_Array=i)},"
            elif type(i) in (type(undefined()),type(None)):
               result += sep
            else:
               result += f"{i}{sep}"
      if result[-lsep:] == sep:
         return result[:-lsep]
      elif result[-1:] == ",":
         return result[:-1]
      else:
         return result
   def lastIndexOf(self, searchElement, fromIndex:builtins.int|int=None):
      """
      Searches for an item in an array, working backward from the last item, and returns the index position of the matching item using ==.
      Parameters:
	      searchElement — The item to find in the array.
	      fromIndex:int (default = 99*10^99) — The location in the array from which to start searching for the item. The default is the maximum value allowed for an index. If you do not specify fromIndex, the search starts at the last item in the array.
      Returns:
	      int — A zero-based index position of the item in the array. If the searchElement argument is not found, the return value is -1.
      """
      if fromIndex == None:
         fromIndex = len(self)
      elif fromIndex < 0:
         RangeError(f"Array.lastIndexOf; fromIndex can not be less than 0, fromIndex is {fromIndex}")
         return None
      index = self[::-1].indexOf(searchElement,len(self)-1-fromIndex)
      return index if index == -1 else len(self)-1-index
   def map(self, callback:callable):
      """
      Executes a function on each item in an array, and constructs a new array of items corresponding to the results of the function on each item in the original array.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple command (such as changing the case of an array of strings) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Array — A new array that contains the results of the function on each item in the original array.
      """
      return Array(*[callback(self[i],i,self) for i in range(len(self))])
   def pop(self):
      """
      Removes the last element from an array and returns the value of that element.
      Returns:
         * — The value of the last element (of any data type) in the specified array.
      """
      return super().pop(-1)
   def push(self, *args):
      """
      Adds one or more elements to the end of an array and returns the new length of the array.
      Parameters:
         *args — One or more values to append to the array.
      """
      self+=list(args)
   def removeAt(self, index:builtins.int|int):
      """
      Remove a single element from an array. This method modifies the array without making a copy.
      Parameters:
	      index:int — An integer that specifies the index of the element in the array that is to be deleted. You can use a negative integer to specify a position relative to the end of the array (for example, -1 is the last element of the array).
      Returns:
	      * — The element that was removed from the original array.
      """
      return super().pop(index)
   def reverse(self):
      """
      Reverses the array in place.
      Returns:
	      Array — The new array.
      """
      super().reverse()
      return self
   def shift(self):
      """
      Removes the first element from an array and returns that element. The remaining array elements are moved from their original position, i, to i-1.
      Returns:
         * — The first element (of any data type) in an array. 
      """
      return super().pop(0)
   def slice(self, startIndex:builtins.int|int=0, endIndex:builtins.int|int=99*10^99):
      """
      Returns a new array that consists of a range of elements from the original array, without modifying the original array. The returned array includes the startIndex element and all elements up to, but not including, the endIndex element.
      If you don't pass any parameters, the new array is a duplicate (shallow clone) of the original array.
      Parameters:
         startIndex:int (default = 0) — A number specifying the index of the starting point for the slice. If startIndex is a negative number, the starting point begins at the end of the array, where -1 is the last element.
         endIndex:int (default = 99*10^99) — A number specifying the index of the ending point for the slice. If you omit this parameter, the slice includes all elements from the starting point to the end of the array. If endIndex is a negative number, the ending point is specified from the end of the array, where -1 is the last element.
      Returns:
         Array — An array that consists of a range of elements from the original array.
      """
      if startIndex < 0:
         startIndex=len(self)+startIndex
      if endIndex < 0:
         endIndex=len(self)+endIndex
      return self[startIndex:endIndex]
   def some(self, callback:callable):
      """
      Executes a test function on each item in the array until an item is reached that returns True. Use this method to determine whether any items in an array meet a criterion, such as having a value less than a particular number.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple comparison (for example item < 20) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Boolean — A Boolean value of True if any items in the array return True for the specified function; otherwise False.
      """
      for i in range(0,len(self)):
         if callback(self[i], i, self) == True:
            return True
      return False
   def sort(self, *args):
      """
      Warning: Maximum element length is 100000
      """
      if len(args) == 0:
         """
         Sorting is case-sensitive (Z precedes a).
         Sorting is ascending (a precedes b).
         The array is modified to reflect the sort order; multiple elements that have identical sort fields are placed consecutively in the sorted array in no particular order.
         All elements, regardless of data type, are sorted as if they were strings, so 100 precedes 99, because "1" is a lower string value than "9".
         """
         def s(x,y):
            trace("Array.sort: BROKEN: Using Array.sort with no arguements doesn't work as intended because the documentation does not include the entire sort order")
            sortorder = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" #123456789 #!Where numbers and symbols
            x,y = str(x),str(y)
            if sortorder.index(x[0]) > sortorder.index(y[0]):
               return 1
            elif sortorder.index(x[0]) < sortorder.index(y[0]):
               return -1
            elif sortorder.index(x[0]) == sortorder.index(y[0]):
               if len(x) > 1 and len(y) > 1:
                  return s(x[1:],y[1:])
               elif len(x) > 1:
                  return 1
               elif len(y) > 1:
                  return -1
               else:
                  return 0
         with helpers.recursionDepth(100000):
            super().sort(key=cmp_to_key(s))
      elif len(args) == 1:
         if type(args[0]) in (bool,Boolean) and args[0] == True:
            super().sort()
         elif isfunction(args[0]):
            super().sort(key=lambda:cmp_to_key(args[0]))
         elif type(args[0]) in (builtins.int,float,int,uint,Number):
            match args[0]:
               case 1: #CASEINSENSITIVE
                  raise Exception("Not Implemented Yet")
               case 2: #DESCENDING
                  raise Exception("Not Implemented Yet")
               case 4: #UNIQUESORT
                  raise Exception("Not Implemented Yet")
               case 8: #RETURNINDEXEDARRAY
                  raise Exception("Not Implemented Yet")
               case 16: #NUMERIC
                  def s(x,y):
                     try:
                        x,y = float(x),float(y)
                     except:
                        raise Exception("Array.sort: Error: Can not use Array.NUMERIC (16) when array doesn't only contain numbers or strings that convert to numbers")
                     if x > y:
                        return 1
                     elif x < y:
                        return -1
                     elif x == y:
                        return 0
                  super().sort(key=cmp_to_key(s))
               case _:
                  raise Exception(f"Array.sort: Error: sortOption {sortOption} is not implemented yet")
         elif type(args[0]) in (tuple,list,Array):
            raise Exception(f"Array.sort: Error: Using multiple sortOptions is not implemented yet")
      else:
         raise Exception(f"Using more than one arguement is not implemented yet")
   def sortOn():
      pass
   def splice(self, startIndex:builtins.int|int, deleteCount:builtins.int|int, *values):
      """
      Adds elements to and removes elements from an array. This method modifies the array without making a copy.
      Parameters:
	      startIndex:int — An integer that specifies the index of the element in the array where the insertion or deletion begins. You can use a negative integer to specify a position relative to the end of the array (for example, -1 is the last element of the array).
	      deleteCount:int — An integer that specifies the number of elements to be deleted. This number includes the element specified in the startIndex parameter. If you do not specify a value for the deleteCount parameter, the method deletes all of the values from the startIndex element to the last element in the array. If the value is 0, no elements are deleted.
	      *values — An optional list of one or more comma-separated values to insert into the array at the position specified in the startIndex parameter. If an inserted value is of type Array, the array is kept intact and inserted as a single element. For example, if you splice an existing array of length three with another array of length three, the resulting array will have only four elements. One of the elements, however, will be an array of length three.
      Returns:
	      Array — An array containing the elements that were removed from the original array. 
      """
      if startIndex < 0:
         startIndex = len(self) + startIndex
      if deleteCount < 0:
         RangeError(f"Array.splice; deleteCount can not be less than 0, deleteCount is {deleteCount}")
         return None
      removedValues = self[startIndex:startIndex+deleteCount]
      self[startIndex:startIndex+deleteCount] = values
      return removedValues
   def toList(self):
      return list(self)
   def toLocaleString(self):
      """
      Returns a string that represents the elements in the specified array. Every element in the array, starting with index 0 and ending with the highest index, is converted to a concatenated string and separated by commas. In the ActionScript 3.0 implementation, this method returns the same value as the Array.toString() method.
      Returns:
	      String — A string of array elements. 
      """
      return self.toString()
   def __listtostr(self,l):
      a = ""
      for i in l:
         if type(i) in (list,tuple,Array):
            a += self.__listtostr(i) + ","
            continue
         elif type(i) in (type(undefined()),type(None)):
            a += ","
            continue
         a += f"{i},"
      return a[:-1]
   def toString(self, formatLikePython:bool|Boolean=False, interpretation=1):
      """
      Returns a string that represents the elements in the specified array. Every element in the array, starting with index 0 and ending with the highest index, is converted to a concatenated string and separated by commas. To specify a custom separator, use the Array.join() method.
      Returns:
	      String — A string of array elements. 
      """
      if formatLikePython == True:
         return super().__str__(self)
      elif interpretation == 1:
         return self.__listtostr(self)
      else:
         return super().__str__(self)[1:-1].replace(", ",",")
   def unshift(self, *args):
      """
      Adds one or more elements to the beginning of an array and returns the new length of the array. The other elements in the array are moved from their original position, i, to i+1.
      Parameters:
	      *args — One or more numbers, elements, or variables to be inserted at the beginning of the array.
      Returns:
	      int — An integer representing the new length of the array.
      """
      tempArray = [*args,*self]
      self.clear()
      self.extend(tempArray)
      return len(self)
class Boolean:
   """
   Lets you create boolean object similar to ActionScript3
   Since python is case sensitive the values are "True" or "False" instead of "true" or "false"
   """
   __slots__ = ("bool")
   def __init__(self, expression=False):
      self.bool = self._Boolean(expression)
   def __str__(self):
      return f'{self.bool}'
   def __getitem__(self):
      return self.bool
   def __setitem__(self, value):
      self.bool = value
   def _Boolean(self, expression, strrepbool:bool|Boolean=False):
      match typeName(expression):
         case "bool":
            return expression
         case "Boolean":
            return expression.value
         case "int" | "float" | "uint" | "Number":
            if expression == 0:
               return False
            else:
               return True
         case "NaN":
            return False
         case "str" | "String":
            match expression:
               case "false":
                  if strrepbool == True:
                     return False
                  else:
                     return True
               case "true":
                  return True
               case "":
                  return False
               case _:
                  return True
         case "null":
            return False
         case "undefined":
            return False
   def toString(self, formatLikePython:bool|Boolean=False):
      if formatLikePython == True:
         return f"{self.bool}"
      else:
         return f"{self.bool}".lower()
   def valueOf(self):
      if self.bool == True:
         return True
      else:
         return False
class Date:
   pass
class DefinitionError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
def decodeURI():
   pass
def decodeURIComponent():
   pass
def encodeURI():
   pass
def encodeURIComponent():
   pass
class Error():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
def escape():
   """
   Converts the parameter to a string and encodes it in a URL-encoded format, where most nonalphanumeric characters are replaced with % hexadecimal sequences. When used in a URL-encoded string, the percentage symbol (%) is used to introduce escape characters, and is not equivalent to the modulo operator (%). 
   The following characters are not converted to escape sequences by the escape() function.
   0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@-_.*+/
   """
   pass
class EvalError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
class int:
   __slots__ = ("value")
   MAX_VALUE = 2147483647
   MIN_VALUE = -2147483648
   def __init__(self, value):
      self.value = self._int(value)
   def __str__(self):
      return f'{self.value}'
   def __getitem__(self):
      return self.value
   def __setitem__(self, value):
      self.value = self._int(value)
   def __add__(self, value):
      return int(self.value + self._int(value))
   def __sub__(self, value):
      return int(self.value - self._int(value))
   def __mul__(self, value):
      return int(self.value * self._int(value))
   def __truediv__(self, value):
      if value == 0:
         if self.value == 0:
            return NaN()
         elif self.value > 0:
            return Infinity()
         elif self.value < 0:
            return NInfinity()
      else:
         try:
            return int(self.value / self._int(value))
         except:
            raise TypeError(f"Can not divide int by {type(value)}")
   def __float__(self):
      return float(self.value)
   def __int__(self):
      return self.value
   def _int(self, value):
      match typeName(value):
         case "NaN" | "Infinity" | "NInfinity":
            return value
         case "int":
            return value
         case "float" | "Number":
            return builtins.int(value)
         case "str" | "String":
            try:
               return builtins.int(value)
            except:
               raise TypeError(f"Can not convert string {value} to integer")
         case _:
            raise TypeError(f"Can not convert type {type(value)} to integer")
   def toExponential(self, fractionDigits:builtins.int|int):
      if fractionDigits < 0 or fractionDigits > 20:
         RangeError("fractionDigits is outside of acceptable range")
      else:
         tempString1 = f"{self.value}"
         exponent = len(tempString1) - 1
         if tempString1[0] == "-":
            exponent -= 1
            tempString2 = tempString1[:2]
            tempString1 = tempString1[2:]
         else:
            tempString2 = tempString1[:1]
            tempString1 = tempString1[1:]
         if fractionDigits > 0:
            tempString2 += "."
            for i in range(0,fractionDigits):
               try:
                  tempString2 += tempString1[i]
               except:
                  tempString2 += "0" #I am assuming this is what it does since it isn't supposed to throw another error
         if exponent > 0:
            tempString2 += f"e+{exponent}"
         return tempString2
   def toFixed(self, fractionDigits:builtins.int|int):
      if fractionDigits < 0 or fractionDigits > 20:
         RangeError("fractionDigits is outside of acceptable range")
      else:
         tempString = f"{self.value}"
         if fractionDigits == 0:
            return tempString
         else:
            tempString += "."
            i = 0
            while i < fractionDigits:
               tempString += "0"
               i += 1
            return tempString
   def toPrecision(self,precision:builtins.int|int|uint):
      if precision < 1 or precision > 21:
         RangeError("fractionDigits is outside of acceptable range")
      tempString = f"{self.value}"
      len_ = len(tempString)
      if precision < len_:
         return toExponential(precision-1)
      elif precision == len_:
         return tempString
      else:
         tempString += "."
         for i in range(0,precision-len_):
            tempString += "0"
         return tempString
   def toString(self, radix:builtins.int|int|uint=10):
      if radix > 36 or radix < 2:
         pass
      else:
         return base_repr(self.value, base=radix)
   def valueOf(self):
      return self.value
def isFinite(num):
   if num in (inf,NINF,NaN) or typeName(num) in ("NInfinity","Infinity","NaN"):
      return False
   else:
      return True
def isNaN(num):
   if num == nan or typeName(num) == "NaN":
      return True
   else:
      return False
def isXMLName(str_:str|String):
   #currently this is spec compatible with the actual xml specs but unknown if it is the same as the actionscript function.
   whitelist = "-_."
   if (len(str_) == 0) or (str_[0].isalpha() == False and str_[0] != "_") or (str_[:3].lower() == "xml") or (str_.find(" ") != -1):
      return False
   for i in str_:
      if i.isalnum() == True or i in whitelist:
         continue
      return False
   return True
class JSON:
   def parse():
      pass
   def stringify():
      pass
class Math:
   __slots__ = ()
   E = 2.71828182845905
   LN10 = 2.302585092994046
   LN2 = 0.6931471805599453
   LOG10E = 0.4342944819032518
   LOG2E = 1.442695040888963387
   PI = 3.141592653589793
   SQRT1_2 = 0.7071067811865476
   SQRT2 = 1.4142135623730951
   @staticmethod
   def abs(val):
      return abs(val)
   @staticmethod
   def acos(val):
      return m.acos(val)
   @staticmethod
   def asin(val):
      return m.asin(val)
   @staticmethod
   def atan(val):
      return m.atan(val)
   @staticmethod
   def atan2(y, x):
      return m.atan2(y,x)
   @staticmethod
   def ceil(val):
      return m.ceil(val)
   @staticmethod
   def cos(angleRadians):
      return m.cos(angleRadians)
   @staticmethod
   def exp(val):
      return m.exp(val)
   @staticmethod
   def floor(val):
      return m.floor(val)
   @staticmethod
   def log(val):
      return m.log(val)
   @staticmethod
   def max(*values):
      if len(values) == 1:
         return values[0]
      else:
         return max(values)
   @staticmethod
   def min(*values):
      if len(values) == 1:
         return values[0]
      else:
         return min(values)
   @staticmethod
   def pow(base, power):
      return m.pow(base,power)
   @staticmethod
   def random():
      return r.random()
   @staticmethod
   def round(val):
      return round(val)
   @staticmethod
   def sin(angleRadians):
     return m.sin(angleRadians)
   @staticmethod
   def sqrt(val):
      return m.sqrt(val)
   @staticmethod
   def tan(angleRadians):
      return m.tan(angleRadians)
class Namespace:
   def __init__():
      pass
   def toString():
      pass
   def valueOf():
      pass
class Number:
   __slots__ = ("number")
   MAX_VALUE = 1.79e308
   MIN_VALUE = 5e-324
   NaN = NaN()
   NEGATIVE_INFINITY = NInfinity()
   POSITIVE_INFINITY = Infinity()
   def __init__(self, num=None):
      self.number = self._Number(num)
   def __str__(self):
      if self.number in (NaN(),Infinity(),NInfinity()):
         return str(self.number)
      if self.number.is_integer() == True:
         return f'{builtins.int(self.number)}'
      return f'{self.number}'
   def __getitem__(self):
      return self.number
   def __setitem__(self, value):
      self.number = self._Number(value)
   def __add__(self, value):
      try:
         return Number(self.number + float(value))
      except ValueError:
         raise TypeError(f"can not add {type(value)} to Number")
   def __sub__(self, value):
      try:
         return Number(self.number - float(value))
      except ValueError:
         raise TypeError(f"can not subtract {type(value)} from Number")
   def __mul__(self, value):
      try:
         return Number(self.number * float(value))
      except ValueError:
         raise TypeError(f"can not multiply Number by {type(value)}")
   def __truediv__(self, value):
      if value == 0:
         if self.number == 0:
            return Number(NaN())
         elif self.number > 0:
            return Number(Infinity())
         elif self.number < 0:
            return Number(NInfinity())
      else:
         try:
            return Number(self.number / float(value))
         except:
            raise TypeError(f"Can not divide Number by {type(value)}")
   def __float__(self):
      return float(self.number)
   def __int__(self):
      return builtins.int(self.number)
   def _Number(self, expression):
      tpexp = type(expression)
      if expression == NInfinity():
         return NInfinity()
      elif expression == Infinity():
         return Infinity()
      elif expression in (None,NaN()):
         return NaN()
      elif tpexp in (builtins.int,int):
         return float(expression)
      elif tpexp in (float,Number):
         return expression
      elif expression == "undefined":
         return NaN()
      elif expression == "null":
         return 0.0
      elif expression == self.NaN:
         return self.NaN
      elif tpexp in (bool,Boolean):
         if expression == True:
            return 1.0
         else:
            return 0.0
      elif tpexp in (str,String):
         if expression == "":
            return 0.0
         else:
            try:
               return float(expression)
            except:
               return NaN()
   def toExponential(self):
      pass
   def toFixed(self):
      pass
   def toPrecision():
      pass
   def toString(self, radix=10):
      #!
      return str(self.number)
   def valueOf(self):
      return self.number
def parseFloat(str_:str|String):
   i = 0
   while str_[i].isspace():
      i += 1
   if str_[i].isdigit():
      j=0
      while str_[i+j].isdigit() or str_[i+j] == ".":
         j += 1
      return Number(str_[i:i+j])
   return NaN()
def parseInt(str_:str|String,radix:int|uint=0):
   l = len(str_)
   zero = False
   i = 0
   while i < l and str_[i].isspace():
      i += 1
   if len(str_[i:]) >= 2 and str_[i:i+2] == "0x":
      radix = 16
      i += 2
   elif radix < 2 or radix > 36:
      trace("parseInt",f"radix {radix} is outside of the acceptable range",isError=True)
      pass
   while i < l and str_[i] == "0":
      zero = True
      i += 1
   radixchars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:radix]
   str_ = str_.upper()
   j = 0
   while i+j < l and str_[i+j] in radixchars:
      j += 1
   if j == 0:
      if zero:
         return 0
      return NaN()
   return int(builtins.int(str_[i:i+j],radix))
class QName:
   def __init__():
      pass
   def toString():
      pass
   def valueOf():
      pass
class RangeError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
class ReferenceError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
class RegExp:
   pass
class SecurityError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
class String(str):
   def __init__(self, value=""):
      self.__hiddeninit(self._String(value))
   def __hiddeninit(self, value):
      super().__init__()
   def _getLength(self):
      return len(self)
   length = property(fget=_getLength)
   def _String(self, expression):
      match typeName(expression):
         case "str" | "String":
            return expression
         case "bool":
            if expression == True:
               return "true"
            elif expression == False:
               return "false"
         case "NaN":
            return "NaN"
         case "Array" | "Boolean" | "Number":
            return expression.toString()
         case _:
            return f"{expression}"
   def __getitem__(self, item):
      return String(super().__getitem__(item))
   def __add__(self, value):
      return String(f"{self}{self._String(value)}")
   def charAt(self, index:builtins.int|int=0):
      if index < 0 or index > len(self) - 1:
         return ""
      return self[index]
   def charCodeAt(self, index:builtins.int|int=0):
      if index < 0 or index > len(self) - 1:
         return NaN()
      return parseInt(r'{:04X}'.format(ord(self[index])),16)
   def concat(self, *args):
      tempString = String(self)
      for i in args:
         tempString += self._String(i)
      return tempString
   def fromCharCode():
      pass
   def indexOf(self, val, startIndex:builtins.int|int=0):
      return self.find(val, startIndex)
   def lastIndexOf(self, val, startIndex:builtins.int|int=None):
      ...
   def localeCompare():
      pass
   def match():
      pass
   def replace():
      pass
   def search():
      pass
   def slice(self,startIndex=0,endIndex=None):
      if endIndex == None:
         return self[startIndex:]
      if startIndex < 0:
         ...
      return self[startIndex:endIndex]
   def split():
      pass
   def substr(self, startIndex:builtins.int|int=0, len_:builtins.int|int=None):
      if len_ < 0:
         trace("Error")
      if startIndex < 0:
         startIndex = len(self) + startIndex
      if len_ == None:
         return self[startIndex:]
      return self[startIndex:startIndex+len_]
   def substring(self, startIndex:builtins.int|int=0, endIndex:builtins.int|int=None):
      if startIndex < 0:
         startIndex = 0
      if endIndex == None:
         endIndex = tempInt
      if endIndex < 0:
         endIndex = 0
      if startIndex > endIndex:
         return self[endIndex:startIndex]
      return self[startIndex:endIndex]
   def toLocaleLowerCase(self):
      return self.toLowerCase()
   def toLocaleUpperCase(self):
      return self.toUpperCase()
   def toLowerCase(self):
      return self.lower()
   def toUpperCase(self):
      return self.upper()
   def valueOf(self):
      return f"{self}"
class SyntaxError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
def trace(*args, isError=False):
   if configmodule.as3DebugEnable == True:
      if isError == True and configmodule.ErrorReportingEnable == 1:
         if configmodule.MaxWarningsReached == False:
            if configmodule.CurrentWarnings < configmodule.MaxWarnings or configmodule.MaxWarnings == 0:
               output = f"Error:{formatTypeToName(args[0])}; {args[1]}"
               configmodule.CurrentWarnings += 1 #!Make this last after restarting
            else:
               output = "Maximum number of errors has been reached. All further errors will be suppressed."
               configmodule.MaxWarningsReached = True #!Make this last after restarting
         else:
            pass
      else:
         output = ""
         for i in args:
            output += f"{i} "
         output = output[:-1]
      if configmodule.TraceOutputFileEnable == 1:
         if configmodule.TraceOutputFileName == configmodule.defaultTraceFilePath:
            if Path(configmodule.TraceOutputFileName).exists() == True:
               with open(configmodule.TraceOutputFileName, "a") as f:
                  f.write(output + "\n")
            else:
               with open(configmodule.TraceOutputFileName, "w") as f:
                  f.write(output + "\n" )
         else:
            if Path(configmodule.TraceOutputFileName).exists() == True:
               if Path(configmodule.TraceOutputFileName).is_file() == True:
                  with open(configmodule.TraceOutputFileName, "a") as f:
                     f.write(output + "\n")
            else:
               with open(configmodule.TraceOutputFileName, "w") as f:
                  f.write(output + "\n")
      else:
         print(output)
class TypeError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
class U29:
   def decodeU29int(type_, data):
      """
      Must have an input of the data type ("h" or "b" for hexidecimal or binary) and the data as a string.
      Binary data must be either 8, 16, 32, or 48 bits.
      The first bit if each byte, aside from the 4th, determines if there is another byte afterwards (1xxxxxxx means there is another). This leaves a maximum of 29 bits for actual data, hence u29int.
      The specs of u29int can be found at https://web.archive.org/web/20080723120955/http://download.macromedia.com/pub/labs/amf/amf3_spec_121207.pdf on page 3
      This function returns a list. Value 0 is the number it translates to, value 1 is the type of u29int value (1, 2, 3, or 4). The types basically mean how many bytes the u29int was (this is a part of the spec)
      """
      data = data.replace(" ", "")
      r = ""
      if type_ == "h":
         bindat = bin(builtins.int(data, 16))[2:].zfill(len(data) * 4)
      elif type_ == "b":
         bindat = data
      else:
         trace("U29Error; Wrong type",isError=True)
      if bindat[0] == "1":
         if bindat[8] == "1":
            if bindat[16] == "1":
               rtype = 4
               for i in range(0,32):
                  if i not in (0,8,16):
                     r += bindat[i]
               result = builtins.int(r,2)
            else:
               rtype = 3
               for i in range(0,24):
                  if i not in (0,8,16):
                     r += bindat[i]
               result = builtins.int(r,2)
         else:
            rtype = 2
            for i in range(0,16):
               if i not in (0,8):
                  r += bindat[i]
            result = builtins.int(r,2)
      else:
         rtype = 1
         for i in range(0,8):
            if i != 0:
               r += bindat[i]
         result = builtins.int(r,2)
      return [result, rtype]
   def decodeU29str(_type, data):
      """
      Must have an input of the data type ("h" or "b" for hexidecimal or binary) and the data as a string.
      A u29str value is an encoded string which is preceded by (a) u29str length byte(s).
      The u29str length byte(s) is, in all the cases I've seen, the length in bits of the string times 2 plus 1 (for some stupid reason).
      """
      dat = data.replace(" ", "")
      if _type == "h":
         bindat = bin(builtins.int(dat, 16))[2:].zfill(len(dat) * 4)
         x=0
      elif _type == "b":
         bindat = dat
      length1 = u29._decodeU29str(bindat)
      temp = u29.read_byte_destructive(bindat)
      bindat = temp[0]
      length = builtins.int((length1[0] - 1) / 2)
      result = ''
      for i in range(0, length):
         temp = u29.read_byte_destructive(bindat)
         bindat = temp[0]
         result += bytes.fromhex('%0*X' % ((len(temp[1]) + 3) // 4, builtins.int(temp[1], 2))).decode('utf-8')
      return result
   def read_byte_destructive(binary_data):
      temp = u29.remove_byte(binary_data)
      return temp[0], temp[1]
   def remove_byte(binary_data):
      temp1 = wrap(binary_data, 8)
      temp2 = temp1.pop(0)
      temp1 = ''.join(temp1)
      return temp1, temp2
   def _decodeU29str(binary_data):
      numlist = binary_data.replace(" ", "")
      numlist = numlist[:32]
      r = ""
      if numlist[0] == '1':
         if numlist[1] == '1':
            if numlist[2] == '1':
               if numlist[3] == '1':
                  for i in range(0,16):
                     #if i == 0 or i == 1 or i == 2 or i == 3 or i == 4 or i == 8 or i == 9 or i == 16 or i == 17 or i == 24 or i == 25:
                     if i in (0,1,2,3,4,8,9,16,17,24,25):
                        continue
                     else:
                        r += numlist[i]
                  number = builtins.int(r,2)
                  return [number,4]
               else:
                  for i in range(0,16):
                     #if i == 0 or i == 1 or i == 2 or i == 3 or i == 8 or i == 9 or i == 16 or i == 17:
                     if i in (0,1,2,3,8,9,16,17):
                        continue
                     else:
                        r += numlist[i]
                  number = builtins.int(r,2)
                  return [number,3]
            else:
               for i in range(0,16):
                  #if i == 0 or i == 1 or i == 2 or i == 8 or i == 9:
                  if i in (0,1,2,8,9):
                     continue
                  else:
                     r += numlist[i]
               number = builtins.int(r,2)
               return [number,2]
         else:
            raise Exception("Not U29 string/utf-8 value")
      else:
         for i in range(0,8):
            if i != 0:
               r += numlist[i]
         number = builtins.int(r,2)
         return [number,1]
class uint:
   pass
def unescape():
   pass
class URIError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
class Vector: #probably should have list as parent
   def __init__(self,type,sourceArray:list|tuple|Array|Vector):
      pass
   def _getFixed(self):
      return self._fixed
   def _setFixed(self,value:bool|Boolean):
      self._fixed = Boolean(value)
   fixed = property(fget=_getFixed,fset=_setFixed)
   def _getLength(self):
      pass
   def _setLength(self,value):
      pass
   length = property(fget=_getLength,fset=_setLength)
   def concat():
      pass
   def every():
      pass
   def filter():
      pass
   def forEach():
      pass
   def indexOf():
      pass
   def insertAt():
      pass
   def join():
      pass
   def lastIndexOf():
      pass
   def map():
      pass
   def pop():
      pass
   def push():
      pass
   def removeAt():
      pass
   def reverse():
      pass
   def shift():
      pass
   def slice():
      pass
   def some():
      pass
   def sort():
      pass
   def splice():
      pass
   def toLocaleString():
      pass
   def toString():
      pass
   def unshift():
      pass
class VerifyError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message

def EnableDebug():
   """
   Enables 'debug mode' for this module. This is a substitute for have an entire separate interpreter.
   If you want to automatically enable debug mode based on the commandline arguements of a file, do something like:
   if __name__ == "__main__":
      import sys.argv
      if "-debug" in sys.argv:
         <this module>.EnableDebug()
   """
   configmodule.as3DebugEnable = True
def DisableDebug():
   configmodule.as3DebugEnable = False
@deprecated("This is now built into the Array constructor")
def listtoarray(l:list|tuple):
   """
   A function to convert a python list to an Array.
   """
   return Array(*l)
def typeName(obj:object):
   return formatTypeToName(type(obj))
def formatTypeToName(arg:type):
   tempStr = f"{arg}"
   if tempStr.find(".") != -1:
      return tempStr.split(".")[-1].split("'")[0]
   else:
      return tempStr.split("'")[1]
def isEven(Num:builtins.int|float|int|Number|uint|NaN|Infinity|NInfinity):
   match typeName(Num):
      case "NaN" | "Infinity" | "NInfinity":
         return False
      case "int" | "uint":
         if Num % 2 == 0:
            return True
         else:
            return False
      case "float" | "Number":
         pass
def isOdd(Num:builtins.int|float|int|Number|uint|NaN|Infinity|NInfinity):
   match typeName(Num):
      case "NaN" | "Infinity" | "NInfinity":
         return False
      case "int" | "uint":
         if Num % 2 == 0:
            return False
         else:
            return True
      case "float" | "Number":
         pass
def _isValidDirectory(directory,separator=configmodule.separator):
   match configmodule.platform:
      case "Windows":
         blacklistedChars = '<>:"\\/|?*' #add ASCII characters from 0-31
         blacklistedNames = ("CON","PRN","AUX","NUL","COM0","COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8","COM9","COM¹","COM²","COM³","LPT0","LPT1","LPT2","LPT3","LPT4","LPT5","LPT6","LPT7","LPT8","LPT9","LPT¹","LPT²","LPT³")
         #convert path to uppercase since windows is not cas sensitive
         directory = directory.upper()
         #remove trailing path separator
         if directory[-1:] == separator:
            directory = directory[:-1]
         #remove drive letter or server path designator
         if directory[0].isalpha() and directory[1] == ":" and directory[2] == separator:
            directory = directory[3:]
         elif directory[:2] == "\\\\":
            directory = directory[2:]
         elif directory[:2] == f".{separator}":
            directory = directory[-(len(directory)-2):]
         #split path into each component
         dirlist = directory.split(separator)
         for i in dirlist:
            #invalid if blacklisted characters are used
            for j in i:
               if j in blacklistedChars:
                  return False
            #invalid if last character is " " or "."
            if i[-1:] in " .":
               return False
            #invalid if name is blacklisted and if name before a period is blacklisted
            if i.split(".")[0] in blacklistedNames:
               return False
         return True
      case "Linux" | "Darwin":
         blacklistedChars = "/<>|:&"
         #remove trailing path separator
         if directory[-1:] == separator:
            directory = directory[:-1]
         elif directory[-2:] == f"{separator}.":
            directory = directory[:-2]
         #remove starting path separator
         if directory[:1] == separator:
            directory = directory[-(len(directory)-1):]
         elif directory[:2] in (f".{separator}",f"~{separator}"):
            directory = directory[-(len(directory)-2):]
         dirlist = directory.split(separator)
         for i in dirlist:
            #invalid if blacklisted characters are used
            for j in i:
               if j in blacklistedChars:
                  return False
         return True
   return True
def _resolveDir(dir_):
   return str(Path(dir_).resolve())
def setDataDirectory(directory:str|String):
   if _isValidDirectory(_resolveDir(directory)) == True:
      configmodule.appdatadirectory = directory
   else:
      Error(f"setDataDirectory; Directory {directory} not valid")
