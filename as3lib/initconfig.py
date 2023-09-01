import platform, subprocess
from . import configmodule
def sm_x11():
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

   #Tell others that module has been initialized
   configmodule.initdone = True
