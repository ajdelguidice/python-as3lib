import sys, resource
from . import toplevel as as3

def help():
    return "This module inlcudes many things that might be useful when using this library but aren't in actionscript. EX: a helper for increasing python's maximum recursion depth."

class recursionDepth:
    #used like "with recursionDepth(Number):"
    def __init__(self, limit):
        self.limit = limit
    def __enter__(self):
        self.olimit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.limit)
    def __exit__(self, *args):
        sys.setrecursionlimit(self.olimit)
    @staticmethod
    def set(limit):
        sys.setrecursionlimit(limit)
    @staticmethod
    def get():
        return sys.getrecursionlimit()

class stackLimit:
    #used like "with stackLimit(Number):". DOES NOT CHANGE THE HARD LIMIT as that could be dangerous
    def __init__(self, limit):
        if limit == as3.Infinity:
            self.limit = resource.RLIM_INFINITY
        else:
            if (resource.getrlimit(resource.RLIMIT_STACK)[1] == resource.RLIM_INFINITY or limit < resource.getrlimit(resource.RLIMIT_STACK)[1]) and limit > 0:
                self.limit = limit
            else:
                self.limit = resource.getrlimit(resource.RLIMIT_STACK)[0]
    def __enter__(self):
        self.olimit = resource.getrlimit(resource.RLIMIT_STACK)
        resource.setrlimit(resource.RLIMIT_STACK, (self.limit,self.olimit[1]))
    def __exit__(self, *args):
        resource.setrlimit(resource.RLIMIT_STACK, self.olimit)
    @staticmethod
    def set(limit):
        if limit == as3.Infinity:
            limit = resource.RLIM_INFINITY
        else:
            if (resource.getrlimit(resource.RLIMIT_STACK)[1] == resource.RLIM_INFINITY or limit < resource.getrlimit(resource.RLIMIT_STACK)[1]) and limit > 0:
                resource.setrlimit(resource.RLIMIT_STACK, (limit,resource.getrlimit(resource.RLIMIT_STACK)[1]))
    @staticmethod
    def get():
        return resource.getrlimit(resource.RLIMIT_STACK)
