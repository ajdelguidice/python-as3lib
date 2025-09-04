import builtins
from as3lib._toplevel.Object import *
from as3lib._toplevel.Constants import *
from as3lib._toplevel.int import *
from as3lib._toplevel.Functions import parseInt

class String(str, Object):
   def __init__(self, value=""):
      self.__hiddeninit(self._String(value))
   def __hiddeninit(self, value):
      super().__init__()
   def _getLength(self):
      return len(self)
   length = property(fget=_getLength)
   def _String(self, expression):
      if isinstance(expression,str):
         return expression
      if isinstance(expression,bool):
         if expression == True:
            return "true"
         return "false"
      if isinstance(expression,NaN):
         return "NaN"
      if hasattr(expression, 'toString'):
         return expression.toString()
      return f"{expression}"
   def __repr__(self):
      return f'as3lib.String({self})'
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
      return self + ''.join([self._String(i) for i in args])
   def fromCharCode():...
   def indexOf(self, val, startIndex:builtins.int|int=0):
      return self.find(val, startIndex)
   def lastIndexOf(self, val, startIndex:builtins.int|int=None):...
   def localeCompare():...
   def match():...
   def replace():...
   def search():...
   def slice(self,startIndex=0,endIndex=None):
      if endIndex == None:
         return self[startIndex:]
      if startIndex < 0:...
      return self[startIndex:endIndex]
   def split(delimiter = None, limit = 0x7fffffff):
      if isinstance(delimiter,(undefined,NoneType)):
         arr = Array(self)
      elif delimiter == "" or False: #an empty string, an empty regular expression, or a regular expression that can match an empty string
         arr = Array(sourceArray=[i for i in self])
      elif False:... #If the delimiter parameter is a regular expression, only the first match at a given position of the string is considered, even if backtracking could find a nonempty substring match at that position.
      elif False:... #If the delimiter parameter is a regular expression containing grouping parentheses, then each time the delimiter is matched, the results (including any undefined results) of the grouping parentheses are spliced into the output array.
      if limit != 0x7fffffff:
         return arr[:limit]
      return arr
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
