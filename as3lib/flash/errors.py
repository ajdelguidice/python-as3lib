from as3lib._toplevel.Errors import Error

#finish implementing everything from these classes
class DRMManagerError(Error):
   name = 'DRMManagerError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class EOFError():
   name = 'EOFError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class IllegalOperationError():
   name = 'IllegalOperationError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class InvalidSWFError():
   name = 'InvalidSWFError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class IOError():
   name = 'IOError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class MemoryError():
   name = 'MemoryError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class PermissionError():
   name = 'PermissionError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class ScriptTimeoutError():
   name = 'ScriptTimeoutError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class SQLError():
   name = 'SQLError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class SQLErrorOperation():
   name = 'SQLErrorOperation'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
class StackOverflowError():
   name = 'StackOverflowError'
   def __init__(self, message):
      self.message = message
      super().__init__(message)
