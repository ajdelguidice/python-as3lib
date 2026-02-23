from . import as3state, config
from pathlib import Path
from subprocess import check_output
import os
import builtins
from functools import partial
from miniamf import add_type

'''
initerrors
0 - platform not implemented
1 - function not implemented for current platform
2 - (Linux specific) unexpected display server (expected x11 or wayland)
3 - dependency not found
4 - other error
'''


# Helper functions
def traceFilePath_Flash(sysverOverride: tuple = None):
   '''
   Outputs the defualt file path for trace as defined by https://web.archive.org/web/20180227100916/helpx.adobe.com/flash-player/kb/configure-debugger-version-flash-player.html
   Arguements:
      sysverOverride - A tuple containing the system and version of system you want to choose. ex: ('Windows','XP')
   '''
   if as3state.platform == 'Windows':
      username = os.getlogin()
   else:
      from pwd import getpwuid
      username = getpwuid(os.getuid())[0]
   if sysverOverride:
      if sysverOverride[0] == 'Linux':
         return f'/home/{username}/.macromedia/Flash_Player/Logs/flashlog.txt'
      if sysverOverride[0] == 'Darwin':
         return f'/Users/{username}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt'
      if sysverOverride[0] == 'Windows':
         if sysverOverride[1] in {'95', '98', 'ME', 'XP'}:
            return f'C:/Documents and Settings/{username}/Application Data/Macromedia/Flash Player/Logs/flashlog.txt'
         return f'C:/Users/{username}/AppData/Roaming/Macromedia/Flash Player/Logs/flashlog.txt'
   if as3state.platform == 'Linux':
      return f'/home/{username}/.macromedia/Flash_Player/Logs/flashlog.txt'
   if as3state.platform == 'Windows':
      return f'C:/Users/{username}/AppData/Roaming/Macromedia/Flash Player/Logs/flashlog.txt'
   if as3state.platform == 'Darwin':
      return f'/Users/{username}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt'


def sm_x11():
   '''
   Gets and returns screen width, screen height, refresh rate, and color depth on x11
   '''
   for option in check_output(('xrandr', '--current')).decode('utf-8').split('\n'):
      if '*' in option:
         for i in option.split(' '):
            if i != '' and '*' in i:
               rr = i.strip('*+')
               break
         break
   depth = check_output('xwininfo -root | grep Depth', shell=True).decode('utf-8').split(':')[1].strip(' \n')
   width = check_output('xwininfo -root | grep Width', shell=True).decode('utf-8').split(':')[1].strip(' \n')
   height = check_output('xwininfo -root | grep Height', shell=True).decode('utf-8').split(':')[1].strip(' \n')
   return int(width), int(height), float(rr), int(depth)


def sm_wayland():
   return sm_x11()  # Only works on XWayland


def sm_windows():
   import ctypes
   try:
      import win32api
   except ModuleNotFoundError:
      as3state.initerror.append((3, 'Windows: Requirement pywin32 either not installed or not accessible.'))
      return 1600, 900, 60.0, 16
   settings = win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1)
   return int(ctypes.windll.user32.GetSystemMetrics(0)), int(ctypes.windll.user32.GetSystemMetrics(1)), float(getattr(settings, 'DisplayFrequency')), int(getattr(settings, 'BitsPerPel'))


def sm_darwin():
   as3state.initerror.append((1, 'Darwin: Fetching screen properties is not implemented.'))
   return 1600, 900, 60.0, 16  # Placeholder


def setScreenProperties(func):
   try:
      temp = func()
   except:
      temp = (1600, 900, 60.0, 16)
   as3state.width, as3state.height, as3state.refreshrate, as3state.colordepth = temp


# Initialise as3lib
if as3state.startTime is None:
   from miniamf import util
   as3state.startTime = int(util.utcnow().timestamp() * 1000)
if not as3state.initdone:
   import platform
   as3state.platform = platform.system()
   as3state.separator = '\\' if as3state.platform == 'Windows' else '/'
   as3state.pythonversion = platform.python_version()
   as3state.librarydirectory = Path(__file__).resolve().parent
   as3state.userdirectory = Path.home()
   as3state.desktopdirectory = Path(os.environ.get('XDG_DESKTOP_DIR', as3state.userdirectory / 'Desktop'))
   as3state.documentsdirectory = Path(os.environ.get('XDG_DOCUMENTS_DIR', as3state.userdirectory / 'Documents'))
   as3state.defaultTraceFilePath_Flash = Path(traceFilePath_Flash())

   if as3state.platform == 'Linux':
      as3state.displayserver = os.environ.get('XDG_SESSION_TYPE', 'error')
      if as3state.displayserver == 'x11':
         setScreenProperties(sm_x11)
      elif as3state.displayserver == 'wayland':
         setScreenProperties(sm_wayland)
      else:
         as3state.initerror.append((2, f'Linux: Display server "{as3state.displayserver}" not supported.'))
   elif as3state.platform == 'Windows':
      setScreenProperties(sm_windows)
   elif as3state.platform == 'Darwin':
      as3state.initerror.append((4, 'Detected platform "Darwin" is untested and is missing a lot of features.'))
      setScreenProperties(sm_darwin)
   elif as3state.platform == '':
      as3state.initerror.append((4, 'Current platform could not be determined.'))
   else:
      as3state.initerror.append((0, f'Current platform {as3state.platform} not supported.'))

   # Ensure that at least something is loaded if values fail to load
   # This is a fix for the case where platform is not valid AND the display config values are missing
   if None in {as3state.width, as3state.height, as3state.refreshrate, as3state.colordepth}:
      setScreenProperties(None)

   # Load the config
   config.Load()
   if as3state.ClearLogsOnStartup and as3state.TraceOutputFileName.exists():
      with open(as3state.TraceOutputFileName, 'w') as f:
         f.write('')

   # Display errors to user
   if as3state.initerror:
      print(f'Warning: as3lib has initialised with errors, some functionality may be broken.\n{"".join(f"\t({i[0]}) {i[1]}\n" for i in as3state.initerror)}')

   # Set the default appdatadirectory
   import __main__
   if hasattr(__main__, '__file__'):
      as3state.appdatadirectory = Path(__main__.__file__).resolve().parent
   else:  # Fall back to working directory
      as3state.appdatadirectory = Path.cwd()

   # Tell others that library has been initialised
   as3state.initdone = True


# Export toplevel and set up miniamf adapters
from ._toplevel.Array import Array
from ._toplevel.Boolean import Boolean, false, true
from ._toplevel.Class import Class
from ._toplevel.Constants import undefined, null
from ._toplevel.Date import Date
from ._toplevel.Errors import ArgumentError, DefinitionError, Error, EvalError, RangeError, ReferenceError, SecurityError, SyntaxError, TypeError, URIError, VerifyError
from ._toplevel.Functions import decodeURI, decodeURIComponent, encodeURI, encodeURIComponent, escape, isFinite, isNaN, isXMLName, parseFloat, parseInt, unescape, isValidDirectory
from ._toplevel.int import int
Int = int  # Backwards compatibility
from ._toplevel.int import uint
from ._toplevel.JSON import JSON
from ._toplevel.Keywords import delete, each, stricteq, strictne
from ._toplevel.Math import Math
from ._toplevel.Number import Infinity, NaN, Number
from ._toplevel.Object import Object
from ._toplevel.RegExp import RegExp
from ._toplevel.String import String
from ._toplevel.trace import trace
from ._toplevel.XML import Namespace, QName, XML, XMLList
from ._toplevel.Vector import Vector


try:
   from miniamf.amf3 import IntVector, UintVector, DoubleVector, ObjectVector
   # TODO: Add adapter for Date, Object, XML stuff
   def adapter(func, obj, encoder):
      return func(obj)

   def arrayAdapter(obj, encoder):
      return list(each(obj))

   def vectorAdapter(obj, encoder):
      if obj._type is int:
         out = IntVector(each(obj))
      elif obj._type is uint:
         out = UintVector(each(obj))
      elif obj._type is Number:
         out = DoubleVector(each(obj))
      else:
         out = ObjectVector(each(obj))
         # TODO
         # out.classname =
      out.fixed = obj.fixed
      return out

   add_type(Array, arrayAdapter)
   add_type(Boolean, partial(adapter, bool))
   add_type(int, partial(adapter, builtins.int))
   add_type(Number, partial(adapter, float))
   add_type(String, partial(adapter, str))
   add_type(uint, partial(adapter, int))
   add_type(Vector, vectorAdapter)
except Exception as e:
   raise Error('Failed to set up miniamf type adapters.') from e


# Create NativeApplication Instance
from as3lib.flash.desktop import NativeApplication
as3state.nativeApplication = NativeApplication()


# Legacy type annotations. These will be removed in a future version because
# python types are so different to as3 ones that these are often misleading.
from typing import Union
from types import NoneType

allNumber = Union[builtins.int, float, int, uint, Number]
allInt = Union[builtins.int, int, uint]
allString = Union[str, String]
allArray = Union[list, tuple, Array, Vector]
allBoolean = Union[bool, Boolean]
allNone = Union[undefined, null, NoneType]


# Library state setting functions
def EnableDebug():
   as3state.as3DebugEnable = True


def DisableDebug():
   as3state.as3DebugEnable = False


def setDataDirectory(dir_: str):
   dir_ = Path(dir_)
   if not isValidDirectory(dir_):
      raise Error(f'setDataDirectory; Directory "{dir_}" not valid')
   as3state.appdatadirectory = dir_


__all__ = (
   'true',
   'false',
   'Infinity',
   'NaN',
   'undefined',
   'null',

   'delete',
   'each',

   'stricteq',
   'strictne',

   'ArgumentError',
   'Array',
   'Boolean',
   'Class',
   'Date',
   'DefinitionError',
   'decodeURI',
   'decodeURIComponent',
   'encodeURI',
   'encodeURIComponent',
   'Error',
   'escape',
   'EvalError',
   'int',
   'isFinite',
   'isNaN',
   'isXMLName',
   'JSON',
   'Math',
   'Namespace',
   'Number',
   'Object',
   'parseFloat',
   'parseInt',
   'QName',
   'RangeError',
   'ReferenceError',
   'RegExp',
   'SecurityError',
   'String',
   'SyntaxError',
   'trace',
   'TypeError',
   'uint',
   'unescape',
   'URIError',
   'XML',
   'XMLList',
   'Vector',
   'VerifyError',
   'EnableDebug',
   'DisableDebug',
   'isValidDirectory',
   'setDataDirectory'
)
