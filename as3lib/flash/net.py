from __future__ import annotations
from as3lib import (ArgumentError, Array, as3state, Boolean, Error, false,
                    int, null, Object, ReferenceError, String, TypeError,
                    uint)
from as3lib.flash.events import Event, EventDispatcher
from as3lib.flash.utils import ByteArray
from as3lib.helpers import staticproperty
import builtins
import miniamf
from miniamf import sol


class DatagramSocket(EventDispatcher):
    @property
    def bound(self):
        raise NotImplementedError

    @property
    def connected(self):
        raise NotImplementedError

    @staticproperty
    def isSupported(cls):
        raise NotImplementedError

    @property
    def localAddress(self):
        raise NotImplementedError

    @property
    def localPort(self):
        raise NotImplementedError

    @property
    def remoteAddress(self):
        raise NotImplementedError

    @property
    def remotePort(self):
        raise NotImplementedError

    def __init__(self):
        super().__init__()
        raise NotImplementedError

    def bind(self, localPort: int = 0, localAddress: String = '0.0.0.0'):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def connect(self, remoteAddress: String, remotePort: int):
        raise NotImplementedError

    def receive(self):
        raise NotImplementedError

    def send(self, bytes: ByteArray, offset: uint = 0, length: uint = 0,
             address: String = null, port: int = 0):
        raise NotImplementedError


class FileFilter(Object):
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = String(value)

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, value):
        self._extension = String(value)

    @property
    def macType(self):
        return self._macType

    @macType.setter
    def macType(self, value):
        self._macType = null if macType is null else String(value)

    def __init__(self, description: String, extension: String, macType: String = null):
        self.description = description
        self.extension = extension
        self.macType = macType


class FileReference(EventDispatcher):
    @property
    def creationDate(self):
        return self._creationDate

    @property
    def creator(self):
        return self._creator

    @property
    def data(self):
        return self._data

    @property
    def extension(self):
        return self._extension

    @property
    def modificationDate(self):
        return self._modificationDate

    @property
    def name(self):
        return self._name

    @staticproperty
    def permissionStatus(cls):
        raise NotImplementedError

    @property
    def size(self):
        return self._size

    @property
    def type(self):
        return self._type

    def __init__(self):
        super().__init__()
        self._location = None

    def browse(self, typeFilter: Array = null):
        raise NotImplementedError

    def cancel(self):
        # NOTE: Cancels the 'download' without calling the cancel event
        raise NotImplementedError

    def dowload(self, request: URLRequest, defaultFileName: String = null):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError

    def requestPermission(self):
        raise NotImplementedError

    def save(self, data, defaultFileName: String = null):
        raise NotImplementedError

    def upload(self, request: URLRequest,
               uploadDataFieldName: String = 'FileData',
               testUpload: Boolean = false):
        raise NotImplementedError

    def uploadUnencoded(self, request: URLRequest):
        raise NotImplementedError


class FileReferenceList(EventDispatcher):
    @property
    def fileList(self):
        return self._fileList

    def __init__(self):
        super().__init__()
        self._fileList = Array()

    def browse(self, typeFilter: Array = null):
        raise NotImplementedError


class GroupSpecifier(Object):
    ...


class InterfaceAddress(Object):
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = String(value)

    @property
    def broadcast(self):
        return self._broadcast

    @broadcast.setter
    def broadcast(self, value):
        self._broadcast = String(value)

    @property
    def ipVersion(self):
        return self._ipVersion

    @ipVersion.setter
    def ipVersion(self, value):
        self._ipVersion = String(value)

    @property
    def prefixLength(self):
        return self._prefixLength

    @prefixLength.setter
    def prefixLength(self, value):
        self._prefixLength = int(value)

    def __init__(self):
        super().__init__()
        raise NotImplementedError


class IPVersion(Object):
    IPV4 = String('IPv4')
    IPV6 = String('IPv6')


class LocalConnection(EventDispatcher):
    @property
    def client(self):
        raise NotImplementedError

    @client.setter
    def client(self, value):
        raise NotImplementedError

    @property
    def domain(self):
        raise NotImplementedError

    @property
    def isPerUser(self):
        raise NotImplementedError

    @isPerUser.setter
    def isPerUser(self, value):
        raise NotImplementedError

    @staticproperty
    def isSupported(self):
        raise NotImplementedError

    def __init__(self):
        super().__init__()
        raise NotImplementedError

    def allowDomain(self, *domains):
        raise NotImplementedError

    def allowInsecureDomain(self, *domains):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def connect(self, connectionName: String):
        raise NotImplementedError

    def send(self, connectionName: String, methodName: String, *arguements):
        raise NotImplementedError

class NetConnection(EventDispatcher):
    ...


class NetGroup(EventDispatcher):
    ...


class NetGroupInfo(Object):
    ...


class NetGroupReceiveMode(Object):
    EXACT = String('exact')
    NEAREST = String('nearest')


class NetGroupReplicationStrategy(Object):
    LOWEST_FIRST = String('lowestFirst')
    RAREST_FIRST = String('rarestFirst')


class NetGroupSendMode(String):
    NEXT_DECREASING = String('nextDecreasing')
    NEXT_INCREASING = String('nextIncreasing')


class NetGroupSendResult(Object):
    ERROR = String('error')
    NO_ROUTE = String('no route')
    SENT = String('sent')


class NetMonitor(EventDispatcher):
    ...


class NetStream(EventDispatcher):
    ...


class NetStreamAppendBytesAction(Object):
    END_SEQUENCE = String('endSequence')
    RESET_BEGIN = String('resetBegin')
    RESET_SEEK = String('resetSeek')


class NetStreamInfo(Object):
    ...


class NetStreamMulticastInfo(Object):
    ...


class NetStreamPlayOptions(EventDispatcher):
    ...


class NetStreamPlayTransitions(Object):
    APPEND = String('append')
    APPEND_AND_WAIT = String('appendAndWait')
    RESET = String('reset')
    RESUME = String('resume')
    STOP = String('stop')
    SWAP = String('swap')
    SWITCH = String('switch')


class NetworkInfo(EventDispatcher):
    ...


class NetworkInterface(Object):
    ...


class ObjectEncoding(Object):
    @staticproperty
    def dynamicPropertyWriter(self):
        raise NotImplementedError

    @dynamicPropertyWriter.setter
    def dynamicPropertyWriter(self, value):
        raise NotImplementedError

    AMF0 = uint(0)
    AMF3 = uint(3)
    DEFAULT = uint(3)


class Responder(Object):
    ...


class Socket(EventDispatcher):
    ...


class SecureSocket(Socket):
    ...


class ServerSocket(EventDispatcher):
    ...


class SharedObject(EventDispatcher):
    # TODO: Implement remote shared objects
    _defaultObjectEncoding = ObjectEncoding.DEFAULT
    _preventBackup = false

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    @property
    def data(self):
        return self._data

    @staticproperty
    def defaultObjectEncoding(cls):
        return cls._defaultObjectEncoding

    @defaultObjectEncoding.setter
    def defaultObjectEncoding(cls, value):
        cls._defaultObjectEncoding = uint(value)

    @property
    def fps(self):
        raise NotImplementedError

    @fps.setter
    def fps(self, value):
        # NOTE: Write only
        raise NotImplementedError

    @property
    def objectEncoding(self):
        return self._objectEncoding

    @objectEncoding.setter
    def objectEncoding(self, value):
        self._objectEncoding = uint(value)

    @staticproperty
    def preventBackup(cls):
        return cls._preventBackup

    @preventBackup.setter
    def preventBackup(cls, value):
        cls._preventBackup = Boolean(value)

    @property
    def size(self):
        return uint(len(self._getEncoded()))

    def _getEncoded(self):
        return sol.encode(str(self._name), self._data, encoding=builtins.int(self.objectEncoding))

    def __init__(self):
        self.objectEncoding = SharedObject.defaultObjectEncoding
        self.client = self
        super().__init__()
        self._name = null
        self._path = null
        self._data = {}

    def clear(self):
        self._path.unlink(missing_ok=True)
        self_data.clear()

    def close(self):
        raise NotImplementedError

    def connect(self, myConnection: NetConnection, params: String = null):
        raise NotImplementedError

    def flush(self, minDiskSpace: int = 0):
        with self._path.open('wb+') as f:
            f.write(self._getEncoded().getvalue())
        ...
        return SharedObjectFlushStatus.FLUSHED

    @staticmethod
    def getLocal(name: String, localPath: String = null,
                 secure: Boolean = false):
        # gets local shared object; if object exists, set path and load it. if not, just set path
        # localPath is relative to as3state.appdatadirectory
        name = String(name)
        localPath = String() if localPath is null else String(localPath)
        secure = Boolean(secure)
        obj = SharedObject()
        obj._name = name
        obj._path = as3state.appdatadirectory / str(localPath).strip('/\\') / f'{name}.sol'
        if obj._path.is_file():
            with obj._path.open('rb') as f:
                obj._data = dict(sol.load(f))
        return obj

    @staticmethod
    def getRemote(name: String, remotePath: String = null,
                  persistance: Object = false, secure: Boolean = false):
        raise NotImplementedError

    def send(self, *arguments):
        raise NotImplementedError

    def setDirty(self, propertyName: String):
        raise NotImplementedError

    def setProperty(self, propertyName: String, value: Object = null):
        raise NotImplementedError


class SharedObjectFlushStatus(Object):
    FLUSHED = String('flushed')
    PENDING = String('pending')


class URLLoader(EventDispatcher):
    ...


class URLLoaderDataFormat(Object):
    BINARY = String('binary')
    TEXT = String('text')
    VARIABLES = String('variables')


class URLRequest(Object):
    ...


class URLRequestDefaults(Object):
    ...


class URLRequestHeader(Object):
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = String(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = String(value)

    def __init__(self, name: String = '', value: String = ''):
        self.name = name
        self.value = value


class URLRequestMethod(Object):
    DELETE = String('delete')
    GET = String('get')
    HEAD = String('head')
    OPTIONS = String('options')
    POST = String('post')
    PUT = String('put')


class URLStream(EventDispatcher):
    ...


class URLVariables(Object):
    ...


class XMLSocket(EventDispatcher):
    ...


def getClassByAlias(aliasName: String):
    try:
        return miniamf.get_class_alias(aliasName)
    except miniamf.UnknownClassAlias:
        raise ReferenceError(f'Alias {aliasName} was not registered.')


def navigateToURL(request: URLRequest, window: String = null):
    raise NotImplementedError


def registerClassAlias(aliasName: String, classObject):
    if aliasName is None or classObject is None:
        raise TypeError('Arguements to registerClassAlias can not be null.')
    miniamf.register_class(classObject, aliasName)


def sendToURL(request: URLRequest):
    raise NotImplementedError
