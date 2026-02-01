from warnings import warn


# TODO: Make item assignment work with non-string values.
# TODO: Prototypes
class Object:
   # ActionScript3 Base object
   prototype = None

   def __init__(self):...

   def __str__(self):
      return self.toString()

   def __getitem__(self, item):
      return getattr(self, str(item))

   def __setitem__(self, item, value):
      setattr(self, str(item), value)

   def hasOwnProperty(self, name: str):
      raise NotImplementedError

   def isPrototypeOf(self, theClass):
      warn('isPrototypeOf will not work properly because the prototype property is not implemented.')
      # This should work properly once prototype is implemented properly
      p = theClass.prototype
      while p is not None:
         if p is self.__class__:
            return True
         p = p.prototype
      return False

   def propertyIsEnumerable(self, name: str):
      raise NotImplementedError

   def setPropertyIsEnumerable(self, name: str, isEnum=True):
      raise NotImplementedError

   def toLocaleString(self):
      return '[object %s]' % type(self).__name__

   def toString(self):
      return '[object %s]' % type(self).__name__

   def valueOf(self):
      return self
