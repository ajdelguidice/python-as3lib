# This file defines the actionscript keywords as python decorators/functions
from as3lib._toplevel.Boolean import Boolean, true
from as3lib._toplevel.Number import Number
from dataclasses import dataclass
from miniamf import register_package


@dataclass
class amfMetaData:
   # The variable names for this are defined by miniamf's __amf__ property
   static_attrs: list
   exclude_attrs: list
   readonly_attrs: list
   proxy_attrs: list
   amf3: bool
   dynamic: bool
   alias: bool  # TODO: Placeholder data type
   external: bool
   synonym_attrs: list


@dataclass
class as3PackageMetaData:
   namespace: str
   ...


class extends:
   def __init__(self, parent):
      self._p = parent

   def __call__(self, cls):
      cls.prototype = self._p
      return cls


class package:...


class implements:
   def __init__(self, *interfaces):
      self._i = interfaces

   def __call__(self, cls):
      cls._as3_implements = self._i


class namespace:
   # Currently only works on packages
   def __init__(self, ns):
      self.ns = ns

   def __call__(self, cls):
      register_package(cls, self.ns)
      return cls


# Operations
def stricteq(obj1, obj2):
   if isinstance(obj1, Number) and obj1._is_nan() and isinstance(obj2, Number) and obj2._is_nan():
      return true
   return Boolean(type(obj1) == type(obj2) and obj1 == obj2)


def strictne(obj1, obj2):
   return Boolean(type(obj1) != type(obj2) or obj1 != obj2)


# Other keywords
def delete(obj):
   # TODO: Other functionality of delete
   del obj
   return true


def each(iterable):
   '''
   Replacement for 'for each ...'

   Used like 'for i in each(<variable>):'
   '''
   if hasattr(iterable, '__each__'):
      return iterable.__each__()
   if hasattr(iterable, 'values') and callable(iterable.values):
      return iterable.values()
   # Do it a bit jank because python and actionscript differ in the way that
   # iterating is done.
   return (iterable[i] for i in range(len(iterable)))


# Helpers
def as3_enumerate(iterable):
   '''
   Python enumerate function for AS3 objects. AS3 objects use a custom
   implementation of __iter__ which breaks the builtin enumerate function.
   '''
   return ((i, iterable[i]) for i in iterable)
