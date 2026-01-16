from as3lib._toplevel.BaseTypes import (Array, Boolean, int, null, Number,
                                        String, undefined, uint, Vector)
import builtins
from typing import Union
from types import NoneType


allNumber = Union[builtins.int, float, int, uint, Number]
allInt = Union[builtins.int, int, uint]
allString = Union[str, String]
allArray = Union[list, tuple, Array, Vector]
allBoolean = Union[bool, Boolean]
allNone = Union[undefined, null, NoneType]
