from as3lib._toplevel.trace import errorTrace
from as3lib._toplevel.Object import Object
import traceback


def _genErrNum():
   i = 0
   while True:
      yield i
      i += 1


_ErNo = _genErrNum()


# !Implement the debug functionality as specified here https://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/Error.html
class Error(Exception, Object):
   @property
   def errorID(self):
      return self._id

   @property
   def message(self):
      return self._message

   @message.setter
   def message(self, value):
      self._message = value

   @property
   def name(self):
      return self._name

   @name.setter
   def name(self, value):
      self._name = value

   def __init__(self, message='', id=0):
      self._name = 'Error'
      self._id = next(_ErNo) if id == 0 else id
      self._message = message if message != '' else 'Error'
      errorTrace(self.toString())

   @staticmethod
   def getErrorMessage(number):
      raise NotImplementedError

   def getStackTrace(self):
      return f'{self.name}: Error #{self.errorID}: {self.message}\n{"".join(traceback.format_tb(self.__traceback__))}'

   def toString(self):
      return f'{self.name}: {self.message}'


class ArgumentError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'ArgumentError'


class DefinitionError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'DefinitionError'


class EvalError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'EvalError'

class RangeError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'RangeError'


class ReferenceError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'ReferenceError'


class SecurityError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'SecurityError'


class SyntaxError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'SyntaxError'


class TypeError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'TypeError'


class URIError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'URIError'


class VerifyError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'VerifyError'
