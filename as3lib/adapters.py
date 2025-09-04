#Adapters for miniamf

from functools import partial
import as3lib
from miniamf import add_type

def adapter(func, obj, encoder):
    return func(obj)


add_type(as3lib.Array, partial(adapter,list))
add_type(as3lib.Boolean, partial(adapter,bool))
add_type(as3lib.int, partial(adapter,int))
add_type(as3lib.Number, partial(adapter,float))
add_type(as3lib.String, partial(adapter,str))
add_type(as3lib.uint, partial(adapter,int))
