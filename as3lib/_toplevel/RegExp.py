from __future__ import annotations
from as3lib._toplevel.Boolean import false, true
from as3lib._toplevel.Constants import null, undefined
from as3lib._toplevel.Errors import TypeError
from as3lib._toplevel.Object import Object
from as3lib._toplevel.String import String
from io import StringIO
import re as regex


class RegExp(Object):
   '''
   Because global is a keyword in python, the global property has been renamed
   to global_
   '''
   @property
   def dotall(self):
      return self._dotall

   @property
   def extended(self):
      return self._extended

   @property
   def global_(self):
      return self._global

   @property
   def ignoreCase(self):
      return self._ignoreCase

   @property
   def lastIndex(self):
      return self._lastIndex

   @lastIndex.setter
   def lastIndex(self, value):
      self._lastIndex = value

   @property
   def multiline(self):
      return self._multiline

   @property
   def source(self):
      return self._source

   def __init__(self, re=undefined, flags=undefined, *args):
      if re is undefined:
         re = ''
      if re is null:
         re = 'null'
      self._lastIndex = 0
      if isinstance(re, RegExp):
         if flags is not undefined:
            raise TypeError('Cannot supply flags when constructing one RegExp from another', 1100)
         # TODO: Make sure this is correct
         self._source = re.source

         self._dotall = re.dotall
         self._extended = re.extended
         self._global = re.global_
         self._ignoreCase = re.ignoreCase
         # TODO: Find out what is done with this
         # self._lastIndex = re.lastIndex

         self._multiline = re.multiline
      else:
         if flags is undefined or flags is null:
            flags = ''
         self._source = String(re)
         self._dotall = 's' in flags
         self._extended = 'x' in flags
         self._global = 'g' in flags
         self._ignoreCase = 'i' in flags
         self._multiline = 'm' in flags

      flags = 0
      if self.ignoreCase:
         flags |= regex.IGNORECASE
      if self.multiline:
         flags |= regex.MULTILINE
      if self.dotall:
         flags |= regex.DOTALL
      if self.extended:
         flags |= regex.VERBOSE
      self._re = regex.compile(self.source, flags)

   def exec(self, str):
      # TODO: output.index
      # TODO: global flag
      matches = list(self._re.finditer(str))
      if not matches:
         return null
      match = matches[0]
      output = Object()
      for k, v in match.groupdict().items():
         if v is None or v == '':
            v = undefined
         setattr(output, k, v)
      output.input = str
      group = match.group()
      if group is None:
         output[0] = undefined
      else:
         output[0] = group
      output.index = match.start()
      groups = match.groups()
      if groups is not None:
         i = 1
         for item in groups:
            output[i] = item
            i += 1
      if self.global_:
         raise NotImplementedError
      return output

   def test(self, str):
      if self.exec(str) is null:
         return false
      return true

   def toString(self):
      with StringIO() as s:
         s.write('/%s/' % self.source)
         if self.global_:
            s.write('g')
         if self.ignoreCase:
            s.write('i')
         if self.multiline:
            s.write('m')
         if self.dotall:
            s.write('s')
         if self.extended:
            s.write('x')
         return s.getvalue()
