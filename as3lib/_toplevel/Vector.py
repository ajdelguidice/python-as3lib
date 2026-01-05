from as3lib._toplevel.Boolean import Boolean
from as3lib._toplevel.Constants import null, undefined
from as3lib._toplevel.Errors import RangeError, TypeError
from as3lib._toplevel.int import int, uint
from as3lib._toplevel.Number import Number
from as3lib._toplevel.Object import Object
from as3lib._toplevel.String import String
import builtins
from functools import partial
from multipledispatch import dispatch
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
               out.add(str(x))
            if i + 1 < n:
               out.add(s)
         return out.getvalue()

   def __repr__(self):
      return 'as3lib.Vector.<%s>(%s)' % (self._type.__name__, self)

   def __getitem__(self, item):
      if isinstance(item, slice):...
      else:
         return super().__getitem__(item)

   def __setitem__(self, item, value):
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

Vector.Boolean = partial(Vector, type=Boolean)
Vector.int = partial(Vector, type=int)
Vector.Number = partial(Vector, type=Number)
Vector.uint = partial(Vector, type=uint)
Vector.String = partial(Vector, type=String)
