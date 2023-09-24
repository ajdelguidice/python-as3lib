import platform, subprocess
from . import configmodule
import configparser
from pathlib import Path
from os.path import dirname
from os import getuid
from pwd import getpwuid

def defaultTraceFilePath():
   """
   Outputs the default file path for trace in this library
   """
   path = dirname(__file__) + "/flashlog.txt"
   return path
def defaultTraceFilePath_Flash(legacyVersionOverride=False):
   """
   Outputs the defualt file path for trace as defined by https://web.archive.org/web/20180227100916/helpx.adobe.com/flash-player/kb/configure-debugger-version-flash-player.html
   Since anything earlier than Windows 7 isn't supported by python 3, you normally wouldn't be able to get the file path for these systems but I have included an optional parameter to force this function to return it.
   """
   username = getpwuid(getuid())[0]
   if legacyVersionOverride == True:
      return r"C:\Documents and Settings" + f"\\{username}\Application Data\Macromedia\Flash Player\Logs\flashlog.txt"
   else:
      if configmodule.platform == "Linux":
         return r"/home/" + f"{username}/.macromedia/Flash_Player/Logs/flashlog.txt"
      elif configmodule.platform == "Windows":
         return r"C:\Users" + f"\\{username}\AppData\Roaming\Macromedia\Flash Player\Logs\flashlog.txt"
      elif configmodule.platform == "Darwin":
         return r"/Users/" + f"{username}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt"

def sm_x11():
   """
   Gets and returns screen width, screen height, refresh rate, and color depth on x11
   """
   xr = str(subprocess.check_output("xrandr --current", shell=True)).split("\\n")
   for option in xr:
      if option.find("*") != -1:
         curop = option
         break
      else:
         continue
   curop = curop.split(" ")
   ops = []
   for i in curop:
      if i == "":
         continue
      else:
         ops.append(i)
   resandref = []
   resandref.append(ops.pop(0))
   for i in ops:
      if i.find("*") != -1:
         resandref.append(i)
      else:
         continue
   tempres = resandref[0].split("x")
   cdp = str(subprocess.check_output("xwininfo -root | grep Depth", shell=True)).replace("\\n","").replace("b'","").replace(" ","").replace("'","").split(":")[1]
   return int(tempres[0]),int(tempres[1]),float(resandref[1].replace("*","").replace("+","")),int(cdp)

def initconfig():
   #set up variables needed by mutiple submodules
   configmodule.defaultTraceFilePath = defaultTraceFilePath()
   configmodule.defaultTraceFilePath_Flash = defaultTraceFilePath_Flash()
   configmodule.platform = platform.system()
   if configmodule.platform == "Linux":
      dmtype = subprocess.check_output("loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Type", shell=True)
      dmtype = str(dmtype).split("=")[1]
      dmtype = dmtype.replace("\\n'","")
      configmodule.windowmanagertype = dmtype
      if configmodule.windowmanagertype == "x11":
         temp = sm_x11()
         configmodule.width = temp[0]
         configmodule.height = temp[1]
         configmodule.refreshrate = temp[2]
         configmodule.colordepth = temp[3]
      elif configmodule.windowmanagertype == "wayland":
         pass
   elif configmodule.platform == "Windows":
      pass
   elif configmodule.platform == "Darwin":
      pass
   if configmodule.platform == "Linux" or configmodule.platform == "Darwin":
      configpath = dirname(__file__) + "/mm.cfg"
      if Path(configpath).exists() == True:
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
   elif configmodule.platform == "Windows":
      configpath = dirname(__file__) + "\mm.cfg"
      if Path(configpath).exists() == True:
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

   #Tell others that module has been initialized
   configmodule.initdone = True
