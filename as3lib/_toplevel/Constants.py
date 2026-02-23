class undefined:
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

   # TODO: Circular reference
   #def __neg__(self):
   #   return NaN

   def __iter__(self):
      return iter([])

   def __each__(self):
      return iter([])

   def toString(self):
      return 'undefined'


class null:
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

   def __neg__(self):
      return 0

   def __iter__(self):
      return iter([])

   def __each__(self):
      return iter([])

   def toString(self):
      return 'null'

undefined = undefined()
null = null()
