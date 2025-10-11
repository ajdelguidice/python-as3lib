import sys
from pathlib import Path
from importlib.machinery import ModuleSpec


# This module is loosely based off of as3lib-miniAMF's util.imports

class ModuleFinder(object):
   """
   This module finder/importer implements a special import process for modules
   tagged with #?as3import. Tagging modules is done by placing the tag at the
   top of the module right after the shebang line (if included).
   
   #?as3import will only import the class inside the module with the same name.
   Explained simpler, this is like overwritting every instance of
   "import module" with "from module import class"

   @ivar loaded_modules: C{list} of modules that this finder has seen. Used
      to stop recursive imports in L{load_module}
   @ivar special_properties: C{dict} of properties for each module that tags
      itself.
   """

   def __init__(self):
      self.loaded_modules = []
      self.special_properties = {}

   def find_spec(self, fullname, path, target=None):
      """
      Called when an import is made. Retrieves the as3lib tag and sets up the
      "metadata" for each module.

      @param fullname: The name of the module being imported.
      @param path: The root path of the module (if a package).
      @param target: Ignored.
      @return: If the module is tagged, returns a C{ModuleSpec}. If not, return
         C{None} to allow the standard import process to continue.
      """
      if fullname in self.loaded_modules:
         return None
      
      _type = 0

      if path is not None:
         filename = fullname.split('.')[-1]
         p = Path(path[0]) / (filename + '.py')
         if p.exists():
            with open(p, 'r') as f:
               while True:
                  line = f.readline()
                  if line.startswith('#!'):  # Skip shebang
                     continue
                  elif line.startswith('#?as3import'):  # Only import class with the same name as the module
                     _type = 1
                  else:
                     break

      if _type:
         self.special_properties[fullname] = [_type, filename]
         return ModuleSpec(fullname, self)

   def create_module(self, spec):
      name = spec.name
      self.loaded_modules.append(name)
      prop = self.special_properties.get(name, None)

      try:
         if prop and prop[0] == 1:
            temp = __import__(name, {}, {}, prop[1])
            sys.modules[name] = getattr(temp, prop[1])
      except Exception as e:
         self.loaded_modules.pop()

         raise e

      return sys.modules[name]
   
   def exec_module(self, module):...


def _init():
   """
   Internal function to install the module finder.
   """
   global finder

   if finder is None:
      finder = ModuleFinder()

   if finder not in sys.meta_path:
      sys.meta_path.insert(0, finder)


finder = None
_init()
