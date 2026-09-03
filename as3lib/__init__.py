from . import as3state, config
from ._toplevel.trace import trace
from .helpers import isValidDirectory
import builtins, os
from functools import partial
from miniamf import add_type
from miniamf.amf3 import IntVector, UintVector, DoubleVector, ObjectVector
from pathlib import Path


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
    as3state.librarydirectory = Path(os.path.dirname(__file__))
    as3state.userdirectory = Path.home()
    as3state.desktopdirectory = Path(os.environ.get('XDG_DESKTOP_DIR', as3state.userdirectory / 'Desktop'))
    as3state.documentsdirectory = Path(os.environ.get('XDG_DOCUMENTS_DIR', as3state.userdirectory / 'Documents'))

    if as3state.platform == '':
        as3state.initerror.append('Could not determine current platform.')
    elif as3state.platform == 'Linux':
        as3state.displayserver = os.environ.get('XDG_SESSION_TYPE', 'error')
        if as3state.displayserver not in {'x11', 'wayland'}:
            as3state.initerror.append(f'Platform/Linux: Session type "{as3state.displayserver}" not supported.')
    elif as3state.platform == 'Windows':
        ...
    else:
        as3state.initerror.append(f'Platform/{as3state.platform} has not been tested. Things may be broken')

    # Load the config
    config.Load()

    # Display errors to user
    if as3state.initerror:
        # NOTE: Use % because f-string expression parts can not contain a backslash on Python 3.10
        trace('[as3lib] Warning: Errors have occurred during initialisation, some functionality may be broken.\n\t%s' % "\n\t".join(as3state.initerror))

    # Set the default appdatadirectory
    import __main__
    if hasattr(__main__, '__file__'):
        as3state.appdatadirectory = Path(os.path.dirname(__main__.__file__))
    else:  # Fall back to working directory
        as3state.appdatadirectory = Path.cwd()

    # Tell others that library has been initialised
    as3state.initdone = True


# Export toplevel and set up miniamf adapters
from ._toplevel import (ArgumentError, Array, Boolean, Class, Date,
                        DefinitionError, Error, EvalError, false, Function,
                        Infinity, int, JSON, Math, Namespace, NaN, null,
                        Number, Object, QName, RangeError, ReferenceError,
                        RegExp, SecurityError, String, SyntaxError, true,
                        TypeError, uint, undefined, URIError, Vector,
                        VerifyError, XML, XMLList, decodeURI,
                        decodeURIComponent, encodeURI, encodeURIComponent,
                        escape, isFinite, isNaN, isXMLName, parseFloat,
                        parseInt, unescape, delete, each, stricteq, strictne)


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


# Create AudioDeviceManager instance
from as3lib.flash.media import AudioDeviceManager
as3state.audioDeviceManager = AudioDeviceManager()


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
    'Function',
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
