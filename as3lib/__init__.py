from . import as3state, config
from pathlib import Path
from subprocess import check_output

"""
initerrors
0 - platform not implemented
1 - function not implemented for current platform
2 - (Linux specific) unexpected display server (expected x11 or wayland)
3 - dependency not found
4 - other error
"""

# Helper functions
def defaultTraceFilePath_Flash(sysverOverride:tuple=None):
   """
   Outputs the defualt file path for trace as defined by https://web.archive.org/web/20180227100916/helpx.adobe.com/flash-player/kb/configure-debugger-version-flash-player.html
   Arguements:
      sysverOverride - A tuple containing the system and version of system you want to choose. ex: ('Windows','XP')
   """
   if as3state.platform == "Windows":
      from os import getlogin
      username = getlogin()
   elif as3state.platform in {"Linux","Darwin"}:
      from os import getuid
      from pwd import getpwuid
      username = getpwuid(getuid())[0]
   if sysverOverride != None:
      if sysverOverride[0] == "Linux":
         return fr"/home/{username}/.macromedia/Flash_Player/Logs/flashlog.txt"
      if sysverOverride[0] == "Darwin":
         return fr"/Users/{username}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt"
      if sysverOverride[0] == "Windows":
         if sysverOverride[1] in {"95","98","ME","XP"}:
            return fr"C:\Documents and Settings\{username}\Application Data\Macromedia\Flash Player\Logs\flashlog.txt"
         if sysverOverride[1] in {"Vista","7","8","8.1","10","11"}:
            return fr"C:\Users\{username}\AppData\Roaming\Macromedia\Flash Player\Logs\flashlog.txt"
   if as3state.platform == "Linux":
      return fr"/home/{username}/.macromedia/Flash_Player/Logs/flashlog.txt"
   if as3state.platform == "Windows":
      return fr"C:\Users\{username}\AppData\Roaming\Macromedia\Flash Player\Logs\flashlog.txt"
   if as3state.platform == "Darwin":
      return fr"/Users/{username}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt"

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
   for i in check_output("loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Type", shell=True).decode("utf-8").split("\n"):
      if len(i) > 0:
         temp2 = i.split("=")[-1]
         if temp2 in {"x11","wayland"}:
            return temp2
   return "error"

def sm_x11():
   """
   Gets and returns screen width, screen height, refresh rate, and color depth on x11
   """
   for option in check_output(('xrandr','--current')).decode("utf-8").split("\n"):
      if option.find("*") != -1:
         for i in [i for i in option.split(" ") if  i != ""][1:]:
            if i.find("*") != -1:
               temprr = i.replace("*","").replace("+","")
               break
         break
   cdp = check_output("xwininfo -root | grep Depth", shell=True).decode("utf-8").replace("\n","").replace(" ","").split(":")[1]
   tempwidth = check_output("xwininfo -root | grep Width", shell=True).decode("utf-8").replace("\n","").replace(" ","").split(":")[1]
   tempheight = check_output("xwininfo -root | grep Height", shell=True).decode("utf-8").replace("\n","").replace(" ","").split(":")[1]
   return int(tempwidth),int(tempheight),float(temprr),int(cdp)

def sm_wayland():...

def sm_windows():
   import ctypes
   try:
      import win32api
   except:
      as3state.initerror.append((3,"Windows: Requirement pywin32 either not installed or not accessible."))
   settings = win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1)
   temp = tuple(getattr(settings,i) for i in ('DisplayFrequency','BitsPerPel'))
   return int(ctypes.windll.user32.GetSystemMetrics(0)), int(ctypes.windll.user32.GetSystemMetrics(1)), float(temp[0]), int(temp[1])

def sm_darwin():...

# Initialise as3lib
if as3state.startTime == None:
   from datetime import datetime
   from miniamf import util
   as3state.startTime = int(util.get_timestamp(datetime.now()) * 1000)
if not as3state.initdone:
   import platform
   as3state.platform = platform.system()
   as3state.separator = "\\" if as3state.platform == "Windows" else "/"
   as3state.pythonversion = platform.python_version()
   as3state.librarydirectory = Path(__file__).resolve().parent
   as3state.userdirectory = Path.home()
   as3state.desktopdirectory = getDesktopDir()
   as3state.documentsdirectory = getDocumentsDir()
   as3state.defaultTraceFilePath_Flash = defaultTraceFilePath_Flash()
   if as3state.platform == "Linux":
      as3state.displayserver = getdmtype()
      if as3state.displayserver == "x11":
         as3state.width,as3state.height,as3state.refreshrate,as3state.colordepth = sm_x11()
      elif as3state.displayserver == "wayland":
         #as3state.width,as3state.height,as3state.refreshrate,as3state.colordepth = sm_wayland()
         ... # Loaded from config
      else:
         as3state.initerror.append((2,f"Linux: Display server \"{as3state.windowmanagertype}\" not supported."))
   elif as3state.platform == "Windows":
      as3state.width,as3state.height,as3state.refreshrate,as3state.colordepth = sm_windows()
   elif as3state.platform == "Darwin":
      as3state.initerror.append((1,"Darwin: Fetching screen properties is not implemented."))
      #as3state.width,as3state.height,as3state.refreshrate,as3state.colordepth = sm_darwin()
      ...
   elif as3state.platform == "":
      as3state.initerror.append((4,"Detected platform is blank. Something is very wrong."))
   else:
      as3state.initerror.append((0,f"Current platform {as3state.platform} not supported."))

   # Load the config
   config.Load()
   if as3state.ClearLogsOnStartup:
      if as3state.TraceOutputFileName.exists():
         with open(as3state.TraceOutputFileName, "w") as f:
            f.write('')

   # Display errors to user
   if len(as3state.initerror) != 0:
      print(f"Warning: as3lib has initialised with errors, some functionality may be broken.\n{''.join(f"\t({i[0]}) {i[1]}\n" for i in as3state.initerror)}")

   # Tell others that library has been initialised
   as3state.initdone = True



# Export toplevel and set up miniamf adapters
from .toplevel import *
from .toplevel import int as Int
try:
   import miniamf
   from . import adapters
except:...


__all__ = (
   "true",
   "false",
   "NInfinity",
   "Infinity",
   "NaN",
   "undefined",
   "null",

   "allBoolean",
   "allArray",
   "allNone",
   "allNumber",
   "allString",

   "ArguementError",
   "Array",
   "Boolean",
   "Date",
   "DefinitionError",
   "decodeURI",
   "decodeURIComponent",
   "encodeURI",
   "encodeURIComponent",
   "Error",
   "escape",
   "EvalError",
   "Int",
   "isFinite",
   "isNaN",
   "isXMLName",
   "JSON",
   "Math",
   "Namespace",
   "Number",
   "parseFloat",
   "parseInt",
   "QName",
   "RangeError",
   "ReferenceError",
   "RegExp",
   "SecurityError",
   "String",
   "SyntaxError",
   "trace",
   "TypeError",
   "uint",
   "unescape",
   "URIError",
   "Vector",
   "VerifyError",
   "EnableDebug",
   "DisableDebug",
   "setDataDirectory"
)

