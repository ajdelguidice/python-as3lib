#Adapters for miniamf

from functools import partial
from . import toplevel
from miniamf import add_type

def adapter(func, obj, encoder):
    return func(obj)


add_type(toplevel.Array, partial(adapter,list))
add_type(toplevel.Boolean, partial(adapter,bool))
add_type(toplevel.int, partial(adapter,int))
add_type(toplevel.Number, partial(adapter,float))
add_type(toplevel.String, partial(adapter,str))
add_type(toplevel.uint, partial(adapter,int))
