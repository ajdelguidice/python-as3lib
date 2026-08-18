from as3lib import Boolean, Object, String
from as3lib.flash.display import DisplayObjectContainer
from as3lib.flash.events import Event, EventDispatcher


class IKArmature(Object):
    @property
    def container(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    @property
    def rootJoint(self):
        raise NotImplementedError

    @property
    def springsEnabled(self):
        return self._springsEnabled

    @springsEnabled.setter
    def springsEnabled(self, value):
        self._springsEnabled = Boolean(value)

    def getBoneByName(targetName: String):
        raise NotImplementedError

    def registerElements(container: DisplayObjectContainer):
        raise NotImplementedError


class IKBone(Object):
    @property
    def headJoint(self):
        raise NotImplementedError

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = String(value)

    @property
    def tailJoint(self):
        raise NotImplementedError


class IKEvent(Event):
    DISTANCE_LIMIT = String('distanceLimit')
    ITERATION_LIMIT = String('iterationLimit')
    SINGLE_STEP = String('singleStep')
    TIME_LIMIT = String('timeLimit')

    @property
    def distance(self):
        raise NotImplementedError

    @property
    def iterationCount(self):
        raise NotImplementedError

    @property
    def joint(self):
        raise NotImplementedError

    @property
    def time(self):
        raise NotImplementedError


class IKJoint(Object):
    ...


class IKManager(EventDispatcher):
    ...


class IKMover(EventDispatcher):
    ...
