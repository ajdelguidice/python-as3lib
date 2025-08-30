import platform
from . import as3state, config
from pathlib import Path
from subprocess import check_output

if platform.system() == "Windows":
   from os import getlogin
   import ctypes
   try:
      import win32api
   except:
      as3state.initerror.append((3,"pywin32 is required for operation on Windows but is either not installed or not accessible."))
elif platform.system() in ("Linux","Darwin"):
   from os import getuid
   from pwd import getpwuid

"""
initerrors
0 - platform not implemented
1 - function not implemented for current platform
2 - (Linux specific) unexpected display server (expected x11 or wayland)
3 - dependency not found
4 - other error
"""

def defaultTraceFilePath_Flash(versionOverride:bool=False,overrideSystem:str=None,overrideVersion:str=None):
   """
   Outputs the defualt file path for trace as defined by https://web.archive.org/web/20180227100916/helpx.adobe.com/flash-player/kb/configure-debugger-version-flash-player.html
   Since anything earlier than Windows 7 isn't supported by python 3, you normally wouldn't be able to get the file path for these systems but I have included an optional parameter to force this function to return it.
   """
   if as3state.platform == "Windows":
      username = getlogin()
   elif as3state.platform in {"Linux","Darwin"}:
      username = getpwuid(getuid())[0]
   if versionOverride == True:
      if overrideSystem == "Linux":
         return fr"/home/{username}/.macromedia/Flash_Player/Logs/flashlog.txt"
      elif overrideSystem == "Darwin":
         return fr"/Users/{username}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt"
      elif overrideSystem == "Windows":
         if overrideVersion in {"95","98","ME","XP"}:
            return fr"C:\Documents and Settings\{username}\Application Data\Macromedia\Flash Player\Logs\flashlog.txt"
         elif overrideVersion in {"Vista","7","8","8.1","10","11"}:
            return fr"C:\Users\{username}\AppData\Roaming\Macromedia\Flash Player\Logs\flashlog.txt"
   elif as3state.platform == "Linux":
      return fr"/home/{username}/.macromedia/Flash_Player/Logs/flashlog.txt"
   elif as3state.platform == "Windows":
      return fr"C:\Users\{username}\AppData\Roaming\Macromedia\Flash Player\Logs\flashlog.txt"
   elif as3state.platform == "Darwin":
      return fr"/Users/{username}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt"

def sm_x11():
   """
   Gets and returns screen width, screen height, refresh rate, and color depth on x11
   """
   xr = check_output(('xrandr','--current')).decode("utf-8").split("\n")
   for option in xr:
      if option.find("*") != -1:
         ops = [i for i in option.split(" ") if  i != ""]
         ops.pop(0)
         break
   for i in ops:
      if i.find("*") != -1:
         temprr = i.replace("*","").replace("+","")
         break
   cdp = check_output("xwininfo -root | grep Depth", shell=True).decode("utf-8").replace("\n","").replace(" ","").split(":")[1]
   tempwidth = check_output("xwininfo -root | grep Width", shell=True).decode("utf-8").replace("\n","").replace(" ","").split(":")[1]
   tempheight = check_output("xwininfo -root | grep Height", shell=True).decode("utf-8").replace("\n","").replace(" ","").split(":")[1]
   return int(tempwidth),int(tempheight),float(temprr),int(cdp)

def sm_wayland():
   temp = cfg['wayland']
   return temp['screenwidth'],temp['screenheight'],temp['refreshrate'],temp['colordepth']

def sm_windows():
   settings = win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1)
   temp = tuple(getattr(settings,i) for i in ('DisplayFrequency','BitsPerPel'))
   return int(ctypes.windll.user32.GetSystemMetrics(0)), int(ctypes.windll.user32.GetSystemMetrics(1)), float(temp[0]), int(temp[1])

def sm_darwin():
   pass

def getSeparator():
   if as3state.platform == "Windows":
      return "\\"
   return "/"

def getDesktopDir():
   if as3state.platform == "Linux":
      deskdir = check_output(('echo','$XDG_DOCUMENTS_DIR')).decode("utf-8").replace("\n","")
      if deskdir != "":
         return Path(deskdir)
   return as3state.userdirectory / "Desktop"

def getDocumentsDir():
   if as3state.platform == "Linux":
      deskdir = check_output(('echo','$XDG_DESKTOP_DIR')).decode("utf-8").replace("\n","")
      if deskdir != "":
         return Path(deskdir)
   return as3state.userdirectory / "Documents"

def getdmtype():
   temp = check_output("loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Type", shell=True).decode("utf-8")
   for i in temp.split("\n"):
      if len(i) > 0:
         temp2 = i.split("=")[-1]
         if temp2 in {"x11","wayland"}:
            return temp2
   return "error"

def getdmname():
   temp = check_output("loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Desktop",shell=True).decode("utf-8")
   for i in temp.split("\n"):
      if len(i) > 0:
         temp2 = i.split("=")[-1]
         if len(temp2) > 0:
            return temp2.lower()
   return "error"

def dependencyCheck():
   global cfg
   from importlib.util import find_spec
   hasDeps = True
   if as3state.platform == "Linux":
      wmt = check_output(('echo','$XDG_SESSION_TYPE')).decode("utf-8").replace("\n","")
      if wmt == "wayland":
         x=0
      else:
         if check_output(('which','xwininfo')).decode("utf-8").startswith("which: no"):
            as3state.initerror.append((3,"Linux (xorg): requirement 'xwininfo' not found"))
            hasDeps = False
         if check_output(('which','xrandr')).decode("utf-8").startswith("which: no"):
            as3state.initerror.append((3,"Linux (xorg): requirement 'xrandr' not found"))
            hasDeps = False
      if check_output(('which','bash')).decode("utf-8").startswith("which: no"):
         as3state.initerror.append((3,"Linux: requirement 'bash' not found"))
         hasDeps = False
      if check_output(('which','awk')).decode("utf-8").startswith("which: no"):
         as3state.initerror.append((3,"Linux: requirement 'awk' not found"))
         hasDeps = False
      if check_output(('which','whoami')).decode("utf-8").startswith("which: no"):
         as3state.initerror.append((3,"Linux: requirement 'whoami' not found"))
         hasDeps = False
      if check_output(('which','loginctl')).decode("utf-8").startswith("which: no"):
         as3state.initerror.append((3,"Linux: requirement 'loginctl' not found"))
         hasDeps = False
      if check_output(('which','echo')).decode("utf-8").startswith("which: no") or check_output(('echo','test')).decode("utf-8").replace("\n","") != "test":
         as3state.initerror.append((3,"Linux: requirement 'echo' not found"))
         hasDeps = False
   elif as3state.platform == "Windows":...
   elif as3state.platform == "Darwin":...
   if find_spec('numpy') == None: #https://pypi.org/project/numpy
      as3state.initerror.append((3,"Python: requirement 'numpy' not found"))
      hasDeps = False
   if find_spec('PIL') == None: #https://pypi.org/project/Pillow
      as3state.initerror.append((3,"Python: requirement 'Pillow' not found"))
      hasDeps = False
   if find_spec('tkhtmlview') == None: #https://pypi.org/project/tkhtmlview
      as3state.initerror.append((3,"Python: requirement 'tkhtmlview' not found"))
      hasDeps = False
   as3state.hasDependencies = hasDeps
      
cfg = None

def init():
   #set up variables needed by mutiple modules
   global cfg
   as3state.librarydirectory = Path(__file__).resolve().parent
   cfg,cfg2 = config.Load()
   as3state.addedFeatures = cfg['addedFeatures']
   as3state.platform = platform.system()
   if not cfg["dependenciesPassed"]:
      dependencyCheck()
   as3state.separator = getSeparator()
   as3state.userdirectory = Path.home()
   as3state.desktopdirectory = getDesktopDir()
   as3state.documentsdirectory = getDocumentsDir()
   as3state.defaultTraceFilePath = as3state.librarydirectory / "flashlog.txt"
   as3state.defaultTraceFilePath_Flash = defaultTraceFilePath_Flash()
   as3state.pythonversion = platform.python_version()
   if as3state.platform == "Linux":
      as3state.displayserver = getdmtype()
      as3state.dmname = getdmname()
      if as3state.displayserver == "x11":
         as3state.width,as3state.height,as3state.refreshrate,as3state.colordepth = sm_x11()
      elif as3state.displayserver == "wayland":
         as3state.width,as3state.height,as3state.refreshrate,as3state.colordepth = sm_wayland()
      else:
         as3state.initerror.append((2,f"windowmanagertype \"{as3state.windowmanagertype}\" not supported"))
   elif as3state.platform == "Windows":
      as3state.width,as3state.height,as3state.refreshrate,as3state.colordepth = sm_windows()
   elif as3state.platform == "Darwin":
      as3state.initerror.append((1,"Darwin: Fetching screen properties is not implemented."))
      #as3state.width,as3state.height,as3state.refreshrate,as3state.colordepth = sm_darwin()
      ...
   elif as3state.platform == "":
      as3state.initerror.append((4,"Platform could not be determined"))
   else:
      as3state.initerror.append((0,f"Current platform {as3state.platform} not supported"))
   as3state.ErrorReportingEnable = cfg['mm.cfg']['ErrorReportingEnable']
   as3state.MaxWarnings = cfg['mm.cfg']['MaxWarnings']
   as3state.TraceOutputFileEnable = cfg['mm.cfg']['TraceOutputFileEnable']
   tempTraceOutputFileName = cfg['mm.cfg']['TraceOutputFileName']
   as3state.ClearLogsOnStartup = cfg['mm.cfg']['ClearLogsOnStartup']
   if not as3state.ClearLogsOnStartup:
      as3state.CurrentWarnings = cfg['mm.cfg']['NoClearWarningNumber']
   if tempTraceOutputFileName == '':
      tempTraceOutputFileName = as3state.defaultTraceFilePath
   if Path(tempTraceOutputFileName).is_dir():
      print("Path provided is a directory, writing to defualt location instead.")
      tempTraceOutputFileName = as3state.defaultTraceFilePath
   as3state.TraceOutputFileName = Path(tempTraceOutputFileName)
   if as3state.ClearLogsOnStartup:
      if as3state.TraceOutputFileName.exists():
         with open(as3state.TraceOutputFileName, "w") as f: 
            f.write('')
   config.Save(cfg)
   del cfg

   #Report errors to user
   if len(as3state.initerror) != 0:
      print(f"Warning: as3lib has initialized with errors, some functionality may be broken.\n{''.join((f"\tType={i[0]}; Message={i[1]}\n" for i in as3state.initerror))}")
   
   #Tell others that library has been initialized
   as3state.initdone = True
