from . import as3state, config
from ._toplevel.trace import trace
from .helpers import isValidDirectory
import builtins, os
from functools import partial
from miniamf import add_type
from miniamf.amf3 import IntVector, UintVector, DoubleVector, ObjectVector
from pathlib import Path
from subprocess import check_output


# Helper functions
def traceFilePath_Flash(sysverOverride: tuple = None):
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


# Initialise as3lib
if as3state.startTime is None:
   from miniamf import util
   as3state.startTime = int(util.utcnow().timestamp() * 1000)
if not as3state.initdone:
   import platform
   as3state.platform = platform.system()
   if as3state.platform == 'Windows':
      as3state._user = os.getlogin()
   else:
      from pwd import getpwuid
      as3state._user = getpwuid(os.getuid())[0]
   as3state.separator = '\\' if as3state.platform == 'Windows' else '/'
   as3state.pythonversion = platform.python_version()
   as3state.librarydirectory = Path(__file__).resolve().parent
   as3state.userdirectory = Path.home()
   as3state.desktopdirectory = Path(os.environ.get('XDG_DESKTOP_DIR', as3state.userdirectory / 'Desktop'))
   as3state.documentsdirectory = Path(os.environ.get('XDG_DOCUMENTS_DIR', as3state.userdirectory / 'Documents'))
   as3state.defaultTraceFilePath_Flash = Path(traceFilePath_Flash())

   if as3state.platform == 'Linux':
      as3state.displayserver = os.environ.get('XDG_SESSION_TYPE', 'error')
      if as3state.displayserver not in {'x11', 'wayland'}:
         as3state.initerror.append(f'Platform/Linux: Session type "{as3state.displayserver}" not supported.')
   elif as3state.platform == 'Windows':...
   elif as3state.platform == 'Darwin':
      as3state.initerror.append('Platform/Darwin: This library is untested on the current platform and is missing some features.')
   elif as3state.platform == '':
      as3state.initerror.append('Could not determine current platform.')
   else:
      as3state.initerror.append(f'Platform/{as3state.platform}: Not supported')

   # Load the config
   config.Load()
   if as3state.ClearLogsOnStartup and as3state.TraceOutputFileName.exists():
      with open(as3state.TraceOutputFileName, 'w') as f:
         f.write('')

   # Display errors to user
   if as3state.initerror:
      # NOTE: Use % because f-string expression parts can not contain a backslash on Python 3.10
      trace('Warning: as3lib has initialised with errors, some functionality may be broken.\n\t%s' % "\n\t".join(as3state.initerror))

   # Set the default appdatadirectory
   import __main__
   if hasattr(__main__, '__file__'):
      as3state.appdatadirectory = Path(__main__.__file__).resolve().parent
   else:  # Fall back to working directory
      as3state.appdatadirectory = Path.cwd()

   # Tell others that library has been initialised
   as3state.initdone = True


# Export toplevel and set up miniamf adapters
from ._toplevel import (ArgumentError, Array, Boolean, Class, Date,
                        DefinitionError, Error, EvalError, false, Infinity,
                        int, JSON, Math, Namespace, NaN, null, Number, Object,
                        QName, RangeError, ReferenceError, RegExp,
                        SecurityError, String, SyntaxError, true, TypeError,
                        uint, undefined, URIError, Vector, VerifyError, XML,
                        XMLList, decodeURI, decodeURIComponent, encodeURI,
                        encodeURIComponent, escape, isFinite, isNaN,
                        isXMLName, parseFloat, parseInt, unescape, delete,
                        each, stricteq, strictne)
Int = int  # Backwards compatibility


# Set up miniamf type adapters
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


# Create NativeApplication Instance
from as3lib.flash.desktop import NativeApplication
as3state.nativeApplication = NativeApplication()


# Library state setting functions
def EnableDebug():
   as3state.as3DebugEnable = true


def DisableDebug():
   as3state.as3DebugEnable = false


def setDataDirectory(dir_: str):
   dir_ = Path(dir_)
   if not isValidDirectory(dir_):
      raise Error(f'setDataDirectory; Directory "{dir_}" not valid')
   as3state.appdatadirectory = dir_


def setHeaderInfo(swfVersion, frameRate, viewportWidth, viewportHeight):
   # TODO: Make a custom module loader to do this. This would require piping
   #       the program into as3lib instead of just importing it.
   #       ex: python -m as3lib <program>
   """
   Temporary function. Used to set the values found in the swf header.

   This function should only be used by the main script as only one set of
   values can be stored.
   """
   as3state.swfVersion = swfVersion
   as3state.frameRate = frameRate
   as3state.viewportWidth = viewportWidth
   as3state.viewportHeight = viewportHeight


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
   'setDataDirectory',
   'setHeaderInfo'
)
