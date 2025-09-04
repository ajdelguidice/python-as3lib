import builtins
from typing import Union
from types import NoneType
from as3lib._toplevel.Array import *
from as3lib._toplevel.Boolean import *
from as3lib._toplevel.Constants import *
from as3lib._toplevel.Date import *
from as3lib._toplevel.int import *
from as3lib._toplevel.Number import *
from as3lib._toplevel.String import *
from as3lib._toplevel.uint import *
from as3lib._toplevel.Vector import *

allNumber = Union[builtins.int,float,int,uint,Number]
allInt = Union[builtins.int,int,uint]
allString = Union[str,String]
allArray = Union[list,tuple,Array,Vector]
allBoolean = Union[bool,Boolean]
allNone = Union[undefined,null,NoneType]
