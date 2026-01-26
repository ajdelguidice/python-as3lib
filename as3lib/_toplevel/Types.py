# WARNING: This file will likely be removed in the future. Python types act
#          too differenly to work properly in some cases so having these as
#          annotations can be misleading.
from as3lib._toplevel.Array import Array
from as3lib._toplevel.Boolean import Boolean
from as3lib._toplevel.Constants import undefined, null
from as3lib._toplevel.int import int, uint
from as3lib._toplevel.Number import Number
from as3lib._toplevel.String import String
from as3lib._toplevel.Vector import Vector
import builtins
from typing import Union
from types import NoneType

allNumber = Union[builtins.int, float, int, uint, Number]
allInt = Union[builtins.int, int, uint]
allString = Union[str, String]
allArray = Union[list, tuple, Array, Vector]
allBoolean = Union[bool, Boolean]
allNone = Union[undefined, null, NoneType]
