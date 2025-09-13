from . import as3state, config
from pathlib import Path
from subprocess import check_output
import os
from importlib import __import__

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
      username = os.getlogin()
   elif as3state.platform in {"Linux","Darwin"}:
      from pwd import getpwuid
      username = getpwuid(os.getuid())[0]
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
try:
   import miniamf
   from . import adapters
except:...

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
   as3state.desktopdirectory = Path(os.environ.get('XDG_DESKTOP_DIR',as3state.userdirectory / "Desktop"))
   as3state.documentsdirectory = Path(os.environ.get('XDG_DOCUMENTS_DIR',as3state.userdirectory / "Documents"))
   as3state.defaultTraceFilePath_Flash = defaultTraceFilePath_Flash()
   if as3state.platform == "Linux":
      as3state.displayserver = os.environ.get('XDG_SESSION_TYPE','error')
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
   elif as3state.platform == '':
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

   # Set the default appdatadirectory
   import __main__
   if hasattr(__main__, "__file__"):
      as3state.appdatadirectory = Path(__main__.__file__).resolve().parent
   else: # Fall back to working directory
      as3state.appdatadirectory = Path.cwd()

   # Tell others that library has been initialised
   as3state.initdone = True


# as3 builtins
def formatToString(obj,objname,*args):
   """
   This function appears in the decompiled version of fl.ScrollEvent and many
   others in the fl package but doesn't appear anywhere in the documentation, not
   even in the toplevel section. I'm going to assume that this is a builtin function
   """
   return ''.join(["[",objname] + [f" {i}={getattr(obj, i)}" for i in args] + ["]"])

def as3import(packageName:str,namespace,name:str=None):
   #!Implement * imports
   """
   DO NOT USE THIS YET. I have not decided on the final form this will take as most of it is not implemented yet. The behaviour might change and break things.
   
   Import implementation similar to actionscript. It functions as described below:
   All imports are relative to as3lib
   Will import the object inside of the package with the name of the package (This is currently the best way that I could think of to emulate what actionscript does)
   namespace must be provided as python's globals are global to each module
   
   Arguements:
      packageName - The name and location (with "." as the path separator) of the package. Does not currently support "*" imports
      namespace - The object in which to import the module into. If "*" is provided as the namespace, name is ignored and the package is returned. EX: if an object called obj is provided, the package will be imported as obj.name
      name - The name that the module will be imported as. If name is not provided and the package is not a "*" import, the last part of the packageName is used.
   """
   pkg = packageName.split(".")
   if pkg[-1] == "*":
      raise NotImplemented("\"*\" imports are not implemented yet")
   else:
      file = as3state.librarydirectory / ("/".join(pkg) + ".py")
      if not file.exists():
         raise Exception(f"Package \"as3lib.{packageName}\" does not exist.")
      if file.is_dir():
         raise NotImplemented("Importing directories as packages is not implemented yet.")
      with open(file,"rb") as f:
         b = (b := f.read())[:b.find(b"\n")].split(b" ")
      if b[0] == b"#?as3package":
         if len(b) == 1: #Import the object inside of the file that is the same as the file name
            package = getattr(__import__(f"as3lib.{'.'.join(pkg)}",globals(),locals(),(pkg[-1]),0),pkg[-1])
            if namespace == "*":
               return package
            if isinstance(namespace,dict) and namespace.get("__name__") != None: #Is a globals() dict
               if name == None:
                  namespace.update({pkg[-1]:package})
               else:
                  namespace.update({name:package})
            elif name == None:
               setattr(namespace,pkg[-1],package)
            else:
               setattr(namespace,name,package)
         else: #!When package has specific place to be
            raise NotImplemented("Packages with specific locations are not implemented.")
         

# Export toplevel and set up miniamf adapters
from as3lib._toplevel.Array import *
from as3lib._toplevel.Boolean import *
from as3lib._toplevel.Constants import *
from as3lib._toplevel.Date import *
from as3lib._toplevel.Errors import *
from as3lib._toplevel.Functions import *
from as3lib._toplevel.int import int as Int
from as3lib._toplevel.JSON import *
from as3lib._toplevel.Math import *
from as3lib._toplevel.Namespace import *
from as3lib._toplevel.Number import *
from as3lib._toplevel.Object import *
from as3lib._toplevel.QName import *
from as3lib._toplevel.RegExp import *
from as3lib._toplevel.String import *
from as3lib._toplevel.trace import *
from as3lib._toplevel.Types import *
from as3lib._toplevel.uint import *
from as3lib._toplevel.Vector import *

__all__ = (
   'formatToString',
   'as3import',

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
   "isValidDirectory"
   "setDataDirectory"
)

