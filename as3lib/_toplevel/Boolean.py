import builtins
from as3lib._toplevel.int import *
from as3lib._toplevel.Constants import *
from as3lib._toplevel.Object import *
from as3lib._toplevel.trace import *
from as3lib._toplevel.Number import *

class Boolean(Object):
   """
   Lets you create boolean object similar to ActionScript3
   Since python has to be different, values are "True" and "False" instead of "true" and "false"
   """
   __slots__ = ("_value")
   def __init__(self, expression=False):
      self._value = self._Boolean(expression)
   def __str__(self):
      return str(self._value).lower()
   def __repr__(self):
      return f'as3lib.Boolean({self._value})'
   def __getitem__(self):
      return self._value
   def __setitem__(self, value):
      self._value = value
   def _Boolean(self, expression=None):
      if isinstance(expression,bool):
         return expression
      if isinstance(expression,Boolean):
         return expression._value
      if isinstance(expression,(builtins.int,float,uint,int,Number)):
         return False if expression == 0 else True
      if isinstance(expression,(NaN,null,undefined,None)):
         return False
      if isinstance(expression,str):
         if expression == "":
            return False
         return True
   def toString(self):
      return str(self._value).lower()
   def valueOf(self):
      return self._value
