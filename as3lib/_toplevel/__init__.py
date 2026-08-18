from __future__ import annotations
import builtins
from ctypes import c_double, c_uint16, c_uint32, c_int32
import datetime
from functools import cmp_to_key, wraps
from io import StringIO
import math
import random
import re as regex
import sys
import time
import traceback

from .. import as3state
from as3lib._toplevel.trace import errorTrace
from as3lib.helpers import function


# Internal Helpers
def _getTimezone():  # Date
    if time.daylight:
        return datetime.timezone(datetime.timedelta(seconds=-time.altzone), time.tzname[1])
    return datetime.timezone(datetime.timedelta(seconds=-time.timezone), time.tzname[0])


def _errNumGen():  # Error
    i = 0
    while True:
        yield i
        i += 1


_genErrorID = _errNumGen()


def _exponentFixNum(value):  # Number
    if value.find('e') != -1:
        a, b = value.split('e')
        return ('%se{:+d}' % a).format(builtins.int(b))
    return value


_base_digits = '0123456789abcdefghijklmnopqrstuvwxyz'


def _as_base(num, radix):  # int
    if num == 0:
        return '0'
    digits = []
    temp = abs(num)
    while temp > 0:
        digits.append(_base_digits[temp % radix])
        temp //= radix
    if num < 0:
        digits.append('-')
    digits.reverse()
    return ''.join(digits)


def _exponentFixInt(value):  # int
    if value.find('e') != -1:
        a, b = value.split('e')
        bi = builtins.int(b)
        if bi == 0:
            return a
        if b.startswith('+'):
            return '%se+%i' % (a, bi)
        return '%se%i' % (a, bi)
    return value


# Classes
class undefined:
    __slots__ = tuple()

    def __init__(self):
        pass

    def __int__(self):
        return 0

    def __str__(self):
        return str(self.toString())

    def __repr__(self):
        return str(self.toString())

    def __bool__(self):
        return False

    def __neg__(self):
        return NaN

    def __iter__(self):
        return iter([])

    def __add__(self, value):
        if isinstance(value, (String, str)):
            return self.toString().concat(value)
        return NaN

    def __sub__(self, value):
        return NaN

    def __mul__(self, value):
        return NaN

    def __truediv__(self, value):
        return NaN

    def __mod__(self, value):
        return NaN

    def __lshift__(self, value):
        # TODO: Check return type
        return int(0)

    def __rshift__(self, value):
        # TODO: Check return type
        return int(0)

    def __eq__(self, value):
        return Boolean(value is undefined or value is null)

    def __ge__(self, value):
        return NaN >= value

    def __gt__(self, value):
        return NaN > value

    def __lt__(self, value):
        return NaN < value

    def __le__(self, value):
        return NaN <= value

    def __and__(self, value):
        return int(0)

    def __invert__(self):
        return int(-1)

    def __or__(self, value):
        return int(_as3lib_CoerceToIntValue(value))

    def __xor__(self, value):
        return int(_as3lib_CoerceToIntValue(value))

    def __each__(self):
        return iter([])

    def toString(self):
        return String('undefined')


class null:
    __slots__ = tuple()

    def __init__(self):
        pass

    def __int__(self):
        return 0

    def __str__(self):
        return str(self.toString())

    def __repr__(self):
        return str(self.toString())

    def __bool__(self):
        return False

    def __neg__(self):
        return 0

    def __iter__(self):
        return iter([])

    def __add__(self, value):
        # TODO: Check type
        return Number(0) + value

    def __sub__(self, value):
        # TODO: Check type
        return Number(0) - value

    def __mul__(self, value):
        # TODO: Check type
        return Number(0) * value

    def __truediv__(self, value):
        # TODO: Check type
        return Number(0) / value

    def __mod__(self, value):
        return Number(0) % value

    def __lshift__(self, value):
        # TODO: Check return type
        return int(0)

    def __rshift__(self, value):
        # TODO: Check return type
        return int(0)

    def __eq__(self, value):
        return Boolean(value is undefined or value is null)

    def __ge__(self, value):
        return Number(0) >= value

    def __gt__(self, value):
        return Number(0) > value

    def __lt__(self, value):
        return Number(0) < value

    def __le__(self, value):
        return Number(0) <= value

    def __and__(self, value):
        return int(0)

    def __invert__(self):
        return int(-1)

    def __or__(self, value):
        return int(_as3lib_CoerceToIntValue(value))

    def __xor__(self, value):
        return int(_as3lib_CoerceToIntValue(value))

    def __each__(self):
        return iter([])

    def toString(self):
        return String('null')


undefined = undefined()
null = null()


def _as3lib_valueOfHelper(obj):
    if hasattr(obj, 'valueOf'):
        return obj.valueOf()
    return obj


def _as3lib_CoerceToNumberValue(obj):
    # TODO: Ensure that using this is the correct solution
    # TODO: Make this work with all as3 types
    obj = _as3lib_valueOfHelper(obj)
    if obj is null:
        return 0
    if obj is undefined:
        return math.nan
    if isinstance(obj, Array):
        # TODO: Check this
        # NOTE: This produces the results:
        #           [] == ''
        #           [1] == 1
        #           ['str'] == NaN
        #           [1, 2] == NaN
        obj = obj.toString()
    if isinstance(obj, (str, String)):
        obj = str(obj).strip()
        if obj.startswith('0x'):
            return parseInt(obj)._value
        if not obj:
            return 0
        return parseFloat(obj)._value
    if isinstance(obj, (Number, int, uint)):
        return obj._value
    if isinstance(obj, (bool, Boolean)):
        return builtins.int(obj)
    if isinstance(obj, Object):
        return math.nan
    return obj


def _as3lib_CoerceToIntValue(obj):
    obj = _as3lib_valueOfHelper(obj)
    if isinstance(obj, (String, str)):
        obj = parseInt(obj)
    if isinstance(obj, (int, uint, Number)):
        obj = obj._value
    if isinstance(obj, (builtins.int)):
        return obj
    if isinstance(obj, (Number, int, uint, float, builtins.int)) and (math.isnan(obj) or math.isinf(obj)):
        return 0
    if isinstance(obj, float):
        return math.floor(obj)
    if hasattr(obj, '__int__'):
        return builtins.int(obj)
    if isinstance(obj, Object):
        return 0
    raise TypeError(f'Can not convert type {type(obj)} to integer')


def _as3lib_toStringHelper(obj):
    if hasattr(obj, 'toString'):
        obj = obj.toString()
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    return str(obj)


# TODO: Determine correct return types for non-boolean operations
#       This is probably determined by the input type
#       EX: In python, int + int => int, int + float => float
class Object:
    # ActionScript3 Base object
    # TODO: Make item assignment work with non-string values.
    # TODO: Prototypes
    prototype = null

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # NOTE: In actionscript, a class can only extend one class. This rule
        #       is expectend to be respected here too.
        # TODO: This is only a partial implementation of prototype
        cls.prototype = cls.__bases__[0]

    def __init__(self):
        '''
        # NOTE: Doing it this way would require proper super support, proper
        #       constructor (property) support, and would require redoing all
        #       constructor functions in this library
        constructorName = type(self).__name__
        if not hasattr(self, constructorName):
            raise
        getattr(self, constructorName)()
        '''
        ...

    def __str__(self):
        return str(self.toString())

    def __getitem__(self, item):
        return getattr(self, str(item))

    def __setitem__(self, item, value):
        setattr(self, str(item), value)

    def __delitem__(self, item):
        super().__delattr__(str(item))

    def __iter__(self):
        return (i for i in self.__dict__.keys())

    def __each__(self):
        return (i for i in self.__dict__.items())

    def __pos__(self):
        return Number(self)

    def __neg__(self):
        return Number(-_as3lib_CoerceToNumberValue(self))

    def __add__(self, value):
        # TODO: This is still slightly wrong
        thisValue = _as3lib_valueOfHelper(self)
        otherValue = _as3lib_valueOfHelper(value)
        if isinstance(thisValue, (str, String, Array)) or isinstance(otherValue, (str, String, Array)):
            return self.toString().concat(value)
        '''
        if (isinstance(self, uint) or isinstance(thisValue, uint)) and (isinstance(value, uint) or isinstance(otherValue, uint)):
            return uint(_as3lib_CoerceToIntValue(self) + _as3lib_CoerceToIntValue(value))
        if (isinstance(self, (int, builtins.int)) or isinstance(thisValue, (int, builtins.int))) and (isinstance(value, (int, builtins.int)) or isinstance(otherValue, (int, builtins.int))):
            return int(_as3lib_CoerceToIntValue(self) + _as3lib_CoerceToIntValue(value))
        '''
        return Number(_as3lib_CoerceToNumberValue(self) + _as3lib_CoerceToNumberValue(value))

    def __sub__(self, value):
        return Number(_as3lib_CoerceToNumberValue(self) - _as3lib_CoerceToNumberValue(value))

    def __mul__(self, value):
        return Number(_as3lib_CoerceToNumberValue(self) * _as3lib_CoerceToNumberValue(value))

    def __truediv__(self, value):
        thisValue = _as3lib_CoerceToNumberValue(self)
        value = _as3lib_CoerceToNumberValue(value)
        if value == 0:
            if thisValue > 0:
                return Number.POSITIVE_INFINITY
            if thisValue < 0:
                return Number.NEGATIVE_INFINITY
            return Number.NaN
        return Number(thisValue / value)

    def __mod__(self, value):
        # TODO: This might not be entirely correct
        thisValue = _as3lib_CoerceToNumberValue(self)
        otherValue = _as3lib_CoerceToNumberValue(value)
        if otherValue == 0 or thisValue == Number.POSITIVE_INFINITY:
            return Number.NaN
        if otherValue == Number.POSITIVE_INFINITY:
            return Number(thisValue)
        if thisValue < 0:
            # Python does not handle negative modulo the same so convert to
            # positive before and then back to negative after the modulo
            return Number(-(-thisValue % otherValue))
        return Number(thisValue % otherValue)

    def __lshift__(self, value):
        thisValue = _as3lib_CoerceToIntValue(self)
        otherValue = _as3lib_CoerceToIntValue(value)
        if otherValue < 0:
            otherValue = -otherValue % 32
            if thisValue < 0:
                return int(-(thisValue << (32 - otherValue)))
            return int(thisValue << (32 - otherValue))
        return int(thisValue << (otherValue % 32))

    def __rshift__(self, value):
        thisValue = _as3lib_CoerceToIntValue(self)
        otherValue = _as3lib_CoerceToIntValue(value)
        if otherValue < 0:
            if thisValue < 0:
                return int(-1)
            return int(0)
        return int(thisValue >> (otherValue % 32))

    def __ge__(self, value):
        return Boolean(_as3lib_CoerceToNumberValue(self) >= _as3lib_CoerceToNumberValue(value))

    def __gt__(self, value):
        return Boolean(_as3lib_CoerceToNumberValue(self) > _as3lib_CoerceToNumberValue(value))

    def __lt__(self, value):
        return Boolean(_as3lib_CoerceToNumberValue(self) < _as3lib_CoerceToNumberValue(value))

    def __le__(self, value):
        return Boolean(_as3lib_CoerceToNumberValue(self) <= _as3lib_CoerceToNumberValue(value))

    def __and__(self, value):
        return int(_as3lib_CoerceToIntValue(self) & _as3lib_CoerceToIntValue(value))

    def __invert__(self):
        return int(~_as3lib_CoerceToIntValue(self))

    def __or__(self, value):
        return int(_as3lib_CoerceToIntValue(self) | _as3lib_CoerceToIntValue(value))

    def __xor__(self, value):
        return int(_as3lib_CoerceToIntValue(self) ^ _as3lib_CoerceToIntValue(value))

    @function
    def hasOwnProperty(self, name: str):
        return str(name) in self.__dict__

    @function
    def isPrototypeOf(self, theClass):
        # This should work properly once prototype is implemented properly
        p = theClass.prototype
        while p is not null:
            if p is self.__class__:
                return true
            p = p.prototype
        return false

    @function
    def propertyIsEnumerable(self, name: str):
        raise NotImplementedError

    @function
    def setPropertyIsEnumerable(self, name: str, isEnum=True):
        raise NotImplementedError

    def toLocaleString(self):
        return String('[object %s]' % type(self).__name__)

    def toString(self):
        return String('[object %s]' % type(self).__name__)

    def valueOf(self):
        return self


class Class(Object):
    ...


class Function(Object):
    def apply(thisArg, argArray):
        ...

    def call(thisArg, *args):
        ...


class Array(list, Object):
    # TODO: Arrays are sparse arrays, meaning there might be an element at index 0 and another at index 5, but nothing in the index positions between those two elements. In such a case, the elements in positions 1 through 4 are undefined, which indicates the absence of an element, not necessarily the presence of an element with the value undefined.
    # NOTE: Actionscript arrays seem to function like a python dictionary which can only uses ints as keys
    CASEINSENSITIVE = 1
    DESCENDING = 2
    UNIQUESORT = 4
    RETURNINDEXEDARRAY = 8
    NUMERIC = 16

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (Number, int, uint, builtins.int, float)):
            super().__init__([undefined for i in range(args[0])])
        else:
            super().__init__(args)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return Array(*[self[i] for i in range(*item.indices(len(self)))])
        else:
            try:
                return super().__getitem__(item)
            except Exception:
                return undefined

    def __setitem__(self, item, value):
        if isinstance(item, (builtins.int, int, uint, Number)) and item+1 > self.length:
            '''
            When you assign a value to an array element (ex: my_array[index] = value), if index is a number, and index+1 is greater than the length property, the length property is updated to index+1.
            '''
            self.length = item+1
        super().__setitem__(item, value)

    def __delitem__(self, item):
        if item < self.length:
            super().__setitem__(item, undefined)

    __add__ = Object.__add__

    @property
    def length(self):
        return len(self)

    @length.setter
    def length(self, value: uint):
        if value < 0:
            raise RangeError(f'Array.length can not be negative. got {value}')
        elif value == 0:
            self.clear()
        elif len(self) > value:
            while len(self) > value:
                self.pop()
        elif len(self) < value:
            while len(self) < value:
                self.append(undefined)

    def __repr__(self):
        return 'Array(%s)' % self

    def __each__(self):
        return (self[i] for i in range(self.length))

    def concat(self, *args):
        newArr = Array(*self)
        for i in args:
            if isinstance(i, (list, tuple)):
                newArr.extend(i)
            else:
                newArr.append(i)
        return newArr

    def every(self, callback: callable):
        if callback is null:
            return true
        for i in range(len(self)):
            if not callback(self[i], i, self):
                return false
        return true

    def filter(self, callback: callable):
        if callback is null:
            return
        tempArray = Array()
        for i in range(len(self)):
            if callback(self[i], i, self):
                tempArray.push(self[i])
        return tempArray

    def forEach(self, callback: callable):
        if callback is null:
            return undefined
        for i in range(len(self)):
            callback(self[i], i, self)

    def indexOf(self, searchElement, fromIndex: int = 0):
        if fromIndex < 0:
            fromIndex = 0
        for i in range(fromIndex, len(self)):
            if self[i] == searchElement:
                return i
        return -1

    def insertAt(self, index: int, element):
        self.insert(index, element)

    @staticmethod
    def _join(o, sep=undefined):
        if sep is undefined:
            s = ','
        else:
            s = str(String(sep))
        with StringIO() as out:
            n = o.length
            for i in range(n):
                x = o[i]
                if x is not undefined and x is not null:
                    out.write(str(x))
                if i + 1 < n:
                    out.write(s)
            return String(out.getvalue())

    def join(self, sep: String = ','):
        return Array._join(self, sep)

    def lastIndexOf(self, searchElement, fromIndex: int = null):
        if fromIndex is null:
            fromIndex = len(self)
        elif fromIndex < 0:
            raise RangeError(f'Array.lastIndexOf; fromIndex can not negative. got {fromIndex}')
        index = self[::-1].indexOf(searchElement, len(self)-1-fromIndex)
        return index if index == -1 else len(self)-1-index

    def map(self, callback: callable):
        if callback is null:
            return
        return Array(*[callback(self[i], i, self) for i in range(len(self))])

    def pop(self):
        return super().pop(-1)

    def push(self, *args):
        self.extend(args)

    def removeAt(self, index: builtins.int | int):
        return super().pop(index)

    def reverse(self):
        super().reverse()
        return self

    def shift(self):
        return super().pop(0)

    def slice(self, startIndex: int = 0, endIndex: int = 99*10^99):
        if startIndex < 0:
            startIndex = len(self)+startIndex
        if endIndex < 0:
            endIndex = len(self)+endIndex
        return self[startIndex: endIndex]

    def some(self, callback: callable):
        if callback is null:
            return false
        for i in range(len(self)):
            if callback(self[i], i, self):
                return true
        return false

    def _flagSort(self, flags):
        # NOTE: These are flags, not exclusive values
        if flags & 4:  # UNIQUESORT
            # NOTE: Only works for hashable types
            s = set()
            any(x in s or s.add(x) for x in self)
            s = set()
            duplicates = set(x for x in self if x in s or s.add(x))
            if duplicates:
                return Number(0)
        if flags & 1:  # CASEINSENSITIVE
            raise NotImplementedError
        if flags & 2:  # DESCENDING
            raise NotImplementedError
        if flags & 8:  # RETURNINDEXEDARRAY
            raise NotImplementedError
        if flags & 16:  # NUMERIC
            super().sort(key=Number)

    def sort(self, *args):
        # NOTE: Only returns when 4 or 8 is specified
        if len(args) == 0:  # Default sorting
            # TODO: Ensure that this is correct
            super().sort(key=str)  # TODO: Should be String
        elif len(args) == 1:  # Comparison function or flags
            if callable(args[0]):
                super().sort(key=cmp_to_key(args[0]))
            else:
                s = self._flagSort(args[0])
                if args[0] & 4 or args[0] & 8:
                    return s
        elif len(args) == 2:  # Comparison function and flags
            raise NotImplementedError

    def sortOn(self, fieldName, options=null):
        if isinstance(fieldName, (list, tuple, Array)):
            if isinstance(options, (list, tuple, Array)):
                # TODO: Ignore flags if fieldName.length != options.length
                # TODO: Ignore UNIQUESORT and RETURNINDEXEDARRAY if not in the
                #       first element
                ...
            ...
        raise NotImplementedError

    def splice(self, startIndex: int = null, deleteCount: uint = null, *values):
        if startIndex is null:
            return null
        if deleteCount is null:
            deleteCount = self.length
        startIndex, deleteCount = int(startIndex), int(deleteCount)
        if deleteCount < 0:
            return Array()
        removedValues = self[startIndex: startIndex+deleteCount]
        self[startIndex: startIndex+deleteCount] = values
        return removedValues

    def toList(self):
        return list(self)

    def toLocaleString(self):
        with StringIO() as out:
            n = self.length
            for i in range(n):
                x = self[i]
                if x is not undefined and x is not null:
                    if hasattr(x, 'toLocaleString'):
                        out.write(str(x.toLocaleString()))
                    else:
                        out.write(str(x))
                if i + 1 < n:
                    out.write(',')
            return String(out.getvalue())

    def toString(self):
        return Array._join(self)

    def unshift(self, *args):
        tempArray = [*args, *self]
        self.clear()
        self.extend(tempArray)
        return len(self)


class Boolean(Object):
    __slots__ = ('_value')

    def __init__(self, expression=False):
        self._value = self._Boolean(expression)

    def __repr__(self):
        return 'Boolean(%s)' % self._value

    def __bool__(self):
        return self._value

    def __float__(self):
        return float(self._value)

    def __int__(self):
        return builtins.int(self._value)

    def __eq__(self, value):
        return self._value == value

    def __abs__(self):
        return Number(self._value)

    def _Boolean(self, expression):
        if isinstance(expression, bool):
            return expression
        # NOTE: For some reason, python str does not have __bool__ but can be
        #       converted to one anyways
        if hasattr(expression, '__bool__') or isinstance(expression, str):
            return bool(expression)
        return False

    def toString(self):
        return String(self._value).toLowerCase()

    def valueOf(self):
        return self._value


false = Boolean(False)
true = Boolean(True)


class Date(Object):
    # Notes:
    # Python's datetime object (used internally for Date) has microseconds, not
    # milliseconds, so some math must be done to convert between the two when
    # used.
    #
    # Python uses 1 as January but flash uses 0, so math needs to be done here too
    #
    # Python starts the week on Monday but flash starts it on Sunday
    #
    # Python timestamps are in seconds but we need milliseconds

    # TODO:
    # toString variants
    # Date.parse
    # Date constructor with string argument.
    # Date constructor with Number arguement sometimes has the wrong date. (possibly related to DST)
    # Rewrite Date to not have to store the date twice. valueOf returns a utc timestamp
    @property
    def date(self):
        return Number(self._value.day)

    @date.setter
    def date(self, value):
        self.setDate(value)

    @property
    def dateUTC(self):
        return Number(self._valueUTC.day)

    @dateUTC.setter
    def dateUTC(self, value):
        self.setUTCDate(value)

    @property
    def day(self):
        return Number(self._value.toordinal() % 7)

    @property
    def dayUTC(self):
        return Number(self._valueUTC.toordinal() % 7)

    @property
    def fullYear(self):
        return Number(self._value.year)

    @fullYear.setter
    def fullYear(self, value):
        self.setFullYear(value)

    @property
    def fullYearUTC(self):
        return Number(self._valueUTC.year)

    @fullYearUTC.setter
    def fullYearUTC(self, value):
        self.setUTCFullYear(value)

    @property
    def hours(self):
        return Number(self._value.hour)

    @hours.setter
    def hours(self, value):
        self.setHours(value)

    @property
    def hoursUTC(self):
        return Number(self._valueUTC.hour)

    @hoursUTC.setter
    def hoursUTC(self, value):
        self.setUTCHours(value)

    @property
    def milliseconds(self):
        return Number(self._value.microsecond / 1000)

    @milliseconds.setter
    def milliseconds(self, value):
        self.setMilliseconds(value)

    @property
    def millisecondsUTC(self):
        return Number(self._valueUTC.microsecond / 1000)

    @millisecondsUTC.setter
    def millisecondsUTC(self, value):
        self.setUTCMilliseconds(value)

    @property
    def minutes(self):
        return Number(self._value.minute)

    @minutes.setter
    def minutes(self, value):
        self.setMinutes(value)

    @property
    def minutesUTC(self):
        return Number(self._valueUTC.minute)

    @minutesUTC.setter
    def minutesUTC(self, value):
        self.setUTCMinutes(value)

    @property
    def month(self):
        return Number(self._value.month - 1)

    @month.setter
    def month(self, value):
        self.setMonth(value)

    @property
    def monthUTC(self):
        return Number(self._valueUTC.month - 1)

    @monthUTC.setter
    def monthUTC(self, value):
        self.setUTCMonth(value)

    @property
    def seconds(self):
        return Number(self._value.second)

    @seconds.setter
    def seconds(self, value):
        self.setSeconds(value)

    @property
    def secondsUTC(self):
        return Number(self._valueUTC.second)

    @secondsUTC.setter
    def secondsUTC(self, value):
        self.setUTCSeconds(value)

    @property
    def time(self):
        return Number(self._valueUTC.timestamp() * 1000)

    @time.setter
    def time(self, value):
        raise NotImplementedError

    @property
    def timezoneOffset(self):
        # TODO: Make sure this is dst aware
        tz = self._value.utcoffset()
        seconds = tz.seconds
        if tz.days:
            # Special handling for when python fucks up the tz
            # For my timezone, it does days=-1 and then adds seconds
            seconds += tz.days * 86400

        return Math.floor(seconds / 60)  # minutes

    def _sync(self):
        self._valueUTC = self._value.astimezone(datetime.timezone.utc)

    def _syncUTC(self):
        self._value = self._valueUTC.astimezone(tz=self._localtz)

    def __init__(self, yearOrTimevalue: Object = null, month: Number = null,
                 date: Number = 1, hour: Number = 0, minute: Number = 0,
                 second: Number = 0, millisecond: Number = 0):
        # TODO: When NaN is passed as the first arguement, all values should be set to NaN
        #       When a value is set after this, all other values become the default
        self._localtz = _getTimezone()
        if yearOrTimevalue is not null and hasattr(yearOrTimevalue, 'valueOf'):
            yearOrTimevalue = yearOrTimevalue.valueOf()
        if yearOrTimevalue is null and month is null:
            # Passed no arguements. Use current date and time
            self._value = datetime.datetime.now(tz=self._localtz)
            self._sync()
        elif isinstance(yearOrTimevalue, (builtins.int, int, float, Number)) and month is null:
            # One arguement of type Number is passed. Interpret as utc timestamp
            # TODO: _localtz is wrong here
            self._valueUTC = datetime.datetime.fromtimestamp(yearOrTimevalue / 1000, datetime.timezone.utc)
            self._syncUTC()
        elif isinstance(yearOrTimevalue, (String, str)) and month is null:
            # One arguement of type String is passed. Parse date string
            raise NotImplementedError('One aruement of type String')  # TODO
        else:
            # Two or more arguements are passed. Use arguements literally
            # TODO: Figure out what timezone this should be
            self._value = datetime.datetime(yearOrTimevalue, month + 1, date, hour, minute, second, millisecond * 1000, tzinfo=self._localtz)
            self._sync()

    def getDate(self):
        return self.date

    def getDay(self):
        return self.day

    def getFullYear(self):
        return self.fullYear

    def getHours(self):
        return self.hours

    def getMilliseconds(self):
        return self.milliseconds

    def getMinutes(self):
        return self.minutes

    def getMonth(self):
        return self.month

    def getSeconds(self):
        return self.seconds

    def getTime(self):
        return self.valueOf()

    def getTimezoneOffset(self):
        return self.timezoneOffset

    def getUTCDate(self):
        return self.dateUTC

    def getUTCDay(self):
        return self.dayUTC

    def getUTCFullYear(self):
        return self.fullYearUTC

    def getUTCHours(self):
        return self.hoursUTC

    def getUTCMilliseconds(self):
        return self.millisecondsUTC

    def getUTCMinutes(self):
        return self.minutesUTC

    def getUTCMonth(self):
        return self.monthUTC

    def getUTCSeconds(self):
        return self.secondsUTC

    @staticmethod
    def parse(date):
        raise NotImplementedError

    def setDate(self, day):
        self._value = self._value.replace(day=day)
        self._sync()
        return self.time

    def setFullYear(self, year, month=null, day=null):
        self._value = self._value.replace(year=year)
        if month is not null or day is not null:
            raise NotImplementedError
        self._sync()
        return self.time

    def setHours(self, hour, minute=null, second=null, millisecond=null):
        self._value = self._value.replace(hour=hour)
        if minute is not null or second is not null or millisecond is not null:
            raise NotImplementedError
        self._sync()
        return self.time

    def setMilliseconds(self, millisecond):
        self._value = self._value.replace(microsecond=millisecond*1000)
        self._sync()
        return self.time

    def setMinutes(self, minute, second=null, millisecond=null):
        self._value = self._value.replace(minute=minute)
        if second is not null or millisecond is not null:
            raise NotImplementedError
        self._sync()
        return self.time

    def setMonth(self, month, day=null):
        self._value = self._value.replace(month=month+1)
        if day is not null:
            raise NotImplementedError
        self._sync()
        return self.time

    def setSeconds(self, second, millisecond=null):
        self._value = self._value.replace(second=second)
        if millisecond is not null:
            raise NotImplementedError
        self._sync()
        return self.time

    def setTime(self, millisecond):
        self.time = millisecond
        return self.time

    def setUTCDate(self, day):
        self._valueUTC = self._valueUTC.replace(day=day)
        self._syncUTC()
        return self.time

    def setUTCFullYear(self, year, month=null, day=null):
        self._valueUTC = self._valueUTC.replace(year=year)
        if month is not null or day is not null:
            raise NotImplementedError
        self._syncUTC()
        return self.time

    def setUTCHours(self, hour, minute=null, second=null, millisecond=null):
        self._valueUTC = self._valueUTC.replace(hour=hour)
        if minute is not null or second is not null or millisecond is not null:
            raise NotImplementedError
        self._syncUTC()
        return self.time

    def setUTCMilliseconds(self, millisecond):
        self._valueUTC = self._valueUTC.replace(microsecond=millisecond*1000)
        self._syncUTC()
        return self.time

    def setUTCMinutes(self, minute, second=null, millisecond=null):
        self._valueUTC = self._valueUTC.replace(minute=minute)
        if second is not null or millisecond is not null:
            raise NotImplementedError
        self._syncUTC()
        return self.time

    def setUTCMonth(self, month, day=null):
        self._valueUTC = self._valueUTC.replace(month=month+1)
        if day is not null:
            raise NotImplementedError
        self._syncUTC()
        return self.time

    def setUTCSeconds(self, second, millisecond=null):
        self._valueUTC = self._valueUTC.replace(second=second)
        if millisecond is not null:
            raise NotImplementedError
        self._syncUTC()
        return self.time

    def _monthName(self, mon):
        return ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                'Oct', 'Nov', 'Dec')[builtins.int(mon)]

    def _dayName(self, date):
        return ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')[builtins.int(date)]

    def _timezone(self):
        return 'GMT%s' % ''.join(self._value.strftime('%:z').split(':')[:2])

    def _time(self, HH, MM, SS):
        return f'{builtins.int(HH):0>2}:{builtins.int(MM):0>2}:{builtins.int(SS):0>2}'

    def toDateString(self):
        # TODO: Make sure this is correct
        return '%s %s %s %s' % (self._dayName(self.day), self._monthName(self.month), self.date, self.fullYear)

    def toJSON(self, k):
        return self.toString()

    def toLocaleDateString(self):
        # Documentation says this returns the same as toDateString
        return self.toDateString()

    def toLocaleString(self):
        raise NotImplementedError

    def toLocaleTimeString(self):
        raise NotImplementedError

    def toString(self):
        return '%s %s %s %s %s %s' % (self._dayName(self.day), self._monthName(self.month), self.date, self._time(self.hours, self.minutes, self.seconds), self._timezone(), self.fullYear)

    def toTimeString(self):
        return '%s %s' % (self._time(self.hours, self.minutes, self.seconds), self._timezone())

    def toUTCString(self):
        return '%s %s %s %s %s UTC' % (self._dayName(self.dayUTC), self._monthName(self.monthUTC), self.dateUTC, self._time(self.hoursUTC, self.minutesUTC, self.secondsUTC), self.fullYearUTC)

    @staticmethod
    def UTC(year, month, date=1, hour=0, minute=0, second=0, millisecond=0):
        return Number(datetime.datetime(year, month, date, hour, minute, second, millisecond * 1000, tzinfo=datetime.timezone.utc).timestamp() * 1000)

    def valueOf(self):
        return self.time


class Error(Exception, Object):
    # TODO: Implement the debug functionality as specified here https://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/Error.html
    @property
    def errorID(self):
        return self._id

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = String(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = String(value)

    def __init__(self, message='', id=0):
        self.name = 'Error'
        self._id = int(next(_genErrorID) if id == 0 else id)
        self.message = message if message != '' else 'Error'
        errorTrace(self.toString())

    @staticmethod
    def getErrorMessage(number):
        raise NotImplementedError

    def getStackTrace(self):
        return f'{self.name}: Error #{self.errorID}: {self.message}\n{"".join(traceback.format_tb(self.__traceback__))}'

    def toString(self):
        return String(f'{self.name}: {self.message}')


class ArgumentError(Error):
    def __init__(self, message='', id=0):
        super().__init__(message, id)
        self.name = 'ArgumentError'


class DefinitionError(Error):
    def __init__(self, message='', id=0):
        super().__init__(message, id)
        self.name = 'DefinitionError'


class EvalError(Error):
    def __init__(self, message='', id=0):
        super().__init__(message, id)
        self.name = 'EvalError'


class RangeError(Error):
    def __init__(self, message='', id=0):
        super().__init__(message, id)
        self.name = 'RangeError'


class ReferenceError(Error):
    def __init__(self, message='', id=0):
        super().__init__(message, id)
        self.name = 'ReferenceError'


class SecurityError(Error):
    def __init__(self, message='', id=0):
        super().__init__(message, id)
        self.name = 'SecurityError'


class SyntaxError(Error):
    def __init__(self, message='', id=0):
        super().__init__(message, id)
        self.name = 'SyntaxError'


class TypeError(Error):
    def __init__(self, message='', id=0):
        super().__init__(message, id)
        self.name = 'TypeError'


class URIError(Error):
    def __init__(self, message='', id=0):
        super().__init__(message, id)
        self.name = 'URIError'


class VerifyError(Error):
    def __init__(self, message='', id=0):
        super().__init__(message, id)
        self.name = 'VerifyError'


class Number(Object):
    __slots__ = '_val'
    MAX_VALUE = 1.79e308
    MIN_VALUE = 5e-324

    @property
    def _value(self):
        return self._val.value

    @_value.setter
    def _value(self, value):
        self._val.value = value

    def __init__(self, num=null):
        if not as3state.initdone:
            # NOTE: This is here because _as3lib_CoerceToNumberValue causes
            #       problems before all as3lib types are defined
            self._val = c_double(num)
        else:
            self._val = c_double(_as3lib_CoerceToNumberValue(num))

    def __repr__(self):
        return 'Number(%s)' % self

    def __hash__(self):
        return hash(self._value)

    def __float__(self):
        return self._value

    def __int__(self):
        return builtins.int(self._value)

    def __index__(self):
        return _as3lib_CoerceToIntValue(self)

    def __eq__(self, value):
        return self._value == value

    def __bool__(self):
        return self._value != 0 and not math.isnan(self)

    def __abs__(self):
        return Number(abs(self._value))

    def __pow__(self, value):
        return Number(self._value ** _as3lib_CoerceToNumberValue(value))

    def __round__(self, places=null):
        if places is null:
            if self._value % 1 >= 0.5:
                return Number(math.ceil(self._value))
            return Number(math.floor(self._value))
        return Number(round(self._value, places))

    def toExponential(self, fractionDigits: uint = null):
        fractionDigits = uint(fractionDigits)
        if fractionDigits > 20:
            raise RangeError('fractionDigits is outside of acceptable range')
        if self._value == 0:
            if fractionDigits == 0:
                return String('1e-15')
            return String(('{:.%if}e-16' % fractionDigits).format(0))
        if math.isnan(self) or math.isinf(self):
            return self.toString()
        return String(_exponentFixNum(('{:.%ie}' % fractionDigits).format(self._value)))

    def toFixed(self, fractionDigits: uint = null):
        fractionDigits = uint(fractionDigits)
        if fractionDigits > 20:
            raise RangeError('fractionDigits is outside of acceptable range')
        return String(('{:.%if}' % fractionDigits).format(self._value))

    def toPrecision(self, precision):
        precision = uint(precision)
        raise NotImplementedError

    def toString(self, radix=10):
        if math.isnan(self):
            return String('NaN')
        if math.isinf(self):
            if self._value < 0:
                return String('-Infinity')
            return String('Infinity')
        if radix != 10:
            return String(_as_base(builtins.int(self._value), radix))
        if self._value.is_integer():
            return String(_exponentFixNum('%i' % self._value))
        # NOTE: Exponent -6 to 20 should not be in exonential according to the
        #       tests
        # NOTE: When decimals are present in the output, only seems to show
        #       max 17 characters that are a part of the number (count
        #       includes '.' if the characters surrounding it are non-zero)
        #       If the length of the significant digits of the number is less
        #       than 17 that entire portion always seems to be shown
        # 0.000001 is 1e-6, 1000000000000000000000 is 1e21
        if self._value >= 0.000001 and self._value < 1000000000000000000000:
            if self._value < 1:
                # TODO: This is incorrect. See above notes
                return String('{:f}'.format(self._value))
            return String('{:f}'.format(self._value).strip('0'))
        return String(_exponentFixNum('%s' % self._value))

    toLocaleString = toString

    def valueOf(self):
        return self._value


Infinity = Number.POSITIVE_INFINITY = Number(math.inf)
NaN = Number.NaN = Number(math.nan)
Number.NEGATIVE_INFINITY = Number(-math.inf)


class Math(Object):
    E = Number(2.718281828459045)
    LN10 = Number(2.302585092994046)
    LN2 = Number(0.6931471805599453)
    LOG10E = Number(0.4342944819032518)
    LOG2E = Number(1.442695040888963387)
    PI = Number(3.141592653589793)
    SQRT1_2 = Number(0.7071067811865476)
    SQRT2 = Number(1.4142135623730951)

    @staticmethod
    def abs(val: Number):
        return abs(Number(val))

    @staticmethod
    def acos(val: Number):
        val = Number(val)
        if math.isnan(val) or val > 1 or val < -1:
            return Number.NaN
        return Number(math.acos(val))

    @staticmethod
    def asin(val: Number):
        val = Number(val)
        if math.isnan(val) or val > 1 or val < -1:
            return Number.NaN
        return Number(math.asin(val))

    @staticmethod
    def atan(val: Number):
        return Number(math.atan(Number(val)))

    @staticmethod
    def atan2(y: Number, x: Number):
        return Number(math.atan2(Number(y), Number(x)))

    @staticmethod
    def ceil(val: Number):
        val = Number(val)
        if math.isnan(val) or math.isinf(val):
            return val
        return Number(math.ceil(val))

    @staticmethod
    def cos(angleRadians: Number):
        a = Number(angleRadians)
        if math.isnan(a) or math.isinf(a):
            return Number.NaN
        return Number(math.cos(a))

    @staticmethod
    def exp(val: Number):
        val = Number(val)
        if math.isnan(val):
            return Number.NaN
        try:
            return math.exp(val)
        except OverflowError:
            return Number.POSITIVE_INFINITY

    @staticmethod
    def floor(val: Number):
        val = Number(val)
        if math.isnan(val) or math.isinf(val):
            return val
        return Number(math.floor(val))

    @staticmethod
    def log(val: Number):
        val = Number(val)
        if val < 0 or math.isnan(val):
            return Number.NaN
        if val == 0:
            return Number.NEGATIVE_INFINITY
        if math.isinf(val):
            return Number.POSITIVE_INFINITY
        return Number(math.log(val))

    @staticmethod
    def max(*values):
        v = [Number.NEGATIVE_INFINITY]
        for i in values:
            n = Number(i)
            if math.isnan(n):
                return Number.NaN
            v.append(n)
        return max(v)

    @staticmethod
    def min(*values):
        v = [Number.POSITIVE_INFINITY]
        for i in values:
            n = Number(i)
            if math.isnan(n):
                return Number.NaN
            v.append(n)
        return min(v)

    @staticmethod
    def pow(base: Number, power: Number):
        base, power = Number(base), Number(power)
        if math.isnan(base) or math.isnan(power):
            return Number.NaN
        return Number(math.pow(base, power))

    @staticmethod
    def random():
        return Number(random.random())

    @staticmethod
    def round(val: Number):
        val = Number(val)
        if math.isnan(val) or math.isinf(val):
            return val
        return round(val)

    @staticmethod
    def sin(angleRadians: Number):
        a = Number(angleRadians)
        if math.isnan(a) or math.isinf(a):
            return Number.NaN
        return Number(math.sin(a))

    @staticmethod
    def sqrt(val: Number):
        val = Number(val)
        if val < 0 or math.isnan(val):
            return Number.NaN
        return Number(math.sqrt(val))

    @staticmethod
    def tan(angleRadians: Number):
        a = Number(angleRadians)
        if math.isnan(a) or math.isinf(a):
            return Number.NaN
        return Number(math.tan(a))


class int(Object):
    # TODO: Make this return a Number if the result is a float
    MAX_VALUE = 2147483647
    MIN_VALUE = -2147483648

    _buffertype = c_int32

    @property
    def _value(self):
        return self._val.value

    @_value.setter
    def _value(self, value):
        self._val.value = value

    def __init__(self, value=0):
        self._val = self._buffertype(_as3lib_CoerceToIntValue(value))

    def __float__(self):
        return float(self._value)

    def __int__(self):
        return self._value

    def __index__(self):
        return self._value

    def __bool__(self):
        return bool(self._value)

    def __repr__(self):
        return 'int(%s)' % self._value

    def __hash__(self):
        return hash(self._value)

    def __add__(self, value):
        return int(super().__add__(value))

    def __sub__(self, value):
        return int(super().__sub__(value))

    def __mul__(self, value):
        return int(super().__mul__(value))

    def __truediv__(self, value):
        res = super().__truediv__(_as3lib_CoerceToIntValue(value))
        if math.isnan(res) or math.isinf(res):
            return res
        return int(res)

    def __mod__(self, value):
        return int(super().__mod__(value))

    def __eq__(self, value):
        return self._value == value

    def toExponential(self, fractionDigits: uint = null):
        fractionDigits = uint(fractionDigits)
        if fractionDigits > 20:
            raise RangeError('fractionDigits is outside of acceptable range')
        if self == 0:
            if fractionDigits == 0:
                return String('1e-15')
            return String(_exponentFixInt(('{:.%se}' % fractionDigits).format(self._value)) + 'e-16')
        return String(_exponentFixInt(('{:.%se}' % fractionDigits).format(self._value)))

    def toFixed(self, fractionDigits: uint = null):
        fractionDigits = uint(fractionDigits)
        if fractionDigits > 20:
            raise RangeError('fractionDigits is outside of acceptable range')
        return String(('{:.%sf}' % fractionDigits).format(self._value))

    def toPrecision(self, precision: uint):
        precision = uint(precision)
        if precision < 1 or precision > 21:
            raise RangeError('precision is outside of acceptable range')
        raise NotImplementedError

    def toString(self, radix: uint = 10):
        if radix <= 36 and radix >= 2:
            return String(_as_base(self._value, radix))

    toLocaleString = toString

    def valueOf(self):
        return self._value


class uint(int):
    # NOTE: The tests from ruffle show that uint doesn't really exist
    MAX_VALUE = 4294967295
    MIN_VALUE = 0

    _buffertype = c_uint32

    def __repr__(self):
        return 'uint(%s)' % self._value


class String(str, Object):
    # NOTE: Using bytearray(<value>.encode('utf-16')) seems to be correct here
    #       Use (len(<bytearray>) - 2) / 2 to get the length
    def __init__(self, value=''):
        self.__init2(_as3lib_toStringHelper(value))

    def __init2(self, value):
        # Workaround for super().__init__() eating arguements
        super().__init__()

    def __str__(self):
        return str.__str__(self)

    def __repr__(self):
        return 'String("%s")' % self

    @property
    def length(self):
        return len(self)

    def __getitem__(self, item):
        return String(super().__getitem__(item))

    def __bool__(self):
        return self.length > 0

    # TODO: Remove these once String is not a subclass of str
    __add__ = Object.__add__
    __mul__ = Object.__mul__
    __rmul__ = Object.__mul__
    __mod__ = Object.__mod__

    def charAt(self, index: Number = 0):
        index = Number(index)
        if index < 0 or index > len(self) - 1:
            return String()
        return String(self[index])

    def charCodeAt(self, index: Number = 0):
        index = Number(index)
        if index < 0 or index > len(self) - 1:
            return Number.NaN
        return Number(builtins.int(r'{:04X}'.format(ord(self[index])), 16))

    def concat(self, *args):
        return String(''.join([self, *(_as3lib_toStringHelper(i) for i in args)]))

    @staticmethod
    def fromCharCode(*charCodes):
        raise NotImplementedError

    def indexOf(self, val, startIndex: int = 0):
        return self.find(String(val), startIndex)

    def lastIndexOf(self, val, startIndex: int = 0x7fffffff):
        return self.rfind(String(val), startIndex)

    def localeCompare(self, other, *values):
        raise NotImplementedError

    def match(self, pattern):
        raise NotImplementedError

    def replace(self, pattern, repl):
        raise NotImplementedError

    def search(self, pattern: Object = undefined):
        if pattern is undefined or pattern is null:
            return -1
        raise NotImplementedError

    def slice(self, startIndex=0, endIndex=null):
        si, ei = Number(startIndex), Number(endIndex)
        if si == Number.POSITIVE_INFINITY or ei == Number.NEGATIVE_INFINITY:
            return String('')
        si = int(si)
        if endIndex is null or ei == Number.POSITIVE_INFINITY:
            return self[si:]
        ei = int(ei)
        return self[si:ei]

    def split(self, delimiter=null, limit=0x7fffffff):
        if delimiter is undefined or delimiter is null:
            return Array(self)
        elif delimiter == '' or False:
            # An empty string, an empty regular expression, or a regular
            # expression that can match an empty string
            return Array(*[i for i in self])
        elif False:
            # If the delimiter parameter is a regular expression, only the first
            # match at a given position of the string is considered, even if
            # backtracking could find a nonempty substring match at that
            # position.
            ...
        elif False:
            # If the delimiter parameter is a regular expression containing
            # grouping parentheses, then each time the delimiter is matched, the
            # results (including any undefined results) of the grouping
            # parentheses are spliced into the output array.
            ...
        else:
            return Array(*super().split(delimiter, limit))

    def substr(self, startIndex: Number = 0, len: Number = null):
        startIndex = Number(startIndex)
        if len is null:
            return self[startIndex:]
        else:
            len = Number(len)
        if len == Number.NEGATIVE_INFINITY:
            return String('')
        if len < 0:
            len += self.length
        return self[startIndex:startIndex+len]

    def substring(self, startIndex: Number = 0, endIndex: Number = null):
        startIndex = Number(startIndex)
        if startIndex < 0:
            startIndex = 0
        endIndex = self.length if endIndex is null else Number(endIndex)
        if endIndex < 0:
            endIndex = 0
        if startIndex > endIndex:
            return self[endIndex:startIndex]
        return self[startIndex:endIndex]

    def toLocaleLowerCase(self):
        return String(self.lower())

    def toLocaleUpperCase(self):
        return String(self.upper())

    def toLowerCase(self):
        return String(self.lower())

    def toUpperCase(self):
        return String(self.upper())

    def toString(self):
        return self

    def valueOf(self):
        return '%s' % self


class RegExp(Object):
    '''
    Because global is a keyword in python, the global property has been renamed
    to global_
    '''
    @property
    def dotall(self):
        return self._dotall

    @property
    def extended(self):
        return self._extended

    @property
    def global_(self):
        return self._global

    @property
    def ignoreCase(self):
        return self._ignoreCase

    @property
    def lastIndex(self):
        return self._lastIndex

    @lastIndex.setter
    def lastIndex(self, value):
        self._lastIndex = value

    @property
    def multiline(self):
        return self._multiline

    @property
    def source(self):
        return self._source

    def __init__(self, re=undefined, flags=undefined, *args):
        if re is undefined:
            re = ''
        if re is null:
            re = 'null'
        self._lastIndex = 0
        if isinstance(re, RegExp):
            if flags is not undefined:
                raise TypeError('Cannot supply flags when constructing one RegExp from another', 1100)
            # TODO: Make sure this is correct
            self._source = re.source

            self._dotall = re.dotall
            self._extended = re.extended
            self._global = re.global_
            self._ignoreCase = re.ignoreCase
            # TODO: Find out what is done with this
            # self._lastIndex = re.lastIndex

            self._multiline = re.multiline
        else:
            if flags is undefined or flags is null:
                flags = ''
            self._source = String(re)
            self._dotall = 's' in flags
            self._extended = 'x' in flags
            self._global = 'g' in flags
            self._ignoreCase = 'i' in flags
            self._multiline = 'm' in flags

        flags = 0
        if self.ignoreCase:
            flags |= regex.IGNORECASE
        if self.multiline:
            flags |= regex.MULTILINE
        if self.dotall:
            flags |= regex.DOTALL
        if self.extended:
            flags |= regex.VERBOSE
        self._re = regex.compile(str(self.source), flags)

    def exec(self, str):
        # TODO: output.index
        # TODO: global flag
        matches = list(self._re.finditer(str))
        if not matches:
            return null
        match = matches[0]
        output = Object()
        for k, v in match.groupdict().items():
            if v is None or v == '':
                v = undefined
            setattr(output, k, v)
        output.input = str
        group = match.group()
        if group is None:
            output[0] = undefined
        else:
            output[0] = group
        output.index = match.start()
        groups = match.groups()
        if groups is not None:
            i = 1
            for item in groups:
                output[i] = item
                i += 1
        if self.global_:
            raise NotImplementedError
        return output

    def test(self, str):
        if self.exec(str) is null:
            return false
        return true

    def toString(self):
        with StringIO() as s:
            s.write('/%s/' % self.source)
            if self.global_:
                s.write('g')
            if self.ignoreCase:
                s.write('i')
            if self.multiline:
                s.write('m')
            if self.dotall:
                s.write('s')
            if self.extended:
                s.write('x')
            return String(s.getvalue())


class JSON(Object):
    @staticmethod
    def parse(text, reviver=null):
        raise NotImplementedError

    @staticmethod
    def stringify(value, replacer=null, space=null):
        raise NotImplementedError


class _VectorType:
    __slots__ = ('_type',)

    @property
    def type(self):
        return self._type

    def __init__(self, type):
        self._type = type

    def __call__(self, *args, **kwargs):
        return Vector(*args, **kwargs, type=self._type)

    def __str__(self):
        if isinstance(self.type, _VectorType):
            typeName = self.type
        else:
            typeName = self.type.__name__
        return 'Vector.<%s>' % typeName

    __repr__ = __str__


class Vector(list, Object):
    '''
    AS3 Vector datatype.

    This class is not really a vector as I haven't found a way to do that in
    python. It is instead just a type locked list.

    Use Vector[T] instead of Vector.<T>
    '''
    # TODO: Use correct arguement types
    @staticmethod
    def _convertToType(obj, type, isSuperclass):
        if isinstance(type, _VectorType):
            return type(obj)
        if obj is null or isSuperclass and isinstance(obj, type) or not isSuperclass and builtins.type(obj) is type:
            return obj
        try:
            return type(obj)
        except:
            raise TypeError(f'Type Coercion failed: cannot convert {object.__repr__(obj)} to {type}', 1034)

    @property
    def fixed(self):
        return self._fixed

    @fixed.setter
    def fixed(self, value):
        self._fixed = Boolean(value)

    @property
    def length(self):
        return uint(len(self))

    @length.setter
    def length(self, value):
        if self.fixed:
            raise RangeError('Can not set vector length while fixed is set to true.')
        if value > 4294967296:
            raise RangeError('New length outside of accepted range (0-4294967296).')
        value = uint(value)
        if len(self) > value:
            while len(self) > value:
                self.pop()
        elif len(self) < value:
            self.extend([null] * (value - len(self)))

    def __class_getitem__(cls, value):
        '''
        This is the closest python equivalent to Vector.<T>[]

        It is instead used like "Vector[T]([])"
        '''
        return _VectorType(value)

    def __init__(self, length=0, fixed: Boolean = false, **kwargs):
        self._type = kwargs['type']

        # Function behaviour
        if isinstance(length, (list, tuple, Array, Vector)):
            # TODO: Make sure this works properly
            if isinstance(length, Vector):
                self._fixed = length.fixed
                self._superclass = length._superclass
            self.fixed = false
            self._superclass = True
            super().__init__([Vector._convertToType(i, self._type, self._superclass) for i in each(length)])

        # Constructor behaviour
        else:
            self._superclass = False
            self.fixed = fixed
            super().__init__([null] * length)

    def __iter__(self):
        return (i for i in range(len(self)))

    def __each__(self):
        return (self[i] for i in range(len(self)))

    def extend(self, iterable):
        super().extend(each(iterable))

    @staticmethod
    def _join(o, sep=undefined):
        if sep is undefined:
            s = ','
        else:
            s = str(String(sep))
        with StringIO() as out:
            for i in o:
                x = o[i]
                if x is not null:
                    out.write(str(x))
                if i + 1 < o.length:
                    out.write(s)
            return String(out.getvalue())

    def __repr__(self):
        return 'Vector.<%s>(%s)' % (self._type.__name__, self)

    def __getitem__(self, item):
        return super().__getitem__(item)

    def __setitem__(self, item, value):
        if item == self.length and not self.fixed:
            # Vectors, unlike Arrays, can only set values at an index less
            # than or equal their length
            self.append(Vector._convertToType(value, self._type, self._superclass))
        else:
            super().__setitem__(item, Vector._convertToType(value, self._type, self._superclass))

    def __delitem__(self, item):
        raise NotImplementedError

    def concat(self, *args):
        temp = Vector[self._type](self)
        if len(args) > 0:
            for i in args:
                if not isinstance(i, Vector):
                    raise TypeError('Vector.concat; One or more arguements are not of type Vector')
                # TODO: This check will not work with _VectorType
                if not issubclass(i._type, self._type):
                    raise TypeError('Vector.concat; One or more arguements do not have a base type that can be converted to the current base type.')
                temp.extend(i)
        temp.fixed = self.fixed
        return temp

    def every(self, callback, thisObject=null):
        if callback is null:
            return true
        for i in self:
            if not callback(self[i], i, self):
                return false
        return true

    def filter(self, callback, thisObject=null):
        # TODO: Handle null callback
        tempVector = Vector[self._type]()
        tempVector._superclass = self._superclass
        for i in self:
            if callback(self[i], i, self):
                tempVector.push(self[i])
        return tempVector

    def forEach(self, callback, thisObject=null):
        if callback is null:
            return undefined
        for i in self:
            callback(self[i], i, self)

    def indexOf(self, searchElement, fromIndex: int = 0):
        if fromIndex < 0:
            fromIndex = len(self) - fromIndex
        for i in range(fromIndex, len(self)):
            if stricteq(self[i], searchElement):
                return i
        return -1

    def insertAt(self, index, element):
        if self.fixed:
            raise RangeError('insertAt can not be called on a Vector with fixed set to true.')
        elif self._superclass:
            if element is null or isinstance(element, self._type):
                raise NotImplementedError
        else:
            raise NotImplementedError

    def join(self, sep: String = ','):
        return Vector._join(self, sep)

    def lastIndexOf(self, searchElement, fromIndex = null):
        # TODO: Negative fromIndex
        if fromIndex is null:
            fromIndex = self.length - 1
        fromIndex = int(fromIndex)
        for i in range(fromIndex, -1, -1):
            if stricteq(self[i], searchElement):
                return int(i)
        return int(-1)

    def map(self, callback, thisObject=null):
        # TODO: Handle null callback
        tempVect = Vector[self._type](self.length)
        tempVect._superclass = self._superclass
        for i in self:
            tempVect[i] = callback(self[i], i, self)
        return tempVect

    def pop(self):
        if self.fixed:
            raise RangeError('pop can not be called on a Vector with fixed set to true.')
        return super().pop(-1)

    def push(self, *args):
        if self.fixed:
            raise RangeError('push can not be called on a Vector with fixed set to true.')
        # !Check item types
        self.extend(args)
        return len(self)

    def removeAt(self, index: int):
        if self.fixed:
            raise RangeError('removeAt can not be called on a Vector with fixed set to true.')
        index = int(index)
        if index < -self.length or self.length and index > self.length - 1:
            raise RangeError('index is out of bounds.')
        return super().pop(index)

    def reverse(self):
        super().reverse()
        return self

    def shift(self):
        if self.fixed:
            raise RangeError('shift can not be called on a Vector with fixed set to true.')
        return super().pop(0)

    def slice(self, startIndex: int = 0, endIndex: int = 16777215):
        raise NotImplementedError

    def some(self, callback, thisObject=null):
        if callback is null:
            return false
        for i in self:
            if callback(self[i], i, self):
                return true
        return false

    def sort(self, sortBehavior):
        raise NotImplementedError

    def splice(self, startIndex: int, deleteCount: uint = null, *items):
        raise NotImplementedError

    def toLocaleString(self):
        with StringIO() as out:
            n = self.length
            for i in range(n):
                x = self[i]
                if x is not undefined and x is not null:
                    if hasattr(x, 'toLocaleString'):
                        out.write(str(x.toLocaleString()))
                    else:
                        out.write(str(x))
                if i + 1 < n:
                    out.write(',')
            return String(out.getvalue())

    def toString(self):
        return Vector._join(self)

    def unshift(self, *args):
        if self.fixed:
            raise RangeError('unshift can not be called on a Vector with fixed set to true.')
        fillerArray = []
        for i in args:
            fillerArray.append(Vector._convertToType(i, self._type, self._superclass))
        tempVect = (*fillerArray, *each(self))
        self.clear()
        self.extend(tempVect)
        return len(self)


class Namespace(Object):
    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = value if value is undefined else String(value)

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, value):
        self._uri = String(value)

    def __init__(self, *args):
        # Fix enumeration order
        self._uri = undefined
        self._prefix = undefined

        if len(args) >= 2:
            val1 = args[0]
            val2 = args[1]
            if val1 is null:
                val1 = undefined
            self.prefix = val1 if isXMLName(val1) or val1 == '' else undefined
            if isinstance(val2, QName):
                self.uri = val2.uri
            elif self.prefix != '' and isinstance(val2, str) and not len(val2):
                raise TypeError('Illegal prefix %s for no namespace.' % self.prefix, 1098)
            else:
                self.uri = val2
        elif len(args):
            val = args[0]
            if isinstance(val, Namespace):
                self.prefix = val.prefix
                self.uri = val.uri
            elif isinstance(val, QName):
                self.prefix = undefined
                self.uri = val.uri
            elif isinstance(val, str) and val == '':
                self.prefix = ''
                self.uri = ''
            else:
                self.prefix = undefined
                self.uri = val
        else:
            self.prefix = ''
            self.uri = ''

    def toString(self):
        return self.uri

    def valueOf(self):
        return self.uri


class QName(Object):
    @property
    def localName(self):
        return self._localName

    @property
    def uri(self):
        return self._uri

    def __init__(self, *args):
        self._uri = null
        if len(args) >= 2:
            uri = args[0]
            localName = args[1]
            if isinstance(uri, Namespace):
                self._uri = uri.uri
            elif uri is not null:
                self._uri = String(uri)
            if isinstance(localName, QName):
                self._localName = localName.localName
            else:
                self._localName = String(localName)
        elif len(args):
            qname = args[0]
            if isinstance(qname, QName):
                self._localName = qname.localName
                self._uri = qname.uri
            elif qname is undefined or qname is null:
                self._localName = String()
            else:
                self._localName = String(qname)
        else:
            self._localName = String()

    def toString(self):
        if self.uri == '':
            return self.localName
        elif self.uri is null:
            return String('*::%s' % self.localName)
        return String('%s::%s' % (self.uri, self.localName))

    def valueOf(self):
        return self


class XMLList(Object):
    # TODO: Check to see if any of these functions should return a flattened list
    def __init__(self, value):
        self._value = Array()
        ...

    def attribute(self, attributeName):
        res = Array()
        for i in each(self._value):
            j = i.attributes(attributeName)
            if j.length() > 0:
                res.append(j)
        return XMLList(res)

    def attributes(self):
        return XMLList([i.attributes() for i in each(self._value)])

    def child(self, propertyName):
        return XMLList([i.child(propertyName) for i in each(self._value)])

    def children(self):
        return XMLList([i.children() for i in each(self._value)])

    def comments(self):
        raise NotImplementedError

    def contains(self, value):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError

    def decendants(self, name):
        raise NotImplementedError

    def elements(self, name):
        raise NotImplementedError

    def hasComplexContext(self):
        raise NotImplementedError

    def hasOwnProperty(self, p):
        raise NotImplementedError

    def hasSimpleContext(self):
        raise NotImplementedError

    def length(self):
        return self._value.length

    def normalize(self):
        raise NotImplementedError

    def parent(self):
        raise NotImplementedError

    def processingInstructions(self, name):
        raise NotImplementedError

    def propertyIsEnumerable(self, p):
        raise NotImplementedError

    def text(self):
        return XMLList([i.text() for i in self._value])

    def toString(self):
        raise NotImplementedError

    def toXMLString(self):
        raise NotImplementedError

    def valueOf(self):
        return self


class XML(Object):
    # Prerequisite: Object attribute access
    # TODO: Implement accessing children. This should be done by using <xmlobj>.<child>. Doing this appears to return all children with the name <child>
    # TODO: Add special handling for "@" at the start of child name
    ignoreComments = true
    ignoreProcessingInstructions = true
    ignoreWhitespace = true
    prettyIndent = 2
    prettyPrinting = true

    def __init__(self, value):
        self._name: QName = None
        self._type = None  # INTERNAL: Node type (text, comment, processing-instruction, attribute, or element)
        self._namespace = None
        self._namespaces = Array()
        ...

    def addNamespace(self, ns):
        raise NotImplementedError

    def appendChild(self, child):
        raise NotImplementedError

    def attribute(self, attributeName):
        raise NotImplementedError

    def attributes(self):
        raise NotImplementedError

    def child(self, propertyName):
        raise NotImplementedError

    def childIndex(self):
        raise NotImplementedError

    def children(self):
        raise NotImplementedError

    def comments(self):
        raise NotImplementedError

    def contains(self, value):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError

    @staticmethod
    def defaultSettings():
        obj = Object()
        obj.ignoreComments = true
        obj.ignoreProcessingInstructions = true
        obj.ignoreWhitespace = true
        obj.prettyIndent = int(2)
        obj.prettyPrinting = true
        return obj

    def decendants(self, name):
        raise NotImplementedError

    def elements(self, name):
        raise NotImplementedError

    def hasComplexContext(self):
        raise NotImplementedError

    def hasOwnProperty(self, p):
        raise NotImplementedError

    def hasSimpleContext(self):
        raise NotImplementedError

    def inScopeNamespace(self):
        raise NotImplementedError

    def inserChildAfter(self, child1, child2):
        raise NotImplementedError

    def insertChildBefore(self, child1, child2):
        raise NotImplementedError

    def length(self):
        return 1

    def localName(self):
        return self._name.localName

    def name(self):
        return self._name

    def namespace(prefix):
        raise NotImplementedError

    def namespaceDeclarations(self):
        raise NotImplementedError

    def nodeKind(self):
        return self._type

    def normalize(self):
        raise NotImplementedError

    def parent(self):
        raise NotImplementedError

    def prependChild(self):
        raise NotImplementedError

    def processingInstructions(self, name):
        raise NotImplementedError

    def propertyIsEnumerable(self, p):
        raise NotImplementedError

    def removeNamespace(self, ns):
        raise NotImplementedError

    def replace(self, propertyName, value):
        raise NotImplementedError

    def setChildren(self, value):
        raise NotImplementedError

    def setLocalName(self, name):
        self._name._localName = name

    def setName(self, name):
        raise NotImplementedError

    def setNamespace(self, ns: Namespace):
        self._namespace = ns

    @staticmethod
    def setSettings(*args, **rest):
        if len(args) == 1 and isinstance(args[0], Object):
            rest = args[0]
        if 'ignoreComments' in rest:
            XML.ignoreComments = rest['ignoreComments']
        if 'ignoreProcessingInstructions' in rest:
            XML.ignoreProcessingInstructions = rest['ignoreProcessingInstructions']
        if 'ignoreWhitespace' in rest:
            XML.ignoreWhitespace = rest['ignoreWhitespace']
        if 'prettyIndent' in rest:
            XML.prettyIndent = rest['prettyIndent']
        if 'prettyPrinting' in rest:
            XML.prettyPrinting = rest['prettyPrinting']

    @staticmethod
    def settings():
        obj = Object()
        obj.ignoreComments = XML.ignoreComments
        obj.ignoreProcessingInstructions = XML.ignoreProcessingInstructions
        obj.ignoreWhitespace = XML.ignoreWhitespace
        obj.prettyIndent = XML.prettyIndent
        obj.prettyPrinting = XML.prettyPrinting
        return obj

    def text(self):
        raise NotImplementedError

    def toString(self):
        raise NotImplementedError

    def toXMLString(self):
        raise NotImplementedError

    def valueOf(self):
        return self


# Functions
def decodeURI(uri):
    raise NotImplementedError


def decodeURIComponent(uri):
    raise NotImplementedError


def encodeURI(uri):
    raise NotImplementedError


def encodeURIComponent(uri):
    raise NotImplementedError


def escape(str):
    '''
    Converts the parameter to a string and encodes it in a URL-encoded format, where most nonalphanumeric characters are replaced with % hexadecimal sequences. When used in a URL-encoded string, the percentage symbol (%) is used to introduce escape characters, and is not equivalent to the modulo operator (%).
    The following characters are not converted to escape sequences by the escape() function.
    0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@-_.*+/
    '''
    raise NotImplementedError


def isFinite(num):
    num = Number(num)
    return not (math.isnan(num) or math.isinf(num))


def isNaN(num):
    return math.isnan(Number(num))


def isXMLName(str: String):
    # currently this is spec compatible with the actual xml specs but unknown if it is the same as the actionscript function.
    str = builtins.str(String(str))
    whitelist = {'-', '_', '.'}
    if not len(str) or not str[0].isalpha() and str[0] != '_' or str.lower().startswith('xml') or ' ' in str:
        return false
    for i in str:
        if not i.isalnum() and i not in whitelist:
            return false
    return true


def parseFloat(str: String = undefined):
    # TODO: Make stop at second period
    # TODO: Properly handle Infinity
    # TODO: Handle exponent overflow
    if str is undefined:
        return Number.NaN
    str = builtins.str(String(str))
    str = str.lstrip()
    sign = ''
    if str.startswith(('-', '+')):
        sign = str[0]
        str = str[1:]
    if str == 'Infinity':
        if sign == '-':
            return Number.NEGATIVE_INFINITY
        return Number.POSITIVE_INFINITY
    if str.startswith('0x'):
        # parseFloat does not appear to handle hex values
        return Number(0)
    if str.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.')):
        digits = '0123456789.'
        exponent = ''
        size = len(str)
        j = 0
        while j < size and str[j] in digits:
            j += 1
        if j < size and str[j] in 'eE':
            exp_index = 0
            exponent = str[j+1:]
            exponentSign = ''
            str = str[:j]
            if exponent.startswith(('-', '+')):
                exponentSign = exponent[0]
                exponent = exponent[1:]
            while exp_index < len(exponent) and exponent[exp_index].isdigit():
                exp_index += 1
            if exp_index:
                return Number(float(f'{sign}{str}e{exponentSign}{exponent[:exp_index]}'))
            if sign:
                return Number.NaN
        return Number(float(sign + str[:j]))
    return Number.NaN


def parseInt(str: String = undefined, radix: uint = 0):
    # TODO:
    #       '010' => 2
    radix = uint(radix)
    if str is undefined:
        # Special case [object undefined]
        if radix >= 32:
            return Number(int(builtins.int('null', radix)))
        return Number.NaN
    str = builtins.str(String(str))
    str = str.lstrip()
    sign = ''
    if str.startswith(('-', '+')):
        sign = str[0]
        str = str[1:]
    if (radix == 16 or not radix) and str.startswith('0x'):
        radix = 16
        str = str[2:]
    if radix == 0:
        radix = 10
    if radix < 2 or radix > 36:
        return Number.NaN
    radixchars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:radix]
    str = str.upper()
    if radix == 10 and str.find('E') != -1:
        return Math.floor(parseFloat(str))
    index = 0
    while index < len(str) and str[index] in radixchars:
        index += 1
    if index == 0:
        return Number.NaN
    # TODO: See if Number is supposed to handle this instead of parseInt
    try:
        return Number(builtins.int(sign + str[:index], radix))
    except OverflowError:
        return Number.POSITIVE_INFINITY


def unescape(str):
    raise NotImplementedError


# Keyword functions
def delete(obj):
    # TODO: Other functionality of delete
    del obj
    return true


def each(iterable):
    '''
    Replacement for 'for each ...'

    Used like 'for i in each(<variable>):'
    '''
    if hasattr(iterable, '__each__'):
        return iterable.__each__()
    if hasattr(iterable, 'values') and callable(iterable.values):
        return iterable.values()
    # Do it a bit jank because python and actionscript differ in the way that
    # iterating is done.
    return (iterable[i] for i in range(len(iterable)))


# Operations
def _typeCompare(obj1, obj2):
    # This is needed because python objects can be used alongside as3lib
    # objects.
    if type(obj1) is int:
        return type(obj2) in {int, builtins.int}
    if type(obj1) is uint:
        return type(obj2) in {uint, builtins.int}
    if type(obj1) is builtins.int:
        return type(obj2) in {int, uint, builtins.int}
    if type(obj1) is Number:
        return type(obj2) in {Number, float}
    if type(obj1) is float:
        return type(obj2) in {Number, float}
    return type(obj1) is type(obj2)


def stricteq(obj1, obj2):
    if isinstance(obj1, Number) and math.isnan(obj1) and isinstance(obj2, Number) and math.isnan(obj2):
        return true
    return Boolean(_typeCompare(obj1, obj2) and obj1 == obj2)


def strictne(obj1, obj2):
    return Boolean(not _typeCompare(obj1, obj2) or obj1 != obj2)


# Helpers
def as3_enumerate(iterable):
    '''
    Python enumerate function for AS3 objects. AS3 objects use a custom
    implementation of __iter__ which breaks the builtin enumerate function.
    '''
    return ((i, iterable[i]) for i in iterable)
