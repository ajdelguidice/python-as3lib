from as3lib import as3state, TOML
from as3lib.as3state import __version__
from as3lib._toplevel import Error
import configparser
from importlib.util import find_spec
from pathlib import Path


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


def Load():
    if as3state._cfg is not None:
        raise Error('Config has already been loaded')
    # Load config from files
    configpath = as3state.librarydirectory / 'as3lib.toml'
    modified = False
    if configpath.exists():
        with configpath.open('rb') as f:
            temp = TOML.readFile(f)
        as3state._cfg = temp
        tempmm = temp.get('mm.cfg', {})
        cfg = {
            'version': int(temp.get('version', __version__)),
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
        cfg = {
            'version': __version__,
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
                'version': __version__,
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
    as3state.addedFeatures = cfg['addedFeatures']
    as3state.hasDependencies = True if cfg['dependenciesPassed'] and cfg['version'] == __version__ else _dependencyCheck()
    as3state.flashVersion = cfg['flashVersion']
    as3state.ErrorReportingEnable = cfg['mm.cfg']['ErrorReportingEnable']
    as3state.MaxWarnings = cfg['mm.cfg']['MaxWarnings']
    as3state.TraceOutputFileEnable = cfg['mm.cfg']['TraceOutputFileEnable']
    tempTraceOutputFileName = cfg['mm.cfg']['TraceOutputFileName']
    if tempTraceOutputFileName == '' or Path(tempTraceOutputFileName).is_dir():
        print('[as3lib] Info: Using defualt TraceOutputFileName')
        tempTraceOutputFileName = as3state.librarydirectory / 'flashlog.txt'
    as3state.TraceOutputFileName = Path(tempTraceOutputFileName)
    if as3state.TraceOutputFileName.exists():
        as3state.TraceOutputFileName.unlink()
    Save(modified)


def Save(saveAnyways: bool = False):
    tempcfg = {
        'version': __version__,
        'migrateOldConfig': False,
        'dependenciesPassed': as3state.hasDependencies,
        'addedFeatures': as3state.addedFeatures,
        'flashVersion': as3state.flashVersion,
        'mm.cfg': {
            'ErrorReportingEnable': as3state.ErrorReportingEnable,
            'MaxWarnings': as3state.MaxWarnings,
            'TraceOutputFileEnable': as3state.TraceOutputFileEnable,
            'TraceOutputFileName': as3state.TraceOutputFileName,
        }
    }
    if saveAnyways or as3state._cfg != tempcfg:
        TOML.write(as3state.librarydirectory / 'as3lib.toml', tempcfg)
        as3state._cfg = tempcfg
