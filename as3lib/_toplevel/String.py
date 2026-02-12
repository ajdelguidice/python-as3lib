from as3lib._toplevel.Array import Array
from as3lib._toplevel.Constants import null, undefined
from as3lib._toplevel.int import int
from as3lib._toplevel.Number import Number
from as3lib._toplevel.Object import Object
import builtins


class String(str, Object):
   def __init__(self, value=''):
      self.__init2(self._String(value))

   def __init2(self, value):
      # Workaround for super().__init__() eating arguements
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
      return str(expression)

   def __repr__(self):
      return 'as3lib.String(%s)' % self

   def __getitem__(self, item):
      return String(super().__getitem__(item))

   def __add__(self, value):
      return String('%s%s' % (self, self._String(value)))

   def __bool__(self):
      return self.length > 0

   def __neg__(self):
      # TODO: Make sure that this is correct
      return -Number(self)

   def __pos__(self):
      # TODO: Make sure that this is correct
      return Number(self)

   def charAt(self, index: builtins.int | int = 0):
      if index < 0 or index > len(self) - 1:
         return ''
      return self[index]

   def charCodeAt(self, index: builtins.int | int = 0):
      if index < 0 or index > len(self) - 1:
         return Number.NaN
      return Number(builtins.int(r'{:04X}'.format(ord(self[index])), 16))

   def concat(self, *args):
      return self + ''.join([self._String(i) for i in args])

   @staticmethod
   def fromCharCode(*charCodes):
      raise NotImplementedError

   def indexOf(self, val, startIndex: builtins.int | int = 0):
      return self.find(String(val), startIndex)

   def lastIndexOf(self, val, startIndex: builtins.int | int = 0x7fffffff):
      return self.rfind(String(val), startIndex)

   def localeCompare(self, other, *values):
      raise NotImplementedError

   def match(self, pattern):
      raise NotImplementedError

   def replace(self, pattern, repl):
      raise NotImplementedError

   def search(self, pattern = undefined):
      if pattern is undefined or pattern is null:
         return -1
      raise NotImplementedError

   def slice(self, startIndex=0, endIndex=null):
      si, ei = Number(startIndex), Number(endIndex)
      if si == Number.POSITIVE_INFINITY or ei == Number.NEGATIVE_INFINITY:
         return String('')
      si = int(si)
      if endIndex is null or ei == Number.POSITIVE_INFINITY:
         return self[si:]
      ei = int(ei)
      return self[si:ei]

   def split(self, delimiter=null, limit=0x7fffffff):
      if delimiter is undefined or delimiter is null:
         return Array(self)
      elif delimiter == '' or False:
         # An empty string, an empty regular expression, or a regular
         # expression that can match an empty string
         return Array(*[i for i in self])
      elif False:
         # If the delimiter parameter is a regular expression, only the first
         # match at a given position of the string is considered, even if
         # backtracking could find a nonempty substring match at that
         # position.
         ...
      elif False:
         # If the delimiter parameter is a regular expression containing
         # grouping parentheses, then each time the delimiter is matched, the
         # results (including any undefined results) of the grouping
         # parentheses are spliced into the output array.
         ...
      else:
         return Array(*super().split(delimiter, limit))

   def substr(self, startIndex: Number = 0, len: Number = null):
      startIndex = Number(startIndex)
      if len is null:
         return self[startIndex:]
      else:
         len = Number(len)
      if len == Number.NEGATIVE_INFINITY:
         return String('')
      if len < 0:
         len += self.length
      return self[startIndex:startIndex+len]

   def substring(self, startIndex: Number = 0, endIndex: Number = null):
      startIndex = Number(startIndex)
      if startIndex < 0:
         startIndex = 0
      endIndex = self.length if endIndex is null else Number(endIndex)
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
      return '%s' % self
