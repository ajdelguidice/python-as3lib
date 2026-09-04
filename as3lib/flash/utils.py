from __future__ import annotations
from as3lib import (ArgumentError, as3state, Boolean, Error, false, int, null,
                    Number, Object, String, true, TypeError, uint, undefined)
from as3lib.flash.errors import EOFError, IOError
from as3lib.flash.events import EventDispatcher, TimerEvent
import builtins
from miniamf import util
from miniamf.amf3 import ByteArray as _ByteArray
from threading import Timer as timedExec


def _INTERVAL_ID_GEN():
    # Can't use the python id here because it can be over the limit of a uint
    i = uint(0)
    while True:
        yield i
        i += 1


_NEW_INTERVAL_ID = _INTERVAL_ID_GEN()


def clearInterval(id: uint):
    as3state.intervals[uint(id)].clear()


def clearTimeout(id: uint):
    as3state.intervals[uint(id)].clear()


def describeType(value):
    raise NotImplementedError


def escapeMultiByte(value: String):
    raise NotImplementedError


def getDefinitionByName(name: String):
    raise NotImplementedError


def getQualifiedClassName(value):
    raise NotImplementedError


def getQualifiedSuperclassName(value):
    raise NotImplementedError


def getTimer():
    return int(util.utcnow().timestamp()) * 1000 - as3state.startTime


class _INTERVAL_TIMER:
    def __init__(self, delay, function, args, id):
        self.delay = delay/1000
        self.func = function
        self.func_args = args
        self.id = id
        as3state.intervals[id] = self
        self.start()

    def _tick(self):
        del self._timer
        self.start()
        self.func(*self.func_args)

    def start(self):
        self._timer = timedExec(self.delay, self._tick)
        self._timer.start()

    def clear(self):
        self._timer.cancel()
        del as3state.intervals[self.id]


def setInterval(closure: callable, delay: Number, *arguements):
    id = next(_NEW_INTERVAL_ID)
    _INTERVAL_TIMER(uint(delay), closure, arguements, id)
    return id


class _TIMEOUT_TIMER(_INTERVAL_TIMER):
    def _tick(self):
        self.func(*self.func_args)
        del as3state.intervals[self.id]


def setTimeout(closure: callable, delay: Number, *arguements):
    id = next(_NEW_INTERVAL_ID)
    _TIMEOUT_TIMER(uint(delay), closure, arguements, id)
    return id


def unescapeMultiByte(value: String):
    raise NotImplementedError


class IDataInput:
    ...


class IDataOutput:
    ...


class ByteArray(_ByteArray):
    defaultObjectEncoding = 3  # This can be set globally

    @property
    def bytesAvailable(self):
        return uint(self.remaining())

    @property
    def endian(self):
        return String(super().endian)

    @endian.setter
    def endian(self, endian: String):
        # TODO: Error messages
        if endian is null:
            raise TypeError('', 2007)
        endian = String(endian)
        # if endian not in Endian:
        if endian not in {Endian.BIG_ENDIAN, Endian.LITTLE_ENDIAN}:
            raise ArgumentError('', 2008)
        super().endian = endian

    @property
    def length(self):
        return uint(len(self))

    @length.setter
    def length(self, value: int):
        raise NotImplementedError

    @property
    def position(self):
        return self.tell()

    @position.setter
    def position(self, value):
        self.seek(value)

    @property
    def shareable(self):
        return self._sharable

    @shareable.setter
    def shareable(self, value: Boolean):
        self._sharable = Boolean(value)

    def __init__(self, data=None):
        super().__init__(data)
        self.objectEncoding = ByteArray.defaultObjectEncoding  # This currently does nothing

    def __repr__(self):
        return f'ByteArray({self.getvalue()})'

    def atomicCompareAndSwapIntAt(self, byteIndex: int, expectedValue: int, newValue: int):
        if byteIndex % 4 != 0 or byteIndex < 0:
            raise ArgumentError('ByteArray.atomicCompareAndSwapIntAt; byteIndex must be a multiple of 4 and can not be negative.')
        raise NotImplementedError

    def atomicCompareAndSwapLength(self, expectedLength: int, newLength: int):
        '''
        In a single atomic operation, compares this byte array's length with a provided value and, if they match, changes the length of this byte array.

        This method is intended to be used with a byte array whose underlying memory is shared between multiple workers (the ByteArray instance's shareable property is true). It does the following:

            1) Reads the integer length property of the ByteArray instance
            2) Compares the length to the value passed in the expectedLength argument
            3) If the two values are equal, it changes the byte array's length to the value passed as the newLength parameter, either growing or shrinking the size of the byte array
            4) Otherwise, the byte array is not changed

        All these steps are performed in one atomic hardware transaction. This guarantees that no operations from other workers make changes to the contents of the byte array during the compare-and-resize operation.

        Parameters
            expectedLength:int — the expected value of the ByteArray's length property. If the specified value and the actual value match, the byte array's length is changed.
            newLength:int — the new length value for the byte array if the comparison succeeds
        Returns
            int — the previous length value of the ByteArray, regardless of whether or not it changed
        '''
        oldlen = self.length
        if self.length == expectedLength:
            self.length = newLength
        return oldlen

    def clear(self):
        'Clears the contents of the byte array and resets the length and position properties to 0. Calling this method explicitly frees up the memory used by the ByteArray instance.'
        self.truncate(0)

    def compress(self, algorithm: String):
        # TODO: Error messages
        if algorithm is null:
            raise TypeError('', 2007)
        algorithm = String(algorithm)
        # if algorithm not in CompressionAlgorithm:
        if algorithm not in {CompressionAlgorithm.DEFLATE, CompressionAlgorithm.LZMA, CompressionAlgorithm.ZLIB}:
            raise IOError('', 2058)
        if algorithm != 'zlib':
            raise NotImplementedError('The underlying stream currently only supports zlib compression.')
        self.compressed = True

    def deflate(self):
        raise NotImplementedError

    def inflate(self):
        raise NotImplementedError

    def readBytes(self, bytes: ByteArray, offset: uint = 0, length: uint = 0):
        bytes.seek(offset)
        bytes.write(self.read(length))

    def toJSON(self, k: String):
        return String('ByteArray')

    def toString(self):
        raise NotImplementedError

    def uncompress(self, algorithm: String):
        # TODO: Error messages
        if algorithm is null:
            raise TypeError('', 2007)
        algorithm = String(algorithm)
        # if algorithm not in CompressionAlgorithm:
        if algorithm not in {CompressionAlgorithm.DEFLATE, CompressionAlgorithm.LZMA, CompressionAlgorithm.ZLIB}:
            raise IOError('', 2058)
        if algorithm != 'zlib':
            raise NotImplementedError('The underlying stream currently only supports zlib compression.')
        self.compressed = False

    def writeBytes(self, bytes: ByteArray, offset: uint = 0, length: uint = 0):
        startpos = bytes.tell()
        bytes.seek(offset)
        self.write(bytes.read(length))
        bytes.seek(startpos)  # !I don't know if it is supposed to do this


class CompressionAlgorithm(Object):
    DEFLATE = String('deflate')
    LZMA = String('lzma')
    ZLIB = String('zlib')


class Dictionary(Object):
    # TODO: weak keys
    def __init__(self, weakKeys: Boolean = false):
        if weakKeys:
            raise NotImplementedError
        self._useWeakKeys = Boolean(weakKeys)
        self._dict = {}
        # The weak keys must be in a separate dict because string keys are never
        # weak.
        self._weakDict = None  # TODO

    def _canCoerce(self, obj):
        if isinstance(obj, (int, uint, Number, Boolean, str, bool, builtins.int, float)) or obj is undefined or obj is null:
            return True
        return False

    def _getKey(self, item):
        if self._canCoerce(item):
            return str(item)
        return item

    def __getitem__(self, item):
        return self._dict.get(self._getKey(item))

    def __setitem__(self, item, value):
        self._dict[self._getKey(item)] = value

    def __delitem__(self, item):
        del self._dict[self._getKey(item)]

    def __contains__(self, item):
        return self._getKey(item) in self._dict

    def __iter__(self):
        return iter(list(self._dict.keys()))

    def __each__(self):
        return self._dict.values()

    def toJSON(self, k: String):
        return String('Dictionary')


class Endian(Object):
    BIG_ENDIAN = String('bigEndian')
    LITTLE_ENDIAN = String('littleEndian')


class Timer(EventDispatcher):
    # TODO: Fix timer being broken with short delays
    @property
    def currentCount(self):
        return self._currentCount

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, number_ms: Number):
        if self.running:
            self.stop()
            self._delay = Number(number_ms)
            self.start()
        else:
            self._delay = Number(number_ms)

    @property
    def repeatCount(self):
        return self._repeatCount

    @repeatCount.setter
    def repeatCount(self, number: int):
        # If repeatCount is set to a total that is the same or less then currentCount the timer stops and will not fire again.
        number = int(number)
        if number <= self._currentCount:
            self.stop()
        self._repeatCount = number

    @property
    def running(self):
        return self._running

    def _TimerTick(self):
        self._currentCount += 1
        del self._timer
        if self.currentCount >= self.repeatCount and self.repeatCount != 0:
            self.dispatchEvent(TimerEvent('timer'))
            self.dispatchEvent(TimerEvent('timerComplete'))
            self._running = false
        else:
            self._timer = timedExec(self.delay/1000, self._TimerTick)
            self._timer.start()
            self.dispatchEvent(TimerEvent('timer'))

    def __init__(self, delay: Number, repeatCount: int = 0):
        super().__init__()
        self._currentCount = int(0)
        self._running = false
        delay = Number(delay)
        if delay < 0:
            raise Error()
        self.delay = delay
        self.repeatCount = repeatCount

    def reset(self):
        self.stop()
        self._currentCount = int(0)

    def start(self):
        if not self.running and (self.currentCount < self.repeatCount or self.repeatCount == 0):
            self._timer = timedExec(self.delay/1000, self._TimerTick)
            self._running = true
            self._timer.start()

    def stop(self):
        if self.running:
            self._timer.cancel()
            del self._timer
            self._running = false
