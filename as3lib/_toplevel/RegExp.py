from __future__ import annotations
from as3lib._toplevel.Array import Array
from as3lib._toplevel.Boolean import Boolean
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

   def __init__(self, re=undefined, flags=undefined):
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

   def _doRE(self, str):
      # Implementation of exec and test. They both seem to do the same thing
      # behind the scenes.
      # TODO: output.index
      # TODO: global flag
      match = self._re.match(str)
      if match is None:
         return null
      output = Array()
      output.input = str
      group = match.group()
      if group is not None:
         output.push(group)
      else:
         output.push(undefined)
      output.index = match.start()
      groups = match.groups()
      if groups is not None:
         output.push(*groups)
      if not len(output):
         return null
      if self.global_:
         raise NotImplementedError
      return output

   def exec(self, str):
      return self._doRE(str)

   def test(self, str):
      if self._doRE(str) is null:
         return Boolean(False)
      return Boolean(True)

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
