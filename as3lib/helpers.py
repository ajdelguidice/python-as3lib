# This module inlcudes many things that might be useful when using this
# library but aren't in actionscript. EX: a helper for increasing python's
# maximum recursion depth.
from io import StringIO
from pathlib import PurePath
import platform, sys
from . import as3state


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
        cls = instance.__class__ if instance is not None else self
        self.fset(cls, value)
#-----------------------------------------------------------------------------


class staticproperty_writeOnly:
    def __init__(self, fset):
        self.fset = fset

    def __get__(self, instance, owner):
        raise AttributeError("can't get attribute")

    def __set__(self, instance, value):
        cls = instance.__class__ if instance is not None else self
        self.fset(cls, value)


class function:
    '''
    Internal workaround for specific functions to make them behave correctly

    This is only temporary and will either be removed or completely reworked
    once prototypes are properly implemented.
    '''
    def __init__(self, func, instance=None, owner=None):
        self.func = func
        self.instance = instance
        self.owner = owner

    def __get__(self, instance, owner=None):
        return type(self)(self.func, instance, owner)

    def __call__(self, *args, **kwargs):
        if self.owner is None:
            raise NotImplementedError('function defined outside of a class')
        if self.instance is None:
            # Part of a class
            return self.func(self.owner, *args, **kwargs)
        return self.func(self.instance, *args, **kwargs)


def isChildClass(obj, cls):
    '''
    Checks both isinstance and issubclass for (obj,cls)
    '''
    return isinstance(obj, cls) or issubclass(obj, cls)


def TraceFilePath_Flash(sysverOverride: tuple = None):
    '''
    These paths are defined by https://web.archive.org/web/20180227100916/helpx.adobe.com/flash-player/kb/configure-debugger-version-flash-player.html
    Arguements:
        sysverOverride - A tuple containing the system and version of system you want to choose. ex: ('Windows','XP')
    '''
    user = as3state._user
    if sysverOverride:
        if sysverOverride[0] == 'Linux':
            return f'/home/{user}/.macromedia/Flash_Player/Logs/flashlog.txt'
        if sysverOverride[0] == 'Darwin':
            return f'/Users/{user}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt'
        if sysverOverride[0] == 'Windows':
            if sysverOverride[1] in {'95', '98', 'ME', 'XP'}:
                return f'C:/Documents and Settings/{user}/Application Data/Macromedia/Flash Player/Logs/flashlog.txt'
            return f'C:/Users/{user}/AppData/Roaming/Macromedia/Flash Player/Logs/flashlog.txt'
    if as3state.platform == 'Linux':
        return f'/home/{user}/.macromedia/Flash_Player/Logs/flashlog.txt'
    if as3state.platform == 'Windows':
        return f'C:/Users/{user}/AppData/Roaming/Macromedia/Flash Player/Logs/flashlog.txt'
    if as3state.platform == 'Darwin':
        return f'/Users/{user}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt'


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
