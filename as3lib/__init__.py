from . import as3state, TOML
from ._toplevel.trace import trace
from .helpers import isValidDirectory
import builtins, configparser, os
from functools import partial
from importlib.util import find_spec
from miniamf import add_type
from miniamf.amf3 import IntVector, UintVector, DoubleVector, ObjectVector
from pathlib import Path


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


class _config:
    '''
    This class holds all config options for this library.
    '''
    @property
    def TOML(self):
        # Backwards compatibility
        return TOML

    @property
    def hasDependencies(self):
        return self._hasDependencies

    @property
    def addedFeatures(self):
        # Enables features added by this library.
        return self._addedFeatures

    @addedFeatures.setter
    def addedFeatures(self, value):
        self._addedFeatures = bool(value)

    @property
    def flashVersion(self):
        # This currently doesn't do anything
        # [majorVersion,minorVersion,buildNumber,internalBuildNumber]
        return self._flashVersion

    @flashVersion.setter
    def flashVersion(self, value):
        self._flashVersion = value

    @property
    def ErrorReportingEnable(self):
        # Enables logging of errors (console output seems to always be active in the debugger)
        return self._ErrorReportingEnable

    @ErrorReportingEnable.setter
    def ErrorReportingEnable(self, value):
        self._ErrorReportingEnable = bool(value)

    @property
    def MaxWarnings(self):
        # Number of warnings to log before stopping.
        return self._MaxWarnings

    @MaxWarnings.setter
    def MaxWarnings(self, value):
        self._MaxWarnings = bool(value)

    @property
    def TraceOutputFileEnable(self):
        # Enables trace logging (console output is always be active in the debugger)
        return self._TraceOutputFileEnable

    @TraceOutputFileEnable.setter
    def TraceOutputFileEnable(self, value):
        self._TraceOutputFileEnable = bool(value)

    @property
    def TraceOutputFileName(self):
        # Path to the log
        return self._TraceOutputFileName

    @TraceOutputFileName.setter
    def TraceOutputFileName(self, value):
        if value == '' or Path(value).is_dir():
            print('[as3lib] Info: Using defualt TraceOutputFileName')
            value = as3state.librarydirectory / 'flashlog.txt'
        self._TraceOutputFileName = Path(value)

    def __init__(self):
        configpath = as3state.librarydirectory / 'as3lib.toml'
        if configpath.exists():
            modified = False
            with configpath.open('rb') as f:
                temp = TOML.readFile(f)
            self._cfg = temp
            tempmm = temp.get('mm.cfg', {})
            cfg = {
                'version': int(temp.get('version', as3state.__version__)),
                'migrateOldConfig': bool(temp.get('migrateOldConfig', False)),
                'dependenciesPassed': bool(temp.get('dependenciesPassed', False)),
                'addedFeatures': bool(temp.get('addedFeatures', False)),
                'flashVersion': tuple(temp.get('flashVersion', (32, 0, 0, 371))),
                'mm.cfg': {
                    'ErrorReportingEnable': bool(tempmm.get('ErrorReportingEnable', False)),
                    'MaxWarnings': int(tempmm.get('MaxWarnings', 100)),
                    'TraceOutputFileEnable': bool(tempmm.get('TraceOutputFileEnable', False)),
                    'TraceOutputFileName': str(tempmm.get('TraceOutputFileName', ''))
                }
            }
        else:
            modified = True
            self._cfg = None
            cfg = {
                'version': as3state.__version__,
                'migrateOldConfig': True,
                'dependenciesPassed': False,
                'addedFeatures': False,
                'flashVersion': (32, 0, 0, 371),  # I chose this version because it was the last version of flash before adobe's timebomb
                'mm.cfg': {
                    'ErrorReportingEnable': False,
                    'MaxWarnings': 100,
                    'TraceOutputFileEnable': False,
                    'TraceOutputFileName': ''
                }
            }
        if cfg['migrateOldConfig']:
            modified = True
            mmcfgpath = as3state.librarydirectory / 'mm.cfg'
            wlcfgpath = as3state.librarydirectory / 'wayland.cfg'
            oldcfgpath = as3state.librarydirectory / 'as3lib.cfg'
            if mmcfgpath.exists():
                with open(mmcfgpath, 'r') as f:
                    if hasattr(configparser, 'UNNAMED_SECTION'):
                        UNNAMED_SECTION = configparser.UNNAMED_SECTION
                        mmcfg = configparser.ConfigParser(allow_unnamed_section=True)
                        mmcfg.read_file(f)
                    else:  # Python < 3.13 compatibility
                        UNNAMED_SECTION = 'UNNAMED_SECTION'
                        mmcfg = configparser.ConfigParser()
                        mmcfg.read_string('[UNNAMED_SECTION]\n' + f.read())
                cfg['mm.cfg'] = {
                    'ErrorReportingEnable': mmcfg.getint(UNNAMED_SECTION, 'ErrorReportingEnable', fallback=0) == 1,
                    'MaxWarnings': mmcfg.getint(UNNAMED_SECTION, 'MaxWarnings', fallback=100),
                    'TraceOutputFileEnable': mmcfg.getboolean(UNNAMED_SECTION, 'TraceOutputFileEnable', fallback=0) == 1,
                    'TraceOutputFileName': mmcfg.get(UNNAMED_SECTION, 'TraceOutputFileName', fallback='')
                }
                del mmcfg
            if wlcfgpath.exists():
                wlcfgpath.unlink(missing_ok=True)
            if oldcfgpath.exists():
                oldcfg = configparser.ConfigParser()
                with open(oldcfgpath, 'r') as f:
                    oldcfg.read_file(f)
                cfg = {
                    'version': as3state.__version__,
                    'migrateOldConfig': False,
                    'dependenciesPassed': False,
                    'addedFeatures': False,
                    'flashVersion': (32, 0, 0, 371),
                    'mm.cfg': {
                        'ErrorReportingEnable': oldcfg.getboolean('mm.cfg', 'ErrorReportingEnable', fallback=False),
                        'MaxWarnings': 100,  # Reset value because I messed up the type
                        'TraceOutputFileEnable': oldcfg.getboolean('mm.cfg', 'TraceOutputFileEnable', fallback=False),
                        'TraceOutputFileName': oldcfg.get('mm.cfg', 'TraceOutputFileName', fallback='')
                    }
                }
                oldcfgpath.unlink(missing_ok=True)
            cfg['mm.cfg']['TraceOutputFileName'] = cfg['mm.cfg']['TraceOutputFileName'].strip('\'"')  # Sometimes the value's quotes are left in the string
            cfg['migrateOldConfig'] = False
        # Load some values into global state
        self.addedFeatures = cfg['addedFeatures']
        self._hasDependencies = True if cfg['dependenciesPassed'] and cfg['version'] == as3state.__version__ else self._dependencyCheck()
        self.flashVersion = cfg['flashVersion']
        self.ErrorReportingEnable = cfg['mm.cfg']['ErrorReportingEnable']
        self.MaxWarnings = cfg['mm.cfg']['MaxWarnings']
        self.TraceOutputFileEnable = cfg['mm.cfg']['TraceOutputFileEnable']
        self.TraceOutputFileName = cfg['mm.cfg']['TraceOutputFileName']
        if self.TraceOutputFileName.exists():
            self.TraceOutputFileName.unlink()
        self.Save(modified)

    @staticmethod
    def _dependencyCheck():
        hasDeps = True
        if find_spec('numpy') is None:  # https://pypi.org/project/numpy
            as3state.initerror.append('Dependencies/Python: "numpy" not found')
            hasDeps = False
        if find_spec('PIL') is None:  # https://pypi.org/project/Pillow
            as3state.initerror.append('Dependencies/Python: "Pillow" not found')
            hasDeps = False
        if find_spec('tkhtmlview') is None:  # https://pypi.org/project/tkhtmlview
            as3state.initerror.append('Dependencies/Python: "tkhtmlview" not found')
            hasDeps = False
        if find_spec('miniamf') is None:
            as3state.initerror.append('Dependencies/Python: "Mini-AMF" or "as3lib-miniAMF" not found')
            hasDeps = False
        if find_spec('tomllib') is None and find_spec('tomli') is None:
            as3state.initerror.append('Dependencies/Python: "tomllib" or "tomli" not found')
            hasDeps = False
        return hasDeps

    def Save(self, saveAnyways: bool = False):
        tempcfg = {
            'version': as3state.__version__,
            'migrateOldConfig': False,
            'dependenciesPassed': self.hasDependencies,
            'addedFeatures': self.addedFeatures,
            'flashVersion': self.flashVersion,
            'mm.cfg': {
                'ErrorReportingEnable': self.ErrorReportingEnable,
                'MaxWarnings': self.MaxWarnings,
                'TraceOutputFileEnable': self.TraceOutputFileEnable,
                'TraceOutputFileName': self.TraceOutputFileName,
            }
        }
        if saveAnyways or self._cfg != tempcfg:
            TOML.write(as3state.librarydirectory / 'as3lib.toml', tempcfg)
            self._cfg = tempcfg


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
    config = _config()

    # Display errors to user
    if as3state.initerror:
        # NOTE: Use % because f-string expression parts can not contain a backslash on Python 3.10
        trace('[as3lib] Warning: Errors have occurred during initialisation, some functionality may be broken.\n\t%s' % "\n\t".join(as3state.initerror))

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
