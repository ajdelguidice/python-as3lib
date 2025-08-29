import platform, subprocess, configparser
from . import as3state
from pathlib import Path

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
   xr = subprocess.check_output("xrandr --current", shell=True).decode("utf-8").split("\n")
   for option in xr:
      if option.find("*") != -1:
         ops = [i for i in option.split(" ") if  i != ""]
         ops.pop(0)
         break
   for i in ops:
      if i.find("*") != -1:
         temprr = i.replace("*","").replace("+","")
         break
   cdp = subprocess.check_output("xwininfo -root | grep Depth", shell=True).decode("utf-8").replace("\n","").replace(" ","").split(":")[1]
   tempwidth = subprocess.check_output("xwininfo -root | grep Width", shell=True).decode("utf-8").replace("\n","").replace(" ","").split(":")[1]
   tempheight = subprocess.check_output("xwininfo -root | grep Height", shell=True).decode("utf-8").replace("\n","").replace(" ","").split(":")[1]
   return int(tempwidth),int(tempheight),float(temprr),int(cdp)

def sm_wayland():
   return config.getint("wayland","screenwidth",fallback=1600),config.getint("wayland","screenheight",fallback=900),config.getfloat("wayland","refreshrate",fallback=60.00),config.getint("wayland","colordepth",fallback=8)

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
      deskdir = subprocess.check_output("echo $XDG_DOCUMENTS_DIR",shell=True).decode("utf-8").replace("\n","")
      if deskdir != "":
         return Path(deskdir)
   return as3state.userdirectory / "Desktop"

def getDocumentsDir():
   if as3state.platform == "Linux":
      deskdir = subprocess.check_output("echo $XDG_DESKTOP_DIR",shell=True).decode("utf-8").replace("\n","")
      if deskdir != "":
         return Path(deskdir)
   return as3state.userdirectory / "Documents"

def getdmtype():
   temp = subprocess.check_output("loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Type", shell=True).decode("utf-8")
   for i in temp.split("\n"):
      if len(i) > 0:
         temp2 = i.split("=")[-1]
         if temp2 in {"x11","wayland"}:
            return temp2
   return "error"

def getdmname():
   temp = subprocess.check_output("loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Desktop",shell=True).decode("utf-8")
   for i in temp.split("\n"):
      if len(i) > 0:
         temp2 = i.split("=")[-1]
         if len(temp2) > 0:
            return temp2.lower()
   return "error"

def dependencyCheck():
   global config
   import importlib.util
   hasDeps = True
   if as3state.platform == "Linux":
      wmt = subprocess.check_output("echo $XDG_SESSION_TYPE",shell=True).decode("utf-8")
      if wmt == "wayland":
         x=0
      else:
         try:
            subprocess.check_output("which xwininfo",shell=True)
         except:
            as3state.initerror.append((3,"Linux (xorg): requirement 'xwininfo' not found"))
            hasDeps = False
         try:
            subprocess.check_output("which xrandr",shell=True)
         except:
            as3state.initerror.append((3,"Linux (xorg): requirement 'xrandr' not found"))
            hasDeps = False
      try:
         subprocess.check_output("which bash",shell=True)
      except:
         as3state.initerror.append((3,"Linux: requirement 'bash' not found"))
         hasDeps = False
      try:
         subprocess.check_output("which awk",shell=True)
      except:
         as3state.initerror.append((3,"Linux: requirement 'awk' not found"))
         hasDeps = False
      try:
         subprocess.check_output("which whoami",shell=True)
      except:
         as3state.initerror.append((3,"Linux: requirement 'whoami' not found"))
         hasDeps = False
      try:
         subprocess.check_output("which loginctl",shell=True)
      except:
         as3state.initerror.append((3,"Linux: requirement 'loginctl' not found"))
         hasDeps = False
      try:
         subprocess.check_output("which echo",shell=True)
         assert subprocess.check_output("echo test",shell=True).decode("utf-8").replace("\n","") == "test"
      except:
         as3state.initerror.append((3,"Linux: requirement 'echo' not found"))
         hasDeps = False
   elif as3state.platform == "Windows":
      pass
   elif as3state.platform == "Darwin":
      pass
   try: #https://pypi.org/project/numpy
      importlib.util.find_spec('numpy').origin
   except:
      as3state.initerror.append((3,"Python: requirement 'numpy' not found"))
      hasDeps = False
   try: #https://pypi.org/project/Pillow
      importlib.util.find_spec('PIL').origin
   except:
      as3state.initerror.append((3,"Python: requirement 'Pillow' not found"))
      hasDeps = False
   try: #https://pypi.org/project/tkhtmlview
      importlib.util.find_spec('tkhtmlview').origin
   except:
      as3state.initerror.append((3,"Python: requirement 'tkhtmlview' not found"))
      hasDeps = False
   config.set("dependencies","passed",str(hasDeps))
   as3state.hasDependencies = hasDeps

def configLoader():
   configpath = as3state.librarydirectory / "as3lib.cfg"
   if configpath.exists():
      config = configparser.ConfigParser()
      config.optionxform=str
      config2 = configparser.ConfigParser()
      config2.optionxform=str
      with open(configpath, 'r') as f:
         config.read_string(f.read())
         config2.read_string(f.read())
      return config,config2
   else:
      mmcfgpath = as3state.librarydirectory / "mm.cfg"
      wlcfgpath = as3state.librarydirectory / "wayland.cfg"
      ErrorReportingEnable = False
      MaxWarnings = False
      TraceOutputFileEnable = False
      TraceOutputFileName = ""
      ClearLogsOnStartup = 1
      if mmcfgpath.exists() == True:
         mmcfg = configparser.ConfigParser()
         with open(mmcfgpath, 'r') as f:
            mmcfg.read_string('[dummy_section]\n' + f.read())
         ErrorReportingEnable = mmcfg.getboolean("dummy_section","ErrorReportingEnable",fallback=False)
         MaxWarnings = mmcfg.getboolean("dummy_section","MaxWarnings",fallback=False)
         TraceOutputFileEnable = mmcfg.getboolean("dummy_section","TraceOutputFileEnable",fallback=False)
         TraceOutputFileName = mmcfg.get("dummy_section","TraceOutputFileName",fallback="")
         ClearLogsOnStartup = mmcfg.getint("dummy_section","ClearLogsOnStartup",fallback=1)
      sw = 1600
      sh = 900
      rr = 60.00
      cd = 8
      if wlcfgpath.exists():
         wlcfg = configparser.ConfigParser()
         with open(wlcfgpath, 'r') as f:
            wlcfg.read_string(f.read())
         sw = wlcfg.getint("Screen","screenwidth",fallback=1600)
         sh = wlcfg.getint("Screen","screenheight",fallback=900)
         rr = wlcfg.getfloat("Screen","refreshrate",fallback=60.00)
         cd = wlcfg.getint("Screen","colordepth",fallback=8)
         wlcfgpath.unlink(missing_ok=True)
      config = configparser.ConfigParser()
      config.read_string(f"[dependencies]\npassed=false\n\n[mm.cfg]\nErrorReportingEnable={ErrorReportingEnable}\nMaxWarnings={MaxWarnings}\nTraceOutputFileEnable={TraceOutputFileEnable}\nTraceOutputFileName=\"{TraceOutputFileName}\"\nClearLogsOnStartup={ClearLogsOnStartup}\nNoClearWarningNumber=0\n\n[wayland]\nscreenwidth={sw}\nscreenheight={sh}\nrefreshrate={rr}\ncolordepth={cd}")
      return config,"default"
      
config = None

def initconfig():
   #set up variables needed by mutiple modules
   global config
   as3state.librarydirectory = Path(__file__).resolve().parent
   config,config2 = configLoader()
   as3state.platform = platform.system()
   if config.getboolean("dependencies","passed",fallback=False) == False:
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
   as3state.ErrorReportingEnable = config.getboolean("mm.cfg","ErrorReportingEnable",fallback=False)
   as3state.MaxWarnings = config.getboolean("mm.cfg","MaxWarnings",fallback=False)
   as3state.TraceOutputFileEnable = config.getboolean("mm.cfg","TraceOutputFileEnable",fallback=False)
   tempTraceOutputFileName = config.get("mm.cfg","TraceOutputFileName",fallback="")
   as3state.ClearLogsOnStartup = config.getint("mm.cfg","ClearLogsOnStartup",fallback=1)
   if as3state.ClearLogsOnStartup == 0:
      as3state.CurrentWarnings = config.getint("mm.cfg","NoClearWarningNumber",fallback=0)
   if tempTraceOutputFileName == "":
      tempTraceOutputFileName = as3state.defaultTraceFilePath
   if Path(tempTraceOutputFileName).is_dir():
      print("Path provided is a directory, writing to defualt location instead.")
      tempTraceOutputFileName = as3state.defaultTraceFilePath
   as3state.TraceOutputFileName = Path(tempTraceOutputFileName)
   if as3state.ClearLogsOnStartup == 1:
      if as3state.TraceOutputFileName.exists():
         with open(as3state.TraceOutputFileName, "w") as f: 
            f.write("")
   if config != config2 or config2 == "default":
      with open(as3state.librarydirectory / "as3lib.cfg","w") as f:
         config.write(f)
   del config

   #Report errors to user
   if len(as3state.initerror) != 0:
      print(f"Warning: as3lib has initialized with errors, some functionality may be broken.\n{''.join((f"\tType={i[0]}; Message={i[1]}\n" for i in as3state.initerror))}")
   
   #Tell others that library has been initialized
   as3state.initdone = True
