from as3lib._toplevel.Number import Number
from as3lib._toplevel.Object import Object
import datetime


# Notes:
# Python's datetime object (used internally for Date) has microseconds, not
# milliseconds, so some math must be done to convert between the two when
# used.
#
# Python uses 1 as January but flash uses 0, so math needs to be done here too
#
# Python starts the week on Monday but flash starts it on Sunday

# TODO:
# UTC stuff
# Timezone stuff
# Most toString variants
# Date.parse
# Date constructor with one argument.


class Date(Object):
   @property
   def date(self):
      return Number(self._value.day)

   @date.setter
   def date(self, value):
      self._value = self._value.replace(day=value)

   @property
   def dateUTC(self):
      raise NotImplementedError

   @dateUTC.setter
   def dateUTC(self, value):
      raise NotImplementedError

   @property
   def day(self):
      return Number(self._value.toordinal() % 7)

   @property
   def dayUTC(self):
      raise NotImplementedError

   @property
   def fullYear(self):
      return Number(self._value.year)

   @fullYear.setter
   def fullYear(self, value):
      self._value = self._value.replace(year=value)

   @property
   def fullYearUTC(self):
      raise NotImplementedError

   @fullYearUTC.setter
   def fullYearUTC(self, value):
      raise NotImplementedError

   @property
   def hours(self):
      return Number(self._value.hour)

   @hours.setter
   def hours(self, value):
      self._value = self._value.replace(hour=value)

   @property
   def hoursUTC(self):
      raise NotImplementedError

   @hoursUTC.setter
   def hoursUTC(self, value):
      raise NotImplementedError

   @property
   def milliseconds(self):
      return Number(self._value.microsecond / 1000)

   @milliseconds.setter
   def milliseconds(self, value):
      self._value = self._value.replace(microsecond=value*1000)

   @property
   def millisecondsUTC(self):
      raise NotImplementedError

   @millisecondsUTC.setter
   def millisecondsUTC(self, value):
      raise NotImplementedError

   @property
   def minutes(self):
      return Number(self._value.minute)

   @minutes.setter
   def minutes(self, value):
      self._value = self._value.replace(minute=value)

   @property
   def minutesUTC(self):
      raise NotImplementedError

   @minutesUTC.setter
   def minutesUTC(self, value):
      raise NotImplementedError

   @property
   def month(self):
      return Number(self._value.month - 1)

   @month.setter
   def month(self, value):
      self._value = self._value.replace(month=value+1)

   @property
   def monthUTC(self):
      raise NotImplementedError

   @monthUTC.setter
   def monthUTC(self, value):
      raise NotImplementedError

   @property
   def seconds(self):
      return Number(self._value.second)

   @seconds.setter
   def seconds(self, value):
      self._value = self._value.replace(second=value)

   @property
   def secondsUTC(self):
      raise NotImplementedError

   @secondsUTC.setter
   def secondsUTC(self, value):
      raise NotImplementedError

   @property
   def time(self):
      # TODO: Return timestamp in utc not local time
      return Number(self._value.timestamp() * 1000)

   @time.setter
   def time(self, value):
      raise NotImplementedError

   @property
   def timezoneOffset(self):
      raise NotImplementedError

   def __init__(self, yearOrTimevalue=None, month=None, date=1, hour=0, minute=0, second=0, millisecond=0):
      if yearOrTimevalue is None and month is None:
         # Passed no arguements. Use current date and time
         self._value = datetime.datetime.now()
      elif isinstance(yearOrTimevalue, (int, float, Number)) and month is None:
         # One arguement of type Number is passed. Interpret as utc timestamp
         raise NotImplementedError('One aruement of type Number')  # TODO
      elif isinstance(yearOrTimevalue, str) and month is None:
         # One arguement of type String is passed. Parse date string
         raise NotImplementedError('One aruement of type String')  # TODO
      else:
         # Two or more arguements are passed. Use arguements literally
         self._value = datetime.datetime(yearOrTimevalue, month + 1, date, hour, minute, second, millisecond * 1000)

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
      raise NotImplementedError

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

   def toDateString(self):
      raise NotImplementedError

   def toJSON(self, k):
      return self.toString()

   def toLocaleDateString(self):
      raise NotImplementedError

   def toLocaleString(self):
      raise NotImplementedError

   def toLocaleTimeString(self):
      raise NotImplementedError

   def toString(self):
      # TODO: Timezone
      return '%s %s %s %s:%s:%s %s %s' % (
         self._dayName(self.day), self._monthName(self.month), self.date, self.hours, self.minutes, self.seconds, None, self.fullYear)

   def toTimeString(self):
      #TODO: Timezone
      return '%s:%s:%s %s' % (self.hours, self.minutes, self.seconds, None)

   def toUTCString(self):
      # TODO: UTCday, UTCmon
      return '%s %s %s %s:%s:%s %s UTC' % (self._dayName(self.dayUTC), self._monthName(self.monthUTC), self.dateUTC, self.hoursUTC, self.secondsUTC, self.fullYearUTC)

   @staticmethod
   def UTC(year, month, date=1, hour=0, minute=0, second=0, millisecond=0):
      return Number(datetime.datetime(year, month, date, hour, minute, second, millisecond * 1000, tzinfo=datetime.timezone.utc).timestamp() * 1000)

   def valueOf(self):
      # TODO: This should be a utc timestamp
      return Number(self._value.timestamp() * 1000)
