from as3lib import Error


class DRMManagerError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'DRMManagerError'


class EOFError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'EOFError'


class IllegalOperationError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'IllegalOperationError'


class InvalidSWFError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'InvalidSWFError'


class IOError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'IOError'


class MemoryError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'MemoryError'


class PermissionError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'PermissionError'


class ScriptTimeoutError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'ScriptTimeoutError'


class SQLError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'SQLError'


class SQLErrorOperation(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'SQLErrorOperation'


class StackOverflowError(Error):
   def __init__(self, message=''):
      super().__init__(message)
      self.name = 'StackOverflowError'
