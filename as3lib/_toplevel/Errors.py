from as3lib._toplevel.Functions import trace
from as3lib._toplevel.Object import Object
import traceback

#! Implement the debug functionality as specified here https://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/Error.html
class Error(Exception, Object):
   #! Make this a child of Object
   name = 'Error'
   message = 'Error'
   errorID = 0 # This isn't implemented yet
   def __init__(self, message="", id=0):
      self.errorID = id
      self.message = message
      trace(self.toString(),isError=True)
   def getStackTrace(self):
      return f'{self.name}: Error #{self.errorID}: {self.message}\n{"".join(traceback.format_tb(self.__traceback__))}'
   def toString(self):
      return f'{self.name}: {self.message}'

class ArgumentError(Error):
   name = 'ArguementError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class DefinitionError(Error):
   name = 'DefinitionError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class EvalError(Error):
   name = 'EvalError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class RangeError(Error):
   name = 'RangeError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class ReferenceError(Error):
   name = 'ReferenceError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class SecurityError(Error):
   name = 'SecurityError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class SyntaxError(Error):
   name = 'SyntaxError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class TypeError(Error):
   name = 'TypeError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class URIError(Error):
   name = 'URIError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class VerifyError(Error):
   name = 'VerifyError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
