from as3lib import Object


class PermissionStatus(Object):
    DENIED = 'denied'
    GRANTED = 'granted'
    ONLY_WHEN_IN_USE = 'onlyWhenInUse'
    UNKNOWN = 'unknown'
