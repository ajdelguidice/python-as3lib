from . import configmodule, toplevel
import re
from typing import Union
def mouseButtonNameToTkname(name:Union[str, toplevel.String]):
   if configmodule.platform == "Linux":
      if configmodule.windowmanagertype == "x11":
         return Linux_X11.mouseButtonNameToTkname(name)
      elif configmodule.windowmanagertype == "wayland":
         pass
   elif configmodule.platform == "Windows":
      pass
   elif configmodule.platform == "Darwin":
      pass
class Linux_X11:
   def mouseButtonNameToTkname(name:Union[str, toplevel.String]):
      if name == "Left":
         return "<Button-1>"
      elif name == "Middle":
         return "<Button-2>"
      elif name == "Right":
         return "<Button-3>"
   def tkeventToJavascriptKeycode(event):
      temp = [None, None, None, None, None, None, None, None, None, 27, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 189, 187, 8, 9, 81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 219, 221, 13, 17, 65, 83, 68, 70, 71, 72, 74, 75, 76, 186, 222, 192, 16, 220, 90, 88, 67, 86, 66, 78, 77, 188, 190, 191, 16, 106, 18, 32, 20, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 144, 145, 103, 104, 105, 109, 100, 101, 102, 107, 97, 98, 99, 96, 110, None, None, None, 122, 123, None, None, None, None, None, None, None, 13, 17, 111, None, 18, None, 36, 38, 33, 37, 39, 35, 40, 34, 45, 46, None, None, None, None, None, None, None, 19]
      return temp[e.keycode]
class Linux_Wayland:
   pass
class Windows:
   pass
class Darwin_X11:
   def mouseButtonNameToTkname(name:Union[str, toplevel.String]):
      if name == "Left":
         return "<Button-1>"
      elif name == "Middle":
         return "<Button-2>"
      elif name == "Right":
         return "<Button-3>"
   def tkeventToJavascriptKeycode(event):
      pass
class Darwin_Aqua:
   def mouseButtonNameToTkname(name:Union[str, toplevel.String]):
      if name == "Left":
         return "<Button-1>"
      elif name == "Middle":
         return "<Button-3>"
      elif name == "Right":
         return "<Button-2>"
   def tkeventToJavascriptKeycode(event):
      pass
 