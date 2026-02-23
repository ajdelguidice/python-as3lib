from as3lib import as3state
from as3lib._toplevel.Constants import null, undefined
from as3lib._toplevel.Errors import Error
from as3lib._toplevel.int import int, uint
from as3lib._toplevel.Number import _parseFloat, Number
from as3lib._toplevel.String import String
import builtins
from pathlib import Path, PurePath


def decodeURI(uri):
   raise NotImplementedError


def decodeURIComponent(uri):
   raise NotImplementedError


def encodeURI(uri):
   raise NotImplementedError


def encodeURIComponent(uri):
   raise NotImplementedError


def escape(str):
   '''
   Converts the parameter to a string and encodes it in a URL-encoded format, where most nonalphanumeric characters are replaced with % hexadecimal sequences. When used in a URL-encoded string, the percentage symbol (%) is used to introduce escape characters, and is not equivalent to the modulo operator (%).
   The following characters are not converted to escape sequences by the escape() function.
   0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@-_.*+/
   '''
   raise NotImplementedError


def isFinite(num):
   num = Number(num)
   return not (num._is_nan() or num == Number.POSITIVE_INFINITY or num == Number.NEGATIVE_INFINITY)


def isNaN(num):
   return Number(num)._is_nan()


def isXMLName(str: String):
   # currently this is spec compatible with the actual xml specs but unknown if it is the same as the actionscript function.
   str = String(str)
   whitelist = {'-', '_', '.'}
   if not str.length or not str[0].isalpha() and str[0] != '_' or str.lower().startswith('xml') or ' ' in str:
      return False
   for i in str:
      if not i.isalnum() and i not in whitelist:
         return False
   return True


def parseFloat(str: String = undefined):
   return _parseFloat(undefined if str is undefined else String(str))


def parseInt(str: String = undefined, radix: uint = 0):
   # TODO: Find a better way of doing the sign detection
   radix = uint(radix)
   if radix == 0:
      radix = 10
   if radix < 2 or radix > 36:
      return Number.NaN
   if str is undefined:
      if radix >= 32:
         return Number(builtins.int('undefined', radix))
      return Number.NaN
   str = String(str)
   str = str.lstrip()
   zero = False
   minus = 0
   j1 = 0
   while j1 < len(str) and str[j1] in '-+':
      if str[j1] == '-':
         minus += 1
      j1 += 1
   str = str[j1:]
   if len(str) >= 2 and str.startswith('0x'):
      radix = 16
      str = str[2:]
   if str.startswith('0'):
      zero = True
      str.lstrip("0")
   radixchars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:radix]
   str = str.upper()
   j = 0
   while j < len(str) and str[j] in radixchars:
      j += 1
   if j == 0:
      return Number(0) if zero else Number.NaN
   return Number(builtins.int(str[:j], radix) * (-1 if minus % 2 else 1))


def unescape(str):
   raise NotImplementedError


def isEven(num: builtins.int | float | int | Number | uint):
   num = Number(num)
   if not isFinite(num):
      return False
   if num.valueOf().is_integer():
      return num % 2 == 0
   ...


def isOdd(num: builtins.int | float | int | Number | uint):
   num = Number(num)
   if not isFinite(num):
      return False
   if num.valueOf().is_integer():
      return num % 2 != 0
   ...


def objIsChildClass(obj, cls):
   '''
   Checks both isinstance and issubclass for (obj,cls)
   '''
   return isinstance(obj, cls) or issubclass(obj, cls)


if as3state.platform == 'Windows':
   BlacklistedChars = {'<', '>', ':', '"', '\\', '/', '|', '?', '*', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''}
   BlacklistedNames = {'CON', 'PRN', 'AUX', 'NUL', 'COM0', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM¹', 'COM²', 'COM³', 'LPT0', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9', 'LPT¹', 'LPT²', 'LPT³'}

   def isValidDirectory(directory, separator=None):
      '''
      Checks if a given directory is valid on the current platform
      '''
      if isinstance(directory, PurePath):
         # While this is ten times slower than using a string, it is much simpler and more robust so should give less incorrect answers
         temp = directory.resolve()
         while True:
            # get directory name and convert it to uppercase since windows is not case sensitive
            tempname = temp.name.upper()
            # invalid if blacklisted characters are used
            for i in tempname:
               if i in BlacklistedChars:
                  return False
            # invalid if last character is " " or "." or if name or name before a period is blacklisted
            if tempname.endswith((' ', '.')) or tempname.split('.')[0] in BlacklistedNames:
               return False
            temp = temp.parent
            if temp == temp.parent:
               break
         # Check drive letter
         if not (str(temp)[0].isalpha() and str(temp)[1:] in {':', ':\\', ':/'}):
            return False
      elif separator is not None:
         directory = str(directory)
         # convert path to uppercase since windows is not cas sensitive
         directory = directory.upper()
         # remove trailing path separator
         if directory[-1] == separator:
            directory = directory[:-1]
         # remove drive letter or server path designator
         if directory[0].isalpha() and directory[1] == ':' and directory[2] == separator:
            directory = directory[3:]
         elif directory.startswith('\\\\'):
            directory = directory[2:]
         elif directory.startswith(f'.{separator}'):
            directory = directory[-(len(directory)-2):]
         for i in directory.split(separator):
            # invalid if blacklisted characters are used
            for j in i:
               if j in BlacklistedChars:
                  return False
            # invalid if last character is " " or "." or if name or name before a period is blacklisted
            if i.endswith((' ', '.')) or i.split('.')[0] in BlacklistedNames:
               return False
      return True
else:
   BlacklistedChars = {'/', '<', '>', '|', ':', '&', ''}
   BlacklistedNames = {'.', '..'}

   def isValidDirectory(directory, separator=None):
      '''
      Checks if a given directory is valid on the current platform
      '''
      if isinstance(directory, PurePath):
         # While this is ten times slower than using a string, it is much simpler and more robust so should give less incorrect answers
         temp = directory.resolve()
         while True:
            tempname = temp.name
            # invalid if blacklisted names are used
            if tempname in BlacklistedNames:
               return False
            # invalid if blacklisted characters are used
            for i in tempname:
               if i in BlacklistedChars:
                  return False
            temp = temp.parent
            if temp == temp.parent:
               break
      elif separator is not None:
         directory = str(directory)
         # remove trailing path separator
         if directory[-1] == separator:
            directory = directory[:-1]
         elif directory.endswith(f'{separator}.'):
            directory = directory[:-2]
         # remove starting path separator
         if directory[0] == separator:
            directory = directory[-(len(directory)-1):]
         elif directory.startswith((f'.{separator}', f'~{separator}')):
            directory = directory[-(len(directory)-2):]
         for i in directory.split(separator):
            # invalid if blacklisted names are used
            if i in BlacklistedNames:
               return False
            # invalid if blacklisted characters are used
            for j in i:
               if j in BlacklistedChars:
                  return False
      return True
