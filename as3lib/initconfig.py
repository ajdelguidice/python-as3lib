import platform, subprocess, configparser
from . import configmodule
from pathlib import Path

if platform.system() == "Windows":
   from os import getlogin
   import ctypes
   try:
      import win32api
   except:
      configmodule.initerror.append((3,"pywin32 is required for operation on Windows but is either not installed or not accessible."))
elif platform.system() in ("Linux","Darwin"):
   from os import getuid
   from pwd import getpwuid

"""
initerror list
1: platform not implemented yet
2: (Linux specific) display manager type not found (expected x11 or wayland)
3: requirement not found
"""

def defaultTraceFilePath_Flash(versionOverride:bool=False,overrideSystem:str=None,overrideVersion:str=None):
   """
   Outputs the defualt file path for trace as defined by https://web.archive.org/web/20180227100916/helpx.adobe.com/flash-player/kb/configure-debugger-version-flash-player.html
   Since anything earlier than Windows 7 isn't supported by python 3, you normally wouldn't be able to get the file path for these systems but I have included an optional parameter to force this function to return it.
   """
   if configmodule.platform == "Windows":
      username = getlogin()
   elif configmodule.platform in ("Linux","Darwin"):
      username = getpwuid(getuid())[0]
   if versionOverride == True:
      if overrideSystem == "Linux":
         return fr"/home/{username}/.macromedia/Flash_Player/Logs/flashlog.txt"
      elif overrideSystem == "Darwin":
         return fr"/Users/{username}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt"
      elif overrideSystem == "Windows":
         if overrideVersion in ("95","98","ME","XP"):
            return fr"C:\Documents and Settings\{username}\Application Data\Macromedia\Flash Player\Logs\flashlog.txt"
         elif overrideVersion in ("Vista","7","8","8.1","10","11"):
            return fr"C:\Users\{username}\AppData\Roaming\Macromedia\Flash Player\Logs\flashlog.txt"
   elif configmodule.platform == "Linux":
      return fr"/home/{username}/.macromedia/Flash_Player/Logs/flashlog.txt"
   elif configmodule.platform == "Windows":
      return fr"C:\Users\{username}\AppData\Roaming\Macromedia\Flash Player\Logs\flashlog.txt"
   elif configmodule.platform == "Darwin":
      return fr"/Users/{username}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt"

def sm_x11():
   """
   Gets and returns screen width, screen height, refresh rate, and color depth on x11
   """
   xr = f'{subprocess.check_output("xrandr --current", shell=True)}'.split("\\n")
   for option in xr:
      if option.find("*") != -1:
         curop = option.split(" ")
         break
   ops = []
   for i in curop:
      if i != "":
         ops.append(i)
   ops.pop(0)
   for i in ops:
      if i.find("*") != -1:
         temprr = i.replace("*","").replace("+","")
         break
   cdp = f'{subprocess.check_output("xwininfo -root | grep Depth", shell=True)}'.replace("\\n","").replace("b'","").replace(" ","").replace("'","").split(":")[1]
   tempwidth = f'{subprocess.check_output("xwininfo -root | grep Width", shell=True)}'.replace("\\n","").replace("b'","").replace(" ","").replace("'","").split(":")[1]
   tempheight = f'{subprocess.check_output("xwininfo -root | grep Height", shell=True)}'.replace("\\n","").replace("b'","").replace(" ","").replace("'","").split(":")[1]
   return int(tempwidth),int(tempheight),float(temprr),int(cdp)

def sm_wayland():
   configpath = configmodule.librarydirectory / "wayland.cfg"
   if configpath.exists() == True:
      with open(configpath, 'r') as f:
         configwithheader = f.read()
      config = configparser.ConfigParser()
      config.read_string(configwithheader)
      actual_config = config["Screen"]
      existing_options = ["screenwidth" in actual_config,"screenheight" in actual_config,"refreshrate" in actual_config,"colordepth" in actual_config]
      if existing_options[0] == True:
         sw = int(actual_config["screenwidth"])
      else:
         sw = 1600
      if existing_options[1] == True:
         sh = int(actual_config["screenheight"])
      else:
         sh = 900
      if existing_options[2] == True:
         rr = float(actual_config["refreshrate"])
      else:
         rr = 60.00
      if existing_options[3] == True:
         cd = int(actual_config["colordepth"])
      else:
         cd = 8
   else:
      print("(The things that these answers controls is not implemented yet) This seems to be your first time using the module as3lib. Since you are using wayland, some things could not be automatically detected. Please input them in the fields bellow. This information is a part of the flash display module, if you aren't planning to use that, you can put in whatever you want. This information can be configured later in the file <library directory>/wayland.cfg")
      sw = input("Maximum width (px), or -1 for no limit: ")
      sh = input("Maximum height (px), or -1 for no limit: ")
      rr = input("Refresh rate (Hz): ")
      cd = input("Color depth (bits): ")
      with open(configpath, "w") as cfg:
         cfg.write(f"[Screen]\nscreenwidth={int(sw)}\nscreenheight={int(sh)}\nrefreshrate={float(rr)}\ncolordepth={int(cd)}")
   return int(sw), int(sh), float(rr), int(cd)

def sm_windows():
   #temp = []
   settings = win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1)
   #for i in ('BitsPerPel', 'DisplayFrequency'):
   #   temp.append(getattr(settings, i))
   temp = (getattr(settings,i) for i in ('BitsPerPel', 'DisplayFrequency'))
   return int(ctypes.windll.user32.GetSystemMetrics(0)), int(ctypes.windll.user32.GetSystemMetrics(1)), float(temp[1]), int(temp[0])

def sm_darwin():
   pass

def getSeparator():
   if configmodule.platform == "Windows":
      return "\\"
   return "/"

def getDesktopDir():
   #!Use $XDG_DESKTOP_DIR on linux
   return configmodule.userdirectory / "Desktop"

def getDocumentsDir():
   #!Use $XDG_DOCUMENTS_DIR on linux
   return configmodule.userdirectory / "Documents"

def getdmtype():
   temp = str(subprocess.check_output("loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Type", shell=True))
   if temp[:2] == "b'" and temp[-1:] == "'":
      temp = temp[2:-1]
   temp = temp.split("\\n")
   for i in temp:
      if len(i) > 0:
         temp2 = i.split("=")[-1]
         if temp2 in ("x11","wayland"):
            return temp2
   return "error"

def getdmname():
   temp = str(subprocess.check_output("loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Desktop",shell=True))
   if temp[:2] == "b'" and temp[-1:] == "'":
      temp = temp[2:-1]
   temp = temp.split("\\n")
   for i in temp:
      if len(i) > 0:
         temp2 = i.split("=")[-1]
         if len(temp2) > 0:
            return temp2.lower()
   return "error"

def dependencyCheck():
   if configmodule.platform == "Linux":
      wmt = str(subprocess.check_output("echo $XDG_SESSION_TYPE",shell=True))[2:].replace("\\n'","")
      if wmt == "wayland":
         x=0
      else:
         try:
            subprocess.check_output("which xwininfo",shell=True)
         except:
            configmodule.initerror.append((3,"linux xorg requirement 'xwininfo' not found"))
         try:
            subprocess.check_output("which xrandr",shell=True)
         except:
            configmodule.initerror.append((3,"linux xorg requirement 'xrandr' not found"))
      try:
         subprocess.check_output("which bash",shell=True)
      except:
         configmodule.initerror.append((3,"linux requirement 'bash' not found"))
      try:
         subprocess.check_output("which awk",shell=True)
      except:
         configmodule.initerror.append((3,"linux requirement 'awk' not found"))
      try:
         subprocess.check_output("which whoami",shell=True)
      except:
         configmodule.initerror.append((3,"linux requirement 'whoami' not found"))
      try:
         subprocess.check_output("which loginctl",shell=True)
      except:
         configmodule.initerror.append((3,"linux requirement 'loginctl' not found"))
      try:
         subprocess.check_output("which echo",shell=True)
         if str(subprocess.check_output("echo test",shell=True)).replace("\\n","")[2:-1] != "test":
            raise
      except:
         configmodule.initerror.append((3,"linux requirement 'echo' not found"))
   elif configmodule.platform == "Windows":
      pass
   elif configmodule.platform == "Darwin":
      pass
   #<a href="https://pypi.org/project/numpy">numpy</a>
   #<a href="https://pypi.org/project/Pillow">Pillow</a>
   #<a href="https://pypi.org/project/tkhtmlview">tkhtmlview</a>

def initconfig():
   #set up variables needed by mutiple modules
   configmodule.librarydirectory = Path(__file__).resolve().parent
   configmodule.platform = platform.system()
   dependencyCheck()
   configmodule.separator = getSeparator()
   configmodule.userdirectory = Path.home()
   configmodule.desktopdirectory = getDesktopDir()
   configmodule.documentsdirectory = getDocumentsDir()
   configmodule.defaultTraceFilePath = configmodule.librarydirectory / "flashlog.txt"
   configmodule.defaultTraceFilePath_Flash = defaultTraceFilePath_Flash()
   configmodule.pythonversion = platform.python_version()
   if configmodule.platform == "Linux":
      configmodule.windowmanagertype = getdmtype()
      configmodule.dmname = getdmname()
      if configmodule.windowmanagertype == "x11":
         temp = sm_x11()
         configmodule.width = temp[0]
         configmodule.height = temp[1]
         configmodule.refreshrate = temp[2]
         configmodule.colordepth = temp[3]
      elif configmodule.windowmanagertype == "wayland":
         temp = sm_wayland()
         configmodule.width = temp[0]
         configmodule.height = temp[1]
         configmodule.refreshrate = temp[2]
         configmodule.colordepth = temp[3]
      else:
         configmodule.initerror.append((2,f"windowmanagertype \"{configmodule.windowmanagertype}\" not supported"))
   elif configmodule.platform == "Windows":
      temp = sm_windows()
      configmodule.width = temp[0]
      configmodule.height = temp[1]
      configmodule.refreshrate = temp[2]
      configmodule.colordepth = temp[3]
   elif configmodule.platform == "Darwin":
      configmodule.initerror.append((1,"Error fetching screen properties; Darwin; Not Implemented Yet"))
      #configmodule.width = temp[0]
      #configmodule.height = temp[1]
      #configmodule.refreshrate = temp[2]
      #configmodule.colordepth = temp[3]
      pass
   configpath = configmodule.librarydirectory / "mm.cfg"
   if configpath.exists() == True:
      with open(configpath, 'r') as f:
         configwithheader = '[dummy_section]\n' + f.read()
      config = configparser.ConfigParser()
      config.read_string(configwithheader)
      actual_config = config["dummy_section"]
      existing_options = ["ErrorReportingEnable" in actual_config,"MaxWarnings" in actual_config,"TraceOutputFileEnable" in actual_config,"TraceOutputFileName" in actual_config,"ClearLogsOnStartup" in actual_config]
      if existing_options[0] == True:
         configmodule.ErrorReportingEnable = int(actual_config["ErrorReportingEnable"])
      if existing_options[1] == True:
         configmodule.MaxWarnings = int(actual_config["MaxWarnings"])
      if existing_options[2] == True:
         configmodule.TraceOutputFileEnable = int(actual_config["TraceOutputFileEnable"])
      if existing_options[3] == True:
         configmodule.TraceOutputFileName = actual_config["TraceOutputFileName"]
      if existing_options[4] == True:
         configmodule.ClearLogsOnStartup = int(actual_config["ClearLogsOnStartup"])
   if configmodule.TraceOutputFileName == "":
      configmodule.TraceOutputFileName = configmodule.defaultTraceFilePath
   if Path(configmodule.TraceOutputFileName).is_dir() == True:
      print("Path provided is a directory, writing to defualt location instead.")
      configmodule.TraceOutputFileName = configmodule.defaultTraceFilePath
   if configmodule.ClearLogsOnStartup == 1:
      if Path(configmodule.TraceOutputFileName).exists() == True:
         with open(configmodule.TraceOutputFileName, "w") as f: 
            f.write("")

   #Report errors to user
   if len(configmodule.initerror) != 0:
      print(f"Warning: as3lib has initialized with errors, some functionality might be broken.\n{''.join((f"\tType={i[0]}; Message={i[1]}\n" for i in configmodule.initerror))}")
   
   #Tell others that library has been initialized
   configmodule.initdone = True
