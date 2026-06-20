# This module inlcudes many things that might be useful when using this
# library but aren't in actionscript. EX: a helper for increasing python's
# maximum recursion depth.
from io import StringIO
from pathlib import PurePath
import platform, sys


class recursionDepth:
    # used like "with recursionDepth(Number):"
    def __init__(self, limit):
        self.limit = limit

    def __enter__(self):
        self.olimit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.limit)

    def __exit__(self, *args):
        sys.setrecursionlimit(self.olimit)

    @staticmethod
    def set(limit):
        sys.setrecursionlimit(limit)

    @staticmethod
    def get():
        return sys.getrecursionlimit()


class textObject(StringIO):
    def __iadd__(self, string: str):
        self.write(string)
        return self

    def __eq__(self, value):
        return self.getvalue() == value

    def clear(self):
        self.seek(0)
        self.truncate(0)

    def get(self):
        return self.getvalue()


#-----------------------------------------------------------------------------
# https://www.py4u.org/blog/python-static-class-property-set-get/
class staticproperty:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, instance, owner):
        return self.fget(owner)

    def setter(self, fset):
        self.fset = fset
        return self

    def __set__(self, instance, value):
        if not hasattr(self, 'fset'):
            raise AttributeError("can't set attribute")
        cls = instance.__class__ if instance is not None else self.__objclass__
        self.fset(cls, value)
#-----------------------------------------------------------------------------


def isChildClass(obj, cls):
    '''
    Checks both isinstance and issubclass for (obj,cls)
    '''
    return isinstance(obj, cls) or issubclass(obj, cls)


if platform.system() == 'Windows':
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
