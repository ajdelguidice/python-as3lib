class _AS3_CONSTANTSOBJECT(type):
   '''
   Metaclass for objects defining as3 constants.
   Objects with this as a metaclass can:
      - be enumerated
   Objects with this as a metaclass can not:
      - have subclasses
      - have objects inside defined or modified after creation (python has a way around this but please don't)
      - be instantiated properly. You can instantiate these but they will not have any of the functions available to them. This is a weakness of metaclasses and the way python does things.
   '''
   def __new__(cls, name, bases, classdict):
      for b in bases:
         if isinstance(b, _AS3_CONSTANTSOBJECT):
            raise TypeError(f'type "{b.__name__}" is not an acceptable base type')
      return type.__new__(cls, name, bases, dict(classdict))

   def __setattr__(cls, name, value):
      raise Exception('Modifying enum values is not allowed.')

   def __delattr__(cls, name):
      raise Exception('Modifying enum values is not allowed.')

   def __iter__(cls):
      for name, attr in cls.__dict__.items():
         if not name.startswith('__') and not hasattr(attr, '__call__'):
            yield name

   def hasOwnProperty(cls, name):
      return not name.startswith('__') and name in cls.__dict__

   def isPrototypeOf(cls, name):
      raise NotImplementedError

   def propertyIsEnumerable(cls, name):
      return cls.hasOwnProperty(name)

   def setPropertyIsEnumerable(cls, name):
      raise NotImplementedError

   def toLocaleString(cls):
      return cls.toString()

   def toString(cls):
      return f'{cls.__name__}({", ".join(f"{k}={v}" for k,v in cls.__dict__.items() if not k.startswith('__'))})'

   def valueOf(cls):
      return cls
