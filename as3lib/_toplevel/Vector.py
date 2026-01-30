from as3lib._toplevel.Boolean import Boolean
from as3lib._toplevel.Constants import null, undefined
from as3lib._toplevel.Errors import RangeError, TypeError
from as3lib._toplevel.int import int, uint
from as3lib._toplevel.Keywords import each
from as3lib._toplevel.Number import Number
from as3lib._toplevel.Object import Object
from as3lib._toplevel.String import String
import builtins
from functools import partial
from io import StringIO


class Vector(list, Object):
   '''
   AS3 Vector datatype.

   This class is not really a vector as I haven't found a way to do that in
   python. It is instead just a type locked list.

   I have not found a way to create a syntax similar to Vector.<T> so you
   currently have to declare it like Vector(..., type=T). The way this is
   currently handled also does not allow you to use Vector.<T> as a type.
   '''
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
      for i in each(arr):
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

   def __init__(self, length=0, fixed=False, **kwargs):
      if isinstance(length, list):  # Function behaviour
         # TODO: Make sure this works properly
         if isinstance(length, Vector):
            self._fixed = length.fixed
            self._superclass = length._superclass
         self._type = kwargs['type']
         self._fixed = False
         self._superclass = True
         length = [Vector.coercePythonToAs3Object(i, self._type) for i in each(length)]
         Vector._checkTypeAll(length, self._type, self._superclass)
         super().__init__(length)
      else:  # Constructor behaviour
         self._type = kwargs['type']
         self._superclass = False
         self._fixed = fixed
         super().__init__((null for i in range(length)))

   def __iter__(self):
      return (i for i in range(len(self)))

   def __each__(self):
      return (self[i] for i in range(len(self)))

   def extend(self, iterable):
      if self.fixed:
         raise RangeError('Can not change vector length while fixed is set to true.')
      super().extend(each(iterable))

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
         for i in o:
            x = o[i]
            if x != None:
               out.write(str(x))
            if i + 1 < o.length:
               out.write(s)
         return out.getvalue()

   def __repr__(self):
      return 'as3lib.Vector.<%s>(%s)' % (self._type.__name__, self)

   def __getitem__(self, item):
      return super().__getitem__(item)

   def __setitem__(self, item, value):
      value = Vector.coercePythonToAs3Object(value, self._type)
      Vector._checkType(value, self._type, self._superclass)
      super().__setitem__(item, value)

   def concat(self, *args):
      temp = Vector(self, type=self._type)
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
      for i in self:
         if not callback(self[i], i, self):
            return False
      return True

   def filter(self, callback, thisObject=null):
      # TODO: Handle null callback
      tempVector = Vector(type=self._type)
      tempVector._superclass = self._superclass
      for i in self:
         if callback(self[i], i, self):
            tempVector.push(item)
      return tempVector

   def forEach(self, callback, thisObject=null):
      if callback is null:
         return undefined
      for i in self:
         callback(self[i], i, self)

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
         if element is null or isinstance(element, self._type):
            raise NotImplementedError
      else:
         raise NotImplementedError

   def join(self, sep: str = ','):
      return Vector._join(self, sep)

   def lastIndexOf(self, searchElement, fromIndex=None):
      if fromIndex is None:
         fromIndex = len(self)
      elif fromIndex < 0:
         fromIndex = len(self) - fromIndex
      raise NotImplementedError
      # index = self[::-1].indexOf(searchElement,len(self)-1-fromIndex)
      # return index if index == -1 else len(self)-1-index

   def map(self, callback, thisObject=null):
      # TODO: Handle null callback
      tempVect = Vector(self.length, type=self._type)
      tempVect._superclass = self._superclass
      for i in self:
         tempVect[i] = callback(self[i], i, self)
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
      for i in self:
         if callback(self[i], i, self):
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
      l = []
      for i in args:
         l.append(Vector.coercePythonToAs3Object(i, self._type))
         Vector._checkType(l[-1], self._type, self._superclass)
      tempVect = (*l, *each(self))
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
