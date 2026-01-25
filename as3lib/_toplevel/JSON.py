from as3lib._toplevel.Constants import null
from as3lib._toplevel.Object import Object


class JSON(Object):
   @staticmethod
   def parse(text, reviver=null):
         raise NotImplementedError

   @staticmethod
   def stringify(value, replacer=null, space=null):
         raise NotImplementedError
