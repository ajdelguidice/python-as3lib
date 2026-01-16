from as3lib._toplevel.BaseTypes import Math, Number
from as3lib._toplevel.Object import Object
import datetime, time


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
# Rewrite Date to not have to store the date twice. The original implementation
# likely only store the utc timestamp


def _getTimezone():
   if time.daylight:
      return datetime.timezone(datetime.timedelta(seconds=-time.altzone),time.tzname[1])
   return datetime.timezone(datetime.timedelta(seconds=-time.timezone),time.tzname[0])


class Date(Object):
   @property
   def date(self):
      return Number(self._value.day)

   @date.setter
   def date(self, value):
      self._value = self._value.replace(day=value)
      self._sync()

   @property
   def dateUTC(self):
      return Number(self._valueUTC.day)

   @dateUTC.setter
   def dateUTC(self, value):
      self._valueUTC = self._valueUTC.replace(day=value)
      self._syncUTC()

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
      self._value = self._value.replace(year=value)
      self._sync()

   @property
   def fullYearUTC(self):
      return Number(self._valueUTC.year)

   @fullYearUTC.setter
   def fullYearUTC(self, value):
      self._valueUTC = self._valueUTC.replace(year=value)
      self._syncUTC()

   @property
   def hours(self):
      return Number(self._value.hour)

   @hours.setter
   def hours(self, value):
      self._value = self._value.replace(hour=value)
      self._sync()

   @property
   def hoursUTC(self):
      return Number(self._valueUTC.hour)

   @hoursUTC.setter
   def hoursUTC(self, value):
      self._valueUTC = self._valueUTC.replace(hour=value)
      self._syncUTC()

   @property
   def milliseconds(self):
      return Number(self._value.microsecond / 1000)

   @milliseconds.setter
   def milliseconds(self, value):
      self._value = self._value.replace(microsecond=value*1000)
      self._sync()

   @property
   def millisecondsUTC(self):
      return Number(self._valueUTC.microsecond / 1000)

   @millisecondsUTC.setter
   def millisecondsUTC(self, value):
      self._valueUTC = self._valueUTC.replace(microsecond=value*1000)
      self._syncUTC()

   @property
   def minutes(self):
      return Number(self._value.minute)

   @minutes.setter
   def minutes(self, value):
      self._value = self._value.replace(minute=value)
      self._sync()

   @property
   def minutesUTC(self):
      return Number(self._valueUTC.minute)

   @minutesUTC.setter
   def minutesUTC(self, value):
      self._valueUTC = self._valueUTC.replace(minute=value)
      self._syncUTC()

   @property
   def month(self):
      return Number(self._value.month - 1)

   @month.setter
   def month(self, value):
      self._value = self._value.replace(month=value+1)
      self._sync()

   @property
   def monthUTC(self):
      return Number(self._valueUTC.month - 1)

   @monthUTC.setter
   def monthUTC(self, value):
      self._valueUTC = self._valueUTC.replace(month=value+1)
      self._syncUTC()

   @property
   def seconds(self):
      return Number(self._value.second)

   @seconds.setter
   def seconds(self, value):
      self._value = self._value.replace(second=value)
      self._sync()

   @property
   def secondsUTC(self):
      return Number(self._valueUTC.second)

   @secondsUTC.setter
   def secondsUTC(self, value):
      self._valueUTC = self._valueUTC.replace(second=value)
      self._syncUTC()

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

   def __init__(self, yearOrTimevalue=None, month=None, date=1, hour=0, minute=0, second=0, millisecond=0):
      # TODO: When NaN is passed as the first arguement, all values should be set to NaN
      #       When a value is set after this, all other values become the default
      self._localtz = _getTimezone()
      if yearOrTimevalue is None and month is None:
         # Passed no arguements. Use current date and time
         self._value = datetime.datetime.now(tz=self._localtz)
         self._sync()
      elif isinstance(yearOrTimevalue, (int, float, Number)) and month is None:
         # One arguement of type Number is passed. Interpret as utc timestamp
         # TODO: _localtz is wrong here
         self._valueUTC = datetime.datetime.fromtimestamp(yearOrTimevalue / 1000, datetime.timezone.utc)
         self._syncUTC()
      elif isinstance(yearOrTimevalue, str) and month is None:
         # One arguement of type String is passed. Parse date string
         raise NotImplementedError('One aruement of type String')  # TODO
      elif isinstance(yearOrTimevalue, Object) and month is None:
         # TODO: All values should be set to NaN if yearOrTimevalue.valueOf returns a string
         self._valueUTC = datetime.datetime.fromtimestamp(yearOrTimevalue.valueOf() / 1000, datetime.timezone.utc)
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
      self.date = day
      self._sync()
      return self.milliseconds

   def setFullYear(self, year, month, day):
      raise NotImplementedError

   def setHours(self, hour, minute, second, millisecond):
      raise NotImplementedError

   def setMilliseconds(self, millisecond):
      raise NotImplementedError

   def setMinutes(self, minutes, seconds, milliseconds):
      raise NotImplementedError

   def setMonth(self, month, day):
      raise NotImplementedError

   def setSeconds(self, second, millisecond):
      raise NotImplementedError

   def setTime(self, millisecond):
      raise NotImplementedError

   def setUTCDate(self, day):
      self.dateUTC = day
      self._syncUTC()
      return self.milliseconds

   def setUTCFullYear(self, year, month, day):
      raise NotImplementedError

   def setUTCHours(self, hour, minute, second, millisecond):
      raise NotImplementedError

   def setUTCMilliseconds(self, millisecond):
      raise NotImplementedError

   def setUTCMinutes(self, minutes, seconds, milliseconds):
      raise NotImplementedError

   def setUTCMonth(self, month, day):
      raise NotImplementedError

   def setUTCSeconds(self, second, millisecond):
      raise NotImplementedError

   def _monthName(self, mon):
      return ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
              'Oct', 'Nov', 'Dec')[int(mon)]

   def _dayName(self, date):
      return ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')[int(date)]

   def _timezone(self):
      sec = self.timezoneOffset
      sign = '-' if sec < 0 else '+'
      hours = Math.abs(Math.floor(sec / 60))
      minutes = sec % 60
      if hours == 0 and minutes == 0:
         return 'GMT'
      return f'GMT{sign}{hours:0>2}{minutes:0>2}'

   def _time(self, HH, MM, SS):
      return f'{int(HH):0>2}:{int(MM):0>2}:{int(SS):0>2}'

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
      return '%s %s %s %s %s %s' % (
         self._dayName(self.day), self._monthName(self.month), self.date, self._time(self.hours, self.minutes, self.seconds), self._timezone(), self.fullYear)

   def toTimeString(self):
      return '%s %s' % (self._time(self.hours, self.minutes, self.seconds), self._timezone())

   def toUTCString(self):
      return '%s %s %s %s %s UTC' % (self._dayName(self.dayUTC), self._monthName(self.monthUTC), self.dateUTC, self._time(self.hoursUTC, self.minutesUTC, self.secondsUTC), self.fullYearUTC)

   @staticmethod
   def UTC(year, month, date=1, hour=0, minute=0, second=0, millisecond=0):
      return Number(datetime.datetime(year, month, date, hour, minute, second, millisecond * 1000, tzinfo=datetime.timezone.utc).timestamp() * 1000)

   def valueOf(self):
      return self.time
