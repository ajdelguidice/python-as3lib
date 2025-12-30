class _undefined:
   __slots__ = ("value")

   def __init__(self):
      self.value = None

   def __str__(self):
      return "undefined"

   def __repr__(self):
      return "as3lib.undefined"


class _null:
   __slots__ = ("value")

   def __init__(self):
      self.value = None

   def __str__(self):
      return "null"

   def __repr__(self):
      return "as3lib.null"

undefined = _undefined()
null = _null()
