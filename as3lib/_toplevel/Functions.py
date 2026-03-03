from as3lib import as3state
from as3lib._toplevel import int, uint, Number
import builtins
from pathlib import Path, PurePath


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
