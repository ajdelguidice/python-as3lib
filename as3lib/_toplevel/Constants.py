class _undefined:
   __slots__ = ("value")

   def __init__(self):
      self.value = None

   def __int__(self):
      return 0

   def __str__(self):
      return self.toString()

   def __repr__(self):
      return self.toString()

   def toString(self):
      return 'undefined'


class _null:
   __slots__ = ("value")

   def __init__(self):
      self.value = None

   def __int__(self):
      return 0

   def __str__(self):
      return self.toString()

   def __repr__(self):
      return self.toString()

   def __bool__(self):
      return False

   def toString(self):
      return 'null'

undefined = _undefined()
null = _null()
