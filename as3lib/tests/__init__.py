import as3lib
import unittest


class as3libTestCase(unittest.TestCase):
   def assertIdentical(self, obj1, obj2):
      if obj1 is not obj2:
         self.fail('%r is not %r' % (obj1, obj2))

   def assertNaN(self, obj):
      # NOTE: Relies on NaN being properly set up
      if not as3lib.isNaN(obj):
         self.fail('%r is not NaN' % obj)

   def assertNaNExact(self, obj):
      if obj is not as3lib.NaN:
         self.fail('%r is not NaN' % obj)


class TestNotImplemented(NotImplementedError):
   ...


class MethodNotImplemented(NotImplementedError):
   ...
