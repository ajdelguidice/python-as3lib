from as3lib import Error


class DRMManagerError(Error):
   def __init__(self, message='', id=0):
      super().__init__(message, id)
      self.name = 'DRMManagerError'


class EOFError(Error):
   def __init__(self, message='', id=0):
      super().__init__(message, id)
      self.name = 'EOFError'


class IllegalOperationError(Error):
   def __init__(self, message='', id=0):
      super().__init__(message, id)
      self.name = 'IllegalOperationError'


class InvalidSWFError(Error):
   def __init__(self, message='', id=0):
      super().__init__(message, id)
      self.name = 'InvalidSWFError'


class IOError(Error):
   def __init__(self, message='', id=0):
      super().__init__(message, id)
      self.name = 'IOError'


class MemoryError(Error):
   def __init__(self, message='', id=0):
      super().__init__(message, id)
      self.name = 'MemoryError'


class PermissionError(Error):
   def __init__(self, message='', id=0):
      super().__init__(message, id)
      self.name = 'PermissionError'


class ScriptTimeoutError(Error):
   def __init__(self, message='', id=0):
      super().__init__(message, id)
      self.name = 'ScriptTimeoutError'


class SQLError(Error):
   def __init__(self, message='', id=0):
      super().__init__(message, id)
      self.name = 'SQLError'


class SQLErrorOperation(Error):
   def __init__(self, message='', id=0):
      super().__init__(message, id)
      self.name = 'SQLErrorOperation'


class StackOverflowError(Error):
   def __init__(self, message='', id=0):
      super().__init__(message, id)
      self.name = 'StackOverflowError'
