from as3lib import false, Number, Object
from as3lib.helpers import staticproperty


class Mutex(Object):
    def __init__(self):
        raise NotImplementedError

    def lock(self):
        raise NotImplementedError

    def tryLock(self):
        raise NotImplementedError

    def unlock(self):
        raise NotImplementedError


class Condition(Object):
    @staticproperty
    def isSupported(cls):
        return false

    @property
    def mutex(self):
        return self._mutex

    def __init__(self, mutex: Mutex):
        self._mutex = mutex
        raise NotImplementedError

    def notify(self):
        raise NotImplementedError

    def notifyAll(self):
        raise NotImplementedError

    def wait(self, timeout: Number = -1):
        raise NotImplementedError
