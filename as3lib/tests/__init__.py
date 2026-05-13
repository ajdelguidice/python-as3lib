from as3lib import each, NaN, Number, stricteq, strictne
import unittest


class as3libTestCase(unittest.TestCase):
   def isNaNExplicit(self, obj):
      return hasattr(obj, '_is_nan') and obj._is_nan() or obj is NaN or obj is Number.NaN

   def assertEqualCheckNaN(self, value, check):
      if self.isNaNExplicit(check):
         self.assertNaN(value)
      else:
         self.assertEqual(value, check)

   def assertNaN(self, obj):
      if not self.isNaNExplicit(obj):
         self.fail('%r is not NaN' % obj)

   def assertArray(self, array, check, length=None):
      if length is not None:
         self.assertEqual(len(array), length)
      for i, item in enumerate(check):
         if array[i] != item:
            self.fail('Index %i; Expected "%r", got "%r"' % (i, item, array[i]))

   def assertType(self, obj, type_):
      self.assertEqual(type(obj), type_)

   def assertMatrix(self, matrix, a, b, c, d, tx, ty):
      self.assertEqual(matrix.a, a)
      self.assertEqual(matrix.b, b)
      self.assertEqual(matrix.c, c)
      self.assertEqual(matrix.d, d)
      self.assertEqual(matrix.tx, tx)
      self.assertEqual(matrix.ty, ty)

   def assertPoint(self, point, x, y):
      self.assertEqual(point.x, x)
      self.assertEqual(point.y, y)

   def assertVector3D(self, vector, x, y, z, w=None):
      self.assertEqual(vector.x, x)
      self.assertEqual(vector.y, y)
      self.assertEqual(vector.z, z)
      if w is not None:
         self.assertEqual(vector.w, w)

   def assertVector3DNaN(self, vector, w=None):
      self.assertNaN(vector.x)
      self.assertNaN(vector.y)
      self.assertNaN(vector.z)
      if w is not None:
         if w is NaN:
            self.assertNaN(vector.w)
         else:
            self.assertEqual(vector.w, w)

   def assertMatrix3D(self, matrix, values):
      self.assertArray(matrix.rawData, values)

   def assertEvent(self, e, event, type_, bubbles, cancelable, phase=None):
      self.assertIs(type(e), event)
      self.assertEqual(e.type, type_)
      self.assertEqual(e.bubbles, bubbles)
      self.assertEqual(e.cancelable, cancelable)
      if phase is not None:
         self.assertEqual(e.eventPhase, phase)

   def assertIter(self, obj, values, length=None):
      self.assertArray([i for i in obj], values, length)

   def assertEach(self, obj, values, length=None):
      self.assertArray([i for i in each(obj)], values, length)

   def assertQName(self, obj, localName, uri):
      self.assertEqual(obj.localName, localName)
      self.assertEqual(obj.uri, uri)

   def assertRaisesAS3(self, error, errorID, message, func, *args):
      try:
         func(*args)
      except Exception as e:
         self.assertIs(type(e), error)
         self.assertEqual(e.errorID, errorID)
         if message is not None:
            self.assertEqual(e.message, message)
      else:
         self.fail('Function didn\'t raise an error.')

   def assertStrictEQ(self, obj1, obj2):
      self.assertTrue(stricteq(obj1, obj2))

   def assertNotStrictEQ(self, obj1, obj2):
      self.assertFalse(stricteq(obj1, obj2))

   def assertStrictNE(self, obj1, obj2):
      self.assertTrue(strictne(obj1, obj2))

   def assertNotStrictNE(self, obj1, obj2):
      self.assertFalse(strictne(obj1, obj2))


class TestNotImplemented(NotImplementedError):
   ...


class MethodNotImplemented(NotImplementedError):
   ...
