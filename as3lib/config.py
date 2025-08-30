from as3lib import as3state
from io import StringIO
try:
   import tomllib
except:
   import tomli as tomllib

class TOML:
   def Value(value):
      if isinstance(value,str):
         return f'"{value}"'
      if isinstance(value,bool):
         return 'true' if value else 'false'
      if isinstance(value,(list,tuple)):
         return TOML.Array(value)
      if isinstance(value,dict):
         return TOML.Table(value)
      return f'{value}'
   def Table(value):
      with StringIO() as text:
         text.write('{')
         for k,v in value.items():
            text.write(f'{k} = {TOML.Value(v)},')
         temp = text.getvalue()
         if temp.endswith(','): #!Make this better
            return temp[:-1] + '}'
         return temp + '}'
   def Array(value):
      with StringIO() as text:
         text.write('[')
         for i in value:
            text.write(f'{TOML.Value(i)},')
         text.write(']')
         return text.getvalue()
   def Write(file, valDict, mode='w'):
      nontables = []
      tables = []
      for k,v in valDict.items():
         if isinstance(v,dict):
            tables.append(k)
         else:
            nontables.append(k)
      with StringIO() as text:
         for k in nontables:
            text.write(f'{k} = {TOML.Value(valDict[k])}\n')
         if len(nontables) > 0:
            text.write('\n')
         for k in tables:
            text.write(f'["{k}"]\n' if str(k).find('.') != -1 else f'[{k}]\n')
            for k2,v2 in valDict[k].items():
               text.write(f'{k2} = {TOML.Value(v2)}\n')
            text.write('\n')
         with open(file,mode) as f:
            f.write(text.getvalue())

def Load():
   configpath = as3state.librarydirectory / 'as3lib.toml'
   if configpath.exists():
      with configpath.open("rb") as f:
         temp = tomllib.load(f)
      tempmm = temp.get('mm.cfg')
      tempway = temp.get('wayland')
      cfg = {
         'migrateOldConfig':bool(temp['migrateOldConfig']),
         'dependenciesPassed':bool(temp['dependenciesPassed']),
         'mm.cfg':{
            'ErrorReportingEnable':bool(tempmm.get('ErrorReportingEnable',False)),
            'MaxWarnings':int(tempmm.get('MaxWarnings',100)),
            'TraceOutputFileEnable':bool(tempmm.get('TraceOutputFileEnable',False)),
            'TraceOutputFileName':str(tempmm.get('TraceOutputFileName','')),
            'ClearLogsOnStartup':bool(tempmm.get('ClearLogsOnStartup',True)),
            'NoClearWarningNumber':int(tempmm.get('NoClearWarningNumber',0))
         },
         'wayland':{
            'screenwidth':int(tempway.get('screenwidth',1600)),
            'screenheight':int(tempway.get('screenheight',900)),
            'refreshrate':float(tempway.get('refreshrate',60.0)),
            'colordepth':int(tempway.get('colordepth',8))
         }
      }
      cfg2 = dict(cfg)
   else:
      cfg = {
         'migrateOldConfig':True,
         'dependenciesPassed':False,
         'mm.cfg':{
            'ErrorReportingEnable':False,
            'MaxWarnings':100,
            'TraceOutputFileEnable':False,
            'TraceOutputFileName':'',
            'ClearLogsOnStartup':True,
            'NoClearWarningNumber':0
         },
         'wayland':{
            'screenwidth':1600,
            'screenheight':900,
            'refreshrate':60.00,
            'colordepth':8
         }
      }
      cfg2 = ''
   if cfg['migrateOldConfig']:
      from configparser import ConfigParser
      mmcfgpath = as3state.librarydirectory / "mm.cfg"
      wlcfgpath = as3state.librarydirectory / "wayland.cfg"
      oldcfgpath = as3state.librarydirectory / 'as3lib.cfg'
      if mmcfgpath.exists():
         mmcfg = ConfigParser()
         with open(mmcfgpath, 'r') as f:
            mmcfg.read_string('[dummy_section]\n' + f.read())
         cfg['mm.cfg'] = {
            'ErrorReportingEnable':True if mmcfg.getint('dummy_section','ErrorReportingEnable',fallback=0) == 1 else False,
            'MaxWarnings':mmcfg.getint('dummy_section','MaxWarnings',fallback=100),
            'TraceOutputFileEnable':True if mmcfg.getboolean('dummy_section','TraceOutputFileEnable',fallback=0) == 1 else False,
            'TraceOutputFileName':mmcfg.get('dummy_section','TraceOutputFileName',fallback=''),
            'ClearLogsOnStartup':True,
            'NoClearWarningNumber':0
         }
         del mmcfg
      if wlcfgpath.exists():
         wlcfg = ConfigParser()
         with open(wlcfgpath, 'r') as f:
            wlcfg.read_file(f)
         cfg['wayland'] = {
            'screenwidth':wlcfg.getint('Screen','screenwidth',fallback=1600),
            'screenheight':wlcfg.getint('Screen','screenheight',fallback=900),
            'refreshrate':wlcfg.getfloat('Screen','refreshrate',fallback=60.00),
            'colordepth':wlcfg.getint('Screen','colordepth',fallback=8)
         }
         wlcfgpath.unlink(missing_ok=True)
         del wlcfg
      if oldcfgpath.exists():
         oldcfg = ConfigParser()
         with open(oldcfgpath, 'r') as f:
            oldcfg.read_file(f)
         cfg = {
            'migrateOldConfig':False,
            'dependenciesPassed':False,
            'mm.cfg':{
               'ErrorReportingEnable':oldcfg.getboolean('mm.cfg','ErrorReportingEnable',fallback=False),
               'MaxWarnings':100, #Reset value because I messed up the type
               'TraceOutputFileEnable':oldcfg.getboolean('mm.cfg','TraceOutputFileEnable',fallback=False),
               'TraceOutputFileName':oldcfg.get('mm.cfg','TraceOutputFileName',fallback=''),
               'ClearLogsOnStartup':True if oldcfg.getint('mm.cfg','ClearLogsOnStartup',fallback=1) == 1 else False,
               'NoClearWarningNumber':oldcfg.getint('mm.cfg','NoClearWarningNumber',fallback=0)
            },
            'wayland':{
               'screenwidth':oldcfg.getint('wayland','screenwidth',fallback=1600),
               'screenheight':oldcfg.getint('wayland','screenheight',fallback=900),
               'refreshrate':oldcfg.getfloat('wayland','refreshrate',fallback=60.0),
               'colordepth':oldcfg.getint('wayland','colordepth',fallback=8)
            }
         }
         oldcfgpath.unlink(missing_ok=True)
      cfg['mm.cfg']['TraceOutputFileName'] = cfg['mm.cfg']['TraceOutputFileName'].strip('\'"') #Sometimes the value's quotes are left in the string
      cfg['migrateOldConfig'] = False
   return cfg, cfg2
