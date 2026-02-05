# Most of these test cases are based on ones made by the ruffle.rs project
# https://github.com/ruffle-rs/ruffle

import as3lib
from as3lib import (ArgumentError, Array, Boolean, Date, DefinitionError,
                    delete, encodeURI, encodeURIComponent, Error, escape,
                    EvalError, false, Infinity, JSON, Math, Namespace, NaN,
                    null, Number, Object, QName, RangeError, ReferenceError,
                    RegExp, SecurityError, String, SyntaxError, true,
                    TypeError, uint, undefined, unescape, URIError, Vector,
                    VerifyError, XML, XMLList)
from as3lib.flash.errors import (EOFError, IllegalOperationError,
                                 InvalidSWFError, IOError, MemoryError,
                                 ScriptTimeoutError, StackOverflowError)
from as3lib.flash.utils import setTimeout
from as3lib.tests import as3libTestCase, TestNotImplemented, MethodNotImplemented
# TODO: Clear prototypes after every test


class ArrayTests(as3libTestCase):
   # NOTE: prototype is required for some tests
   def assertIndex(self, index, length, hasprop):
      arr = Array()
      arr[index] = 0
      self.assertEqual(arr.length, length)
      self.assertEqual(arr.hasOwnProperty(index), hasprop)
      self.assertEqual(arr[index], 0)

   def test_access(self):
      # TODO: Add more of this test
      a = Array('a', 'b', 'c')
      self.assertEqual(a[0], 'a')
      self.assertEqual(a[1], 'b')
      self.assertEqual(a[2], 'c')

      a = Array(5)
      self.assertEqual(a.length, 5)
      a[0] = 'First'
      a[2] = 'Second'
      a[3] = 'Third'
      self.assertEqual(a.removeAt(1), undefined)
      self.assertEqual(a.length, 4)

   def test_concat(self):
      a = Array('a', 'b', 'c')
      b = Array('d', 'e', 'f')
      c = a.concat(b)
      self.assertEqual(c, ['a', 'b', 'c', 'd', 'e', 'f'])
      d = a.concat('d', 'e', 'f')
      self.assertEqual(d, ['a', 'b', 'c', 'd', 'e', 'f'])
      e = a.concat('g', b, 'h')
      self.assertEqual(e, ['a', 'b', 'c', 'g', 'd', 'e', 'f', 'h'])
      f = a.concat(b, b)
      self.assertEqual(f, ['a', 'b', 'c', 'd', 'e', 'f', 'd', 'e', 'f'])
      g = a.concat(null, undefined)
      self.assertEqual(g, ['a', 'b', 'c', null, undefined])

   def test_constructor(self):
      self.assertEqual(Array().length, 0)
      self.assertEqual(Array(5).length, 5)
      self.assertEqual(Array('5').length, 1)
      self.assertEqual(Array(5, 6).length, 2)
      self.assertEqual(Array(5, 'abc').length, 2)

   def test_delete(self):
      a = Array('a', 'b', 'c')

      # Delete a[1]
      self.assertTrue(delete(a[1]))
      self.assertEqual(a.length, 3)
      self.assertArray(a, ['a', undefined, 'c', undefined])
      self.assertFalse(a.hasOwnProperty(1))

      # Delete a[2]
      self.assertTrue(delete(a[2]))
      self.assertEqual(a.length, 3)
      self.assertArray(a, ['a', undefined, undefined, undefined])
      self.assertFalse(a.hasOwnProperty(2))

      # Delete a[3]
      self.assertTrue(delete(a[3]))
      self.assertEqual(a.length, 3)
      self.assertArray(a, ['a', undefined, undefined, undefined])
      self.assertFalse(a.hasOwnProperty(3))

      # Delete a[4]
      self.assertTrue(delete(a[4]))
      self.assertEqual(a.length, 3)
      self.assertArray(a, ['a', undefined, undefined, undefined])
      self.assertFalse(a.hasOwnProperty(4))

   def test_enumeration(self):
      # NOTE: This test seems to prove that Arrays act more like python dictionaries
      a = Array(1, 2, 3, 4, 5)
      self.assertArray(a, [1, 2, 3, 4, 5])

      array = Array(5)
      array[0] = 'elem0'
      array[4] = 'elem4'
      array.prop = 'property'
      array[-1] = 'elem negative one'

      # TODO: Validate order

      # TODO: This will fail until array is rewritten
      self.assertIter(array, [0, 4], 4)

      self.assertEach(array, ['elem0', 'elem4'], 4)

   def test_enumeration_elements(self):
      a = Array(1, 2, 3, 4, 5)
      a.elem = 'test'

      self.assertEach(a, [1, 2, 3, 4, 5, 'test'], 6)

      self.assertTrue(a.propertyIsEnumerable('elem'))
      self.assertFalse(a.propertyIsEnumerable('another'))
      self.assertFalse(a.propertyIsEnumerable('random'))
      self.assertTrue(a.propertyIsEnumerable('3'))
      self.assertFalse(a.propertyIsEnumerable('7'))

   def test_every(self):
      a = Array(5, 3, 1, 9, 16)
      self.assertFalse(a.every(lambda val, i, j: val == 5))
      self.assertTrue(a.every(lambda val, i, j: val != 20))

      b = Array()
      self.assertTrue(b.every(lambda val, i, j: val == 5))

   def test_filter(self):
      a = Array(5, 3, 1, 9, 16)
      b = a.filter(lambda val, i, j: val <= 5)
      self.assertEqual(b, [5, 3, 1])

   def test_forEach(self):
      a = Array(5, 'abc')

      def test(val, index, array):
         self.assertTrue(val in a)
         self.assertLess(index, len(a))
         self.assertIs(array, a)

      a.forEach(test)

   def test_hasOwnProperty(self):
      a = Array(5)

      Array.prototype[3] = 'works'
      self.assertFalse(a.hasOwnProperty('2'))
      self.assertFalse(a.hasOwnProperty('3'))

      a[3] = 'nohole'
      self.assertFalse(a.hasOwnProperty('2'))
      self.assertTrue(a.hasOwnProperty('3'))

   def test_holes(self):
      a = Array(5)

      Array.prototype[3] = 'works'
      self.assertEqual(a[2], undefined)
      self.assertEqual(a[3], 'works')

      a[3] = 'nohole'
      self.assertEqual(a[3], 'nohole')

   def test_max_index(self):
      self.assertIndex(0, 1, True)
      self.assertIndex('0', 1, True)
      self.assertIndex(4294967293, 4294967294, True)
      self.assertIndex(4294967294, 4294967295, True)
      self.assertIndex(4294967295, 0, True)
      self.assertIndex(4294967296, 0, True)
      self.assertIndex(4294967297, 0, True)
      self.assertIndex("4294967293", 4294967294, True)
      self.assertIndex("4294967294", 4294967295, True)
      self.assertIndex("4294967295", 0, True)
      self.assertIndex("4294967296", 0, True)
      self.assertIndex("4294967297", 0, True)
      self.assertIndex(2147483645, 2147483646, True)
      self.assertIndex(2147483646, 2147483647, True)
      self.assertIndex(2147483647, 2147483648, True)
      self.assertIndex(2147483648, 2147483649, True)
      self.assertIndex(2147483649, 2147483650, True)

   def test_indexOf(self):
      a = Array(5, '5', 3, False, 4, 5, undefined, 9)
      self.assertEqual(a.indexOf(5), 0)
      self.assertEqual(a.indexOf(5, 1), 5)
      self.assertEqual(a.indexOf(5, 2), 5)
      self.assertEqual(a.indexOf(5, 6), -1)
      self.assertEqual(a.indexOf(5, 10), -1)
      self.assertEqual(a.indexOf(True), -1)
      self.assertEqual(a.indexOf(undefined), 6)
      self.assertEqual(a.indexOf('5'), 1)

   def test_join(self):
      a = Array('a', 'b', 'c')
      b = Array(1, 2, 3)
      c = Array(a, b)
      d = Array('str', 123, undefined, null, true, false)
      self.assertEqual(a.join(), 'a,b,c')
      self.assertEqual(b.join(), '1,2,3')
      self.assertEqual(c.join(), 'a,b,c,1,2,3')
      self.assertEqual(c.join(undefined), 'a,b,c,1,2,3')
      self.assertEqual(c.join(null), 'a,b,cnull1,2,3')
      self.assertEqual(c.join(false), 'a,b,cfalse1,2,3')
      self.assertEqual(a.join(NaN), 'aNaNbNaNc')
      self.assertEqual(b.join(5), '15253')
      self.assertEqual(c.join(' + '), 'a,b,c + 1,2,3')
      self.assertEqual(c.join(b), 'a,b,c1,2,31,2,3')
      self.assertEqual(d.join('!'), 'str!123!!!true!false')

   def test_lastIndexOf(self):
      a = Array(5, '5', 3, False, 4, 5, undefined, 9)
      self.assertEqual(a.lastIndexOf(5), 5)
      self.assertEqual(a.lastIndexOf(5, 1), 0)
      self.assertEqual(a.lastIndexOf(5, 2), 0)
      self.assertEqual(a.lastIndexOf(5, 6), 5)
      self.assertEqual(a.lastIndexOf(5, 10), 5)
      self.assertEqual(a.lastIndexOf(True), -1)
      self.assertEqual(a.lastIndexOf(undefined), 6)
      self.assertEqual(a.lastIndexOf('5'), 1)

   def test_length(self):
      self.assertEqual(Array().length, 0)
      self.assertEqual(Array(0, 1, 2, 3, 4).length, 5)
      self.assertEqual(Array(undefined).length, 1)
      a = Array(0, 1, 2)
      self.assertEqual(a.length, 3)
      a.length = 5
      self.assertEqual(a.length, 5)
      self.assertEqual(a.toString(), '0,1,2,,')
      a.length = 0
      self.assertEqual(a.length, 0)
      self.assertEqual(a.toString(), '')

   def test_literal(self):
      a = Array('a', 'b', 'c')
      self.assertEqual(a[0], 'a')
      self.assertEqual(a[1], 'b')
      self.assertEqual(a[2], 'c')

   def test_map(self):
      a = Array(5, 3, 1, 9, 16)
      b = a.map(lambda val, i, j: val + 1)
      self.assertEqual(b, [6, 4, 2, 10, 17])

   def test_pop(self):
      a = Array(5)
      a[1] = 'other_test'
      a[2] = 'test'
      Array.prototype[3] = 'works'

      self.assertEqual(a.toString(), ',other_test,test,works,')
      self.assertEqual(a.length, 5)

      self.assertEqual(a.pop(), 'test')
      self.assertEqual(a.toString(), ',other_test,,works')
      self.assertEqual(a.length, 4)

      self.assertEqual(a.pop(), 'other_test')
      self.assertEqual(a.toString(), ',,')
      self.assertEqual(a.length, 3)

      self.assertEqual(a.pop(), undefined)
      self.assertEqual(a.toString(), ',')
      self.assertEqual(a.length, 2)

      self.assertEqual(a.pop(), undefined)
      self.assertEqual(a.toString(), '')
      self.assertEqual(a.length, 1)

      self.assertEqual(a.pop(), undefined)
      self.assertEqual(a.toString(), '')
      self.assertEqual(a.length, 0)

      self.assertEqual(a.pop(), undefined)
      self.assertEqual(a.toString(), '')
      self.assertEqual(a.length, 0)

   def test_push(self):
      a = Array(5)
      a[2] = 'test'
      Array.prototype[3] = 'works'

      self.assertEqual(a.toString(), ',,test,works,')

      a.push('hi', 'bye')
      self.assertEquals(a.length, 7)
      self.assertEquals(a.toString(), ',,test,works,,hi,bye')

      a.push()
      self.assertEquals(a.length, 7)
      self.assertEquals(a.toString(), ',,test,works,,hi,bye')

   def test_reverse(self):
      a = Array(5)
      Array.prototype[0] = 0
      a[1] = 1
      a[2] = 2
      a[3] = undefined
      Array.prototype[4] = 4

      self.assertEqual(a.length, 5)

      b = a.reverse()
      self.assertEqual(a, b)
      self.assertEqual(a.toString(), ',2,1,,4')
      self.assertEqual(b.toString(), ',2,1,,4')

      Array.prototype[4] = 999
      self.assertEqual(b.toString(), ',2,1,,999')

   def test_shift(self):
      a = Array(5)
      a[2] = 'test'
      Array.prototype[3] = 'works'

      self.assertArray(a, [undefined, undefined, 'test', 'works', undefined], 5)

      self.assertEqual(a.shift(), undefined)
      self.assertArray(a, [undefined, 'test', undefined, 'works'], 4)

      self.assertEqual(a.shift(), undefined)
      self.assertArray(a, ['test', undefined, undefined], 3)

      self.assertEqual(a.shift(), 'test')
      self.assertArray(a, [undefined, undefined], 2)

      self.assertEqual(a.shift(), undefined)
      self.assertArray(a, [undefined], 1)

      self.assertEqual(a.shift(), undefined)
      self.assertArray(a, [], 0)

      self.assertEqual(a.shift(), undefined)
      self.assertArray(a, [], 0)

   def test_slice(self):
      a = Array(8)

      Array.prototype[0] = 999
      Array.prototype[1] = 998
      a[2] = 2
      Array.prototype[3] = 997
      a[4] = 4
      Array.prototype[5] = 996
      a[6] = 6
      Array.prototype[7] = 995

      b = a.slice()
      self.assertArray(b, [999, 998, 2, 997, 4, 996, 6, 995])

      c = a.slice(0, 3)
      self.assertArray(c, [999, 998, 2])

      d = a.slice(-1, 3)
      self.assertArray(d, [], 0)

      e = a.slice(0, -3)
      self.assertArray(e, [999, 998, 2, 997, 4])

      f = a.slice(-1, -3)
      self.assertArray(f, [], 0)

      g = a.slice(-3, -1)
      self.assertArray(g, [999, 6])

   def test_some(self):
      a = Array(5, 3, 1, 9, 16)
      self.assertTrue(a.some(lambda val, i, j: val == 5))
      self.assertFalse(a.some(lambda val, i, j: val == 20))

      b = Array()
      self.assertFalse(b.some(lambda val, i, j: val == 30))

   def test_sort(self):
      def newArray():  # fresh_array
         a = Array(5, 3, 1, 'Abc', '2', 'aba', false, null, 'zzz')
         a[11] = 'not a hole'
         return a

      def newArray2():  # fresh_array_b
         b = Array(5, 3, '2', false, true, NaN)
         return b

      def sub_comparison(a, b):
         return a - b

      def length_based_comparison(a, b):
         # NOTE: Checks were originally done like '"length" in a'
         if hasattr(a, 'length'):
            if hasattr(b, 'length'):
               return a.length - b.length
            return a.length - b
         if hasattr(b, 'length'):
            return a - b.length
         return a - b

      def lbc(a, b):
         # trace(a);
         # trace(b);
         x = length_based_comparison(a, b)
         # trace(x);
         return x

      def sc(a, b):
         # trace(a);
         # trace(b);
         x = sub_comparison(a, b)
         # trace(x);
         return x

      def check_holes(a, check):
         Array.prototype[10] = 'hole10'
         Array.prototype[11] = 'hole11'
         Array.prototype[12] = 'hole12'

         self.assertArray(a, check)

         # Clean up
         delete(Array.prototype[10])
         delete(Array.prototype[11])
         delete(Array.prototype[12])

         Array.prototype[9] = undefined
         Array.prototype[10] = 'hole in slot 10'

      # NOTE: Only returns when 4 or 8 is specified
      a = newArray()
      Array.prototype[9] = undefined
      Array.prototype[10] = 'hole in slot 10'
      s = a.sort(Array.UNIQUESORT)
      self.assertNotEqual(s, 0)


      a = newArray()
      s = a.sort(Array.RETURNINDEXEDARRAY)
      self.assertArray(s, [2, 4, 1, 0, 3, 5, 6, 10, 11, 7, 8, 9])

      a.sort()
      self.assertArray(a, [1, '2', 3, 5, 'Abc', 'aba', false,
                           'hole in slot 10', 'not a hole', null, 'zzz',
                           undefined])

      check_holes(a, [1, '2', 3, 5, 'Abc', 'aba', false, 'hole in slot 10',
                      'not a hole', null, 'zzz', 'hole11'])


      a = newArray()

      s = a.sort(Array.CASEINSENSITIVE | Array.RETURNINDEXEDARRAY)
      self.assertArray(s, [2, 4, 1, 0, 5, 3, 6, 10, 11, 7, 8, 9])

      a.sort(Array.CASEINSENSITIVE)
      self.assertArray(a, [1, '2', 3, 5, 'aba', 'Abc', false,
                           'hole in slot 10', 'not a hole', null, 'zzz',
                           undefined])

      check_holes(a, [1, '2', 3, 5, 'aba', 'Abc', false, 'hole in slot 10',
                      'not a hole', null, 'zzz', 'hole11'])


      a = newArray()

      s = a.sort(Array.DESCENDING | Array.RETURNINDEXEDARRAY)
      self.assertArray(s, [8, 7, 11, 10, 6, 5, 3, 0, 1, 4, 2, 9])

      a.sort(Array.DESCENDING)
      self.assertArray(a, ['zzz', null, 'not a hole', 'hole in slot 10',
                           false, 'aba', 'Abc', 5, 3, '2', 1, undefined])

      check_holes(a, ['zzz', null, 'not a hole', 'hole in slot 10', false,
                      'aba', 'Abc', 5, 3, '2', 1, 'hole11'])


      a = newArray()

      s = a.sort(Array.CASEINSENSITIVE | Array.DESCENDING | Array.RETURNINDEXEDARRAY)
      self.assertArray(s, [8, 7, 11, 10, 6, 3, 5, 0, 1, 4, 2, 9])

      a.sort(Array.CASEINSENSITIVE | Array.DESCENDING)
      self.assertArray(a, ['zzz', null, 'not a hole', 'hole in slot 10',
                           false, 'Abc', 'aba', 5, 3, '2', 1,
                           undefined])

      check_holes(a, ['zzz', null, 'not a hole', 'hole in slot 10', false,
                      'Abc', 'aba', 5, 3, '2', 1, 'hole11'])


      b = Array(5, 3, 2, 1, '2', false, true, NaN)
      s = b.sort(Array.NUMERIC | Array.UNIQUESORT)
      self.assertEqual(s, 0)


      b = newArray2()

      s = b.sort(Array.NUMERIC | Array.RETURNINDEXEDARRAY)
      self.assertArray(s, [3, 4, 2, 1, 0, 5])

      b.sort(Array.NUMERIC)
      self.assertArray(b, [false, true, '2', 3, 5, NaN])

      check_holes(b, [false, true, '2', 3, 5, NaN])


      b = newArray2()

      b.sort(Array.NUMERIC | 1)
      self.assertArray(b, [false, true, '2', 3, 5, NaN])


      b = newArray2()

      s = b.sort(Array.NUMERIC | Array.DESCENDING | Array.RETURNINDEXEDARRAY)
      self.assertArray(s, [5, 0, 1, 2, 4, 3])

      b.sort(16 | Array.DESCENDING)
      self.assertArray(b, [NaN, 5, 3, '2', true, false])

      check_holes(b, [NaN, 5, 3, '2', true, false])


      a = Array(7, 2, 1, '3', '4')

      a.sort(sub_comparison)
      self.assertArray(a, [7, '4', '3', 2, 1])

      a.sort(sub_comparison, 2)
      self.assertArray(a, [1, 2, '3', '4', 7])

      s = a.sort(sub_comparison, Array.RETURNINDEXEDARRAY)
      self.assertArray(s, [4, 3, 2, 1, 0])

      s = a.sort(sub_comparison, Array.DESCENDING | 8)
      self.assertArray(s, [0, 1, 2, 3, 4])

      s = a.sort(sub_comparison, Array.UNIQUESORT)
      self.assertNotEqual(s, 0)


      c = Array(3, 'abc')

      s = c.sort(sub_comparison, Array.UNIQUESORT)
      self.assertEqual(s, 0)

      d = Array(3, '4')

      s = d.sort(sub_comparison, 4)
      self.assertArray(s, ['4', 3])

   def test_sort_random(self):
      # A simple deterministic PRNG; namely, Xorshift.
      def _rng():
         rngState = as3lib.Int(0x12345678)
         while True:
            rngState ^= rngState << 13
            rngState ^= rngState >> 17
            rngState ^= rngState << 5
            yield rngState

      rng = _rng()

      array = Array(*[i for i in range(50)])

      # "sort" the array using randomly-chosen comparison results.
      def sortfunc(a, b):
         r = next(rng)
         if r % 8 == 0:
            return 0
         if r > 0:
            return 1
         return -1

      array.sort(sortfunc)
      self.assertArray(array, [13, 35, 24, 1, 8, 33, 6, 3, 9, 38, 20, 7, 23,
                               40, 19, 16, 12, 15, 14, 4, 22, 37, 21, 18, 45,
                               25, 41, 27, 36, 32, 47, 44, 43, 48, 29, 5, 26,
                               11, 10, 39, 17, 42, 49, 2, 31, 28, 0, 30, 34,
                               46])

   def test_sortOn(self):
      raise TestNotImplemented

   def test_sparse_ops(self):
      arr = Array(1, 2)
      arr[50] = 6
      arr[100] = 10
      arr[500] = 11

      self.assertEqual(arr[0], 1)
      self.assertEqual(arr[50], 6)
      self.assertEqual(arr[100], 10)
      self.assertEqual(arr[500], 11)
      self.assertEqual(arr[1000], undefined)
      self.assertEqual(arr.length, 501)

      # Delete
      delete(arr[50])
      self.assertEqual(arr.length, 501)
      self.assertEqual(arr[50], undefined)
      self.assertEqual(arr[100], 10)

      # Push
      arr.push(12)
      self.assertEqual(arr.length, 502)
      self.assertEqual(arr[501], 12)
      self.assertEqual(arr.pop(), 12)
      self.assertEqual(arr.length, 501)
      self.assertEqual(arr[500], 11)

      # NOTE: This will fail until array is rewritten
      # For
      self.assertIter(arr, [0, 1, 100, 500], 4)

      # For each
      self.assertEach(arr, [1, 2, 10, 11], 4)

      # Shift
      self.assertEqual(arr.shift(), 1)
      self.assertEqual(arr.length, 500)
      self.assertEqual(arr[0], 2)
      self.assertEqual(arr[99], 10)
      self.assertEqual(arr[499], 11)

      # Unshift
      arr.unshift(1)
      self.assertEqual(arr.length, 501)
      self.assertEqual(arr[0], 1)
      self.assertEqual(arr[100], 10)
      self.assertEqual(arr[500], 11)

      # RemoveAt
      self.assertEqual(arr.removeAt(150), undefined)
      self.assertEqual(arr.length, 500)
      self.assertEqual(arr[499], 11)
      self.assertEqual(arr[500], undefined)

   def test_splice(self):
      # TODO: Ensure that the length asserts are correct
      def constructArray():
         arr = Array(8)
         arr[2] = 2
         arr[4] = 4
         arr[6] = 6
         return arr

      Array.prototype[0] = 999
      Array.prototype[1] = 998
      Array.prototype[3] = 997
      Array.prototype[5] = 996
      Array.prototype[7] = 995

      a = constructArray()
      b = a.splice()

      self.assertArray(a, [999, 998, 2, 997, 4, 996, 6, 995], 8)
      # TODO: Make correct assert for b. I'm not sure what type it is
      # trace(b)
      # 2026-01-15T17:59:59.453530Z  INFO avm_trace: undefined

      a = constructArray()
      c = a.splice(0, 3, 'test1', 'test2')

      self.assertArray(a, ['test1', 'test2', 997, 4, 996, 6, 995], 7)
      self.assertArray(c, [999, 998, 2], 3)

      a = constructArray()
      d = a.splice(-1, 3, 'test3', 'test4')

      self.assertArray(a, [999, 998, 2, 997, 4, 996, 6, 'test3', 'test4'], 9)
      self.assertArray(d, [995], 1)

      a = constructArray()
      e = a.splice(-3, 3, 'test5', 'test6')

      self.assertArray(a, [999, 998, 2, 997, 4, 'test5', 'test6'], 7)
      self.assertArray(e, [996, 6, 995], 3)

      a = constructArray()
      e = a.splice(20, 0, 'test7')

      self.assertArray(a, [999, 998, 2, 997, 4, 996, 6, 995, 'test7'], 9)
      self.assertArray(e, [], 0)

      a = constructArray()
      f = a.splice(2)

      self.assertArray(a, [999, 998], 2)
      self.assertArray(f, [2, 997, 4, 996, 6, 995], 6)

      a = constructArray()

      Array.prototype[0] = 99
      Array.prototype[5] = 96
      Array.prototype[7] = 95

      self.assertArray(a, [99, 998, 2, 997, 4, 96, 6, 95], 8)
      self.assertArray(c, [999, 998, 2], 3)
      self.assertArray(d, [995], 1)
      self.assertArray(e, [], 0)
      self.assertArray(f, [2, 997, 4, 996, 6, 995], 6)

   def test_splice2(self):
      raise TestNotImplemented

   def _spliceTypes_arrToString(self, array):
      if array is null:
         return 'null'
      if not isinstance(array, Array):
         return String() + array
      if array.length > 1000:
         return '<len(%i)>' % array.length
      if array.length == 0:
         return '<empty>'
      return f'[{array.map(lambda el, *args: self._spliceTypes_arrToString(el))}]'

   def assertSpliceTypes(self, array, func, retcheck, acheck):
      a = array.concat()  # clone
      ret = func(a)
      self.assertEqual(self._spliceTypes_arrToString(ret), retcheck)
      self.assertEqual(self._spliceTypes_arrToString(a), acheck)

   def test_splice_types(self):
      array = Array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)

      self.assertSpliceTypes(array, lambda a: a.splice(), 'null', '[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]')
      self.assertSpliceTypes(array, lambda a: a.splice('0'), '[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]', '<empty>')
      self.assertSpliceTypes(array, lambda a: a.splice('5'), '[5,6,7,8,9,10,11,12,13,14,15]', '[0,1,2,3,4]')
      self.assertSpliceTypes(array, lambda a: a.splice(true), '[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]', '[0]')
      self.assertSpliceTypes(array, lambda a: a.splice(false), '[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]', '<empty>')
      self.assertSpliceTypes(array, lambda a: a.splice(Object()), '[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]', '<empty>')
      self.assertSpliceTypes(array, lambda a: a.splice(1, '2'), '[1,2]', '[0,3,4,5,6,7,8,9,10,11,12,13,14,15]')
      self.assertSpliceTypes(array, lambda a: a.splice(-1, 2), '[15]', '[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]')
      self.assertSpliceTypes(array, lambda a: a.splice('-5', 3), '[11,12,13]', '[0,1,2,3,4,5,6,7,8,9,10,14,15]')
      self.assertSpliceTypes(array, lambda a: a.splice(1, -2), '<empty>', '[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]')
      self.assertSpliceTypes(array, lambda a: a.splice(1, true), '[1]', '[0,2,3,4,5,6,7,8,9,10,11,12,13,14,15]')
      self.assertSpliceTypes(array, lambda a: a.splice(1, false), '<empty>', '[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]')
      self.assertSpliceTypes(array, lambda a: a.splice(1, 'true'), '<empty>', '[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]')
      self.assertSpliceTypes(array, lambda a: a.splice(1, 'false'), '<empty>', '[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]')
      self.assertSpliceTypes(array, lambda a: a.splice(1, Object()), '<empty>', '[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]')
      self.assertSpliceTypes(array, lambda a: a.splice(1, '5'), '[1,2,3,4,5]', '[0,6,7,8,9,10,11,12,13,14,15]')

   def test_storage(self):
      a = Array('a', 'b', 'c')

      self.assertEqual(a.length, 3)

      # Overwrite 0 through 3
      a[0] = 'd'
      a[1] = 'e'
      a[2] = 'f'
      a[3] = 'g'
      self.assertEqual(a.length, 4)
      self.assertEqual(a, ['d', 'e', 'f', 'g'])

   def test_toLocaleString(self):
      # TODO: The answer that ruffle gives looks wrong, check on actual flash player
      a = Array(String('a'), String('b'), String('c'))
      b = Array(Number(1), Number(2), Number(3))
      c = Array(a, b)

      self.assertEqual(a.toLocaleString(), '[object String],[object String],[object String]')
      self.assertEqual(b.toLocaleString(), '1,2,3')
      self.assertEqual(c.toLocaleString(), '[object String],[object String],[object String],1,2,3')

   def test_toString(self):
      a = Array('a', 'b', 'c')
      b = Array(1, 2, 3)
      c = Array(a, b)
      d = Array('str', 123, undefined, null, true, false)

      self.assertEqual(a.toString(), 'a,b,c')
      self.assertEqual(b.toString(), '1,2,3')
      self.assertEqual(c.toString(), 'a,b,c,1,2,3')
      self.assertEqual(d.toString(), 'str,123,,,true,false')

   def test_unshift(self):
      a = Array(5)
      a[2] = 'test'
      Array.prototype[3] = 'works'

      self.asserArray(a, [undefined, undefined, 'test', 'works', undefined])

      a.unshift("hi", "bye")
      self.asserArray(a, ['hi', 'bye', undefined, 'works', 'test', undefined, undefined])

      a.unshift()
      self.asserArray(a, ['hi', 'bye', undefined, 'works', 'test', undefined, undefined])

   def test_valueOf(self):
      # TODO: Make sure that valueOf is supposed to return the array
      a = Array('a', 'b', 'c')
      self.assertEqual(a.valueOf(), a)

      b = Array(1, 2, 3)
      self.assertEqual(b.valueOf(), b)

      c = Array(a, b)
      self.assertEqual(c.valueOf(), c)

   def test_null_callback(self):
      # TODO: Make sure this is correct
      a = Array()
      a.push(1)

      self.assertTrue(a.every(null))
      self.assertIs(a.filter(null), None)
      self.assertEqual(a.forEach(null), undefined)
      self.assertIs(a.map(null), None)
      self.assertFalse(a.some(null))


class BitwiseTests(as3libTestCase):
   def assertAnd(self, value, check):
      self.assertEqual(true & value, check[0])
      self.assertEqual(false & value, check[1])
      self.assertEqual(null & value, check[2])
      self.assertEqual(undefined & value, check[3])
      self.assertEqual(String('') & value, check[4])
      self.assertEqual(String('str') & value, check[5])
      self.assertEqual(String('true') & value, check[6])
      self.assertEqual(String('false') & value, check[7])
      self.assertEqual(Number(0.0) & value, check[8])
      self.assertEqual(NaN & value, check[9])
      self.assertEqual(Number(-0.0) & value, check[10])
      self.assertEqual(Infinity & value, check[11])
      self.assertEqual(Number(1.0) & value, check[12])
      self.assertEqual(Number(-1.0) & value, check[13])
      self.assertEqual(Number(0xFF1306) & value, check[14])
      self.assertEqual(Object() & value, check[15])
      self.assertEqual(String('0.0') & value, check[16])
      self.assertEqual(String('NaN') & value, check[17])
      self.assertEqual(String('-0.0') & value, check[18])
      self.assertEqual(String('Infinity') & value, check[19])
      self.assertEqual(String('1.0') & value, check[20])
      self.assertEqual(String('-1.0') & value, check[21])
      self.assertEqual(String('0xFF1306') & value, check[22])

   def test_and(self):
      asrt_1 = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0)

      asrt_0 = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0)

      asrt_n1 = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 16716550, 0, 0, 0,
                 0, 0, 1, -1, 16716550)

      asrt_16716550 = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16716550,
                       16716550, 0, 0, 0, 0, 0, 0, 16716550, 16716550)

      self.assertAnd(true, asrt_1)

      self.assertAnd(false, asrt_0)
      self.assertAnd(null, asrt_0)
      self.assertAnd(undefined, asrt_0)
      self.assertAnd(String(''), asrt_0)
      self.assertAnd(String('str'), asrt_0)
      self.assertAnd(String('true'), asrt_0)
      self.assertAnd(String('false'), asrt_0)
      self.assertAnd(Number(0.0), asrt_0)
      self.assertAnd(NaN, asrt_0)
      self.assertAnd(Number(-0.0), asrt_0)
      self.assertAnd(Infinity, asrt_0)

      self.assertAnd(Number(1.0), asrt_1)

      self.assertAnd(Number(-1.0), asrt_n1)

      self.assertAnd(Number(0xFF1306), asrt_16716550)

      self.assertAnd(Object(), asrt_0)
      self.assertAnd(String('0.0'), asrt_0)
      self.assertAnd(String('NaN'), asrt_0)
      self.assertAnd(String('-0.0'), asrt_0)
      self.assertAnd(String('Infinity'), asrt_0)

      self.assertAnd(String('1.0'), asrt_1)

      self.assertAnd(String('-1.0'), asrt_n1)

      self.assertAnd(String('0xFF1306'), asrt_16716550)

   def assertNot(self, value, check):
      self.assertEqual(~value, check)

   def test_not(self):
      self.assertNot(true, -2)

      self.assertNot(false, -1)
      self.assertNot(null, -1)
      self.assertNot(undefined, -1)
      self.assertNot(String(''), -1)
      self.assertNot(String('str'), -1)
      self.assertNot(String('true'), -1)
      self.assertNot(String('false'), -1)
      self.assertNot(Number(0.0), -1)
      self.assertNot(NaN, -1)
      self.assertNot(Number(-0.0), -1)
      self.assertNot(Infinity, -1)

      self.assertNot(Number(1.0), -2)

      self.assertNot(Number(-1.0), 0)

      self.assertNot(Number(0xFF1306), -16716551)

      self.assertNot(Object(), -1)
      self.assertNot(String('0.0'), -1)
      self.assertNot(String('NaN'), -1)
      self.assertNot(String('-0.0'), -1)
      self.assertNot(String('Infinity'), -1)

      self.assertNot(String('1.0'), -2)

      self.assertNot(String('-1.0'), 0)

      self.assertNot(String('0xFF1306'), -16716551)

   def assertOr(self, value, check):
      self.assertEqual(true | value, check[0])
      self.assertEqual(false | value, check[1])
      self.assertEqual(null | value, check[2])
      self.assertEqual(undefined | value, check[3])
      self.assertEqual(String('') | value, check[4])
      self.assertEqual(String('str') | value, check[5])
      self.assertEqual(String('true') | value, check[6])
      self.assertEqual(String('false') | value, check[7])
      self.assertEqual(Number(0.0) | value, check[8])
      self.assertEqual(NaN | value, check[9])
      self.assertEqual(Number(-0.0) | value, check[10])
      self.assertEqual(Infinity | value, check[11])
      self.assertEqual(Number(1.0) | value, check[12])
      self.assertEqual(Number(-1.0) | value, check[13])
      self.assertEqual(Number(0xFF1306) | value, check[14])
      self.assertEqual(Object() | value, check[15])
      self.assertEqual(String('0.0') | value, check[16])
      self.assertEqual(String('NaN') | value, check[17])
      self.assertEqual(String('-0.0') | value, check[18])
      self.assertEqual(String('Infinity') | value, check[19])
      self.assertEqual(String('1.0') | value, check[20])
      self.assertEqual(String('-1.0') | value, check[21])
      self.assertEqual(String('0xFF1306') | value, check[22])

   def test_or(self):
      asrt_1 = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 16716551, 1, 1, 1,
                1, 1, 1, -1, 16716551)

      asrt_0 = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 16716550, 0, 0, 0,
                0, 0, 1, -1, 16716550)

      asrt_n1 = (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                 -1, -1, -1, -1, -1, -1, -1, -1)

      asrt_16716550 = (16716551, 16716550, 16716550, 16716550, 16716550,
                       16716550, 16716550, 16716550, 16716550, 16716550,
                       16716550, 16716550, 16716551, -1, 16716550, 16716550,
                       16716550, 16716550, 16716550, 16716550, 16716551, -1,
                       16716550)

      self.assertOr(true, asrt_1)

      self.assertOr(false, asrt_0)
      self.assertOr(null, asrt_0)
      self.assertOr(undefined, asrt_0)
      self.assertOr(String(''), asrt_0)
      self.assertOr(String('str'), asrt_0)
      self.assertOr(String('true'), asrt_0)
      self.assertOr(String('false'), asrt_0)
      self.assertOr(Number(0.0), asrt_0)
      self.assertOr(NaN, asrt_0)
      self.assertOr(Number(-0.0), asrt_0)
      self.assertOr(Infinity, asrt_0)

      self.assertOr(Number(1.0), asrt_1)

      self.assertOr(Number(-1.0), asrt_n1)

      self.assertOr(Number(0xFF1306), asrt_16716550)

      self.assertOr(Object(), asrt_0)
      self.assertOr(String('0.0'), asrt_0)
      self.assertOr(String('NaN'), asrt_0)
      self.assertOr(String('-0.0'), asrt_0)
      self.assertOr(String('Infinity'), asrt_0)

      self.assertOr(String('1.0'), asrt_1)

      self.assertOr(String('-1.0'), asrt_n1)

      self.assertOr(String('0xFF1306'), asrt_16716550)

   def assertXor(self, value, check):
      self.assertEqual(true ^ value, check[0])
      self.assertEqual(false ^ value, check[1])
      self.assertEqual(null ^ value, check[2])
      self.assertEqual(undefined ^ value, check[3])
      self.assertEqual(String('') ^ value, check[4])
      self.assertEqual(String('str') ^ value, check[5])
      self.assertEqual(String('true') ^ value, check[6])
      self.assertEqual(String('false') ^ value, check[7])
      self.assertEqual(Number(0.0) ^ value, check[8])
      self.assertEqual(NaN ^ value, check[9])
      self.assertEqual(Number(-0.0) ^ value, check[10])
      self.assertEqual(Infinity ^ value, check[11])
      self.assertEqual(Number(1.0) ^ value, check[12])
      self.assertEqual(Number(-1.0) ^ value, check[13])
      self.assertEqual(Number(0xFF1306) ^ value, check[14])
      self.assertEqual(Object() ^ value, check[15])
      self.assertEqual(String('0.0') ^ value, check[16])
      self.assertEqual(String('NaN') ^ value, check[17])
      self.assertEqual(String('-0.0') ^ value, check[18])
      self.assertEqual(String('Infinity') ^ value, check[19])
      self.assertEqual(String('1.0') ^ value, check[20])
      self.assertEqual(String('-1.0') ^ value, check[21])
      self.assertEqual(String('0xFF1306') ^ value, check[22])

   def test_xor(self):
      asrt_1 = (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, -2, 16716551, 1, 1, 1,
                1, 1, 0, -2, 16716551)

      asrt_0 = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 16716550, 0, 0, 0,
                0, 0, 1, -1, 16716550)

      asrt_n1 = (-2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, 0,
                 -16716551, -1, -1, -1, -1, -1, -2, 0, -16716551)

      asrt_16716550 = (16716551, 16716550, 16716550, 16716550, 16716550,
                       16716550, 16716550, 16716550, 16716550, 16716550,
                       16716550, 16716550, 16716551, -16716551, 0, 16716550,
                       16716550, 16716550, 16716550, 16716550, 16716551,
                       -16716551, 0)

      self.assertXor(true, asrt_1)

      self.assertXor(false, asrt_0)
      self.assertXor(null, asrt_0)
      self.assertXor(undefined, asrt_0)
      self.assertXor(String(''), asrt_0)
      self.assertXor(String('str'), asrt_0)
      self.assertXor(String('true'), asrt_0)
      self.assertXor(String('false'), asrt_0)
      self.assertXor(Number(0.0), asrt_0)
      self.assertXor(NaN, asrt_0)
      self.assertXor(Number(-0.0), asrt_0)
      self.assertXor(Infinity, asrt_0)

      self.assertXor(Number(1.0), asrt_1)

      self.assertXor(Number(-1.0), asrt_n1)

      self.assertXor(Number(0xFF1306), asrt_16716550)

      self.assertXor(Object(), asrt_0)
      self.assertXor(String('0.0'), asrt_0)
      self.assertXor(String('NaN'), asrt_0)
      self.assertXor(String('-0.0'), asrt_0)
      self.assertXor(String('Infinity'), asrt_0)

      self.assertXor(String('1.0'), asrt_1)

      self.assertXor(String('-1.0'), asrt_n1)

      self.assertXor(String('0xFF1306'), asrt_16716550)


class BooleanTests(as3libTestCase):
   def test_constructor(self):
      self.assertFalse(Boolean())
      self.assertTrue(Boolean(true))
      self.assertTrue(Boolean(True))
      self.assertFalse(Boolean(false))
      self.assertFalse(Boolean(False))
      self.assertFalse(Boolean(null))
      self.assertFalse(Boolean(undefined))
      self.assertFalse(Boolean(String('')))
      self.assertFalse(Boolean(''))
      self.assertTrue(Boolean(String('str')))
      self.assertTrue(Boolean('str'))
      self.assertTrue(Boolean(String('true')))
      self.assertTrue(Boolean('true'))
      self.assertTrue(Boolean(String('false')))
      self.assertTrue(Boolean('false'))
      self.assertFalse(Boolean(Number(0.0)))
      self.assertFalse(Boolean(0.0))
      self.assertFalse(Boolean(NaN))
      self.assertFalse(Boolean(Number(-0.0)))
      self.assertFalse(Boolean(-0.0))
      self.assertTrue(Boolean(Infinity))
      self.assertTrue(Boolean(Number(1.0)))
      self.assertTrue(Boolean(1.0))
      self.assertTrue(Boolean(Number(-1.0)))
      self.assertTrue(Boolean(-1.0))
      self.assertTrue(Boolean(Object()))

   def test_negation(self):
      self.assertFalse(not true)
      self.assertTrue(not false)
      self.assertTrue(not null)
      self.assertTrue(not undefined)
      self.assertTrue(not String(''))
      self.assertFalse(not String('str'))
      self.assertFalse(not String('true'))
      self.assertFalse(not String('false'))
      self.assertTrue(not Number(0.0))
      self.assertTrue(not NaN)
      self.assertTrue(not Number(-0.0))
      self.assertFalse(not Infinity)
      self.assertFalse(not Number(1.0))
      self.assertFalse(not Number(-1.0))
      self.assertFalse(not Object())

   def test_toString(self):
      # TODO: Make sure assertIs is correct here
      self.assertEqual(true.toString(), 'true')
      self.assertIs(true.valueOf(), True)
      self.assertEqual(false.toString(), 'false')
      self.assertIs(false.valueOf(), False)


class DateTests(as3libTestCase):
   def assertDate(self, obj, year, month, date, day, hours, minutes, seconds, milliseconds=None):
      self.assertEqual(obj.fullYear, year)
      self.assertEqual(obj.month, month)
      self.assertEqual(obj.date, date)
      self.assertEqual(obj.day, day)
      self.assertEqual(obj.hours, hours)
      self.assertEqual(obj.minutes, minutes)
      self.assertEqual(obj.seconds, seconds)
      if milliseconds is not None:
         self.assertEqual(obj.milliseconds, milliseconds)

   def assertDateUTC(self, obj, year, month, date, day, hours, minutes, seconds, milliseconds=None):
      self.assertEqual(obj.fullYearUTC, year)
      self.assertEqual(obj.monthUTC, month)
      self.assertEqual(obj.dateUTC, date)
      self.assertEqual(obj.dayUTC, day)
      self.assertEqual(obj.hoursUTC, hours)
      self.assertEqual(obj.minutesUTC, minutes)
      self.assertEqual(obj.secondsUTC, seconds)
      if milliseconds is not None:
         self.assertEqual(obj.millisecondsUTC, milliseconds)

   def assertParsed(self, string, useUTC, *args):
      milliseconds = Date.parse(string)
      if as3lib.isNaN(milliseconds) or milliseconds is None:
         self.fail('Date.parse returned NaN')
      newdate = Date(milliseconds)
      if useUTC:
         self.assertDateUTC(newdate, *args)
      else:
         self.assertDate(newdate, *args)

   def assertNotParsed(self, string):
      milliseconds = Date.parse(string)
      if not as3lib.isNaN(milliseconds) and milliseconds is not None:
         self.fail('Date.parse returned valid date when it wasn\'t supposed to')

   def test_timestamp(self):
      date = Date(929156400000)

      self.assertDateUTC(date, 1999, 5, 12, 6, 3, 0, 0)

   def test_arguements(self):
      date = Date(2021, 7, 29, 4, 22, 55, 11)

      self.assertDate(date, 2021, 7, 29, 0, 4, 22, 55, 11)

   def test_invalid_string(self):
      date = Date('12')

      self.assertNaN(date.fullYear)
      self.assertNaN(date.month)
      self.assertNaN(date.date)
      self.assertNaN(date.day)
      self.assertNaN(date.hours)
      self.assertNaN(date.minutes)
      self.assertNaN(date.seconds)

   def test_object_aruement(self):
      o = Object()

      def valueOf():
         return 929156400000

      o.valueOf = valueOf
      date = Date(o)

      self.assertDateUTC(date, 1999, 5, 12, 6, 3, 0, 0)

   def test_invalid_object_aruement(self):
      # TODO: Make Date accept objects
      o = Object()

      def valueOf():
         return "Tue Feb 1 05:12:30 2005"

      o.valueOf = valueOf
      date = Date(o)

      self.assertNaN(date.fullYear)
      self.assertNaN(date.month)
      self.assertNaN(date.date)
      self.assertNaN(date.day)
      self.assertNaN(date.hours)
      self.assertNaN(date.minutes)
      self.assertNaN(date.seconds)

   def test_string_arguement(self):
      date = Date("Tue Feb 1 05:12:30 2005")

      self.assertDate(date, 2005, 1, 1, 2, 5, 12, 30)

   def test_setting_values(self):
      # TODO: test UTC properties
      date = Date(0)

      date.fullYear = 2000
      self.assertEqual(date.fullYear, 2000)

      date.month = 5
      self.assertEqual(date.month, 5)

      date.date = 9
      self.assertEqual(date.date, 9)

      date.hours = 10
      self.assertEqual(date.hours, 10)

      date.minutes = 12
      self.assertEqual(date.minutes, 12)

      date.seconds = 59
      self.assertEqual(date.seconds, 59)

      date.milliseconds = 24
      self.assertEqual(date.milliseconds, 24)

   def test_get_and_set_methods(self):
      # TODO: Test extra arguements
      # TODO: getDay, {set/get}Time, UTC
      date = Date(2021, 7, 29, 4, 22, 55, 11)

      date.setFullYear(2020)
      self.assertEqual(date.getFullYear(), 2020)

      date.setMonth(4)
      self.assertEqual(date.getMonth(), 4)

      date.setDate(22)
      self.assertEqual(date.getDate(), 22)

      date.setHours(12)
      self.assertEqual(date.getHours(), 12)

      date.setMinutes(42)
      self.assertEqual(date.getMinutes(), 42)

      date.setSeconds(33)
      self.assertEqual(date.getSeconds(), 33)

      date.milliseconds = 209
      self.assertEqual(date.milliseconds, 209)

      self.assertEqual(date.valueOf(), 1587559353209)

   def test_properties_with_NaN(self):
      date = Date(NaN)

      self.assertNaN(date.fullYear)
      self.assertNaN(date.month)
      self.assertNaN(date.date)
      self.assertNaN(date.day)
      self.assertNaN(date.hours)
      self.assertNaN(date.minutes)
      self.assertNaN(date.seconds)

      date.date = 9
      date.fullYear = 1999

      self.assertDate(date, 1999, 0, 1, 5, 0, 0, 0)

      date.time = NaN
      date.fullYearUTC = 2004

      self.assertDateUTC(date, 2004, 0, 1, 4, 0, 0, 0)

   def test_parser(self):
      self.assertParsed("Wed Apr 12 15:30:17 2006 GMT-0700", True, 2006, 3, 12, 3, 22, 30, 17, 0)
      self.assertParsed("Wed Apr 12 15:30:17 2006 GMT+0700", True, 2006, 3, 12, 3, 8, 30, 17, 0)
      self.assertParsed("Wed Apr 12 15:30:17 2006 GMT-0200", True, 2006, 3, 12, 3, 17, 30, 0)
      self.assertParsed("Sat Apr 30 1974", False, 1974, 3, 30, 2, 0, 0, 0, 0)
      self.assertParsed("1999 Mon Sun Sat Apr 30", False, 1999, 3, 30, 5, 0, 0, 0, 0)
      self.assertParsed("1999 Mon Sun Sat Apr 30 15:30:17", False, 1999, 3, 30, 5, 15, 30, 17, 0)
      self.assertParsed("Apr/03/1988 15:30:17", False, 1988, 3, 3, 0, 15, 30, 17, 0)
      self.assertParsed("15:30:17    Apr/03/1988   ", False, 1988, 3, 3, 0, 15, 30, 17, 0)
      self.assertParsed("Sat Apr 30 77", False, 1977, 3, 30, 6, 0, 0, 0, 0)

      self.assertNotParsed("Wed Apr 12 15:30:17 GMT-0700")
      self.assertNotParsed("Wed 12 15:30:17 GMT-0700 2006")
      self.assertNotParsed("Sat Jan 30")
      self.assertNotParsed("Sat Jan 70 77")
      self.assertNotParsed("Sat Jan 30 random 77")
      self.assertNotParsed("Sat Jan Oct 30 77")
      self.assertNotParsed("Sat Jan 30 77 Apr/03/1988")
      self.assertNotParsed("Sat Jan 30 77 GMT-0700 GMT-0800")


class ErrorTests(as3libTestCase):
   def assertError(self, cls, name):
      # TODO: Implement these
      # self.assertEqual(cls, f'[class {name}]')
      # self.assertEqual(cls.prototype.name, name)
      err = cls('My Error', 42)
      self.assertEqual(err.name, name)
      self.assertEqual(err.errorID, 42)
      self.assertEqual(err.toString(), '%s: My Error' % name)

   def test_getErrorMessage(self):
      # TODO: Verify these on flash player. Ruffle seems to have a stub
      self.assertEqual(Error.getErrorMessage(-1), 'Error #-1')
      self.assertEqual(Error.getErrorMessage(0), 'Error #0')
      self.assertEqual(Error.getErrorMessage(1), 'Error #1')
      self.assertEqual(Error.getErrorMessage(42), 'Error #42')
      self.assertEqual(Error.getErrorMessage(100), 'Error #100')
      # RUFFLE: TODO: Error #1000: The system is out of memory.
      # self.assertEqual(Error.getErrorMessage(1000), 'Error #1000')
      # RUFFLE: TODO: Error #1042: Not an ABC file.  major_version=%1 minor_version=%2.
      # self.assertEqual(Error.getErrorMessage(1042), 'Error #1042')
      self.assertEqual(Error.getErrorMessage(10000), 'Error #10000')

   def test_getStackTrace(self):
      raise TestNotImplemented

   def test_toString(self):
      self.assertError(Error, 'Error')
      self.assertError(RangeError, 'RangeError')
      self.assertError(IllegalOperationError, 'IllegalOperationError')
      self.assertError(ArgumentError, 'ArgumentError')
      self.assertError(ReferenceError, 'ReferenceError')
      self.assertError(DefinitionError, 'DefinitionError')
      self.assertError(EOFError, 'EOFError')
      self.assertError(EvalError, 'EvalError')
      self.assertError(IOError, 'IOError')
      self.assertError(InvalidSWFError, 'InvalidSWFError')
      self.assertError(MemoryError, 'MemoryError')
      self.assertError(ScriptTimeoutError, 'ScriptTimeoutError')
      self.assertError(StackOverflowError, 'StackOverflowError')
      self.assertError(URIError, 'URIError')
      self.assertError(VerifyError, 'VerifyError')


class FunctionTests(as3libTestCase):
   def assertEscape(self, fn, check):
      self.assertEqual(fn(), check[0])
      self.assertEqual(fn(undefined), check[1])
      self.assertEqual(type(fn(undefined)), check[2])
      self.assertEqual(fn(null), check[3])

      input = 'test'
      self.assertEqual(fn(input), check[4])

      input = "!\"£$%^&*()1234567890qwertyuiop[]asdfghjkl;'#\\zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:@~|ZXCVBNM<>?\u0010"
      self.assertEqual(fn(input), check[5])

      input = '\x05'
      self.assertEqual(fn(input), check[6])

      input =  '😭'
      self.assertEqual(fn(input), check[7])

   def test_encodeURI(self):
      asrt = ('undefined', 'null', 'string', 'null', 'test',
              "!%22%C2%A3$%25%5E&*()1234567890qwertyuiop%5B%5Dasdfghjkl;'#zxcvbnm,./QWERTYUIOP%7B%7DASDFGHJKL:@~%7CZXCVBNM%3C%3E?%10",
              '%05', '%F0%9F%98%AD')
      self.assertEscape(encodeURI, asrt)

   def test_encodeURIComponent(self):
      asrt = ('undefined', 'null', 'string', 'null', 'test',
              "!%22%C2%A3%24%25%5E%26*()1234567890qwertyuiop%5B%5Dasdfghjkl%3B'%23zxcvbnm%2C.%2FQWERTYUIOP%7B%7DASDFGHJKL%3A%40~%7CZXCVBNM%3C%3E%3F%10",
              '%05', '%F0%9F%98%AD')
      self.assertEscape(encodeURIComponent, asrt)

   def test_escape(self):
      asrt = ('undefined', 'null', 'string', 'null', 'test',
              '!%21%22%A3%24%25%5E%26*%28%291234567890qwertyuiop%5B%5Dasdfghjkl%3B%27%23zxcvbnm%2C./QWERTYUIOP%7B%7DASDFGHJKL%3A@%7E%7CZXCVBNM%3C%3E%3F%10',
              '%05', '%uD83D%uDE2D')
      self.assertEscape(escape, asrt)

   def test_isfinite(self):
      self.assertTrue(as3lib.isFinite(true))
      self.assertTrue(as3lib.isFinite(false))
      self.assertTrue(as3lib.isFinite(Number(10.0)))
      self.assertTrue(as3lib.isFinite(10.0))
      self.assertTrue(as3lib.isFinite(Number(-10.0)))
      self.assertTrue(as3lib.isFinite(-10.0))
      self.assertTrue(as3lib.isFinite(Number(0.0)))
      self.assertTrue(as3lib.isFinite(0.0))
      self.assertFalse(as3lib.isFinite(NaN))
      self.assertFalse(as3lib.isFinite(Infinity))
      self.assertFalse(as3lib.isFinite(-Infinity))
      self.assertTrue(as3lib.isFinite(String('')))
      self.assertTrue(as3lib.isFinite(''))
      self.assertFalse(as3lib.isFinite(String('hello')))
      self.assertFalse(as3lib.isFinite('hello'))
      self.assertTrue(as3lib.isFinite(String(' ')))
      self.assertTrue(as3lib.isFinite(' '))
      self.assertTrue(as3lib.isFinite(String('  5  ')))
      self.assertTrue(as3lib.isFinite('  5  '))
      self.assertTrue(as3lib.isFinite(String('0')))
      self.assertTrue(as3lib.isFinite('0'))
      self.assertFalse(as3lib.isFinite(String('NaN')))
      self.assertFalse(as3lib.isFinite('NaN'))
      self.assertFalse(as3lib.isFinite(String('Infinity')))
      self.assertFalse(as3lib.isFinite('Infinity'))
      self.assertFalse(as3lib.isFinite(String('-Infinity')))
      self.assertFalse(as3lib.isFinite('-Infinity'))
      self.assertFalse(as3lib.isFinite(String('100a')))
      self.assertFalse(as3lib.isFinite('100a'))
      self.assertTrue(as3lib.isFinite(String('0x10')))
      self.assertTrue(as3lib.isFinite('0x10'))
      self.assertFalse(as3lib.isFinite(String('0xhello')))
      self.assertFalse(as3lib.isFinite('0xhello'))
      self.assertTrue(as3lib.isFinite(String('0x1999999981ffffff')))
      self.assertTrue(as3lib.isFinite('0x1999999981ffffff'))
      self.assertFalse(as3lib.isFinite(String('0xUIXUIDFKHJDF012345678')))
      self.assertFalse(as3lib.isFinite('0xUIXUIDFKHJDF012345678'))
      self.assertTrue(as3lib.isFinite(String('123e-1')))
      self.assertTrue(as3lib.isFinite('123e-1'))
      self.assertFalse(as3lib.isFinite())

   def test_isNaN(self):
      self.assertFalse(as3lib.isNaN(true))
      self.assertFalse(as3lib.isNaN(false))
      self.assertFalse(as3lib.isNaN(Number(10.0)))
      self.assertFalse(as3lib.isNaN(Number(-10.0)))
      self.assertFalse(as3lib.isNaN(Number(0.0)))
      self.assertTrue(as3lib.isNaN(NaN))
      self.assertFalse(as3lib.isNaN(Infinity))
      self.assertFalse(as3lib.isNaN(-Infinity))
      self.assertFalse(as3lib.isNaN(''))
      self.assertTrue(as3lib.isNaN('hello'))
      self.assertFalse(as3lib.isNaN(' '))
      self.assertFalse(as3lib.isNaN('  5  '))
      self.assertFalse(as3lib.isNaN('0'))
      self.assertTrue(as3lib.isNaN("NaN"))
      self.assertFalse(as3lib.isNaN('Infinity'))
      self.assertFalse(as3lib.isNaN('-Infinity'))
      self.assertTrue(as3lib.isNaN('100a'))
      self.assertFalse(as3lib.isNaN('0x10'))
      self.assertTrue(as3lib.isNaN('0xhello'))
      self.assertFalse(as3lib.isNaN('0x1999999981ffffff'))
      self.assertTrue(as3lib.isNaN('0xUIXUIDFKHJDF012345678'))
      self.assertFalse(as3lib.isNaN('123e-1'))
      self.assertTrue(as3lib.isNaN())

   def test_parseFloat(self):
      self.assertNaN(as3lib.parseFloat())

      # integer
      self.assertEqual(as3lib.parseFloat('12345'), Number(12345))

      # decimal point
      self.assertEqual(as3lib.parseFloat('012345.67890'), Number(012345.6789))

      # ignore leading/trailing whitespace
      self.assertEqual(as3lib.parseFloat(" \t\r\n99999.99999\t\r\n      "), Number(99999.99999))

      # long numbers (more than 15 digits)
      self.assertEqual(as3lib.parseFloat('-22222222222222222'), Number(-22222222222222224))
      self.assertEqual(as3lib.parseFloat('-22222222.222222222'), Number(-22222222.222222224))

      # subnormal number
      self.assertEqual(as3lib.parseFloat('.0000000000000000000000005').toString(), '4.999999999999999e-25')

      # ignore trailing garbage
      self.assertEqual(as3lib.parseFloat("0000.12345GIBBERISH"), Number(0.12345))

      # exponent
      self.assertEqual(as3lib.parseFloat("9e99999"), Infinity)
      self.assertEqual(as3lib.parseFloat("+100e-100").toString(), '0.999999999999999e-98')
      self.assertEqual(as3lib.parseFloat("-123.234E+66").toString(), '-1.23234e+68')
      self.assertEqual(as3lib.parseFloat(".2E20E1"), Number(20000000000000000000))
      self.assertEqual(as3lib.parseFloat("-034.1+e20"), Number(-34.1))
      self.assertEqual(as3lib.parseFloat("10e"), Number(10))
      self.assertNaN(as3lib.parseFloat("e10"))
      self.assertNaN(as3lib.parseFloat("10e-"))

      # exponent overflow
      self.assertEqual(as3lib.parseFloat("1e4294967297"), Number(10))
      self.assertEqual(as3lib.parseFloat("1e2147483648"), Number(0))
      self.assertEqual(as3lib.parseFloat("1e-2147483648"), Number(0))

      # multiple dots
      self.assertEqual(as3lib.parseFloat("1.2345.678"), Number(1.2345))
      self.assertEqual(as3lib.parseFloat("1.2345.6e50"), Number(1.2345))

      # infinity
      self.assertEqual(as3lib.parseFloat('Infinity'), Infinity)
      self.assertEqual(as3lib.parseFloat('-Infinity'), -Infinity)
      self.assertEqual(as3lib.parseFloat('+Infinity'), Infinity)
      self.assertNaN(as3lib.parseFloat('Infinitya'))
      self.assertEqual(as3lib.parseFloat('Infinity   a'), Infinity)
      self.assertEqual(as3lib.parseFloat(".   Infinity"), Infinity)
      self.assertEqual(as3lib.parseFloat("e10   Infinity"), Infinity)
      self.assertEqual(as3lib.parseFloat(".e10   Infinity"), Infinity)
      self.assertEqual(as3lib.parseFloat("1   Infinity"), Number(1))

      # invalid strings
      self.assertNaN(as3lib.parseFloat("BADBAD"))
      self.assertNaN(as3lib.parseFloat(''))
      self.assertNaN(as3lib.parseFloat('-'))
      self.assertEqual(as3lib.parseFloat('0xff'), Number(0))
      self.assertNaN(as3lib.parseFloat(String.fromCharCode(305)))

      # non-string inputs
      #  Booleans
      self.assertNaN(as3lib.parseFloat(true))
      #  Numbers
      self.assertEqual(as3lib.parseFloat(1.2), Number(1.2))
      #  Infinity objects
      self.assertEqual(as3lib.parseFloat(Infinity), Infinity)
      #  Function that returns a string
      self.assertEqual(as3lib.parseFloat(lambda: '5'), Number(5))
      #  Class with toString method

      class C:
         def toString():
            return '6'

      self.assertEqual(as3lib.parseFloat(C()), Number(6))

   def test_parseInt(self):
      self.assertNaN(as3lib.parseInt())
      self.assertNaN(as3lib.parseInt(undefined))
      self.assertEqual(as3lib.parseInt(undefined, 32), as3lib.Int(785077))
      self.assertEqual(as3lib.parseInt('undefined', 32), 33790067563981)
      self.assertNaN(as3lib.parseInt(''))
      self.assertEqual(as3lib.parseInt('123'), as3lib.Int(123))
      self.assertEqual(as3lib.parseInt('100', 10), as3lib.Int(100))
      self.assertEqual(as3lib.parseInt('100', 0), as3lib.Int(100))
      self.assertNaN(as3lib.parseInt('100', 1))
      self.assertEqual(as3lib.parseInt('100', 2), as3lib.Int(4))
      self.assertEqual(as3lib.parseInt('100', 36), as3lib.Int(1296))
      self.assertNaN(as3lib.parseInt('100', 37))
      self.assertNaN(as3lib.parseInt('100', -1))
      self.assertEqual(as3lib.parseInt('100', Object()), as3lib.Int(100))
      self.assertNaN(as3lib.parseInt('100', true))
      self.assertEqual(as3lib.parseInt('100', false), as3lib.Int(100))
      self.assertEqual(as3lib.parseInt('100', NaN), as3lib.Int(100))
      self.assertEqual(as3lib.parseInt('100', undefined), as3lib.Int(100))
      self.assertEqual(as3lib.parseInt('0x123'), as3lib.Int(291))
      self.assertEqual(as3lib.parseInt('0xabc'), as3lib.Int(2748))
      self.assertEqual(as3lib.parseInt('010'), as3lib.Int(2))
      self.assertEqual(as3lib.parseInt('-0100'), as3lib.Int(-100))
      self.assertEqual(as3lib.parseInt('-0100z'), as3lib.Int(-100))
      self.assertNaN(as3lib.parseInt('0x+0X100'))
      n = 123
      self.assertEqual(as3lib.parseInt(n), as3lib.Int(123))
      self.assertEqual(as3lib.parseInt(123, 32), as3lib.Int(1091))
      self.assertNaN(as3lib.parseInt('++1'))
      self.assertEqual(as3lib.parseInt('0x100', 36), as3lib.Int(1540944))
      self.assertEqual(as3lib.parseInt(' 0x100', 36), as3lib.Int(1540944))
      self.assertEqual(as3lib.parseInt('0y100', 36), as3lib.Int(1597600))
      self.assertEqual(as3lib.parseInt(' 0y100', 36), as3lib.Int(1597600))
      self.assertEqual(as3lib.parseInt('-0x100', 36), as3lib.Int(-1540944))
      self.assertEqual(as3lib.parseInt(' -0x100', 36), as3lib.Int(-1540944))
      self.assertEqual(as3lib.parseInt('-0y100', 36), as3lib.Int(-1597600))
      self.assertEqual(as3lib.parseInt(' -0y100', 36), as3lib.Int(-1597600))
      self.assertEqual(as3lib.parseInt('-0x100'), as3lib.Int(-256))
      self.assertNaN(as3lib.parseInt('0x-100'))
      self.assertNaN(as3lib.parseInt(' 0x-100'))
      self.assertNaN(as3lib.parseInt('0x -100'))
      self.assertEqual(as3lib.parseInt('-0100'), as3lib.Int(-100))
      self.assertEqual(as3lib.parseInt('0-100'), as3lib.Int(0))
      self.assertEqual(as3lib.parseInt('+0x123', 33), as3lib.Int(0))
      self.assertEqual(as3lib.parseInt('+0x123', 34), as3lib.Int(1298259))
      self.assertEqual(as3lib.parseInt('0'), as3lib.Int(0))
      self.assertEqual(as3lib.parseInt(' 0'), as3lib.Int(0))
      self.assertEqual(as3lib.parseInt(' 0 '), as3lib.Int(0))
      self.assertEqual(as3lib.parseInt('077'), as3lib.Int(77))
      self.assertEqual(as3lib.parseInt('  077'), as3lib.Int(77))
      self.assertEqual(as3lib.parseInt('  077  '), as3lib.Int(77))
      self.assertEqual(as3lib.parseInt('  -077'), as3lib.Int(-77))
      self.assertEqual(as3lib.parseInt('077 '), as3lib.Int(77))
      self.assertEqual(as3lib.parseInt('11', 2), as3lib.Int(3))
      self.assertEqual(as3lib.parseInt('11', 3), as3lib.Int(4))
      self.assertEqual(as3lib.parseInt('11', 3.8), as3lib.Int(4))
      self.assertEqual(as3lib.parseInt('0x12'), as3lib.Int(18))
      self.assertEqual(as3lib.parseInt('0x12', 16), as3lib.Int(18))
      self.assertEqual(as3lib.parseInt('0x12', 16.1), as3lib.Int(18))
      self.assertEqual(as3lib.parseInt('0x12', NaN), as3lib.Int(18))
      self.assertNaN(as3lib.parseInt('0x  '))
      self.assertNaN(as3lib.parseInt('0x'))
      self.assertNaN(as3lib.parseInt('0x  ', 16))
      self.assertNaN(as3lib.parseInt('0x', 16))
      self.assertEqual(as3lib.parseInt('12aaa'), as3lib.Int(12))
      self.assertEqual(as3lib.parseInt("100000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "000000000000000"), Infinity)
      self.assertEqual(as3lib.parseInt("0x1000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "000000000000000"), Infinity)
      self.assertNaN(as3lib.parseInt(String.fromCharCode(305)))
      self.assertEqual(as3lib.parseInt(String.fromCharCode(0x2000) + "123"), as3lib.Int(123))

      #self.assertEqual(as3lib.parseInt('1.2315e2'), as3lib.Int(123))

   def test_trace(self):
      raise TestNotImplemented

   def assertUnescape(self, str, check):
      self.assertEqual(unescape(str), check)

   def test_unescape(self):
      # Valid sequences
      self.assertUnescape('%32%33', '23')
      self.assertUnescape('aa %32%33', 'aa 23')
      self.assertUnescape('%32 aa %33', '2 aa 3')
      self.assertUnescape('%32%33 aa', '23 aa')
      self.assertUnescape(escape('😊'), '😊')
      self.assertUnescape(escape('&& 😊 😊 😊 😊 😊bb'), '&& 😊 😊 😊 😊 😊bb')

      # Invalid sequences
      self.assertUnescape('%32%3', '2%3')
      self.assertUnescape('%%3', '%%3')
      self.assertUnescape('%G3 %25', '%G3 %')
      self.assertUnescape('%u', '%u')
      self.assertUnescape('%u33', '%u33')
      self.assertUnescape('%U3333', '%U3333')
      self.assertUnescape('%u333G', '%u333G')


class GlobalsTests(as3libTestCase):
   def test_falsiness(self):
      self.assertFalse(not true)
      self.assertTrue(not false)
      self.assertTrue(not null)
      self.assertTrue(not undefined)
      self.assertTrue(not String(''))
      self.assertFalse(not String('str'))
      self.assertFalse(not String('true'))
      self.assertFalse(not String('false'))
      self.assertTrue(not Number(0.0))
      self.assertTrue(not NaN)
      self.assertTrue(not Number(-0.0))
      self.assertFalse(not Infinity)
      self.assertFalse(not Number(1.0))
      self.assertFalse(not Number(-1.0))
      self.assertFalse(not Object())

   def test_undefined(self):
      # From https://github.com/ruffle-rs/ruffle/tree/master/tests/tests/swfs/from_shumway/avm1/undefined/undefined-swf7
      self.assertEqual(undefined.toString(), 'undefined')
      self.assertNaN(-undefined)  # TODO: Validate this one
      self.assertTrue(not undefined)
      self.assertEqual(String('s') + undefined, 'sundefined')
      self.assertEqual(undefined + String('s'), 'undefineds')
      self.assertNaN(Number(0) + undefined)
      self.assertNaN(undefined + Number(0))
      self.assertNotEqual(String('undefined'), undefined)
      self.assertNotEqual(undefined, String('undefined'))
      self.assertFalse(Number(0) == undefined)
      self.assertFalse(undefined == Number(0))
      self.assertFalse(Number(1) == undefined)
      self.assertFalse(undefined == Number(1))
      # trace("\'undefined\' < undefined => " + ("undefined" < undefined));
      # trace("undefined < \'undefined\' => " + (undefined < "undefined"));
      # 'undefined' < undefined => undefined
      # undefined < 'undefined' => undefined
      self.assertEqual(Number(0) < undefined, undefined)
      self.assertEqual(undefined < Number(0), undefined)
      self.assertEqual(Number(1) < undefined, undefined)
      self.assertEqual(undefined < Number(1), undefined)
      # trace("\'undefined\' <= undefined => " + ("undefined" <= undefined));
      # trace("undefined <= \'undefined\' => " + (undefined <= "undefined"));
      # 'undefined' <= undefined => true
      # undefined <= 'undefined' => true
      self.assertTrue(Number(0) <= undefined)
      self.assertTrue(undefined <= Number(0))
      self.assertTrue(Number(1) <= undefined)
      self.assertTrue(undefined <= Number(1))
      # trace("\'undefined\' > undefined => " + ("undefined" > undefined));
      # trace("undefined > \'undefined\' => " + (undefined > "undefined"));
      # 'undefined' > undefined => undefined
      # undefined > 'undefined' => undefined
      self.assertEqual(Number(0) > undefined, undefined)
      self.assertEqual(undefined > Number(0), undefined)
      self.assertEqual(Number(1) > undefined, undefined)
      self.assertEqual(undefined > Number(1), undefined)
      # trace("\'undefined\' >= undefined => " + ("undefined" >= undefined));
      # trace("undefined >= \'undefined\' => " + (undefined >= "undefined"));
      # 'undefined' >= undefined => true
      # undefined >= 'undefined' => true
      self.assertTrue(Number(0) >= undefined)
      self.assertTrue(undefined >= Number(0))
      self.assertTrue(Number(1) >= undefined)
      self.assertTrue(undefined >= Number(1))

   def test_null(self):
      raise TestNotImplemented

   def assertLength(self, obj, len):
      self.assertEqual(obj.length, len)

   def test_static_length(self):
      # TODO: Function
      self.assertLength(Object, 1)
      self.assertLength(RegExp, 1)
      self.assertLength(String, 1)
      self.assertLength(XMLList, 1)
      self.assertLength(Namespace, 2)
      self.assertLength(ReferenceError, 1)
      self.assertLength(DefinitionError, 1)
      self.assertLength(ArgumentError, 1)
      self.assertLength(SyntaxError, 1)
      self.assertLength(VerifyError, 1)
      self.assertLength(SecurityError, 1)
      self.assertLength(EvalError, 1)
      self.assertLength(Number, 1)
      self.assertLength(RangeError, 1)
      self.assertLength(Boolean, 1)
      self.assertLength(XML, 1)
      # self.assertLength(Function, 1)
      self.assertLength(TypeError, 1)
      self.assertLength(URIError, 1)
      self.assertLength(Array, 1)
      self.assertLength(uint, 1)
      self.assertLength(Date, 7)
      self.assertLength(Error, 1)
      self.assertLength(UninitializedError, 1)


class NumberTestsBase(as3libTestCase):
   def _assertToExponential(self, val, check):
      # null/0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20
      self.assertEqual(val.toExponential(), check[0])
      self.assertEqual(val.toExponential(0), check[0])
      self.assertEqual(val.toExponential(1), check[1])
      self.assertEqual(val.toExponential(2), check[2])
      self.assertEqual(val.toExponential(3), check[3])
      self.assertEqual(val.toExponential(4), check[4])
      self.assertEqual(val.toExponential(5), check[5])
      self.assertEqual(val.toExponential(6), check[6])
      self.assertEqual(val.toExponential(7), check[7])
      self.assertEqual(val.toExponential(8), check[8])
      self.assertEqual(val.toExponential(9), check[9])
      self.assertEqual(val.toExponential(10), check[10])
      self.assertEqual(val.toExponential(20), check[11])

   def _assertToFixed(self, val, check):
      # null, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20
      self.assertEqual(val.toFixed(), check[0])
      self.assertEqual(val.toFixed(0), check[0])
      self.assertEqual(val.toFixed(1), check[1])
      self.assertEqual(val.toFixed(2), check[2])
      self.assertEqual(val.toFixed(3), check[3])
      self.assertEqual(val.toFixed(4), check[4])
      self.assertEqual(val.toFixed(5), check[5])
      self.assertEqual(val.toFixed(6), check[6])
      self.assertEqual(val.toFixed(7), check[7])
      self.assertEqual(val.toFixed(8), check[8])
      self.assertEqual(val.toFixed(9), check[9])
      self.assertEqual(val.toFixed(10), check[10])
      self.assertEqual(val.toFixed(20), check[11])

   def _assertToPrecision(self, val, check):
      self.assertEqual(val.toPrecision(1), check[0])
      self.assertEqual(val.toPrecision(2), check[1])
      self.assertEqual(val.toPrecision(3), check[2])
      self.assertEqual(val.toPrecision(4), check[3])
      self.assertEqual(val.toPrecision(5), check[4])
      self.assertEqual(val.toPrecision(6), check[5])
      self.assertEqual(val.toPrecision(7), check[6])
      self.assertEqual(val.toPrecision(8), check[7])
      self.assertEqual(val.toPrecision(9), check[8])
      self.assertEqual(val.toPrecision(10), check[9])
      self.assertEqual(val.toPrecision(20), check[10])
      self.assertEqual(val.toPrecision(21), check[11])

   def _assertToString(self, val, check):
      # 2, 3, 4, 5, 6, 7, 8, 9, null/10, ..., valueOf
      self.assertEqual(val.toString(), check[8])
      for i in range(35):
         self.assertEqual(val.toString(i + 2), check[i])
      self.assertEqual(val.valueOf(), check[35])


class intTests(NumberTestsBase):
   def test_constructor(self):
      self.assertEqual(as3lib.Int(), 0)
      self.assertEqual(as3lib.Int(true), 1)
      self.assertEqual(as3lib.Int(True), 1)
      self.assertEqual(as3lib.Int(false), 0)
      self.assertEqual(as3lib.Int(False), 0)
      self.assertEqual(as3lib.Int(null), 0)
      self.assertEqual(as3lib.Int(undefined), 0)

      self.assertEqual(as3lib.Int(String('')), 0)
      self.assertEqual(as3lib.Int(''), 0)
      self.assertEqual(as3lib.Int(String('str')), 0)
      self.assertEqual(as3lib.Int('str'), 0)
      self.assertEqual(as3lib.Int(String('true')), 0)
      self.assertEqual(as3lib.Int('true'), 0)
      self.assertEqual(as3lib.Int(String('false')), 0)
      self.assertEqual(as3lib.Int('false'), 0)

      self.assertEqual(as3lib.Int(Number(0.0)), 0)
      self.assertEqual(as3lib.Int(0.0), 0)
      self.assertEqual(as3lib.Int(NaN), 0)
      self.assertEqual(as3lib.Int(Number(-0.0)), 0)
      self.assertEqual(as3lib.Int(-0.0), 0)
      self.assertEqual(as3lib.Int(Infinity), 0)
      self.assertEqual(as3lib.Int(Number(1.0)), 1)
      self.assertEqual(as3lib.Int(1.0), 1)
      self.assertEqual(as3lib.Int(Number(-1.0)), -1)
      self.assertEqual(as3lib.Int(-1.0), -1)

      self.assertEqual(as3lib.Int(0xFF1306), 16716550)
      self.assertEqual(as3lib.Int(1.2315e2), 123)
      self.assertEqual(as3lib.Int(0x7FFFFFFF), 2147483647)
      self.assertEqual(as3lib.Int(0x80000000), -2147483648)
      self.assertEqual(as3lib.Int(0x80000001), -2147483647)
      self.assertEqual(as3lib.Int(0x180000001), -2147483647)
      self.assertEqual(as3lib.Int(0x100000001), 1)
      self.assertEqual(as3lib.Int(-0x7FFFFFFF), -2147483647)
      self.assertEqual(as3lib.Int(-0x80000000), -2147483648)
      self.assertEqual(as3lib.Int(-0x80000001), 2147483647)
      self.assertEqual(as3lib.Int(-0x180000001), 2147483647)
      self.assertEqual(as3lib.Int(-0x100000001), -1)

      # Parse Tests
      self.assertEqual(as3lib.Int(String('0.0')), 0)
      self.assertEqual(as3lib.Int('0.0'), 0)
      self.assertEqual(as3lib.Int(String('NaN')), 0)
      self.assertEqual(as3lib.Int('NaN'), 0)
      self.assertEqual(as3lib.Int(String('-0.0')), 0)
      self.assertEqual(as3lib.Int('-0.0'), 0)
      self.assertEqual(as3lib.Int(String('Infinity')), 0)
      self.assertEqual(as3lib.Int('Infinity'), 0)
      self.assertEqual(as3lib.Int(String('1.0')), 1)
      self.assertEqual(as3lib.Int('1.0'), 1)
      self.assertEqual(as3lib.Int(String('-1.0')), -1)
      self.assertEqual(as3lib.Int('-1.0'), -1)
      self.assertEqual(as3lib.Int(String('0xFF1306')), 16716550)
      self.assertEqual(as3lib.Int('0xFF1306'), 16716550)
      self.assertEqual(as3lib.Int(String('1.2315e2')), 123)
      self.assertEqual(as3lib.Int('1.2315e2'), 123)
      self.assertEqual(as3lib.Int(String('0x7FFFFFFF')), 2147483647)
      self.assertEqual(as3lib.Int('0x7FFFFFFF'), 2147483647)
      self.assertEqual(as3lib.Int(String('0x80000000')), -2147483648)
      self.assertEqual(as3lib.Int('0x80000000'), -2147483648)
      self.assertEqual(as3lib.Int(String('0x80000001')), -2147483647)
      self.assertEqual(as3lib.Int('0x80000001'), -2147483647)
      self.assertEqual(as3lib.Int(String('0x180000001')), -2147483647)
      self.assertEqual(as3lib.Int('0x180000001'), -2147483647)
      self.assertEqual(as3lib.Int(String('0x100000001')), 1)
      self.assertEqual(as3lib.Int('0x100000001'), 1)
      self.assertEqual(as3lib.Int(String('-0x7FFFFFFF')), -2147483647)
      self.assertEqual(as3lib.Int('-0x7FFFFFFF'), -2147483647)
      self.assertEqual(as3lib.Int(String('-0x80000000')), -2147483648)
      self.assertEqual(as3lib.Int('-0x80000000'), -2147483648)
      self.assertEqual(as3lib.Int(String('-0x80000001')), 2147483647)
      self.assertEqual(as3lib.Int('-0x80000001'), 2147483647)
      self.assertEqual(as3lib.Int(String('-0x180000001')), 2147483647)
      self.assertEqual(as3lib.Int('-0x180000001'), 2147483647)
      self.assertEqual(as3lib.Int(String('-0x100000001')), -1)
      self.assertEqual(as3lib.Int('-0x100000001'), -1)

      self.assertEqual(as3lib.Int(Object()), 0)

   def test_edge_cases(self):
      raise TestNotImplemented
      # uint doesn't exist
      # self.assertEqual(getQualifiedClassName(uint(1)), 'int')
      # trace((1 as uint) is uint);
      # 2026-01-06T18:24:19.825443Z  INFO avm_trace: true
      # trace(getQualifiedClassName(new uint()));
      # 2026-01-06T18:24:19.825446Z  INFO avm_trace: int

      # Int overflow => Number
      self.assertType(as3lib.Int(268435454), as3lib.Int)
      self.assertType(as3lib.Int(268435454 + 1), as3lib.Int)
      self.assertType(as3lib.Int(268435454 + 2), Number)

      # Int underflow => Number
      self.assertType(as3lib.Int(-268435454), as3lib.Int)
      self.assertType(as3lib.Int(-268435454 - 1), as3lib.Int)
      self.assertType(as3lib.Int(-268435454 - 2), as3lib.Int)
      self.assertType(as3lib.Int(-268435454 - 3), Number)

      # properties declared 'uint' don't underflow at 0
      self.assertEqual(Array().length - 1, -1)

      # `as uint` also doesn't underflow, returns null"
      # var a = -1;
      # trace(a as uint);
      # 2026-01-06T18:24:19.825702Z  INFO avm_trace: null

      #  uint type conversions _do_ underflow at 0
      # var b: uint;
      # b = a;
      # trace(b);
      # 2026-01-06T18:24:19.825709Z  INFO avm_trace: 4294967295

   # test_instanceOf can not be reproduced in python
   # This test asserts that numbers declared by themselves without type
   # declarations should be of type Number, not int

   def assertToExponential(self, value, check):
      # null/0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20
      val = as3lib.Int(value)
      self._assertToExponential(val, check)

   def test_toExponential(self):
      asrt_0 = ('1e-15', '0.0e-16', '0.00e-16', '0.000e-16', '0.0000e-16',
                '0.00000e-16', '0.000000e-16', '0.0000000e-16',
                '0.00000000e-16', '0.000000000e-16', '0.0000000000e-16',
                '0.00000000000000000000e-16')
      asrt_1 = ('1', '1.0', '1.00', '1.000', '1.0000', '1.00000', '1.000000',
                '1.0000000', '1.00000000', '1.000000000', '1.0000000000',
                '1.00000000000000000000')

      asrt_n1 = ('-1', '-1.0', '-1.00', '-1.000', '-1.0000', '-1.00000',
                 '-1.000000', '-1.0000000', '-1.00000000', '-1.000000000',
                 '-1.0000000000', '-1.00000000000000000000')

      asrt_16716550 = ('2e+7', '1.7e+7', '1.67e+7', '1.672e+7', '1.6717e+7',
                       '1.67166e+7', '1.671655e+7', '1.6716550e+7',
                       '1.67165500e+7', '1.671655000e+7', '1.6716550000e+7',
                       '1.67165500000000000000e+7')

      asrt_123 = ('1e+2', '1.2e+2', '1.23e+2', '1.230e+2', '1.2300e+2',
                  '1.23000e+2', '1.230000e+2', '1.2300000e+2',
                  '1.23000000e+2', '1.230000000e+2', '1.2300000000e+2',
                  '1.23000000000000000000e+2')

      asrt_2147483647 = ('2e+9', '2.1e+9', '2.15e+9', '2.147e+9', '2.1475e+9',
                         '2.14748e+9', '2.147484e+9', '2.1474836e+9',
                         '2.14748365e+9', '2.147483647e+9', '2.1474836470e+9',
                         '2.14748364700000000000e+9')

      asrt_n2147483648 = ('-2e+9', '-2.1e+9', '-2.15e+9', '-2.147e+9',
                          '-2.1475e+9', '-2.14748e+9', '-2.147484e+9',
                          '-2.1474836e+9', '-2.14748365e+9',
                          '-2.147483648e+9', '-2.1474836480e+9',
                          '-2.14748364800000000000e+9')

      asrt_n2147483647 = ('-2e+9', '-2.1e+9', '-2.15e+9', '-2.147e+9',
                          '-2.1475e+9', '-2.14748e+9', '-2.147484e+9',
                          '-2.1474836e+9', '-2.14748365e+9',
                          '-2.147483647e+9', '-2.1474836470e+9',
                          '-2.14748364700000000000e+9')

      self.assertToExponential(true, asrt_1)

      self.assertToExponential(false, asrt_0)
      self.assertToExponential(null, asrt_0)
      self.assertToExponential(undefined, asrt_0)

      self.assertToExponential(String(''), asrt_0)
      self.assertToExponential('', asrt_0)

      self.assertToExponential(String('str'), asrt_0)
      self.assertToExponential('str', asrt_0)

      self.assertToExponential(String('true'), asrt_0)
      self.assertToExponential('true', asrt_0)

      self.assertToExponential(String('false'), asrt_0)
      self.assertToExponential('false', asrt_0)

      self.assertToExponential(Number(0.0), asrt_0)
      self.assertToExponential(0.0, asrt_0)

      self.assertToExponential(NaN, asrt_0)

      self.assertToExponential(Number(-0.0), asrt_0)
      self.assertToExponential(-0.0, asrt_0)

      self.assertToExponential(Infinity, asrt_0)

      self.assertToExponential(Number(1.0), asrt_1)
      self.assertToExponential(1.0, asrt_1)

      self.assertToExponential(Number(-1.0), asrt_n1)
      self.assertToExponential(-1.0, asrt_n1)

      self.assertToExponential(Number(0xFF1306), asrt_16716550)
      self.assertToExponential(0xFF1306, asrt_16716550)

      self.assertToExponential(Number(1.2315e2), asrt_123)
      self.assertToExponential(1.2315e2, asrt_123)

      self.assertToExponential(Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToExponential(0x7FFFFFFF, asrt_2147483647)

      self.assertToExponential(Number(0x80000000), asrt_n2147483648)
      self.assertToExponential(0x80000000, asrt_n2147483648)

      self.assertToExponential(Number(0x80000001), asrt_n2147483647)
      self.assertToExponential(0x80000001, asrt_n2147483647)

      self.assertToExponential(Number(0x180000001), asrt_n2147483647)
      self.assertToExponential(0x180000001, asrt_n2147483647)

      self.assertToExponential(Number(0x100000001), asrt_1)
      self.assertToExponential(0x100000001, asrt_1)

      self.assertToExponential(Number(-0x7FFFFFFF), asrt_n2147483647)
      self.assertToExponential(-0x7FFFFFFF, asrt_n2147483647)

      self.assertToExponential(Number(-0x80000000), asrt_n2147483648)
      self.assertToExponential(-0x80000000, asrt_n2147483648)

      self.assertToExponential(Number(-0x80000001), asrt_2147483647)
      self.assertToExponential(-0x80000001, asrt_2147483647)

      self.assertToExponential(Number(-0x180000001), asrt_2147483647)
      self.assertToExponential(-0x180000001, asrt_2147483647)

      self.assertToExponential(Number(-0x100000001), asrt_n1)
      self.assertToExponential(-0x100000001, asrt_n1)

      self.assertToExponential(Object(), asrt_0)

      # Parse Tests
      self.assertToExponential(String('0.0'), asrt_0)
      self.assertToExponential('0.0', asrt_0)
      self.assertToExponential(String('NaN'), asrt_0)
      self.assertToExponential('NaN', asrt_0)
      self.assertToExponential(String('-0.0'), asrt_0)
      self.assertToExponential('-0.0', asrt_0)
      self.assertToExponential(String('Infinity'), asrt_0)
      self.assertToExponential('Infinity', asrt_0)
      self.assertToExponential(String('1.0'), asrt_1)
      self.assertToExponential('1.0', asrt_1)
      self.assertToExponential(String('-1.0'), asrt_n1)
      self.assertToExponential('-1.0', asrt_n1)
      self.assertToExponential(String('0xFF1306'), asrt_16716550)
      self.assertToExponential('0xFF1306', asrt_16716550)
      self.assertToExponential(String('1.2315e2'), asrt_123)
      self.assertToExponential('1.2315e2', asrt_123)
      self.assertToExponential(String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToExponential('0x7FFFFFFF', asrt_2147483647)
      self.assertToExponential(String('0x80000000'), asrt_n2147483648)
      self.assertToExponential('0x80000000', asrt_n2147483648)
      self.assertToExponential(String('0x80000001'), asrt_n2147483647)
      self.assertToExponential('0x80000001', asrt_n2147483647)
      self.assertToExponential(String('0x180000001'), asrt_n2147483647)
      self.assertToExponential('0x180000001', asrt_n2147483647)
      self.assertToExponential(String('0x100000001'), asrt_1)
      self.assertToExponential('0x100000001', asrt_1)
      self.assertToExponential(String('-0x7FFFFFFF'), asrt_n2147483647)
      self.assertToExponential('-0x7FFFFFFF', asrt_n2147483647)
      self.assertToExponential(String('-0x80000000'), asrt_n2147483648)
      self.assertToExponential('-0x80000000', asrt_n2147483648)
      self.assertToExponential(String('-0x80000001'), asrt_2147483647)
      self.assertToExponential('-0x80000001', asrt_2147483647)
      self.assertToExponential(String('-0x180000001'), asrt_2147483647)
      self.assertToExponential('-0x180000001', asrt_2147483647)
      self.assertToExponential(String('-0x100000001'), asrt_n1)
      self.assertToExponential('-0x100000001', asrt_n1)

   def assertToFixed(self, value, check):
      # null, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20
      val = as3lib.Int(value)
      self._assertToFixed(val, check)

   def test_toFixed(self):
      asrt_1 = ('1', '1.0', '1.00', '1.000', '1.0000', '1.00000', '1.000000',
                '1.0000000', '1.00000000', '1.000000000', '1.0000000000',
                '1.00000000000000000000')

      asrt_0 = ('0', '0.0', '0.00', '0.000', '0.0000', '0.00000', '0.000000',
                '0.0000000', '0.00000000', '0.000000000', '0.0000000000',
                '0.00000000000000000000')

      asrt_n1 = ('-1', '-1.0', '-1.00', '-1.000', '-1.0000', '-1.00000',
                 '-1.000000', '-1.0000000', '-1.00000000', '-1.000000000',
                 '-1.0000000000', '-1.00000000000000000000')

      asrt_16716550 = ('16716550', '16716550.0', '16716550.00',
                       '16716550.000', '16716550.0000', '16716550.00000',
                       '16716550.000000', '16716550.0000000',
                       '16716550.00000000', '16716550.000000000',
                       '16716550.0000000000', '16716550.00000000000000000000')

      asrt_123 = ('123', '123.0', '123.00', '123.000', '123.0000',
                  '123.00000', '123.000000', '123.0000000', '123.00000000',
                  '123.000000000', '123.0000000000',
                  '123.00000000000000000000')

      asrt_2147483647 = ('2147483647', '2147483647.0', '2147483647.00',
                         '2147483647.000', '2147483647.0000',
                         '2147483647.00000', '2147483647.000000',
                         '2147483647.0000000', '2147483647.00000000',
                         '2147483647.000000000', '2147483647.0000000000',
                         '2147483647.00000000000000000000')

      asrt_n2147483648 = ('-2147483648', '-2147483648.0', '-2147483648.00',
                          '-2147483648.000', '-2147483648.0000',
                          '-2147483648.00000', '-2147483648.000000',
                          '-2147483648.0000000', '-2147483648.00000000',
                          '-2147483648.000000000', '-2147483648.0000000000',
                          '-2147483648.00000000000000000000')

      asrt_n2147483647 = ('-2147483647', '-2147483647.0', '-2147483647.00',
                          '-2147483647.000', '-2147483647.0000',
                          '-2147483647.00000', '-2147483647.000000',
                          '-2147483647.0000000', '-2147483647.00000000',
                          '-2147483647.000000000', '-2147483647.0000000000',
                          '-2147483647.00000000000000000000')

      self.assertToFixed(true, asrt_1)

      self.assertToFixed(false, asrt_0)
      self.assertToFixed(null, asrt_0)
      self.assertToFixed(undefined, asrt_0)

      self.assertToFixed(String(''), asrt_0)
      self.assertToFixed('', asrt_0)

      self.assertToFixed(String('str'), asrt_0)
      self.assertToFixed('str', asrt_0)

      self.assertToFixed(String('true'), asrt_0)
      self.assertToFixed('true', asrt_0)

      self.assertToFixed(String('false'), asrt_0)
      self.assertToFixed('false', asrt_0)

      self.assertToFixed(Number(0.0), asrt_0)
      self.assertToFixed(0.0, asrt_0)

      self.assertToFixed(NaN, asrt_0)

      self.assertToFixed(Number(-0.0), asrt_0)
      self.assertToFixed(-0.0, asrt_0)

      self.assertToFixed(Infinity, asrt_0)

      self.assertToFixed(Number(1.0), asrt_1)
      self.assertToFixed(1.0, asrt_1)

      self.assertToFixed(Number(-1.0), asrt_n1)
      self.assertToFixed(-1.0, asrt_n1)

      self.assertToFixed(Number(0xFF1306), asrt_16716550)
      self.assertToFixed(0xFF1306, asrt_16716550)

      self.assertToFixed(Number(1.2315e2), asrt_123)
      self.assertToFixed(1.2315e2, asrt_123)

      self.assertToFixed(Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToFixed(0x7FFFFFFF, asrt_2147483647)

      self.assertToFixed(Number(0x80000000), asrt_n2147483648)
      self.assertToFixed(0x80000000, asrt_n2147483648)

      self.assertToFixed(Number(0x80000001), asrt_n2147483647)
      self.assertToFixed(0x80000001, asrt_n2147483647)

      self.assertToFixed(Number(0x180000001), asrt_n2147483647)
      self.assertToFixed(0x180000001, asrt_n2147483647)

      self.assertToFixed(Number(0x100000001), asrt_1)
      self.assertToFixed(0x100000001, asrt_1)

      self.assertToFixed(Number(-0x7FFFFFFF), asrt_n2147483647)
      self.assertToFixed(-0x7FFFFFFF, asrt_n2147483647)

      self.assertToFixed(Number(-0x80000000), asrt_n2147483648)
      self.assertToFixed(-0x80000000, asrt_n2147483648)

      self.assertToFixed(Number(-0x80000001), asrt_2147483647)
      self.assertToFixed(-0x80000001, asrt_2147483647)

      self.assertToFixed(Number(-0x180000001), asrt_2147483647)
      self.assertToFixed(-0x180000001, asrt_2147483647)

      self.assertToFixed(Number(-0x100000001), asrt_n1)
      self.assertToFixed(-0x100000001, asrt_n1)

      self.assertToFixed(Object(), asrt_0)

      # Parse Tests
      self.assertToFixed(String('0.0'), asrt_0)
      self.assertToFixed('0.0', asrt_0)
      self.assertToFixed(String('NaN'), asrt_0)
      self.assertToFixed('NaN', asrt_0)
      self.assertToFixed(String('-0.0'), asrt_0)
      self.assertToFixed('-0.0', asrt_0)
      self.assertToFixed(String('Infinity'), asrt_0)
      self.assertToFixed('Infinity', asrt_0)
      self.assertToFixed(String('1.0'), asrt_1)
      self.assertToFixed('1.0', asrt_1)
      self.assertToFixed(String('-1.0'), asrt_n1)
      self.assertToFixed('-1.0', asrt_n1)
      self.assertToFixed(String('0xFF1306'), asrt_16716550)
      self.assertToFixed('0xFF1306', asrt_16716550)
      self.assertToFixed(String('1.2315e2'), asrt_123)
      self.assertToFixed('1.2315e2', asrt_123)
      self.assertToFixed(String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToFixed('0x7FFFFFFF', asrt_2147483647)
      self.assertToFixed(String('0x80000000'), asrt_n2147483648)
      self.assertToFixed('0x80000000', asrt_n2147483648)
      self.assertToFixed(String('0x80000001'), asrt_n2147483647)
      self.assertToFixed('0x80000001', asrt_n2147483647)
      self.assertToFixed(String('0x180000001'), asrt_n2147483647)
      self.assertToFixed('0x180000001', asrt_n2147483647)
      self.assertToFixed(String('0x100000001'), asrt_1)
      self.assertToFixed('0x100000001', asrt_1)
      self.assertToFixed(String('-0x7FFFFFFF'), asrt_n2147483647)
      self.assertToFixed('-0x7FFFFFFF', asrt_n2147483647)
      self.assertToFixed(String('-0x80000000'), asrt_n2147483648)
      self.assertToFixed('-0x80000000', asrt_n2147483648)
      self.assertToFixed(String('-0x80000001'), asrt_2147483647)
      self.assertToFixed('-0x80000001', asrt_2147483647)
      self.assertToFixed(String('-0x180000001'), asrt_2147483647)
      self.assertToFixed('-0x180000001', asrt_2147483647)
      self.assertToFixed(String('-0x100000001'), asrt_n1)
      self.assertToFixed('-0x100000001', asrt_n1)

   def assertToPrecision(self, value, check):
      val = as3lib.Int(value)
      self._assertToPrecision(val, check)

   def test_toPrecision(self):
      asrt_1 = ('1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1')

      asrt_0 = ('0e+1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0')

      asrt_n1 = ('-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                 '-1', '-1')

      asrt_16716550 = ('1e+7', '1.6e+7', '1.6699999999999997e+7', '1.671e+7',
                       '1.6716e+7', '1.67165e+7', '1.671655e+7', '16716550',
                       '16716550', '16716550', '16716550',
                       '16716550.000000002')

      asrt_123 = ('1e+2', '1.2e+2', '123', '123', '123', '123', '123', '123',
                  '123', '123', '123', '123')

      asrt_2147483647 = ('1.9999999999999998e+9', '2.1e+9', '2.14e+9',
                         '2.147e+9', '2.1473999999999998e+9', '2.14748e+9',
                         '2.147483e+9', '2.1474836e+9', '2.14748364e+9',
                         '2147483647', '2147483647', '2147483647')

      asrt_n2147483648 = ('-3e+9', '-2.2e+9', '-2.15e+9', '-2.148e+9',
                          '-2.1475e+9', '-2.14749e+9', '-2.147484e+9',
                          '-2.1474837e+9', '-2.14748365e+9', '-2147483648',
                          '-2147483648', '-2147483648')

      asrt_n2147483647 = ('-3e+9', '-2.2e+9', '-2.15e+9', '-2.148e+9',
                          '-2.1475e+9', '-2.14749e+9', '-2.147484e+9',
                          '-2.1474837e+9', '-2.14748365e+9', '-2147483647',
                          '-2147483647', '-2147483647')

      self.assertToPrecision(true, asrt_1)

      self.assertToPrecision(false, asrt_0)
      self.assertToPrecision(null, asrt_0)
      self.assertToPrecision(undefined, asrt_0)

      self.assertToPrecision(String(''), asrt_0)
      self.assertToPrecision('', asrt_0)

      self.assertToPrecision(String('str'), asrt_0)
      self.assertToPrecision('str', asrt_0)

      self.assertToPrecision(String('true'), asrt_0)
      self.assertToPrecision('true', asrt_0)

      self.assertToPrecision(String('false'), asrt_0)
      self.assertToPrecision('false', asrt_0)

      self.assertToPrecision(Number(0.0), asrt_0)
      self.assertToPrecision(0.0, asrt_0)

      self.assertToPrecision(NaN, asrt_0)

      self.assertToPrecision(Number(-0.0), asrt_0)
      self.assertToPrecision(-0.0, asrt_0)

      self.assertToPrecision(Infinity, asrt_0)

      self.assertToPrecision(Number(1.0), asrt_1)
      self.assertToPrecision(1.0, asrt_1)

      self.assertToPrecision(Number(-1.0), asrt_n1)
      self.assertToPrecision(-1.0, asrt_n1)

      self.assertToPrecision(Number(0xFF1306), asrt_16716550)
      self.assertToPrecision(0xFF1306, asrt_16716550)

      self.assertToPrecision(Number(1.2315e2), asrt_123)
      self.assertToPrecision(1.2315e2, asrt_123)

      self.assertToPrecision(Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToPrecision(0x7FFFFFFF, asrt_2147483647)

      self.assertToPrecision(Number(0x80000000), asrt_n2147483648)
      self.assertToPrecision(0x80000000, asrt_n2147483648)

      self.assertToPrecision(Number(0x80000001), asrt_n2147483647)
      self.assertToPrecision(0x80000001, asrt_n2147483647)

      self.assertToPrecision(Number(0x180000001), asrt_n2147483647)
      self.assertToPrecision(0x180000001, asrt_n2147483647)

      self.assertToPrecision(Number(0x100000001), asrt_1)
      self.assertToPrecision(0x100000001, asrt_1)

      self.assertToPrecision(Number(-0x7FFFFFFF), asrt_n2147483647)
      self.assertToPrecision(-0x7FFFFFFF, asrt_n2147483647)

      self.assertToPrecision(Number(-0x80000000), asrt_n2147483648)
      self.assertToPrecision(-0x80000000, asrt_n2147483648)

      self.assertToPrecision(Number(-0x80000001), asrt_2147483647)
      self.assertToPrecision(-0x80000001, asrt_2147483647)

      self.assertToPrecision(Number(-0x180000001), asrt_2147483647)
      self.assertToPrecision(-0x180000001, asrt_2147483647)

      self.assertToPrecision(Number(-0x100000001), asrt_n1)
      self.assertToPrecision(-0x100000001, asrt_n1)

      self.assertToPrecision(Object(), asrt_0)

      # Parse Tests
      self.assertToPrecision(String('0.0'), asrt_0)
      self.assertToPrecision('0.0', asrt_0)
      self.assertToPrecision(String('NaN'), asrt_0)
      self.assertToPrecision('NaN', asrt_0)
      self.assertToPrecision(String('-0.0'), asrt_0)
      self.assertToPrecision('-0.0', asrt_0)
      self.assertToPrecision(String('Infinity'), asrt_0)
      self.assertToPrecision('Infinity', asrt_0)
      self.assertToPrecision(String('1.0'), asrt_1)
      self.assertToPrecision('1.0', asrt_1)
      self.assertToPrecision(String('-1.0'), asrt_n1)
      self.assertToPrecision('-1.0', asrt_n1)
      self.assertToPrecision(String('0xFF1306'), asrt_16716550)
      self.assertToPrecision('0xFF1306', asrt_16716550)
      self.assertToPrecision(String('1.2315e2'), asrt_123)
      self.assertToPrecision('1.2315e2', asrt_123)
      self.assertToPrecision(String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToPrecision('0x7FFFFFFF', asrt_2147483647)
      self.assertToPrecision(String('0x80000000'), asrt_n2147483648)
      self.assertToPrecision('0x80000000', asrt_n2147483648)
      self.assertToPrecision(String('0x80000001'), asrt_n2147483647)
      self.assertToPrecision('0x80000001', asrt_n2147483647)
      self.assertToPrecision(String('0x180000001'), asrt_n2147483647)
      self.assertToPrecision('0x180000001', asrt_n2147483647)
      self.assertToPrecision(String('0x100000001'), asrt_1)
      self.assertToPrecision('0x100000001', asrt_1)
      self.assertToPrecision(String('-0x7FFFFFFF'), asrt_n2147483647)
      self.assertToPrecision('-0x7FFFFFFF', asrt_n2147483647)
      self.assertToPrecision(String('-0x80000000'), asrt_n2147483648)
      self.assertToPrecision('-0x80000000', asrt_n2147483648)
      self.assertToPrecision(String('-0x80000001'), asrt_2147483647)
      self.assertToPrecision('-0x80000001', asrt_2147483647)
      self.assertToPrecision(String('-0x180000001'), asrt_2147483647)
      self.assertToPrecision('-0x180000001', asrt_2147483647)
      self.assertToPrecision(String('-0x100000001'), asrt_n1)
      self.assertToPrecision('-0x100000001', asrt_n1)

   def assertToString(self, value, check):
      # 2, 3, 4, 5, 6, 7, 8, 9, null/10, ..., valueOf
      val = as3lib.Int(value)
      self._assertToString(val, check)

   def test_toString(self):
      asrt_1 = ('1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', 1)

      asrt_0 = ('0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 0)

      asrt_n1 = ('-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                 '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                 '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                 '-1', '-1', '-1', '-1', '-1', -1)

      asrt_16716550 = ('111111110001001100000110', '1011110021210111',
                       '333301030012', '13234412200', '1354143234',
                       '262042204', '77611406', '34407714', '16716550',
                       '9488434', '5721b1a', '3603a66', '2312074', '17030ba',
                       'ff1306', 'bd28c8', '8f4654', '6e5348', '549b7a',
                       '41k104', '357k74', '2dgl6c', '2295im', '1hjlc0',
                       '1af2g6', '14c7ld', 'r5e3i', 'nibsm', 'kj3sa', 'i33th',
                       'fu4o6', 'e35c4', 'chan8', 'b4v5p', '9yakm', 16716550)

      asrt_123 = ('1111011', '11120', '1323', '443', '323', '234', '173',
                  '146', '123', '102', 'a3', '96', '8b', '83', '7b', '74',
                  '6f', '69', '63', '5i', '5d', '58', '53', '4n', '4j', '4f',
                  '4b', '47', '43', '3u', '3r', '3o', '3l', '3i', '3f', 123)

      asrt_2147483647 = ('1111111111111111111111111111111',
                         '12112122212110202101', '1333333333333333',
                         '13344223434042', '553032005531', '104134211161',
                         '17777777777', '5478773671', '2147483647',
                         'a02220281', '4bb2308a7', '282ba4aaa', '1652ca931',
                         'c87e66b7', '7fffffff', '53g7f548', '3928g3h1',
                         '27c57h32', '1db1f927', '140h2d91', 'ikf5bf1',
                         'ebelf95', 'b5gge57', '8jmdnkm', '6oj8ion',
                         '5ehncka', '4clm98f', '3hk7987', '2sb6cs7',
                         '2d09uc1', '1vvvvvv', '1lsqtl1', '1d8xqrp',
                         '15v22um', 'zik0zj', 2147483647)

      asrt_n2147483648 = ('-10000000000000000000000000000000',
                          '-12112122212110202102', '-2000000000000000',
                          '-13344223434043', '-553032005532', '-104134211162',
                          '-20000000000', '-5478773672', '-2147483648',
                          '-a02220282', '-4bb2308a8', '-282ba4aab',
                          '-1652ca932', '-c87e66b8', '-80000000', '-53g7f549',
                          '-3928g3h2', '-27c57h33', '-1db1f928', '-140h2d92',
                          '-ikf5bf2', '-ebelf96', '-b5gge58', '-8jmdnkn',
                          '-6oj8ioo', '-5ehnckb', '-4clm98g', '-3hk7988',
                          '-2sb6cs8', '-2d09uc2', '-2000000', '-1lsqtl2',
                          '-1d8xqrq', '-15v22un', '-zik0zk', -2147483648)

      asrt_n2147483647 = ('-1111111111111111111111111111111',
                          '-12112122212110202101', '-1333333333333333',
                          '-13344223434042', '-553032005531', '-104134211161',
                          '-17777777777', '-5478773671', '-2147483647',
                          '-a02220281', '-4bb2308a7', '-282ba4aaa',
                          '-1652ca931', '-c87e66b7', '-7fffffff', '-53g7f548',
                          '-3928g3h1', '-27c57h32', '-1db1f927', '-140h2d91',
                          '-ikf5bf1', '-ebelf95', '-b5gge57', '-8jmdnkm',
                          '-6oj8ion', '-5ehncka', '-4clm98f', '-3hk7987',
                          '-2sb6cs7', '-2d09uc1', '-1vvvvvv', '-1lsqtl1',
                          '-1d8xqrp', '-15v22um', '-zik0zj', -2147483647)

      self.assertToString(true, asrt_1)

      self.assertToString(false, asrt_0)
      self.assertToString(null, asrt_0)
      self.assertToString(undefined, asrt_0)

      self.assertToString(String(''), asrt_0)
      self.assertToString('', asrt_0)

      self.assertToString(String('str'), asrt_0)
      self.assertToString('str', asrt_0)

      self.assertToString(String('true'), asrt_0)
      self.assertToString('true', asrt_0)

      self.assertToString(String('false'), asrt_0)
      self.assertToString('false', asrt_0)

      self.assertToString(Number(0.0), asrt_0)
      self.assertToString(0.0, asrt_0)

      self.assertToString(NaN, asrt_0)

      self.assertToString(Number(-0.0), asrt_0)
      self.assertToString(-0.0, asrt_0)

      self.assertToString(Infinity, asrt_0)

      self.assertToString(Number(1.0), asrt_1)
      self.assertToString(1.0, asrt_1)

      self.assertToString(Number(-1.0), asrt_n1)
      self.assertToString(-1.0, asrt_n1)

      self.assertToString(Number(0xFF1306), asrt_16716550)
      self.assertToString(0xFF1306, asrt_16716550)

      self.assertToString(Number(1.2315e2), asrt_123)
      self.assertToString(1.2315e2, asrt_123)

      self.assertToString(Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToString(0x7FFFFFFF, asrt_2147483647)

      self.assertToString(Number(0x80000000), asrt_n2147483648)
      self.assertToString(0x80000000, asrt_n2147483648)

      self.assertToString(Number(0x80000001), asrt_n2147483647)
      self.assertToString(0x80000001, asrt_n2147483647)

      self.assertToString(Number(0x180000001), asrt_n2147483647)
      self.assertToString(0x180000001, asrt_n2147483647)

      self.assertToString(Number(0x100000001), asrt_1)
      self.assertToString(0x100000001, asrt_1)

      self.assertToString(Number(-0x7FFFFFFF), asrt_n2147483647)
      self.assertToString(-0x7FFFFFFF, asrt_n2147483647)

      self.assertToString(Number(-0x80000000), asrt_n2147483648)
      self.assertToString(-0x80000000, asrt_n2147483648)

      self.assertToString(Number(-0x80000001), asrt_2147483647)
      self.assertToString(-0x80000001, asrt_2147483647)

      self.assertToString(Number(-0x180000001), asrt_2147483647)
      self.assertToString(-0x180000001, asrt_2147483647)

      self.assertToString(Number(-0x100000001), asrt_n1)
      self.assertToString(-0x100000001, asrt_n1)

      self.assertToString(Object(), asrt_0)

      # Parse Tests
      self.assertToString(String('0.0'), asrt_0)
      self.assertToString('0.0', asrt_0)
      self.assertToString(String('NaN'), asrt_0)
      self.assertToString('NaN', asrt_0)
      self.assertToString(String('-0.0'), asrt_0)
      self.assertToString('-0.0', asrt_0)
      self.assertToString(String('Infinity'), asrt_0)
      self.assertToString('Infinity', asrt_0)
      self.assertToString(String('1.0'), asrt_1)
      self.assertToString('1.0', asrt_1)
      self.assertToString(String('-1.0'), asrt_n1)
      self.assertToString('-1.0', asrt_n1)
      self.assertToString(String('0xFF1306'), asrt_16716550)
      self.assertToString('0xFF1306', asrt_16716550)
      self.assertToString(String('1.2315e2'), asrt_123)
      self.assertToString('1.2315e2', asrt_123)
      self.assertToString(String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToString('0x7FFFFFFF', asrt_2147483647)
      self.assertToString(String('0x80000000'), asrt_n2147483648)
      self.assertToString('0x80000000', asrt_n2147483648)
      self.assertToString(String('0x80000001'), asrt_n2147483647)
      self.assertToString('0x80000001', asrt_n2147483647)
      self.assertToString(String('0x180000001'), asrt_n2147483647)
      self.assertToString('0x180000001', asrt_n2147483647)
      self.assertToString(String('0x100000001'), asrt_1)
      self.assertToString('0x100000001', asrt_1)
      self.assertToString(String('-0x7FFFFFFF'), asrt_n2147483647)
      self.assertToString('-0x7FFFFFFF', asrt_n2147483647)
      self.assertToString(String('-0x80000000'), asrt_n2147483648)
      self.assertToString('-0x80000000', asrt_n2147483648)
      self.assertToString(String('-0x80000001'), asrt_2147483647)
      self.assertToString('-0x80000001', asrt_2147483647)
      self.assertToString(String('-0x180000001'), asrt_2147483647)
      self.assertToString('-0x180000001', asrt_2147483647)
      self.assertToString(String('-0x100000001'), asrt_n1)
      self.assertToString('-0x100000001', asrt_n1)


class JSONTests(as3libTestCase):
   def test_errors(self):
      recursive = Object()
      recursive.recursivekey = recursive
      self.assertRaisesAS3(SyntaxError, 1132, None, JSON.parse, '{a}')
      self.assertRaisesAS3(TypeError, 1129, None, JSON.stringify, recursive)
      self.assertRaisesAS3(TypeError, 1131, None, JSON.stringify, {'key': 'value'}, '---')
      self.assertRaisesAS3(TypeError, 1131, None, JSON.stringify, recursive, '---')
      self.assertRaisesAS3(TypeError, 1131, None, JSON.stringify, recursive, {'key': '---'})
      JSON.parse("{\"a\": 8}")  # Should work
      self.assertEqual(JSON.stringify(recursive, ['otherkey']), {})
      self.assertRaisesAS3(TypeError, 1129, None, JSON.stringify, recursive, null)
      self.assertEqual(JSON.stringify({"a": 8}, null), '{"a":8}')
      self.assertRaisesAS3(TypeError, 1131, None, JSON.stringify, {"a": 8}, undefined)

   def test_parse(self):
      INPUT = '{"test": "value", "another": [1, 2, 3], "example": {"recursive": "test"}}'
      parsed = JSON.parse(INPUT)
      self.assertEqual(parsed.test, 'value')
      self.assertEqual(parsed.another, [1, 2, 3])
      self.assertTrue(isinstance(parsed.example, Object))
      self.assertEqual(parsed.example.recursive, 'test')

      # Parse with reviver
      def func(k, v):
         return v

      parsed = JSON.parse(INPUT, func)

      self.assertEqual(parsed.test, 'value')
      self.assertArray(parsed.another, [1, 2, 3])
      self.assertEqual(parsed.example, {'recursive': 'test'})
      self.assertEqual(parsed.example.recursive, 'test')

      # Parse with custom reviver
      def func(k, v):
         if isinstance(v, (as3lib.Int, int)):
            return as3lib.String('custom')
         return v

      parsed = JSON.parse(INPUT, func)

      self.assertEqual(parsed.test, 'value')
      self.assertArray(parsed.another, ['custom', 'custom', 'custom'])
      self.assertEqual(parsed.example, {'recursive': 'test'})
      self.assertEqual(parsed.example.recursive, 'test')

   def test_stringify(self):
      raise TestNotImplemented


class MathTests(as3libTestCase):
   def assertFuncReturns(self, check, func, *args):
      if check is NaN:
         self.assertNaN(func(*args))
      else:
         self.assertEqual(func(*args), check)

   def assertFunc1(self, func, *values):
      obj = Object()
      obj.valueOf = lambda: Number(10.1)
      self.assertFuncReturns(values[0], func, 0)
      self.assertFuncReturns(values[1], func, 1)
      self.assertFuncReturns(values[2], func, -1)
      self.assertFuncReturns(values[3], func, 1234.5)
      self.assertFuncReturns(values[4], func, -1234.5)
      self.assertFuncReturns(values[5], func, Infinity)
      self.assertFuncReturns(values[6], func, -Infinity)
      self.assertFuncReturns(values[7], func, NaN)
      self.assertFuncReturns(values[8], func, true)
      self.assertFuncReturns(values[9], func, false)
      self.assertFuncReturns(values[10], func, undefined)
      self.assertFuncReturns(values[11], func, null)
      self.assertFuncReturns(values[12], func, String('55.5'))
      self.assertFuncReturns(values[13], func, obj)

   def assertFunc2(self, func, *values):
      obj = Object()
      obj.valueOf = lambda: Number(10.1)
      self.assertFuncReturns(values[0], func, 0, 0)
      self.assertFuncReturns(values[1], func, 1, 2)
      self.assertFuncReturns(values[2], func, 2, -4)
      self.assertFuncReturns(values[3], func, 4, -2)
      self.assertFuncReturns(values[4], func, -99, -100)
      self.assertFuncReturns(values[5], func, Infinity, -Infinity)
      self.assertFuncReturns(values[6], func, NaN, 100)
      self.assertFuncReturns(values[7], func, 999, NaN)
      self.assertFuncReturns(values[8], func, true, false)
      self.assertFuncReturns(values[9], func, undefined, null)
      self.assertFuncReturns(values[10], func, String('55.5'), String('-1234'))
      self.assertFuncReturns(values[11], func, obj, obj)

   def test_constants(self):
      self.assertEqual(Math.E, 2.718281828459045)
      self.assertEqual(Math.LN10, 2.302585092994046)
      self.assertEqual(Math.LN2, 0.6931471805599453)
      self.assertEqual(Math.LOG10E, 0.4342944819032518)
      self.assertEqual(Math.LOG2E, 1.4426950408889634)
      self.assertEqual(Math.PI, 3.141592653589793)
      self.assertEqual(Math.SQRT1_2, 0.7071067811865476)
      self.assertEqual(Math.SQRT2, 1.4142135623730951)

   def test_abs(self):
      self.assertFunc1(Math.abs, 0, 1, 1, 1234.5, 1234.5, Infinity, Infinity,
                       NaN, 1, 0, NaN, 0, 55.5, 10.1)

   def test_acos(self):
      self.assertFunc1(Math.acos, 1.5707963267948966, 0, 3.141592653589793,
                       NaN, NaN, NaN, NaN, NaN, 0, 1.5707963267948966, NaN,
                       1.5707963267948966, NaN, NaN)

   def test_asin(self):
      self.assertFunc1(Math.asin, 0, 1.5707963267948966, -1.5707963267948966,
                       NaN, NaN, NaN, NaN, NaN, 1.5707963267948966, 0, NaN, 0,
                       NaN, NaN)

   def test_atan(self):
      self.assertFunc1(Math.atan, 0, 0.7853981633974483, -0.7853981633974483,
                       1.5699862824196225, -1.5699862824196225,
                       1.5707963267948966, -1.5707963267948966, NaN,
                       0.7853981633974483, 0, NaN, 0, 1.5527802582408412,
                       1.47210806614649)

   def test_atan2(self):
      self.assertFunc2(Math.atan2, 0, 0.4636476090008061, 2.677945044588987,
                       2.0344439357957027, -2.361219573523157,
                       2.356194490192345, NaN, NaN, 1.5707963267948966, NaN,
                       3.096647253816438, 0.7853981633974483)

   def test_ceil(self):
      self.assertFunc1(Math.ceil, 0, 1, -1, 1235, -1234, Infinity, -Infinity,
                       NaN, 1, 0, NaN, 0, 56, 11)

   def test_cos(self):
      self.assertFunc1(Math.cos, 1, 0.5403023058681398, 0.5403023058681398,
                       -0.989373592132422, -0.989373592132422, NaN, NaN, NaN,
                       0.5403023058681398, 1, NaN, 1, 0.49872621790648564,
                       -0.7805681801691837)

   def test_exp(self):
      self.assertFunc1(Math.exp, 1, 2.718281828459045, 0.36787944117144233,
                       Infinity, 0, Infinity, 0, NaN, 2.718281828459045, 1,
                       NaN, 1, 1.268655614010956e+24, 24343.00942440838)

   def test_floor(self):
      self.assertFunc1(Math.floor, 0, 1, -1, 1234, -1235, Infinity, -Infinity,
                       NaN, 1, 0, NaN, 0, 55, 10)

   def test_log(self):
      self.assertFunc1(Math.log, -Infinity, 0, NaN, 7.118421308785234, NaN,
                       Infinity, NaN, NaN, 0, -Infinity, NaN, -Infinity,
                       4.0163830207523885, 2.312535423847214)

   def test_max(self):
      self.assertFunc2(Math.max, 0, 2, 2, 4, -99, Infinity, NaN, NaN, 1, NaN,
                       55.5, 10.1)

   def test_min(self):
      self.assertFunc2(Math.min, 0, 1, -4, -2, -100, -Infinity, NaN, NaN, 0,
                       NaN, -1234, 10.1)

   def test_pow(self):
      self.assertFunc2(Math.pow, 1, 1, 0.0625, 0.0625,
                       2.7319990264290253e-200, 0, NaN, NaN, 1, 1, 0,
                       13920212824.565023)

   def test_round(self):
      self.assertFunc1(Math.round, 0, 1, -1, 1235, -1234, Infinity, -Infinity,
                       NaN, 1, 0, NaN, 0, 56, 10)

   def test_sin(self):
      self.assertFunc1(Math.sin, 0, 0.8414709848078965, -0.8414709848078965,
                       0.14539565052293643, -0.14539565052293643, NaN, NaN,
                       NaN, 0.8414709848078965, 0, NaN, 0,
                       -0.8667595742607592, -0.6250706488928821)

   def test_sqrt(self):
      self.assertFunc1(Math.sqrt, 0, 1, NaN, 35.13545218152173, NaN, Infinity,
                       NaN, NaN, 1, 0, NaN, 0, 7.44983221287567,
                       3.1780497164141406)

   def test_tan(self):
      self.assertFunc1(Math.tan, 0, 1.5574077246549023, -1.5574077246549023,
                       -0.14695727850342305, 0.14695727850342305, NaN, NaN,
                       NaN, 1.5574077246549023, 0, NaN, 0,
                       -1.7379466792405172, 0.8007893029375109)

   def test_minmax_special_cases(self):
      self.assertEqual(Math.min(), Infinity)
      self.assertEqual(Math.min(0), 0)
      self.assertEqual(Math.min(1, 2, 3), 1)
      self.assertEqual(Math.min(-1.1, -2.2, -3.3), -3.3)
      self.assertNaN(Math.min(9, NaN, false, true, Infinity, undefined))
      self.assertEqual(Math.max(), -Infinity)
      self.assertEqual(Math.max(0), 0)
      self.assertEqual(Math.max(1, 2, 3), 3)
      self.assertEqual(Math.max(-1.1, -2.2, -3.3), -1.1)
      self.assertNaN(Math.max(9, NaN, false, true, Infinity, undefined))


class NamespaceTests(as3libTestCase):
   def assertNamespace(self, ns, prefix, uri):
      try:
         assert ns.prefix == prefix and ns.uri == uri
      except AssertionError as e:
         raise AssertionError('Namespace(%r, %r) != (%r, %r)' % (ns.prefix, ns.uri, prefix, uri)) from e

   def test_constructor(self):
      example = Namespace('value')
      self.assertNamespace(example, undefined, 'value')

      otherNS = Namespace('otherPrefix', 'otherUri')
      qName = QName('namespace', 'name')
      values = (null, undefined, 'test', '', 'NOT A VALID PREFIX', otherNS, qName)

      ns = Namespace()
      self.assertNamespace(ns, '', '')

      ans = ((undefined, 'null'), (undefined, 'undefined'),
             (undefined, 'test'), ('', ''), (undefined, 'NOT A VALID PREFIX'),
             ('otherPrefix', 'otherUri'), (undefined, 'namespace'))
      for i in range(len(values)):
         self.assertNamespace(Namespace(values[i]), *ans[i])

      def asrt_constr(a, check):
         self.assertNamespace(Namespace(a, null), *check[0])
         self.assertNamespace(Namespace(a, undefined), *check[1])
         self.assertNamespace(Namespace(a, 'test'), *check[2])
         if a == '':
            self.assertEqual(Namespace(a, ''), '', '')
         else:
            self.assertRaisesAS3(TypeError, 1098, None, Namespace, a, '')
         self.assertNamespace(Namespace(a, 'NOT A VALID PREFIX'), *check[3])
         self.assertNamespace(Namespace(a, otherNS), *check[4])
         self.assertNamespace(Namespace(a, qName), *check[5])

      ans = (((undefined, 'null'), (undefined, 'undefined'),
              (undefined, 'test'), (undefined, 'NOT A VALID PREFIX'),
              (undefined, 'otherUri'), (undefined, 'namespace')),
             ((undefined, 'null'), (undefined, 'undefined'),
              (undefined, 'test'), (undefined, 'NOT A VALID PREFIX'),
              (undefined, 'otherUri'), (undefined, 'namespace')),
             (('test', 'null'), ('test', 'undefined'), ('test', 'test'),
              ('test', 'NOT A VALID PREFIX'), ('test', 'otherUri'),
              ('test', 'namespace')),
             (('', 'null'), ('', 'undefined'), ('', 'test'), ('', ''),
              ('', 'NOT A VALID PREFIX'), ('', 'otherUri'),
              ('', 'namespace')),
             ((undefined, 'null'), (undefined, 'undefined'),
              (undefined, 'test'), (undefined, 'NOT A VALID PREFIX'),
              (undefined, 'otherUri'), (undefined, 'namespace')),
             (('otherUri', 'null'), ('otherUri', 'undefined'),
              ('otherUri', 'test'), ('otherUri', 'NOT A VALID PREFIX'),
              ('otherUri', 'otherUri'), ('otherUri', 'namespace')),
             ((undefined, 'null'), (undefined, 'undefined'),
              (undefined, 'test'), (undefined, 'NOT A VALID PREFIX'),
              (undefined, 'otherUri'), (undefined, 'namespace')))
      for i in range(len(values)):
         asrt_constr(values[i], ans[i])

   def test_multiargs(self):
      # TODO: Make sure assert is accurate
      ns = Namespace('prefix', 'ns', 'extra')
      self.assertNamespace(ns, 'prefix', 'ns')

   def test_enumeration_order(self):
      namespace = Namespace('p', 'u')

      test = [String(name) for name in namespace]
      asrt = ['uri', 'prefix']
      self.assertArray(test, asrt)

      asrt = ['u', 'p']
      self.assertEach(namespace, asrt)


class NumberTests(NumberTestsBase):
   def test_constructor(self):
      self.assertEqual(Number(), 0)
      self.assertEqual(Number(Number()), 0)
      self.assertEqual(Number(true), 1)
      self.assertEqual(Number(false), 0)
      self.assertEqual(Number(null), 0)
      self.assertNaN(Number(undefined))

      self.assertEqual(Number(String('')), 0)
      self.assertEqual(Number(''), 0)
      self.assertNaN(Number(String('str')))
      self.assertNaN(Number('str'))
      self.assertNaN(Number(String('true')))
      self.assertNaN(Number('true'))
      self.assertNaN(Number(String('false')))
      self.assertNaN(Number('false'))

      self.assertEqual(Number(0.0), 0)

      self.assertNaN(Number(NaN))

      self.assertEqual(Number(-0.0), 0)

      self.assertEqual(Number(Infinity), Infinity)

      self.assertEqual(Number(1.0), 1)
      self.assertEqual(Number(-1.0), -1)
      self.assertEqual(Number(0xFF1306), 16716550)
      self.assertEqual(Number(1.2315e2), 123.15)
      self.assertEqual(Number(0.0), 0)

      self.assertNaN(Number(Object()))

      self.assertEqual(Number(String('0.0')), 0)
      self.assertEqual(Number('0.0'), 0)
      self.assertNaN(Number(String('NaN')))
      self.assertNaN(Number('NaN'))
      self.assertEqual(Number(String('-0.0')), 0)
      self.assertEqual(Number('-0.0'), 0)
      self.assertEqual(Number(String('Infinity')), Infinity)
      self.assertEqual(Number('Infinity'), Infinity)
      self.assertEqual(Number(String('-Infinity')), -Infinity)
      self.assertEqual(Number('-Infinity'), -Infinity)

      self.assertNaN(Number(String('infinity')))
      self.assertNaN(Number('infinity'))
      self.assertNaN(Number(String('inf')))
      self.assertNaN(Number('inf'))

      self.assertEqual(Number(String('1.0')), 1)
      self.assertEqual(Number('1.0'), 1)
      self.assertEqual(Number(String('-1.0')), -1)
      self.assertEqual(Number('-1.0'), -1)
      self.assertEqual(Number(String('0xFF1306')), 16716550)
      self.assertEqual(Number('0xFF1306'), 16716550)
      self.assertEqual(Number(String('1.2315e2')), 123.15)
      self.assertEqual(Number('1.2315e2'), 123.15)

   def assertToExponential(self, value, check):
      val = Number(value)
      self._assertToExponential(val, check)

   def test_toExponential(self):
      asrt = ('1e-8', '1.2e-8', '1.23e-8', '1.231e-8', '1.2315e-8',
              '1.23150e-8', '1.231500e-8', '1.2315000e-8', '1.23150000e-8',
              '1.231500000e-8', '1.2315000000e-8',
              '1.23149999999999997630e-8')
      self.assertToExponential(1.2315e-8, asrt)

      asrt = ('1e-7', '1.2e-7', '1.23e-7', '1.231e-7', '1.2315e-7',
              '1.23150e-7', '1.231500e-7', '1.2315000e-7', '1.23150000e-7',
              '1.231500000e-7', '1.2315000000e-7',
              '1.23149999999999987704e-7')
      self.assertToExponential(1.2315e-7, asrt)

      asrt = ('1e-6', '1.2e-6', '1.23e-6', '1.231e-6', '1.2315e-6',
              '1.23150e-6', '1.231500e-6', '1.2315000e-6', '1.23150000e-6',
              '1.231500000e-6', '1.2315000000e-6',
              '1.23149999999999998292e-6')
      self.assertToExponential(1.2315e-6, asrt)

      asrt = ('1e+2', '1.2e+2', '1.23e+2', '1.232e+2', '1.2315e+2',
              '1.23150e+2', '1.231500e+2', '1.2315000e+2', '1.23150000e+2',
              '1.231500000e+2', '1.2315000000e+2',
              '1.23150000000000005684e+2')
      self.assertToExponential(1.2315e2, asrt)

      asrt = ('1e+19', '1.2e+19', '1.23e+19', '1.232e+19', '1.2315e+19',
              '1.23150e+19', '1.231500e+19', '1.2315000e+19',
              '1.23150000e+19', '1.231500000e+19', '1.2315000000e+19',
              '1.23150000000000000000e+19')
      self.assertToExponential(1.2315e19, asrt)

      asrt = ('1e+20', '1.2e+20', '1.23e+20', '1.232e+20', '1.2315e+20',
              '1.23150e+20', '1.231500e+20', '1.2315000e+20',
              '1.23150000e+20', '1.231500000e+20', '1.2315000000e+20',
              '1.23150000000000000000e+20')
      self.assertToExponential(1.2315e20, asrt)

      asrt = ('1e+21', '1.2e+21', '1.23e+21', '1.232e+21', '1.2315e+21',
              '1.23150e+21', '1.231500e+21', '1.2315000e+21',
              '1.23150000e+21', '1.231500000e+21', '1.2315000000e+21',
              '1.23150000000000013107e+21')
      self.assertToExponential(1.2315e21, asrt)

      asrt = ('1e-8', '1.2e-8', '1.23e-8', '1.232e-8', '1.2316e-8',
              '1.23160e-8', '1.231599e-8', '1.2315988e-8', '1.23159877e-8',
              '1.231598765e-8', '1.2315987654e-8',
              '1.23159876543219883637e-8')
      self.assertToExponential(1.2315987654321987654321987654321987654321987654321987654321e-8, asrt)

      asrt = ('1e-7', '1.2e-7', '1.23e-7', '1.232e-7', '1.2316e-7',
              '1.23160e-7', '1.231599e-7', '1.2315988e-7', '1.23159877e-7',
              '1.231598765e-7', '1.2315987654e-7',
              '1.23159876543219883637e-7')
      self.assertToExponential(1.2315987654321987654321987654321987654321987654321987654321e-7, asrt)

      asrt = ('1e-6', '1.2e-6', '1.23e-6', '1.232e-6', '1.2316e-6',
              '1.23160e-6', '1.231599e-6', '1.2315988e-6', '1.23159877e-6',
              '1.231598765e-6', '1.2315987654e-6',
              '1.23159876543219883637e-6')
      self.assertToExponential(1.2315987654321987654321987654321987654321987654321987654321e-6, asrt)

      asrt = ('1e+2', '1.2e+2', '1.23e+2', '1.232e+2', '1.2316e+2',
              '1.23160e+2', '1.231599e+2', '1.2315988e+2', '1.23159877e+2',
              '1.231598765e+2', '1.2315987654e+2',
              '1.23159876543219880318e+2')
      self.assertToExponential(1.2315987654321987654321987654321987654321987654321987654321e2, asrt)

      asrt = ('1e+19', '1.2e+19', '1.23e+19', '1.232e+19', '1.2316e+19',
              '1.23160e+19', '1.231599e+19', '1.2315988e+19',
              '1.23159877e+19', '1.231598765e+19', '1.2315987654e+19',
              '1.23159876543219875840e+19')
      self.assertToExponential(1.2315987654321987654321987654321987654321987654321987654321e19, asrt)

      asrt = ('1e+20', '1.2e+20', '1.23e+20', '1.232e+20', '1.2316e+20',
              '1.23160e+20', '1.231599e+20', '1.2315988e+20',
              '1.23159877e+20', '1.231598765e+20', '1.2315987654e+20',
              '1.23159876543219875840e+20')
      self.assertToExponential(1.2315987654321987654321987654321987654321987654321987654321e20, asrt)

      asrt = ('1e+21', '1.2e+21', '1.23e+21', '1.232e+21', '1.2316e+21',
              '1.23160e+21', '1.231599e+21', '1.2315988e+21',
              '1.23159877e+21', '1.231598765e+21', '1.2315987654e+21',
              '1.23159876543219866010e+21')
      self.assertToExponential(1.2315987654321987654321987654321987654321987654321987654321e21, asrt)

   def assertToExponential2(self, value, check):
      val = Number(value)
      self.assertEqual(val.toExponential(0), check[0])
      self.assertEqual(val.toExponential(1), check[1])
      self.assertEqual(val.toExponential(2), check[2])
      self.assertEqual(val.toExponential(4), check[3])
      self.assertEqual(val.toExponential(10), check[4])
      self.assertEqual(val.toExponential(20), check[5])

   def test_toExponential2(self):
      asrt_0 = ('1e-15', '0.0e-16', '0.00e-16', '0.0000e-16',
                '0.0000000000e-16', '0.00000000000000000000e-16')
      self.assertToExponential2(0.0, asrt_0)
      self.assertToExponential2(-0.0, asrt_0)

      asrt_inf = ('Infinity', 'Infinity', 'Infinity', 'Infinity', 'Infinity',
                  'Infinity')
      self.assertToExponential2(Number.POSITIVE_INFINITY, asrt_inf)

      asrt_ninf = ('-Infinity', '-Infinity', '-Infinity', '-Infinity',
                   '-Infinity', '-Infinity')
      self.assertToExponential2(Number.NEGATIVE_INFINITY, asrt_ninf)

      asrt_nan = ('NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN')
      self.assertToExponential2(Number.NaN, asrt_nan)

   def assertToFixed(self, value, check):
      val = Number(value)
      self._assertToFixed(val, check)

   def test_toFixed(self):
      asrt = ('0', '0.0', '0.00', '0.000', '0.0000', '0.00000', '0.000000',
              '0.0000000', '0.00000001', '0.000000012', '0.0000000123',
              '0.00000001231500000000')
      self.assertToFixed(1.2315e-8, asrt)

      asrt = ('0', '0.0', '0.00', '0.000', '0.0000', '0.00000', '0.000000',
              '0.0000001', '0.00000012', '0.000000123', '0.0000001231',
              '0.00000012315000000000')
      self.assertToFixed(1.2315e-7, asrt)

      asrt = ('0', '0.0', '0.00', '0.000', '0.0000', '0.00000', '0.000001',
              '0.0000012', '0.00000123', '0.000001231', '0.0000012315',
              '0.00000123150000000000')
      self.assertToFixed(1.2315e-6, asrt)

      asrt = ('123', '123.2', '123.15', '123.150', '123.1500', '123.15000',
              '123.150000', '123.1500000', '123.15000000', '123.150000000',
              '123.1500000000', '123.15000000000000568434')
      self.assertToFixed(1.2315e2, asrt)

      asrt = ('12315000000000000000', '12315000000000000000.0',
              '12315000000000000000.00', '12315000000000000000.000',
              '12315000000000000000.0000', '12315000000000000000.00000',
              '12315000000000000000.000000', '12315000000000000000.0000000',
              '12315000000000000000.00000000',
              '12315000000000000000.000000000',
              '12315000000000000000.0000000000',
              '12315000000000000000.00000000000000000000')
      self.assertToFixed(1.2315e19, asrt)

      asrt = ('123150000000000000000', '123150000000000000000.0',
              '123150000000000000000.00', '123150000000000000000.000',
              '123150000000000000000.0000', '123150000000000000000.00000',
              '123150000000000000000.000000', '123150000000000000000.0000000',
              '123150000000000000000.00000000',
              '123150000000000000000.000000000',
              '123150000000000000000.0000000000',
              '123150000000000000000.00000000000000000000')
      self.assertToFixed(1.2315e20, asrt)

      asrt = ('1231500000000000131072', '1231500000000000131072.0',
              '1231500000000000131072.00', '1231500000000000131072.000',
              '1231500000000000131072.0000', '1231500000000000131072.00000',
              '1231500000000000131072.000000',
              '1231500000000000131072.0000000',
              '1231500000000000131072.00000000',
              '1231500000000000131072.000000000',
              '1231500000000000131072.0000000000',
              '1231500000000000131072.00000000000000000000')
      self.assertToFixed(1.2315e21, asrt)

      asrt = ('0', '0.0', '0.00', '0.000', '0.0000', '0.00000', '0.000000',
              '0.0000000', '0.00000001', '0.000000012', '0.0000000123',
              '0.00000001231598765432')
      self.assertToFixed(1.2315987654321987654321987654321987654321987654321987654321e-8, asrt)

      asrt = ('0', '0.0', '0.00', '0.000', '0.0000', '0.00000', '0.000000',
              '0.0000001', '0.00000012', '0.000000123', '0.0000001232',
              '0.00000012315987654322')
      self.assertToFixed(1.2315987654321987654321987654321987654321987654321987654321e-7, asrt)

      asrt = ('0', '0.0', '0.00', '0.000', '0.0000', '0.00000', '0.000001',
              '0.0000012', '0.00000123', '0.000001232', '0.0000012316',
              '0.00000123159876543220')
      self.assertToFixed(1.2315987654321987654321987654321987654321987654321987654321e-6, asrt)

      asrt = ('123', '123.2', '123.16', '123.160', '123.1599', '123.15988',
              '123.159877', '123.1598765', '123.15987654', '123.159876543',
              '123.1598765432', '123.15987654321988031825')
      self.assertToFixed(1.2315987654321987654321987654321987654321987654321987654321e2, asrt)

      asrt = ('12315987654321987584', '12315987654321987584.0',
              '12315987654321987584.00', '12315987654321987584.000',
              '12315987654321987584.0000', '12315987654321987584.00000',
              '12315987654321987584.000000', '12315987654321987584.0000000',
              '12315987654321987584.00000000',
              '12315987654321987584.000000000',
              '12315987654321987584.0000000000',
              '12315987654321987584.00000000000000000000')
      self.assertToFixed(1.2315987654321987654321987654321987654321987654321987654321e19, asrt)

      asrt = ('123159876543219875840', '123159876543219875840.0',
              '123159876543219875840.00', '123159876543219875840.000',
              '123159876543219875840.0000', '123159876543219875840.00000',
              '123159876543219875840.000000', '123159876543219875840.0000000',
              '123159876543219875840.00000000',
              '123159876543219875840.000000000',
              '123159876543219875840.0000000000',
              '123159876543219875840.00000000000000000000')
      self.assertToFixed(1.2315987654321987654321987654321987654321987654321987654321e20, asrt)

      asrt = ('1231598765432198660096', '1231598765432198660096.0',
              '1231598765432198660096.00', '1231598765432198660096.000',
              '1231598765432198660096.0000', '1231598765432198660096.00000',
              '1231598765432198660096.000000',
              '1231598765432198660096.0000000',
              '1231598765432198660096.00000000',
              '1231598765432198660096.000000000',
              '1231598765432198660096.0000000000',
              '1231598765432198660096.00000000000000000000')
      self.assertToFixed(1.2315987654321987654321987654321987654321987654321987654321e21, asrt)

   def assertToPrecision(self, value, check):
      val = Number(value)
      self._assertToPrecision(val, check)

   def test_toPrecision(self):
      asrt = ('0.00000001', '0.000000012', '0.0000000123', '0.00000001231',
              '0.000000012315', '0.000000012315', '0.000000012315',
              '0.000000012315', '0.000000012315', '0.000000012315',
              '0.000000012315', '0.000000012315')
      self.assertToPrecision(1.2315e-8, asrt)

      asrt = ('0.0000001', '0.00000012', '0.000000123', '0.0000001231',
              '0.00000012314', '0.000000123149', '0.0000001231499',
              '0.00000012314999', '0.000000123149999', '0.0000001231499999',
              '0.00000012315', '0.00000012315')
      self.assertToPrecision(1.2315e-7, asrt)

      asrt = ('0.000001', '0.0000012', '0.00000123', '0.000001231',
              '0.0000012315', '0.0000012315', '0.0000012315', '0.0000012315',
              '0.0000012315', '0.0000012315', '0.0000012315', '0.0000012315')
      self.assertToPrecision(1.2315e-6, asrt)

      asrt = ('1e+2', '1.2e+2', '123', '123.1', '123.15', '123.15', '123.15',
              '123.15', '123.15', '123.15', '123.15', '123.15')
      self.assertToPrecision(1.2315e2, asrt)

      asrt = ('1e+19', '1.2e+19', '1.23e+19', '1.231e+19', '1.2315e+19',
              '1.2315e+19', '1.2315e+19', '1.2315e+19', '1.23149999e+19',
              '1.2315e+19', '12315000000000000000', '12315000000000000000')
      self.assertToPrecision(1.2315e19, asrt)

      asrt = ('1e+20', '1.2e+20', '1.2299999999999998e+20',
              '1.2309999999999999e+20', '1.2315e+20',
              '1.2314999999999998e+20', '1.2315e+20', '1.2315e+20',
              '1.2315e+20', '1.2315e+20', '1.2315e+20',
              '123150000000000000000')
      self.assertToPrecision(1.2315e20, asrt)

      asrt = ('1.0000000000000002e+21', '1.2e+21', '1.23e+21', '1.231e+21',
              '1.2314999999999998e+21', '1.2315e+21',
              '1.2314999999999998e+21', '1.2315e+21',
              '1.2314999999999998e+21', '1.2315e+21', '1.2315e+21',
              '1.2315e+21')
      self.assertToPrecision(1.2315e21, asrt)

      asrt = ('0.00000001', '0.000000012', '0.0000000123', '0.00000001231',
              '0.000000012315', '0.0000000123159', '0.00000001231598',
              '0.000000012315987', '0.0000000123159876',
              '0.00000001231598765', '0.000000012315987654321987',
              '0.000000012315987654321988')
      self.assertToPrecision(1.2315987654321987654321987654321987654321987654321987654321e-8, asrt)

      asrt = ('0.0000001', '0.00000012', '0.000000123', '0.0000001231',
              '0.00000012315', '0.000000123159', '0.0000001231598',
              '0.00000012315987', '0.000000123159876', '0.0000001231598765',
              '0.00000012315987654321988', '0.00000012315987654321988')
      self.assertToPrecision(1.2315987654321987654321987654321987654321987654321987654321e-7, asrt)

      asrt = ('0.000001', '0.0000012', '0.00000123', '0.000001231',
              '0.0000012315', '0.00000123159', '0.000001231598',
              '0.0000012315987', '0.00000123159876', '0.000001231598765',
              '0.0000012315987654321988', '0.0000012315987654321988')
      self.assertToPrecision(1.2315987654321987654321987654321987654321987654321987654321e-6, asrt)

      asrt = ('1e+2', '1.2e+2', '123', '123.1', '123.15', '123.159',
              '123.1598', '123.15987', '123.159876', '123.1598765',
              '123.15987654321988', '123.15987654321988')
      self.assertToPrecision(1.2315987654321987654321987654321987654321987654321987654321e2, asrt)

      asrt = ('1e+19', '1.2e+19', '1.23e+19', '1.231e+19', '1.2315e+19',
              '1.23159e+19', '1.231598e+19', '1.2315987e+19',
              '1.23159876e+19', '1.231598765e+19', '12315987654321988000',
              '12315987654321988000')
      self.assertToPrecision(1.2315987654321987654321987654321987654321987654321987654321e19, asrt)

      asrt = ('1e+20', '1.2e+20', '1.2299999999999998e+20',
              '1.2309999999999999e+20', '1.2315e+20',
              '1.2315899999999997e+20', '1.231598e+20', '1.2315987e+20',
              '1.23159876e+20', '1.2315987650000002e+20',
              '1.2315987654321987e+20', '123159876543219880000')
      self.assertToPrecision(1.2315987654321987654321987654321987654321987654321987654321e20, asrt)

      asrt = ('1.0000000000000002e+21', '1.2e+21', '1.23e+21', '1.231e+21',
              '1.2314999999999998e+21', '1.23159e+21',
              '1.2315979999999997e+21', '1.2315987000000002e+21',
              '1.2315987599999998e+21', '1.231598765e+21',
              '1.2315987654321987e+21', '1.2315987654321987e+21')
      self.assertToPrecision(1.2315987654321987654321987654321987654321987654321987654321e21, asrt)

   def assertToString(self, value, check):
      val = Number(value)
      self._assertToString(val, check)

   def test_toString(self):
      asrt = ('0', '0', '0', '0', '0', '0', '0', '0', '1.2315e-8', '0', '0',
              '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
              '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
              1.2315e-8)
      self.assertToString(1.2315e-8, asrt)

      asrt = ('0', '0', '0', '0', '0', '0', '0', '0', '1.2315e-7', '0', '0',
              '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
              '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
              1.2315e-7)
      self.assertToString(1.2315e-7, asrt)

      asrt = ('0', '0', '0', '0', '0', '0', '0', '0', '0.0000012315', '0',
              '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
              '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
              0.0000012315)
      self.assertToString(1.2315e-6, asrt)

      asrt = ('1111011', '11120', '1323', '443', '323', '234', '173', '146',
              '123.15', '102', 'a3', '96', '8b', '83', '7b', '74', '6f', '69',
              '63', '5i', '5d', '58', '53', '4n', '4j', '4f', '4b', '47',
              '43', '3u', '3r', '3o', '3l', '3i', '3f', 123.15)
      self.assertToString(1.2315e2, asrt)

      asrt = ('1010101011100111101010110100000010011000111011111000000000000000',
              '10001001022011102101012221121002220002210',
              '22223213222310002120323320000000',
              '1311301203140000000000000000', '2333214230550124231304220',
              '31022401142454651666425', '1253475264023073700000',
              '101038142335847086053', '12315000000000000000',
              '224012757a2912a6a75', '567389253b42b1b840',
              '1567942a101958a619', '5923913645345288c', '1d1cae91584744150',
              'aae7ab4098ef8000', '452635769eaf283g', '1ef7847b999ac0gc',
              'f7g0igfei24i785', '7a6bge7a0000000', '3gf3hd0gbe9di3c',
              '1lblib801ca68kg', '119ll96f4cbhj44', 'e150d1bmd28k80',
              '86f73900000000', '4p17132e9de8km', '31184ba5pg3q53',
              '1p0p2ff9p2224c', '15nb3sji24sqdd', 'n55goh56nl4a0',
              'fjl36k1qhumf8', 'alptb82cev000', '7clnqlpb3ct3r',
              '55fg8hto8d2ag', '3mjap2hdf8gn5', '2lkaf5u8qji8c',
              12315000000000000000)
      self.assertToString(1.2315e19, asrt)

      asrt = ('1101010110100001100101100001000010111111001010110110000000000000000',
              '1010101111000122012210012110222002120011210',
              '1222310030230020113321112300000000',
              '31231024113300000000000000000', '41553452113422232123042220',
              '433324515215610435660401', '15264145410277126600000',
              '1111430565705428122523', '123150000000000000000',
              '20171149223631761636', '4761138053565374840',
              '1130c2319a1434a082c', '407886c671a51a0808',
              '13b374b0da7ecc8750', '6ad0cb085f95b0000', '2906ag35eda6f7eb7',
              '104a2a847555hg8ac', '82289hg5ga3bf4dc', '3f35i73f00000000',
              '1gk4h847ibiceihf', 'jh9k93e0feeiii6', 'ae7c70kdma2fc8h',
              '5kc25aen9anh880', '37g2l8f00000000', '1ngcib4pdh5d2ec',
              '13ad0h5l5cq32g3', 'iq8qpfdeqklg08', 'c01oapm6lkssle',
              '7llpi5lm7r1sa0', '51ap14eihos3qi', '3aq35ggnslm000',
              '27rj72jmc0te16', '1hkiqh8p4fsceo', '11fi25oxtcecwf',
              'pzmw7mefdfkwc', 123150000000000000000)
      self.assertToString(1.2315e20, asrt)

      asrt = ('10000101100001001111110111001010011101110111101100100000000000000000000',
              '102020212211020101010212000210200011210110122',
              '100230021332321103232331210000000000',
              '1130121032321000000000112323232',
              '1111522054041200134220240442', '6266555334142536334056660',
              '205411767123567544000000', '12225736333760720523538',
              '1.2315e+21', '191550344012796085161', '3a30b10844a745140488',
              'ac4949546a037942399', '2c5620cc91359366ca0',
              'c774d259204d8ca692', '42c27ee53bbd900000',
              '1853f78g7c02139f54', 'a29b7ea80gh586868', '4525947b1d6h63g8g',
              '1hbcj3bha0002cccc', 'i1d65j1fhdi1icde', '8lkb63e872eh2eec',
              '4e56818m1h9561g4', '2ad0m6a5hmdm0gg8', '181b3db00000g6hm',
              'j28n27nl6g3a4om', 'b6nm6a3n0li73jh', '6lb5h3en9fbkoc0',
              '440iblpj9e6p85g', '2h78g1r7cj0koc2', '1jdf2bdlun131jt',
              '11c4vn57eup0000', 'mcbr4pvpl916en', 'f61hr2jdamg8s4',
              'aef5lm4ndj8wf7', '77wcy4809qckc8', 1.2315e+21)
      self.assertToString(1.2315e21, asrt)

      asrt = ('0', '0', '0', '0', '0', '0', '0', '0', '1.2315987654321987e-8',
              '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
              '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
              1.2315987654321987e-8)
      self.assertToString(1.2315987654321987654321987654321987654321987654321987654321e-8, asrt)

      asrt = ('0', '0', '0', '0', '0', '0', '0', '0', '1.231598765432198e-7',
              '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
              '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
              1.231598765432198e-7)
      self.assertToString(1.2315987654321987654321987654321987654321987654321987654321e-7, asrt)

      asrt = ('0', '0', '0', '0', '0', '0', '0', '0',
              '0.0000012315987654321988', '0', '0', '0', '0', '0', '0', '0',
              '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
              '0', '0', '0', '0', '0', '0', 0.0000012315987654321988)
      self.assertToString(1.2315987654321987654321987654321987654321987654321987654321e-6, asrt)

      asrt = ('1111011', '11120', '1323', '443', '323', '234', '173', '146',
              '123.15987654321988', '102', 'a3', '96', '8b', '83', '7b', '74',
              '6f', '69', '63', '5i', '5d', '58', '53', '4n', '4j', '4f',
              '4b', '47', '43', '3u', '3r', '3o', '3l', '3i', '3f',
              123.15987654321988)
      self.assertToString(1.2315987654321987654321987654321987654321987654321987654321e2, asrt)

      asrt = ('1010101011101011001011011000010011001001111101010110000000000000',
              '10001001110221221101001101110000200001002',
              '22223223023120103021331112000000',
              '1311303222113212022412104324', '2333232051312212521302002',
              '31023116160233530433244', '1253531330231175260000',
              '101043857331343020038', '12315987654321988000',
              '2240393243114a33193', '56745bb85b79034008',
              '1567c77b454a8a4340', '5924c71d0728c6424', '1d1d38bc7d4244abe',
              'aaeb2d84c9f56000', '4527f25e6ag94ed2', '1ef85b0dbdh80068',
              'f7g98ia644gi908', '7a6gd37eifc8884', '3gf6dha8g890f9b',
              '1lc1bf9l9071eae', '119mm5ee1g7c09l', 'e15g2m0h4l5008',
              '86fhc6h72e75d9', '4p1e10ga332420', '311cppa1ac0gmq',
              '1p10bpl7jelm84', '15nde20aa2qq46', 'n576trc7h4ase',
              'fjm9hk95jtiid', 'alqpdgj4vao00', '7cmc2u3j7ppse',
              '55fwhjx3nwcw2', '3mjn8n7gfpxn4', '2lkk598dhdic8',
              12315987654321988000)
      self.assertToString(1.2315987654321987654321987654321987654321987654321987654321e19, asrt)

      asrt = ('1101010110100101111110001110010111111100011100101011100000000000000',
              '1010101112210121101201111212110012111202222',
              '1222310233301302333203211130000000',
              '31231114442314241003242031430', '41554133243215424542404242',
              '433333546443402526341245', '15264576162774345340000',
              '1111483541644773220118', '123159876543219880000',
              '2017354a1990353a7a78', '47618bb90b856298888',
              '113118b0951929ccc10', '40796d15451c4c842c',
              '13b3c5cd53cb7deb35', '6ad2fc72fe395c000', '2907af677f7c780b3',
              '104ab227a9dc80ge8', '822cide854ahdei4', '3f386bdh97g444c0',
              '1gk63c6k3h066025', 'jhaf70bg234g8k8', 'ae7mfa82h265083',
              '5kc8h54740k18g8', '37g6omgml0hl1of', '1ngfaa67n54lgk0',
              '13aelgajdnc7i4h', 'iqa475gkr7m88c', 'c02iok3ge087n2',
              '7lmc9t42fldeok', '51b62lgtpdgld6', '3aqbu75vhpbg00',
              '27rplt42rbqbs8', '1hknj5tp31i0ek', '11flmgm4ohen85',
              'pzplgkbqtr4g8', 123159876543219880000)
      self.assertToString(1.2315987654321987654321987654321987654321987654321987654321e20, asrt)

      asrt = ('10000101100001111011101110001111101111011100011110110000000000000000000',
              '102020220111000001222020010200112122010012202',
              '100230033131301331323203312000000000',
              '1130122344401340320120440123421',
              '1111530354333513241320044202', '6300003103430536511040465',
              '205417356175734366000000', '12226430058203615627382',
              '1.231598765432198e+21', '191571a527a2319792946',
              '3a3155b9699072348808', 'ac4b3a672c4118108a2',
              '2c56ad4db194b7208ac', 'c7783d8d787a3c6c7b',
              '42c3ddc7dee3d80000', '1854870d6b1954e713', 'a29g3363f7ag82c42',
              '4527fg4b6e7e717h4', '1hbe35giedi22c48g', 'i1djei6ch22k2h95',
              '8lkil4576la4eg26', '4e5ajgbc49mg4d95', '2ad3f43ing88g808',
              '181cjo1j3a74k2bl', 'j29npob0npm02i2', 'b6od01q63ieaphb',
              '6lbhefrrdkm0gcc', '440qeer6jo2k02q', '2h7e39lap74ciqq',
              '1jditqtej6b3h2q', '11c7ne7rrhtg000', 'mcdpkr7s9j29gh',
              'f62vlopcuf66qk', 'aeg6eqbbyy2t1q', '77x3yln9g9gckk',
              1.231598765432198e+21)
      self.assertToString(1.2315987654321987654321987654321987654321987654321987654321e21, asrt)


class ObjectTests(as3libTestCase):
   def assertEnumerate(self, obj1, check):
      out = Array()
      for name in obj1:
         out.push('%s = %s' % (name, obj1[name]))

      out.sort()
      self.assertEqual(out.toString(), check)

   def test_enumeration(self):
      x = Object()
      x.key = 'value'
      x.key2 = 'value2'
      self.assertEnumerate(x, 'key = value,key2 = value2')

      # delete key2
      delete(x['key2'])
      self.assertEnumerate(x, 'key = value')

      # other objects
      self.assertEnumerate(Object(), '')
      self.assertEnumerate(null, '')
      self.assertEnumerate(undefined, '')

   def test_prototype(self):
      obj = Object

      self.assertFalse(obj.hasOwnProperty('toString'))
      self.assertTrue(obj.prototype.hasOwnProperty('toString'))

      temp = Object.prototype.toString
      o = obj()
      self.assertEqual(o.toString(), '[object Object]')
      Object.prototype.toString = lambda: 'Custom toString'
      self.assertEqual(o.toString(), 'Custom toString')

      Object.prototype.toString = temp

   def test_toLocaleString(self):
      o = Object()
      self.assertEqual(o.toLocaleString(), '[object Object]')

   def test_toString(self):
      o = Object()
      self.assertEqual(o.toString(), '[object Object]')

   def test_valueOf(self):
      obj = Object()
      self.assertIs(obj.valueOf(), obj)


class OperationTests(as3libTestCase):
   def assertAdd(self, value, equals):
      self.assertEqual(true + value, check[0])
      self.assertEqual(false + value, check[1])
      self.assertEqual(null + value, check[2])
      self.assertEqual(undefined + value, check[3])
      self.assertEqual(String('') + value, check[4])
      self.assertEqual(String('str') + value, check[5])
      self.assertEqual(String('true') + value, check[6])
      self.assertEqual(String('false') + value, check[7])
      self.assertEqual(Number(0.0) + value, check[8])
      self.assertEqual(NaN + value, check[9])
      self.assertEqual(Number(-0.0) + value, check[10])
      self.assertEqual(Infinity + value, check[11])
      self.assertEqual(Number(1.0) + value, check[12])
      self.assertEqual(Number(-1.0) + value, check[13])
      self.assertEqual(Number(0xFF1306) + value, check[14])
      self.assertEqual(Object() + value, check[15])
      self.assertEqual(String('0.0') + value, check[16])
      self.assertEqual(String('NaN') + value, check[17])
      self.assertEqual(String('-0.0') + value, check[18])
      self.assertEqual(String('Infinity') + value, check[19])
      self.assertEqual(String('1.0') + value, check[20])
      self.assertEqual(String('-1.0') + value, check[21])
      self.assertEqual(String('0xFF1306') + value, check[22])

   def test_add(self):
      asrt_true = (2, 1, 1, NaN, 'true', 'strtrue', 'truetrue', 'falsetrue',
                   1, NaN, 1, Infinity, 2, 0, 16716551, '[object Object]true',
                   '0.0true', 'NaNtrue', '-0.0true', 'Infinitytrue',
                   '1.0true', '-1.0true', '0xFF1306true')
      self.assertAdd(true, asrt_true)

      asrt_false = (1, 0, 0, NaN, 'false', 'strfalse', 'truefalse',
                    'falsefalse', 0, NaN, 0, Infinity, 1, -1, 16716550,
                    '[object Object]false', '0.0false', 'NaNfalse',
                    '-0.0false', 'Infinityfalse', '1.0false', '-1.0false',
                    '0xFF1306false')
      self.assertAdd(false, asrt_false)

      asrt_null = (1, 0, 0, NaN, 'null', 'strnull', 'truenull', 'falsenull',
                   0, NaN, 0, Infinity, 1, -1, 16716550,
                   '[object Object]null', '0.0null', 'NaNnull', '-0.0null',
                   'Infinitynull', '1.0null', '-1.0null', '0xFF1306null')
      self.assertAdd(null, asrt_null)

      asrt_undefined = (NaN, NaN, NaN, NaN, 'undefined', 'strundefined',
                        'trueundefined', 'falseundefined', NaN, NaN, NaN, NaN,
                        NaN, NaN, NaN, '[object Object]undefined',
                        '0.0undefined', 'NaNundefined', '-0.0undefined',
                        'Infinityundefined', '1.0undefined', '-1.0undefined',
                        '0xFF1306undefined')
      self.assertAdd(undefined, asrt_undefined)

      raise TestNotImplemented

      self.assertAdd(String(''), asrt_0)
      self.assertAdd(String('str'), asrt_0)
      self.assertAdd(String('true'), asrt_0)
      self.assertAdd(String('false'), asrt_0)
      self.assertAdd(Number(0.0), asrt_0)
      self.assertAdd(NaN, asrt_0)
      self.assertAdd(Number(-0.0), asrt_0)
      self.assertAdd(Infinity, asrt_0)
      self.assertAdd(Number(1.0), asrt_1)

      self.assertAdd(Number(-1.0), asrt_n1)

      self.assertAdd(Number(0xFF1306), asrt_16716550)

      self.assertAdd(Object(), asrt_0)
      self.assertAdd(String('0.0'), asrt_0)
      self.assertAdd(String('NaN'), asrt_0)
      self.assertAdd(String('-0.0'), asrt_0)
      self.assertAdd(String('Infinity'), asrt_0)
      self.assertAdd(String('1.0'), asrt_1)

      self.assertAdd(String('-1.0'), asrt_n1)

      self.assertAdd(String('0xFF1306'), asrt_16716550)

   def assertSubtract(self, value1, value2, equals):
      self.assertEquals(value1 + value2, equals)

   def test_subtract(self):
      raise TestNotImplemented

   def assertDivide(self, value1, value2, equals):
      self.assertEqual(value1 / value2, equals)

   def assertDivideNaN(self, value1, value2):
      self.assertNaN(value1 / value2)

   def test_divide(self):
      # TODO: Add more of this test
      self.assertDivide(true, true, 1)
      self.assertDivide(false, true, 0)
      self.assertDivide(null, true, 0)
      self.assertDivideNaN(undefined, true)
      self.assertDivide(String(''), true, 0)
      self.assertDivideNaN(String('str'), true)
      self.assertDivideNaN(String('true'), true)
      self.assertDivideNaN(String('false'), true)
      self.assertDivide(Number(0.0), true, 0)
      self.assertDivideNaN(NaN, true)
      self.assertDivide(Number(-0.0), true, 0)
      self.assertDivide(Infinity, true, Infinity)
      self.assertDivide(Number(1.0), true, 1)
      self.assertDivide(Number(-1.0), true, -1)

   def assertLShift(self, value, check):
      self.assertEqual(true << value, check[0])
      self.assertEqual(false << value, check[1])
      self.assertEqual(null << value, check[2])
      self.assertEqual(undefined << value, check[3])
      self.assertEqual(String('') << value, check[4])
      self.assertEqual(String('str') << value, check[5])
      self.assertEqual(String('true') << value, check[6])
      self.assertEqual(String('false') << value, check[7])
      self.assertEqual(Number(0.0) << value, check[8])
      self.assertEqual(NaN << value, check[9])
      self.assertEqual(Number(-0.0) << value, check[10])
      self.assertEqual(Infinity << value, check[11])
      self.assertEqual(Number(1.0) << value, check[12])
      self.assertEqual(Number(-1.0) << value, check[13])
      self.assertEqual(Number(0xFF1306) << value, check[14])
      self.assertEqual(Object() << value, check[15])
      self.assertEqual(String('0.0') << value, check[16])
      self.assertEqual(String('NaN') << value, check[17])
      self.assertEqual(String('-0.0') << value, check[18])
      self.assertEqual(String('Infinity') << value, check[19])
      self.assertEqual(String('1.0') << value, check[20])
      self.assertEqual(String('-1.0') << value, check[21])
      self.assertEqual(String('0xFF1306') << value, check[22])

   def test_lshift(self):
      asrt_1 = (2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, -2, 33433100, 0, 0, 0,
                0, 0, 2, -2, 33433100)

      asrt_0 = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 16716550, 0, 0, 0,
                0, 0, 1, -1, 16716550)

      asrt_n1 = (-2147483648, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2147483648,
                 -2147483648, 0, 0, 0, 0, 0, 0, -2147483648, -2147483648, 0)

      asrt_16716550 = (64, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 64, -64,
                       1069859200, 0, 0, 0, 0, 0, 64, -64, 1069859200)

      self.assertLShift(true, asrt_1)

      self.assertLShift(false, asrt_0)
      self.assertLShift(null, asrt_0)
      self.assertLShift(undefined, asrt_0)
      self.assertLShift(String(''), asrt_0)
      self.assertLShift(String('str'), asrt_0)
      self.assertLShift(String('true'), asrt_0)
      self.assertLShift(String('false'), asrt_0)
      self.assertLShift(Number(0.0), asrt_0)
      self.assertLShift(NaN, asrt_0)
      self.assertLShift(Number(-0.0), asrt_0)
      self.assertLShift(Infinity, asrt_0)
      self.assertLShift(Number(1.0), asrt_1)

      self.assertLShift(Number(-1.0), asrt_n1)

      self.assertLShift(Number(0xFF1306), asrt_16716550)

      self.assertLShift(Object(), asrt_0)
      self.assertLShift(String('0.0'), asrt_0)
      self.assertLShift(String('NaN'), asrt_0)
      self.assertLShift(String('-0.0'), asrt_0)
      self.assertLShift(String('Infinity'), asrt_0)
      self.assertLShift(String('1.0'), asrt_1)

      self.assertLShift(String('-1.0'), asrt_n1)

      self.assertLShift(String('0xFF1306'), asrt_16716550)

   def assertRShift(self, value, check):
      self.assertEqual(true >> value, check[0])
      self.assertEqual(false >> value, check[1])
      self.assertEqual(null >> value, check[2])
      self.assertEqual(undefined >> value, check[3])
      self.assertEqual(String('') >> value, check[4])
      self.assertEqual(String('str') >> value, check[5])
      self.assertEqual(String('true') >> value, check[6])
      self.assertEqual(String('false') >> value, check[7])
      self.assertEqual(Number(0.0) >> value, check[8])
      self.assertEqual(NaN >> value, check[9])
      self.assertEqual(Number(-0.0) >> value, check[10])
      self.assertEqual(Infinity >> value, check[11])
      self.assertEqual(Number(1.0) >> value, check[12])
      self.assertEqual(Number(-1.0) >> value, check[13])
      self.assertEqual(Number(0xFF1306) >> value, check[14])
      self.assertEqual(Object() >> value, check[15])
      self.assertEqual(String('0.0') >> value, check[16])
      self.assertEqual(String('NaN') >> value, check[17])
      self.assertEqual(String('-0.0') >> value, check[18])
      self.assertEqual(String('Infinity') >> value, check[19])
      self.assertEqual(String('1.0') >> value, check[20])
      self.assertEqual(String('-1.0') >> value, check[21])
      self.assertEqual(String('0xFF1306') >> value, check[22])

   def test_rshift(self):
      asrt_1 = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 8358275, 0, 0, 0,
                0, 0, 0, -1, 8358275)

      asrt_0 = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 16716550, 0, 0, 0,
                0, 0, 1, -1, 16716550)

      asrt_n1 = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0,
                 0, -1, 0)

      asrt_16716550 = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 261196, 0,
                       0, 0, 0, 0, 0, -1, 261196)

      self.assertRShift(true, asrt_1)

      self.assertRShift(false, asrt_0)
      self.assertRShift(null, asrt_0)
      self.assertRShift(undefined, asrt_0)
      self.assertRShift(String(''), asrt_0)
      self.assertRShift(String('str'), asrt_0)
      self.assertRShift(String('true'), asrt_0)
      self.assertRShift(String('false'), asrt_0)
      self.assertRShift(Number(0.0), asrt_0)
      self.assertRShift(NaN, asrt_0)
      self.assertRShift(Number(-0.0), asrt_0)
      self.assertRShift(Infinity, asrt_0)
      self.assertRShift(Number(1.0), asrt_1)

      self.assertRShift(Number(-1.0), asrt_n1)

      self.assertRShift(Number(0xFF1306), asrt_16716550)

      self.assertRShift(Object(), asrt_0)
      self.assertRShift(String('0.0'), asrt_0)
      self.assertRShift(String('NaN'), asrt_0)
      self.assertRShift(String('-0.0'), asrt_0)
      self.assertRShift(String('Infinity'), asrt_0)
      self.assertRShift(String('1.0'), asrt_1)

      self.assertRShift(String('-1.0'), asrt_n1)

      self.assertRShift(String('0xFF1306'), asrt_16716550)

   def test_negate(self):
      self.assertEqual(-true, -1)
      self.assertEqual(-false, 0)
      self.assertEqual(-null, 0)
      self.assertNaN(-undefined)
      self.assertEqual(-String(''), 0)
      self.assertNaN(-String('str'))
      self.assertNaN(-String('true'))
      self.assertNaN(-String('false'))
      self.assertEqual(-Number(0.0), 0)
      self.assertNaN(-NaN)
      self.assertEqual(--Number(0.0), 0)
      self.assertEqual(-Infinity, as3lib.NInfinity)
      self.assertEqual(-Number(1.0), as3lib.Int(-1))
      self.assertEqual(--Number(1.0), as3lib.Int(1))
      self.assertNaN(-Object())

   def test_equals(self):
      raise TestNotImplemented

   def test_greaterequals(self):
      raise TestNotImplemented

   def test_greaterthan(self):
      raise TestNotImplemented

   def test_lessequals(self):
      raise TestNotImplemented

   def test_lessthan(self):
      raise TestNotImplemented

   def test_ifeq(self):
      # TODO: Make these use if statements
      self.assertEqual(as3lib.Int(2), String('2'))
      self.assertEqual(as3lib.Int(2), as3lib.Int(2))
      self.assertNotEqual(as3lib.Int(2), as3lib.Int(5))
      self.assertEqual(true, true)
      self.assertEqual(false, false)
      self.assertEqual(true, false)
      self.assertEqual(as3lib.Int(1), true)
      self.assertEqual(as3lib.Int(0), false)
      self.assertEqual(String('abc'), String('abc'))
      self.assertNotEqual(as3lib.Int(0), undefined)
      self.assertEqual(undefined, undefined)
      self.assertNotEqual(NaN, NaN)
      self.assertNotEqual(undefined, NaN)
      self.assertNotEqual(as3lib.Int(0), null)
      self.assertEqual(null, null)
      self.assertEqual(undefined, null)
      self.assertNotEqual(NaN, null)

   def test_ifgt(self):
      raise TestNotImplemented

   def test_ifgte(self):
      raise TestNotImplemented

   def test_iflt(self):
      raise TestNotImplemented

   def test_iflte(self):
      raise TestNotImplemented

   def test_ifne(self):
      raise TestNotImplemented

   def test_ifstricteq(self):
      # NOTE: These probably won't work
      self.assertIsNot(as3lib.Int(2), String('2'))
      self.assertIs(as3lib.Int(2), as3lib.Int(2))
      self.assertIsNot(as3lib.Int(2), as3lib.Int(5))
      self.assertIs(true, true)
      self.assertIs(false, false)
      self.assertIs(true, false)
      self.assertIsNot(as3lib.Int(1), true)
      self.assertIsNot(as3lib.Int(0), false)
      self.assertIs(String('abc'), String('abc'))
      self.assertIsNot(as3lib.Int(0), undefined)
      self.assertIs(undefined, undefined)
      self.assertIs(NaN, NaN)
      self.assertIsNot(undefined, NaN)
      self.assertIsNot(as3lib.Int(0), null)
      self.assertIs(null, null)
      self.assertIsNot(undefined, null)
      self.assertIsNot(NaN, null)

   def test_ifstrictne(self):
      raise TestNotImplemented

   def test_in(self):
      raise TestNotImplemented


class QNameTests(as3libTestCase):
   def test_constructor(self):
      # TODO: Verify what uri is supposed to be here
      qname_public = QName('name')
      self.assertQName(qname_public, 'name', null)

      qname_scoped = QName('https://ruffle.rs/AS3/tests/qname', 'name')
      self.assertQName(qname_scoped, 'name', 'https://ruffle.rs/AS3/tests/qname')

      qname_rescoped = QName('https://ruffle.rs/AS3/tests/qname/2', qname_scoped)
      self.assertQName(qname_rescoped, 'name', 'https://ruffle.rs/AS3/tests/qname/2')

      qname_clone = QName(qname_scoped)
      self.assertQName(qname_clone, 'name', 'https://ruffle.rs/AS3/tests/qname')

      # TODO: Check if null is supposed to be a string in assert here
      qname_null = QName(null, 'name')
      self.assertQName(qname_null, 'name', null)

      qname_any = QName('*')
      self.assertQName(qname_any, '*', null)
      self.assertEqual(qname_any.toString(), '*::*')

   def test_constructor_namespace(self):
      ns_public = Namespace('')

      qname_public = QName(ns_public, 'name')
      self.assertQName(qname_public, 'name', '')

      ns_ruffle = Namespace('https://ruffle.rs/AS3/tests/qname')

      qname_scoped = QName(ns_ruffle, 'name')
      self.assertQName(qname_scoped, 'name', 'https://ruffle.rs/AS3/tests/qname')

      qname_rescoped = QName(ns_ruffle, qname_public)
      self.assertQName(qname_rescoped, 'name', 'https://ruffle.rs/AS3/tests/qname')

      qname_any_name = QName(ns_ruffle, '*')
      self.assertQName(qname_any_name, '*', 'https://ruffle.rs/AS3/tests/qname')
      self.assertEqual(qname_any_name.toString(), 'https://ruffle.rs/AS3/tests/qname::*')

   def test_enumeration(self):
      q = QName("http://someuri", "foo")
      self.assertIter(q, ['uri', 'localName'])
      self.assertEach(q, ['foo', 'http://someuri'])

      q = QName("bar")
      self.assertIter(q, ['uri', 'localName'])

      # TODO: Verify actual return value here. '' is a placeholder
      self.assertEach(q, ['bar', ''])

   def test_indexing(self):
      raise TestNotImplemented

   def assertQNameToString(self, qname, string):
      # TODO: Prototype
      self.assertEqual(qname.toString(), string)
      # self.assertEqual(Object.prototype.toString.call(qname), '[object QName]')

   def test_toString(self):
      qname_public = QName('name')
      self.assertQNameToString(qname_public, 'name')

      qname_scoped = QName('https://ruffle.rs/AS3/tests/qname', 'name')
      self.assertQNameToString(qname_scoped, 'https://ruffle.rs/AS3/tests/qname::name')

      qname_rescoped = QName('https://ruffle.rs/AS3/tests/qname/2', qname_scoped)
      self.assertQNameToString(qname_rescoped, 'https://ruffle.rs/AS3/tests/qname/2::name')

      qname_clone = QName(qname_scoped)
      self.assertQNameToString(qname_clone, 'https://ruffle.rs/AS3/tests/qname::name')

      qname_null = QName(null, 'name')
      self.assertQNameToString(qname_null, '*::name')

   def assertQNameValueOf(self, qname, check):
      # TODO: Prototype
      self.assertEqual(str(qname.valueOf()), check)
      # self.assertEqual(str(Object.prototype.valueOf.call(qname)), check)

   def test_valueOf(self):
      qname_public = QName('name')
      self.assertQNameValueOf(qname_public, 'name')
      self.assertEqual(qname_public.valueOf().localName, 'name')
      self.assertEqual(Object.prototype.valueOf.call(qname_public).localName, 'name')

      qname_scoped = QName('https://ruffle.rs/AS3/tests/qname', 'name')
      self.assertQNameValueOf(qname_scoped, 'https://ruffle.rs/AS3/tests/qname::name')

      qname_rescoped = QName('https://ruffle.rs/AS3/tests/qname/2', qname_scoped)
      self.assertQNameValueOf(qname_rescoped, 'https://ruffle.rs/AS3/tests/qname/2::name')

      qname_clone = QName(qname_scoped)
      self.assertQNameValueOf(qname_clone, 'https://ruffle.rs/AS3/tests/qname::name')

      qname_null = QName(null, 'name')
      self.assertQNameValueOf(qname_null, '*::name')


class RegExpTests(as3libTestCase):
   def assertRegExp(self, re, source, toString, sourceEqual=True, s=False, x=False, g=False,
                    i=False, m=False):
      self.assertEqual(re.toString(), toString)
      if sourceEqual:
         self.assertEqual(re.source, source)
      else:
         self.assertNotEqual(re.source, source)
      self.assertEqual(re.dotall, s)
      self.assertEqual(re.extended, x)
      self.assertEqual(re.global_, g)
      self.assertEqual(re.ignoreCase, i)
      self.assertEqual(re.multiline, m)

   def test_constructor(self):
      re = RegExp()
      self.assertRegExp(re, '', '//')

      def test(source, flags, *args, **kwargs):
         self.assertRegExp(RegExp(source, flags), source, *args, **kwargs)

      test('empty flags', '', '/empty flags/')
      test('dotall flag', 's', '/dotall flag/s', s=True)
      test('extended flag', 'x', '/extended flag/x', x=True)
      test('global flag', 'g', '/global flag/g', g=True)
      test('ignoreCase flag', 'i', '/ignoreCase flag/i', i=True)
      test('multiline flag', 'm', '/multiline flag/m', m=True)
      test('all flags', 'sxgim', '/all flags/gimsx', True, True, True, True,
           True, True)

      test('invalid flags', '|%?-/.あa', '/invalid flags/')
      test('uppercase flags', 'SXGIM', '/uppercase flags/')
      test('duplicate flags', 'ssgg', '/duplicate flags/gs', s=True, g=True)

      test(undefined, undefined, '//', False)
      test(null, null, '/null/', False)
      test(RegExp('#((.*))$', 'm'), undefined, '/#((.*))$/m', False, m=True)
      test(RegExp('empty flags'), undefined, '/empty flags/', False)
      test(RegExp('dotall embedded flags', 's'), undefined,
           '/dotall embedded flags/s', False, s=True)
      self.assertRaisesAS3(TypeError,
                           1100,
                           'Cannot supply flags when constructing one RegExp from another',
                           test,
                           RegExp('/empty string separate flag/', 's'),
                           '')
      self.assertRaisesAS3(TypeError,
                           1100,
                           'Cannot supply flags when constructing one RegExp from another',
                           test,
                           RegExp('/dotall separate flags/', 's'),
                           's')

   def test_exec(self):
      re = RegExp('')
      self.assertArray(re.exec(''), [])

      re = RegExp(r'\d+')
      self.assertEqual(re.exec('abc'), null)

      # TODO: For some reason /\d+/ and RegExp('\d+') work differently
      re = RegExp(r'\d+')
      self.assertArray(re.exec('abc123'), ['123'])

      re = RegExp('ABC', 'i')
      self.assertArray(re.exec('abc'), ['abc'])

      re = RegExp('.bar', 's')
      self.assertArray(re.exec('foo\nbar'), ['\nbar'])

      # Test global and lastIndex
      re = RegExp(r'(\w*)sh(\w*)', 'ig')
      INPUT = 'She sells seashells by the seashore'
      result = re.exec(INPUT)
      self.assertArray(result, ['She', '', 'e'])
      self.assertEqual(result.input, INPUT)
      self.assertEqual(result.index, 0)
      self.assertEqual(result.lastIndex, 3)

      result = re.exec(INPUT)
      self.assertArray(result, ['seashells', 'sea', 'ells'])
      self.assertEqual(result.input, INPUT)
      self.assertEqual(result.index, 10)
      self.assertEqual(result.lastIndex, 19)

   def assertExtended(self, url, proto, host, port, path, query):
      regexp = RegExp(r'(?#comment) ((?P<protocol>[a-zA-Z]+: \/\/) (?P<host>[^:\/]*) (:(?P<port>\d+))?)? (?P<path>[^?]*)? ((?P<query>.*))? ', 'x')
      match = regexp.exec(url)
      #trace("match: " + match)
      self.assertEqual(match['protocol'], proto)
      self.assertEqual(match['host'], host)
      self.assertEqual(match['port'], port)
      self.assertEqual(match['path'], path)
      self.assertEqual(match['query'], query)

   def test_extended(self):
      self.assertExtended('', undefined, undefined, undefined, undefined, undefined)
      self.assertExtended('http://', 'http://', undefined, undefined, undefined, undefined)
      self.assertExtended('http://example.org', 'http://', 'example.org', undefined,
                          undefined, undefined)
      self.assertExtended('http://example.org/abc', 'http://', 'example.org',
                          undefined, '/abc', undefined)
      self.assertExtended('http://example.org:80/abc', 'http://',
                          'example.org', '80', '/abc', undefined)
      self.assertExtended('http://example.org/abc?hey', 'http://',
                          'example.org', undefined, '/abc', '?hey')

   def test_multiargs(self):
      re = RegExp('multiar', 'gs', 'a78w', Object(), null, Number(6667))
      self.assertEqual(re.toString(), '/multiar/gs')

   def test_test(self):
      self.assertTrue(RegExp('').test(''))
      self.assertTrue(RegExp('').test('abc'))
      self.assertFalse(RegExp(r'\d+').test('abc'))

      self.assertTrue(RegExp(r'\d+').test('abc 123'))

      self.assertFalse(RegExp('ABC').test('abc'))

      self.assertTrue(RegExp('ABC', 'i').test('abc'))

      self.assertFalse(RegExp('a.b').test('a\nb'))

      self.assertTrue(RegExp('a.b', 's').test('a\nb'))

      self.assertFalse(RegExp('^bar').test('foo\nbar'))

      self.assertTrue(RegExp('^bar', 'm').test('foo\nbar'))

      # global flag
      re = RegExp('[0-9]{3}', 'g')
      self.assertEqual(re.lastIndex, 0)
      self.assertTrue(re.test('0123456789'))
      self.assertEqual(re.lastIndex, 3)

   def test_toString(self):
      # TODO: Prototype
      re = RegExp('abc', 'xsmig')
      self.assertEqual(re.toString(), '/abc/gimsx')
      raise MethodNotImplemented('prototype')
      # self.assertEqual(RegExp.prototype.toString.call(re), '/abc/gimsx')
      # self.assertEqual(Object.prototype.toString.call(re), '[object, RegExp]')
      # self.assertRaisesAS3(TypeError,
      #                     1034,
      #                     'Type Coercion failed: cannot convert Object@00000000000 to RegExp.',
      #                     test,
      #                     RegExp.prototype.toString.call,
      #                     Object())


class StringTests(as3libTestCase):
   def assertCall(self, str, add, check):
      self.assertEqual(String(str) + add, check)

   def test_call(self):
      cls = String
      self.assertCall('cls(): ', cls(), 'cls(): ')

      self.assertCall('String(undefined): ', String(undefined), 'String(undefined): undefined')
      self.assertCall('String(null): ', String(null), 'String(null): null')
      self.assertCall('String(42): ', String(42), 'String(42): 42')
      self.assertCall('String(false): ', String(false), 'String(false): false')
      self.assertCall('String("abc"): ', String('abc'), 'String("abc"): abc')
      self.assertCall('String({}): ', String(Object()), 'String({}): [object Object]')

      self.assertCall('String(undefined).split(""): ', String(undefined).split(''), 'String(undefined).split(""): u,n,d,e,f,i,n,e,d')
      self.assertCall('String(null).split(""): ', String(null).split(''), 'String(null).split(""): n,u,l,l')
      self.assertCall('String(42).split(""): ', String(42).split(''), 'String(42).split(""): 4,2')
      self.assertCall('String(false).split(""): ', String(false).split(''), 'String(false).split(""): f,a,l,s,e')
      self.assertCall('String("abc").split(""): ', String('abc').split(''), 'String("abc").split(""): a,b,c')
      self.assertCall('String({}).split(""): ', String(Object()).split(''), 'String({}).split(""): [,o,b,j,e,c,t, ,O,b,j,e,c,t,]')

   def test_case(self):
      allUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞĀĂĄĆĈĊČĎĐĒĔĖĘĚĜĞĠĢĤĦĨĪĬĮİĲĴĶĹĻĽĿŁŃŅŇŊŌŎŐŒŔŖŘŚŜŞŠŢŤŦŨŪŬŮŰŲŴŶŸŹŻŽƁƂƄƆƇƉƊƋƎƏƐƑƓƔƖƗƘƜƝƟƠƢƤƦƧƩƬƮƯƱƲƳƵƷƸƼǄǅǇǈǊǋǍǏǑǓǕǗǙǛǞǠǢǤǦǨǪǬǮǱǲǴǶǷǸǺǼǾȀȂȄȆȈȊȌȎȐȒȔȖȘȚȜȞȢȤȦȨȪȬȮȰȲΆΈΉΊΌΎΏΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡ΢ΣΤΥΦΧΨΩΪΫϘϚϜϞϠϢϤϦϨϪϬϮϴЀЁЂЃЄЅІЇЈЉЊЋЌЍЎЏАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯѠѢѤѦѨѪѬѮѰѲѴѶѸѺѼѾҀҊҌҎҐҒҔҖҘҚҜҞҠҢҤҦҨҪҬҮҰҲҴҶҸҺҼҾӁӃӇӋӐӒӔӖӘӚӜӞӠӢӤӦӨӪӬӮӰӲӴӶӸԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖႠႡႢႣႤႥႦႧႨႩႪႫႬႭႮႯႰႱႲႳႴႵႶႷႸႹႺႻႼႽႾႿჀჁჂჃჄჅḀḂḄḆḈḊḌḎḐḒḔḖḘḚḜḞḠḢḤḦḨḪḬḮḰḲḴḶḸḺḼḾṀṂṄṆṈṊṌṎṐṒṔṖṘṚṜṞṠṢṤṦṨṪṬṮṰṲṴṶṸṺṼṾẀẂẄẆẈẊẌẎẐẒẔẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴỶỸἈἉἊἋἌἍἎἏἘἙἚἛἜἝἨἩἪἫἬἭἮἯἸἹἺἻἼἽἾἿὈὉὊὋὌὍὙὛὝὟὨὩὪὫὬὭὮὯᾈᾉᾊᾋᾌᾍᾎᾏᾘᾙᾚᾛᾜᾝᾞᾟᾨᾩᾪᾫᾬᾭᾮᾯᾸᾹᾺΆᾼῈΈῊΉῌῘῙῚΊῨῩῪΎῬῸΌῺΏῼΩKÅⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫⅬⅭⅮⅯⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
      allUpperAns = 'abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþāăąćĉċčďđēĕėęěĝğġģĥħĩīĭįiĳĵķĺļľŀłńņňŋōŏőœŕŗřśŝşšţťŧũūŭůűųŵŷÿźżžɓƃƅɔƈɖɗƌǝəɛƒɠɣɩɨƙɯɲɵơƣƥʀƨʃƭʈưʊʋƴƶʒƹƽǆǆǉǉǌǌǎǐǒǔǖǘǚǜǟǡǣǥǧǩǫǭǯǳǳǵƕƿǹǻǽǿȁȃȅȇȉȋȍȏȑȓȕȗșțȝȟȣȥȧȩȫȭȯȱȳάέήίόύώαβγδεζηθικλμνξοπρςστυφχψωϊϋϙϛϝϟϡϣϥϧϩϫϭϯθѐёђѓєѕіїјљњћќѝўџабвгдежзийклмнопрстуфхцчшщъыьэюяѡѣѥѧѩѫѭѯѱѳѵѷѹѻѽѿҁҋҍҏґғҕҗҙқҝҟҡңҥҧҩҫҭүұҳҵҷҹһҽҿӂӄӈӌӑӓӕӗәӛӝӟӡӣӥӧөӫӭӯӱӳӵӷӹաբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆაბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰჱჲჳჴჵḁḃḅḇḉḋḍḏḑḓḕḗḙḛḝḟḡḣḥḧḩḫḭḯḱḳḵḷḹḻḽḿṁṃṅṇṉṋṍṏṑṓṕṗṙṛṝṟṡṣṥṧṩṫṭṯṱṳṵṷṹṻṽṿẁẃẅẇẉẋẍẏẑẓẕạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹἀἁἂἃἄἅἆἇἐἑἒἓἔἕἠἡἢἣἤἥἦἧἰἱἲἳἴἵἶἷὀὁὂὃὄὅὑὓὕὗὠὡὢὣὤὥὦὧᾀᾁᾂᾃᾄᾅᾆᾇᾐᾑᾒᾓᾔᾕᾖᾗᾠᾡᾢᾣᾤᾥᾦᾧᾰᾱὰάᾳὲέὴήῃῐῑὶίῠῡὺύῥὸόὼώῳωkåⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹⅺⅻⅼⅽⅾⅿⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'
      allLower = 'abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿāăąćĉċčďđēĕėęěĝğġģĥħĩīĭįıĳĵķĺļľŀłńņňŋōŏőœŕŗřśŝşšţťŧũūŭůűųŵŷźżžſƃƅƈƌƒƕƙơƣƥƨƭưƴƶƹƽƿǅǆǈǉǋǌǎǐǒǔǖǘǚǜǝǟǡǣǥǧǩǫǭǯǲǳǵǹǻǽǿȁȃȅȇȉȋȍȏȑȓȕȗșțȝȟȣȥȧȩȫȭȯȱȳɓɔɖɗəɛɠɣɨɩɯɲɵʀʃʈʊʋʒͅάέήίαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώϐϑϕϖϙϛϝϟϡϣϥϧϩϫϭϯϰϱϲϵабвгдежзийклмнопрстуфхцчшщъыьэюяѐёђѓєѕіїјљњћќѝўџѡѣѥѧѩѫѭѯѱѳѵѷѹѻѽѿҁҋҍҏґғҕҗҙқҝҟҡңҥҧҩҫҭүұҳҵҷҹһҽҿӂӄӈӌӑӓӕӗәӛӝӟӡӣӥӧөӫӭӯӱӳӵӷӹաբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆḁḃḅḇḉḋḍḏḑḓḕḗḙḛḝḟḡḣḥḧḩḫḭḯḱḳḵḷḹḻḽḿṁṃṅṇṉṋṍṏṑṓṕṗṙṛṝṟṡṣṥṧṩṫṭṯṱṳṵṷṹṻṽṿẁẃẅẇẉẋẍẏẑẓẕẛạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹἀἁἂἃἄἅἆἇἐἑἒἓἔἕἠἡἢἣἤἥἦἧἰἱἲἳἴἵἶἷὀὁὂὃὄὅὑὓὕὗὠὡὢὣὤὥὦὧὰάὲέὴήὶίὸόὺύὼώᾀᾁᾂᾃᾄᾅᾆᾇᾐᾑᾒᾓᾔᾕᾖᾗᾠᾡᾢᾣᾤᾥᾦᾧᾰᾱᾳιῃῐῑῠῡῥῳⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹⅺⅻⅼⅽⅾⅿⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'
      allLowerAns = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸĀĂĄĆĈĊČĎĐĒĔĖĘĚĜĞĠĢĤĦĨĪĬĮIĲĴĶĹĻĽĿŁŃŅŇŊŌŎŐŒŔŖŘŚŜŞŠŢŤŦŨŪŬŮŰŲŴŶŹŻŽSƂƄƇƋƑǶƘƠƢƤƧƬƯƳƵƸƼǷǄǄǇǇǊǊǍǏǑǓǕǗǙǛƎǞǠǢǤǦǨǪǬǮǱǱǴǸǺǼǾȀȂȄȆȈȊȌȎȐȒȔȖȘȚȜȞȢȤȦȨȪȬȮȰȲƁƆƉƊƏƐƓƔƗƖƜƝƟƦƩƮƱƲƷΙΆΈΉΊΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡ΢ΣΤΥΦΧΨΩΪΫΌΎΏΒΘΦΠϘϚϜϞϠϢϤϦϨϪϬϮΚΡΣΕАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯЀЁЂЃЄЅІЇЈЉЊЋЌЍЎЏѠѢѤѦѨѪѬѮѰѲѴѶѸѺѼѾҀҊҌҎҐҒҔҖҘҚҜҞҠҢҤҦҨҪҬҮҰҲҴҶҸҺҼҾӁӃӇӋӐӒӔӖӘӚӜӞӠӢӤӦӨӪӬӮӰӲӴӶӸԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖḀḂḄḆḈḊḌḎḐḒḔḖḘḚḜḞḠḢḤḦḨḪḬḮḰḲḴḶḸḺḼḾṀṂṄṆṈṊṌṎṐṒṔṖṘṚṜṞṠṢṤṦṨṪṬṮṰṲṴṶṸṺṼṾẀẂẄẆẈẊẌẎẐẒẔṠẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴỶỸἈἉἊἋἌἍἎἏἘἙἚἛἜἝἨἩἪἫἬἭἮἯἸἹἺἻἼἽἾἿὈὉὊὋὌὍὙὛὝὟὨὩὪὫὬὭὮὯᾺΆῈΈῊΉῚΊῸΌῪΎῺΏᾈᾉᾊᾋᾌᾍᾎᾏᾘᾙᾚᾛᾜᾝᾞᾟᾨᾩᾪᾫᾬᾭᾮᾯᾸᾹᾼΙῌῘῙῨῩῬῼⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫⅬⅭⅮⅯⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'

      # toLowerCase
      self.assertEqual(String('teST😋').toLowerCase(), 'test😋')
      self.assertEqual(String(allUpper).toLowerCase(), allUpperAns)

      # toUpperCase
      self.assertEqual(String('teST😋').toUpperCase(), 'TEST😋')
      self.assertEqual(String(allLower).toUpperCase(), allLowerAns)

      # toLocaleLowerCase
      self.assertEqual(String('teST😋').toLocaleLowerCase(), 'test😋')
      self.assertEqual(String(allUpper).toLocaleLowerCase(), allUpperAns)

      # toLocaleUpperCase
      self.assertEqual(String('teST😋').toLocaleUpperCase(), 'TEST😋')
      self.assertEqual(String(allLower).toLocaleUpperCase(), allLowerAns)

   def test_charAt(self):
      s = String('abcdefg')
      self.assertEqual(s.charAt(), 'a')
      self.assertEqual(s.charAt(1), 'b')
      self.assertEqual(s.charAt(1.1), 'b')
      self.assertEqual(s.charAt(1.5), 'b')
      self.assertEqual(s.charAt(7), '')
      self.assertEqual(s.charAt(-1), '')
      self.assertEqual(s.charAt(NaN), 'a')
      self.assertEqual(s.charAt(Number(1.79e+308)), '')
      self.assertEqual(s.charAt(Infinity), '')
      self.assertEqual(s.charAt(-Infinity), '')
      self.assertEqual(String('あいうえお').charAt(1), 'い')
      # NOTE: There is a character here, it just doesn't render
      self.assertEqual(String('مَرحَبًا').charAt(1), 'َ')

      self.assertEqual(String('👨‍👨‍👧‍👦').charAt(0), '�')
      self.assertEqual(String('').charAt(0), '')

   def test_charCodeAt(self):
      s = String('abcdefg')
      self.assertEqual(s.charCodeAt(), 97)
      self.assertEqual(s.charCodeAt(1), 98)
      self.assertEqual(s.charCodeAt(1.1), 98)
      self.assertEqual(s.charCodeAt(1.5), 98)
      self.assertNaN(s.charCodeAt(7))
      self.assertNaN(s.charCodeAt(-1))
      self.assertEqual(s.charCodeAt(NaN), 97)
      self.assertNaN(s.charCodeAt(Number(1.79e+308)))
      self.assertNaN(s.charCodeAt(Infinity))
      self.assertNaN(s.charCodeAt(-Infinity))
      self.assertEqual(String('あいうえお').charCodeAt(1), 12356)
      self.assertEqual(String('مَرحَبًا').charCodeAt(1), 1614)
      self.assertEqual(String('👨‍👨‍👧‍👦').charCodeAt(0), 55357)
      self.assertNaN(String('').charCodeAt(0))

   def test_concat(self):
      ruffle_object = Object()
      ruffle_object.s = 'Ruffle Test Object'
      ruffle_object.toString = lambda: ruffle_object.s

      s = String('5')
      self.assertEqual(s.concat(), '5')
      self.assertEqual(s.concat(1), '51')
      self.assertEqual(s.concat(s), '55')
      self.assertEqual(s.concat(s, 1), '551')
      self.assertEqual(s.concat('asdf'), '5asdf')
      self.assertEqual(s.concat(null, s, undefined, 0, Object(),
                                ruffle_object, true),
                       '5null5undefined0[object Object]Ruffle Test Objecttrue')

   def test_fromCharCode(self):
      # TODO
      # self.assertEqual(String.fromCharCode, 'function Function() {}')
      self.assertEqual(String.fromCharCode(80), 'P')
      self.assertEqual(String.fromCharCode(12345), '〹')
      self.assertEqual(String.fromCharCode(65616), 'P')
      self.assertEqual(String.fromCharCode(-65456), 'P')
      self.assertEqual(String.fromCharCode(0xd801), '�')
      self.assertEqual(String.fromCharCode('BAD'), '')
      self.assertEqual(String.fromCharCode(NaN), '')
      self.assertEqual(String.fromCharCode(), '')
      self.assertEqual(String.fromCharCode(80, 81, 82), 'PQR')
      self.assertEqual(String.fromCharCode(80, 0, 82), 'PR')

   def test_constructor(self):
      self.assertEqual(String(), '')

      self.assertEqual(String(undefined), 'undefined')
      self.assertEqual(String(null), 'null')

      self.assertEqual(String(false), 'false')
      self.assertEqual(String(true), 'true')

      self.assertEqual(String(Number(0)), '0')
      self.assertEqual(String(Number(123)), '123')
      self.assertEqual(String(Number(-1.23)), '-1.23')

      self.assertEqual(String(''), '')
      self.assertEqual(String('abc012aáâ!?*你好こんにちはمَرحَبًا'), 'abc012aáâ!?*你好こんにちはمَرحَبًا')

      self.assertEqual(String(Object()), '[object Object]')
      # TODO: output: function Function() {}
      # trace("//function f():void {}");
      # trace("//new String(f);");
      # function f():void {}
      # self.assertEqual(new String(f));

   def test_indexOf(self):
      raise TestNotImplemented

   def test_lastIndexOf(self):
      raise TestNotImplemented

   def test_length(self):
      self.assertEqual(String('').length, 0)
      self.assertEqual(String('\n\r').length, 2)
      self.assertEqual(String('\t').length, 1)
      self.assertEqual(String('abc012aáâ').length, 9)
      self.assertEqual(String('你好こんにちは').length, 7)
      self.assertEqual(String('مَرحَبًا').length, 8)
      self.assertEqual(String('😀').length, 2)
      self.assertEqual(String('👨‍👨‍👧‍👦').length, 11)

   def assertLocaleCompare(self, str1, str2, check):
      self.assertEqual(str1.localeCompare(str2), check)

   def test_localeCompare(self):
      # basic string test
      str1 = String('abc')
      str2 = String('abc')
      self.assertLocaleCompare(str1, str2, 0)  # =

      str1 = String('abc')
      str2 = String('abd')
      self.assertLocaleCompare(str1, str2, -1)  # <

      str1 = String('abd')
      str2 = String('abc')
      self.assertLocaleCompare(str1, str2, 1)  # >

      # distance between strings
      str1 = String('aaaaaa')
      str2 = String('aaaazz')
      self.assertLocaleCompare(str1, str2, -25)  # <
      self.assertLocaleCompare(str2, str1, 25)  # >

      # different length
      str1 = String('aaaaa')
      str2 = String('aaaaaa')
      self.assertLocaleCompare(str1, str2, -1)  # <

      str1 = String('aaaaaaa')
      str2 = String('aaaaaz')
      self.assertLocaleCompare(str1, str2, -25)  # <

      # unicode string test
      str1 = String('abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþāăąćĉċčďđēĕėęěĝğġģĥħĩīĭįiĳĵķĺļľŀłńņňŋōŏőœŕŗřśŝşšţťŧũūŭůűųŵŷÿźżžɓƃƅɔƈɖɗƌǝəɛƒɠɣɩɨƙɯɲɵơƣƥʀƨʃƭʈưʊʋƴƶʒƹƽǆǆǉǉǌǌǎǐǒǔǖǘǚǜǟǡǣǥǧǩǫǭǯǳǳǵƕƿǹǻǽǿȁȃȅȇȉȋȍȏȑȓȕȗșțȝȟȣȥȧȩȫȭȯȱȳάέήίόύώαβγδεζηθικλμνξοπρςστυφχψωϊϋϙϛϝϟϡϣϥϧϩϫϭϯθѐёђѓєѕіїјљњћќѝўџабвгдежзийклмнопрстуфхцчшщъыьэюяѡѣѥѧѩѫѭѯѱѳѵѷѹѻѽѿҁҋҍҏґғҕҗҙқҝҟҡңҥҧҩҫҭүұҳҵҷҹһҽҿӂӄӈӌӑӓӕӗәӛӝӟӡӣӥӧөӫӭӯӱӳӵӷӹաբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆაბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰჱჲჳჴჵḁḃḅḇḉḋḍḏḑḓḕḗḙḛḝḟḡḣḥḧḩḫḭḯḱḳḵḷḹḻḽḿṁṃṅṇṉṋṍṏṑṓṕṗṙṛṝṟṡṣṥṧṩṫṭṯṱṳṵṷṹṻṽṿẁẃẅẇẉẋẍẏẑẓẕạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹἀἁἂἃἄἅἆἇἐἑἒἓἔἕἠἡἢἣἤἥἦἧἰἱἲἳἴἵἶἷὀὁὂὃὄὅὑὓὕὗὠὡὢὣὤὥὦὧᾀᾁᾂᾃᾄᾅᾆᾇᾐᾑᾒᾓᾔᾕᾖᾗᾠᾡᾢᾣᾤᾥᾦᾧᾰᾱὰάᾳὲέὴήῃῐῑὶίῠῡὺύῥὸόὼώῳωkåⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹⅺⅻⅼⅽⅾⅿⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ')
      str2 = String('abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþāăąćĉċčďđēĕėęěĝğġģĥħĩīĭįiĳĵķĺļľŀłńņňŋōŏőœŕŗřśŝşšţťŧũūŭůűųŵŷÿźżžɓƃƅɔƈɖɗƌǝəɛƒɠɣɩɨƙɯɲɵơƣƥʀƨʃƭʈưʊʋƴƶʒƹƽǆǆǉǉǌǌǎǐǒǔǖǘǚǜǟǡǣǥǧǩǫǭǯǳǳǵƕƿǹǻǽǿȁȃȅȇȉȋȍȏȑȓȕȗșțȝȟȣȥȧȩȫȭȯȱȳάέήίόύώαβγδεζηθικλμνξοπρςστυφχψωϊϋϙϛϝϟϡϣϥϧϩϫϭϯθѐёђѓєѕіїјљњћќѝўџабвгдежзийклмнопрстуфхцчшщъыьэюяѡѣѥѧѩѫѭѯѱѳѵѷѹѻѽѿҁҋҍҏґғҕҗҙқҝҟҡңҥҧҩҫҭүұҳҵҷҹһҽҿӂӄӈӌӑӓӕӗәӛӝӟӡӣӥӧөӫӭӯӱӳӵӷӹաբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆაბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰჱჲჳჴჵḁḃḅḇḉḋḍḏḑḓḕḗḙḛḝḟḡḣḥḧḩḫḭḯḱḳḵḷḹḻḽḿṁṃṅṇṉṋṍṏṑṓṕṗṙṛṝṟṡṣṥṧṩṫṭṯṱṳṵṷṹṻṽṿẁẃẅẇẉẋẍẏẑẓẕạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹἀἁἂἃἄἅἆἇἐἑἒἓἔἕἠἡἢἣἤἥἦἧἰἱἲἳἴἵἶἷὀὁὂὃὄὅὑὓὕὗὠὡὢὣὤὥὦὧᾀᾁᾂᾃᾄᾅᾆᾇᾐᾑᾒᾓᾔᾕᾖᾗᾠᾡᾢᾣᾤᾥᾦᾧᾰᾱὰάᾳὲέὴήῃῐῑὶίῠῡὺύῥὸόὼώῳωkåⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹⅺⅻⅼⅽⅾⅿⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩａｂｃｃｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ')
      self.assertLocaleCompare(str1, str1, 0)  # =
      self.assertLocaleCompare(str2, str1, -1)  # <
      self.assertLocaleCompare(str1, str2, 1)  # >

      # distance between unicode strings
      str1 = String('aaaaａａ')
      str2 = String('aaaazz')
      str3 = String('aaaaｚｚ')
      self.assertLocaleCompare(str1, str2, 65223)  # >
      self.assertLocaleCompare(str1, str3, -25)  # <

      # emoji strings
      str1 = String('😋')
      str2 = String('a')
      self.assertLocaleCompare(str1, str2, 55260)  # >
      self.assertLocaleCompare(str1, str1, 0)  # =

      # empty other string
      str1 = String('abc')
      str2 = String('undefined')
      self.assertLocaleCompare(str1, str2, -20)  # <
      self.assertLocaleCompare(str2, str2, 0)  # =

   def test_match(self):
      ruffle_object = Object()
      ruffle_object.s = 'Ruffle Test Object'
      def fn(obj):
         return obj.s
      ruffle_object.toString = fn

      # Match tests
      str = String('matchablematmatmat')
      ret = str.match('mat')
      self.assertArray(ret, ['mat'])

      re = RegExp('MA*T|a[a-z]*e', 'i')
      re.lastIndex = 3
      self.assertArray(str.match(re), ['mat'])
      self.assertEqual(re.lastIndex, 3)
      self.assertArray(str.match(re), ['mat'])
      self.assertEqual(re.lastIndex, 3)
      self.assertArray(str.match(re), ['mat'])
      self.assertEqual(re.lastIndex, 3)

      self.assertArray(str.match(RegExp('MA*T|a[a-z]*e', 'i')), ['mat'])
      self.assertArray(str.match(RegExp('ma*t|a[a-z]*e', '')), ['mat'])
      self.assertArray(str.match(RegExp('ma*t|a[a-z]*e', 'g')), ['mat', 'able', 'mat', 'mat', 'mat'])
      # TODO: Make sure this returns an empty array and not an empty string or
      #       array with empty string in it
      self.assertEqual(str.match(RegExp('notmatch', 'g')).length, 0)

      subject = String('AAA')
      re = RegExp('(((((((((((((((((((a*)(abc|b))))))))))))))))))*.)*(...)*', 'g')
      self.assertArray(subject.match(re), ['AAA'])

      re = RegExp('((((((((((((((((((d|.*)))))))))))))))))*.)*(...)*', 'g')
      self.assertArray(subject.match(re), ['AAA'])

      re = RegExp('((((((((((((((((((a+)*))))))))))))))))*.)*(...)*', 'g')
      self.assertArray(subject.match(re), ['AAA'])

      re = RegExp('((((((((((((((((((a+)*))))))))))))))))*.)*(...)*')
      self.assertEqual(subject.match(re).toString, 'AAA,A,,,,,,,,,,,,,,,,,,')

      pattern = '((((((((((((((((((a+)*))))))))))))))))*.)*(...)*'
      self.assertEqual(subject.match(pattern).toString, 'AAA,A,,,,,,,,,,,,,,,,,,')
      pattern = '(A)(A)'
      self.assertArray(subject.match(pattern), ['AA', 'A', 'A'])
      pattern = 'AAA'
      self.assertArray(subject.match(pattern), ['AAA'])
      pattern = 'AA'
      self.assertArray(subject.match(pattern), ['AA'])
      pattern = 'A'
      self.assertArray(subject.match(pattern), ['A'])

      self.assertEqual(str.match(ruffle_object).toString, 'null')

      regexTest = String('v1')
      regex = RegExp(r'^\b[A-Za-z]{1,2}', 'ig')
      self.assertArray(regexTest.match(regex), ['v'])
      self.assertEqual(regex.lastIndex, 1)
      self.assertArray(regexTest.match(regex), ['v'])
      self.assertEqual(regex.lastIndex, 0)

   def assertReplace(self, string, pattern, repl, check):
      self.assertEqual(String(string).replace(pattern, repl), check)

   def test_replace(self):
      # string replacements
      self.assertReplace('a a a', 'a', '', ' a a')
      self.assertReplace('a a a', 'a', 'b', 'b a a')
      self.assertReplace('aaaa', 'aa', 'a', 'aaa')
      self.assertReplace('a a a', '', 'x', 'xa a a')

      # regex
      self.assertReplace('  123', RegExp('123', 'g'), 'x', '  x')
      self.assertReplace('123  ', RegExp('123', 'g'), 'x', 'x  ')
      self.assertReplace('  123  ', RegExp('123', 'g'), 'x', '  x  ')

      self.assertReplace('123  123', RegExp(' +', 'g'), 'x', '123x123')
      self.assertReplace('123  123', RegExp(r'\d+', 'g'), 'x', 'x  x')
      self.assertReplace('123  123', RegExp('.*', 'g'), 'x', 'xx')

      # empty regex
      self.assertReplace('aaa', RegExp('', 'g'), 'x', 'xaxaxax')

      # lastIndex should not be modified
      regex = RegExp('a', 'g')
      regex.lastIndex = 1
      self.assertReplace('aaaa', regex, 'x', 'xxxx')
      self.assertEqual(regex.lastIndex, 1)

      # $ with non-special successor char
      self.assertReplace('abaa', RegExp('b'), '$k', 'a$kaa')  # $k
      self.assertReplace('abaa', RegExp('b'), '|$&|', 'a|b|aa')  # $&
      self.assertReplace('axbfg', RegExp('b'), '$`', 'axaxfg')  # $`
      self.assertReplace('axbfg', RegExp('b'), "$'", 'axfgfg')  # $'
      self.assertReplace('abc', RegExp('(b)'), '<$1>', 'a<b>c')  # $1

      # capture group 0 not recognized
      self.assertReplace('abc', RegExp('(b)'), '<$0>', 'a<$0>c')

      # capture group 00 not recognized
      self.assertReplace('abc', RegExp('(b)'), '<$00>', 'a<$00>c')

      # leading 0 capture group number
      self.assertReplace('abc', RegExp('(b)'), '<$01>', 'a<b1>c')

      # not enough groups
      self.assertReplace('abc', RegExp('(b)'), '<$2>', 'a<$2>c')

      # two-digit capture group number, but not enough groups
      self.assertReplace('abc', RegExp('(b)'), '<$20>', 'a<$20>c')

      # two-digit capture group number, but not enough groups with prefix as a
      # valid group
      self.assertReplace('abc', RegExp('(b)'), '<$10>', 'a<b0>c')

      # Two-digit capture group number
      r = RegExp('(.)(.)(.)(.)(.)(.)(.)(.)(.)(.)')
      self.assertReplace('abbbbbbbbb#bbc', r, '<$10>', '<b>#bbc')

      # replace function
      def replFn() -> String:
         return String('foo')

      self.assertReplace('abbbb', RegExp('a'), replFn, 'foobbbb')

      # replace with functions returning non-string values

      def replFn2():
         return 2

      def replFn3():
         # NOTE: This was originally an empty function
         return undefined

      self.assertReplace('abbbb', RegExp('a'), replFn2, '2bbbb')
      self.assertReplace('abbbb', RegExp('a'), replFn3, 'undefinedbbbb')

      # replace a regex with function, check arguments

      # relies on implicit coercion to string
      def rFN(*args):
         return Array(*args)

      # The (b) and (c) groups have no matches.
      self.assertReplace('<<a>>', RexExp('(a)(b)?|(c)'), rFN,
                         '<<a,a,,,2,<<a>>>>')

      # The pattern is string and the replacement is a function
      self.assertReplace('<<a>>', 'a', rFN, '<<a,2,<<a>>>>')

      # regex calling into itself
      pattern = RegExp('simple', 'g')

      def fn(match):
         return match.replace(pattern, 'complicated')

      self.assertReplace('this is simple, really simple.', pattern, fn,
                         'this is complicated, really complicated.')

   def test_search(self):
      ruffle_object = Object()
      ruffle_object.s = 'Ruffle Test Object'
      ruffle_object.toString = lambda: ruffle_object.s

      str = String('mtchablematmatmat')
      ret = str.search('mat')
      self.assertEqual(ret, 8)

      re = RegExp('MA*T|a[a-z]*e', 'i')
      re.lastIndex = 3
      self.assertEqual(str.search(re), 0)
      self.assertEqual(re.lastIndex, 3)
      self.assertEqual(str.search(re), 0)
      self.assertEqual(re.lastIndex, 3)
      self.assertEqual(str.search(re), 0)
      self.assertEqual(re.lastIndex, 3)

      self.assertEqual(str.search(RegExp('MA*T|a[a-z]*e', 'i')), 0)
      self.assertEqual(str.search(RegExp('ma*t|a[a-z]*e', '')), 0)
      self.assertEqual(str.search(RegExp('ma*t|a[a-z]*e','g')), 0)
      self.assertEqual(str.search(RegExp('notmatch', 'g')), -1)

      subject = String('AAA')
      self.assertEqual(subject.search(RegExp('(((((((((((((((((((a*)(abc|b))))))))))))))))))*.)*(...)*', 'g')), 0)
      self.assertEqual(subject.search(RegExp('((((((((((((((((((d|.*)))))))))))))))))*.)*(...)*', 'g')), 0)
      self.assertEqual(subject.search(RegExp('((((((((((((((((((a+)*))))))))))))))))*.)*(...)*', 'g')), 0)

      self.assertEqual(subject.search('((((((((((((((((((a+)*))))))))))))))))*.)*(...)*'), 0)
      self.assertEqual(subject.search('(A)(A)'), 0)
      self.assertEqual(subject.search('AAA'), 0)
      self.assertEqual(subject.search('AA'), 0)
      self.assertEqual(subject.search('A'), 0)

      self.assertEqual(str.search(ruffle_object), -1)

   def assertSlice(self, string, sidx, eidx, check):
      self.assertEqual(string.slice(sidx, eidx), check)

   def test_slice(self):
      s = String('')
      self.assertEqual(s.slice(), '')
      # trace( typeof s2.slice()) -> string
      self.assertSlice(s, false, true, '')
      self.assertSlice(s, 0, 9, '')
      self.assertSlice(s, 25, 29, '')

      s = String('123456789')
      self.assertEqual(s.slice(), '123456789')
      # trace(typeof s.slice()) -> string
      self.assertSlice(s, 0, 9, '123456789')
      self.assertSlice(s, 0, 0, '')
      self.assertSlice(s, 9, 0, '')
      self.assertSlice(s, 0, -1, '12345678')
      self.assertSlice(s, -6, -1, '45678')
      self.assertSlice(s, false, true, '1')
      self.assertSlice(s, 4, -3, '56')
      self.assertSlice(s, 25, 29, '')
      self.assertSlice(s, -5, 9, '56789')
      self.assertSlice(s, 2, NaN, '')
      self.assertSlice(s, NaN, 2, '12')
      self.assertSlice(s, 2, undefined, '')
      self.assertSlice(s, undefined, 2, '12')
      self.assertSlice(s, -0.01, 0, '')
      self.assertSlice(s, s.length, s.length, '')
      self.assertSlice(s, s.length + 1, 0, '')
      self.assertSlice(s, Infinity, 5, '')
      self.assertSlice(s, 5, Infinity, '6789')
      self.assertSlice(s, Infinity, Infinity, '')
      self.assertSlice(s, -Infinity, -Infinity, '')
      self.assertSlice(s, -Infinity, Infinity, '123456789')
      self.assertSlice(s, Infinity, -Infinity, '')
      self.assertSlice(s, NaN, Infinity, '123456789')
      self.assertSlice(s, Infinity, NaN, '')
      self.assertSlice(s, NaN, -Infinity, '')
      self.assertSlice(s, -Infinity, NaN, '')

   def test_split(self):
      text = String('a.b.c')
      self.assertArray(text.split('a.b.c'), ['', ''])
      self.assertArray(text.split('.'), ['a', 'b', 'c'])
      self.assertArray(text.split(''), ['a', '.', 'b', '.', 'c'])
      self.assertArray(text.split(), ['a.b.c'])

      # text.split(regex)
      text = String('abbabc')
      regex = RegExp('b+')
      self.assertArray(text.split(regex), ['a', 'a', 'c'])

      # no match
      text = String('ccccc')
      regex = RegExp('b')
      self.assertArray(text.split(regex), ['ccccc'])

      # match all
      text = String('cccc')
      regex = RegExp('.*')
      self.assertArray(text.split(regex), ['', ''])

      # empty string, match all
      # TODO: Check if this is supposed to be an array or just an empty string
      text = String('')
      regex = RegExp('.*')
      self.assertArray(text.split(regex), [''])

      # multibyte chars
      text = String('ąąbąą')
      regex = RegExp('b')
      self.assertArray(text.split(regex), ['ąą', 'ąą'])

      # Group expansion
      text = String('abba')
      regex = RegExp('(b(b))')
      self.assertArray(text.split(regex), ['a', 'bb', 'a'])

      # Split on empty regex
      text = String('aął')
      regex = RegExp('(?:)')
      self.assertArray(text.split(regex), ['aął'])

      # Split on non-empty regex with zero-length match
      text = String('aąbcde')
      regex = RegExp('f*')
      self.assertArray(text.split(regex), ['aąbcde'])

      # Limit
      text = String('aąbaababa')
      regex = RegExp('b')
      self.assertArray(text.split(regex, 3), ['aą', 'aa', 'a'])

      # Limit on group captures - flash returns 6 parts instead of 5
      text = String('aąbbaabbabbabbabbabba')
      regex = RegExp('(b(b))')
      self.assertArray(text.split(regex, 5), ['aą', 'bb', 'b', 'aa', 'bb', 'a'])

   def assertSubstr(self, string, sidx, len, check):
      self.assertEqual(string.substr(sidx, len), check)

   def test_substr(self):
      s = String('')
      self.assertEqual(s.substr(), '')
      # trace( typeof s.substr()) -> string
      self.assertSubstr(s, false, true, '')
      self.assertSubstr(s, 25, 29, '')

      s = String('123456789')
      self.assertEqual(s.substr(), '123456789')
      # trace(typeof s.slice()) -> string
      self.assertSubstr(s, false, true, '1')
      self.assertSubstr(s, 4, -3, '')
      self.assertSubstr(s, 25, 29, '')
      self.assertSubstr(s, -5, 9, '56789')
      self.assertSubstr(s, 2, NaN, '')
      self.assertSubstr(s, NaN, 2, '12')
      self.assertSubstr(s, 2, undefined, '')
      self.assertSubstr(s, undefined, 2, '12')
      self.assertSubstr(s, -0.01, 0, '')
      self.assertSubstr(s, s.length, s.length, '')
      self.assertSubstr(s, s.length + 1, 0, '')
      self.assertSubstr(s, Infinity, 5, '')
      self.assertSubstr(s, 5, Infinity, '6789')
      self.assertSubstr(s, Infinity, Infinity, '')
      self.assertSubstr(s, -Infinity, -Infinity, '')
      self.assertSubstr(s, -Infinity, Infinity, '123456789')
      self.assertSubstr(s, Infinity, -Infinity, '')
      self.assertSubstr(s, NaN, Infinity, '123456789')
      self.assertSubstr(s, Infinity, NaN, '')
      self.assertSubstr(s, NaN, -Infinity, '')
      self.assertSubstr(s, -Infinity, NaN, '')

   def test_substr_negative(self):
      text = String('abcdefg')
      list1 = (3, 0, 1, 2, 1, 1, 2, 2, 0, 2, 5)
      list2 = (5, -2, -2, -2, -4, -Infinity, -1, 9, -3, -7, -10)
      ans_list = ('defg', 'abcde', 'bcdef', '', 'bcd', '', '', 'cdefg',
                  'abcd', '', '')
      for i in range(len(list1)):
         ans = text.substr(list1[i], list2[i])
         if ans != ans_list[i]:
            self.fail('substr(%s, %s); "%s" != "%s"' % (list1[i], list2[i], ans,
                                                    ans_list[i]))

   def test_substr_weird(self):
      raise TestNotImplemented
      idxs = (0, -0.01, Infinity, -Infinity, NaN, -(NaN), 1.001, -0.6, -0.3,
              4, 1, -1, 1e+21)
      for i in len(idxs):
         for j in len(idxs):
            trace("Substr of " + idxs[i] + "-" + idxs[j] + ": " + "123456789".substr(idxs[i],idxs[j]))
         trace("Substr of " + idxs[i] + ": " + "123456789".substr(idxs[i]))
      '''
      2026-01-22T19:05:52.247820Z  INFO avm_trace: Substr of 0-0:
      2026-01-22T19:05:52.247856Z  INFO avm_trace: Substr of 0--0.01:
      2026-01-22T19:05:52.247867Z  INFO avm_trace: Substr of 0-Infinity: 123456789
      2026-01-22T19:05:52.247873Z  INFO avm_trace: Substr of 0--Infinity:
      2026-01-22T19:05:52.247879Z  INFO avm_trace: Substr of 0-NaN:
      2026-01-22T19:05:52.247884Z  INFO avm_trace: Substr of 0-NaN:
      2026-01-22T19:05:52.247891Z  INFO avm_trace: Substr of 0-1.001: 1
      2026-01-22T19:05:52.247898Z  INFO avm_trace: Substr of 0--0.6:
      2026-01-22T19:05:52.247904Z  INFO avm_trace: Substr of 0--0.3:
      2026-01-22T19:05:52.247910Z  INFO avm_trace: Substr of 0-4: 1234
      2026-01-22T19:05:52.247915Z  INFO avm_trace: Substr of 0-1: 1
      2026-01-22T19:05:52.247921Z  INFO avm_trace: Substr of 0--1: 12345678
      2026-01-22T19:05:52.247930Z  INFO avm_trace: Substr of 0-1e+21: 123456789
      2026-01-22T19:05:52.247935Z  INFO avm_trace: Substr of 0: 123456789
      2026-01-22T19:05:52.247943Z  INFO avm_trace: Substr of -0.01-0:
      2026-01-22T19:05:52.247951Z  INFO avm_trace: Substr of -0.01--0.01:
      2026-01-22T19:05:52.247958Z  INFO avm_trace: Substr of -0.01-Infinity: 123456789
      2026-01-22T19:05:52.247965Z  INFO avm_trace: Substr of -0.01--Infinity:
      2026-01-22T19:05:52.247971Z  INFO avm_trace: Substr of -0.01-NaN:
      2026-01-22T19:05:52.247977Z  INFO avm_trace: Substr of -0.01-NaN:
      2026-01-22T19:05:52.247983Z  INFO avm_trace: Substr of -0.01-1.001: 1
      2026-01-22T19:05:52.247991Z  INFO avm_trace: Substr of -0.01--0.6:
      2026-01-22T19:05:52.247997Z  INFO avm_trace: Substr of -0.01--0.3:
      2026-01-22T19:05:52.248003Z  INFO avm_trace: Substr of -0.01-4: 1234
      2026-01-22T19:05:52.248009Z  INFO avm_trace: Substr of -0.01-1: 1
      2026-01-22T19:05:52.248015Z  INFO avm_trace: Substr of -0.01--1: 12345678
      2026-01-22T19:05:52.248023Z  INFO avm_trace: Substr of -0.01-1e+21: 123456789
      2026-01-22T19:05:52.248029Z  INFO avm_trace: Substr of -0.01: 123456789
      2026-01-22T19:05:52.248035Z  INFO avm_trace: Substr of Infinity-0:
      2026-01-22T19:05:52.248041Z  INFO avm_trace: Substr of Infinity--0.01:
      2026-01-22T19:05:52.248046Z  INFO avm_trace: Substr of Infinity-Infinity:
      2026-01-22T19:05:52.248051Z  INFO avm_trace: Substr of Infinity--Infinity:
      2026-01-22T19:05:52.248056Z  INFO avm_trace: Substr of Infinity-NaN:
      2026-01-22T19:05:52.248061Z  INFO avm_trace: Substr of Infinity-NaN:
      2026-01-22T19:05:52.248067Z  INFO avm_trace: Substr of Infinity-1.001:
      2026-01-22T19:05:52.248073Z  INFO avm_trace: Substr of Infinity--0.6:
      2026-01-22T19:05:52.248079Z  INFO avm_trace: Substr of Infinity--0.3:
      2026-01-22T19:05:52.248084Z  INFO avm_trace: Substr of Infinity-4:
      2026-01-22T19:05:52.248089Z  INFO avm_trace: Substr of Infinity-1:
      2026-01-22T19:05:52.248095Z  INFO avm_trace: Substr of Infinity--1:
      2026-01-22T19:05:52.248100Z  INFO avm_trace: Substr of Infinity-1e+21:
      2026-01-22T19:05:52.248105Z  INFO avm_trace: Substr of Infinity:
      2026-01-22T19:05:52.248111Z  INFO avm_trace: Substr of -Infinity-0:
      2026-01-22T19:05:52.248117Z  INFO avm_trace: Substr of -Infinity--0.01:
      2026-01-22T19:05:52.248123Z  INFO avm_trace: Substr of -Infinity-Infinity: 123456789
      2026-01-22T19:05:52.248129Z  INFO avm_trace: Substr of -Infinity--Infinity:
      2026-01-22T19:05:52.248135Z  INFO avm_trace: Substr of -Infinity-NaN:
      2026-01-22T19:05:52.248140Z  INFO avm_trace: Substr of -Infinity-NaN:
      2026-01-22T19:05:52.248146Z  INFO avm_trace: Substr of -Infinity-1.001: 1
      2026-01-22T19:05:52.248152Z  INFO avm_trace: Substr of -Infinity--0.6:
      2026-01-22T19:05:52.248158Z  INFO avm_trace: Substr of -Infinity--0.3:
      2026-01-22T19:05:52.248164Z  INFO avm_trace: Substr of -Infinity-4: 1234
      2026-01-22T19:05:52.248169Z  INFO avm_trace: Substr of -Infinity-1: 1
      2026-01-22T19:05:52.248175Z  INFO avm_trace: Substr of -Infinity--1: 12345678
      2026-01-22T19:05:52.248182Z  INFO avm_trace: Substr of -Infinity-1e+21: 123456789
      2026-01-22T19:05:52.248188Z  INFO avm_trace: Substr of -Infinity: 123456789
      2026-01-22T19:05:52.248193Z  INFO avm_trace: Substr of NaN-0:
      2026-01-22T19:05:52.248199Z  INFO avm_trace: Substr of NaN--0.01:
      2026-01-22T19:05:52.248204Z  INFO avm_trace: Substr of NaN-Infinity: 123456789
      2026-01-22T19:05:52.248210Z  INFO avm_trace: Substr of NaN--Infinity:
      2026-01-22T19:05:52.248215Z  INFO avm_trace: Substr of NaN-NaN:
      2026-01-22T19:05:52.248220Z  INFO avm_trace: Substr of NaN-NaN:
      2026-01-22T19:05:52.248225Z  INFO avm_trace: Substr of NaN-1.001: 1
      2026-01-22T19:05:52.248231Z  INFO avm_trace: Substr of NaN--0.6:
      2026-01-22T19:05:52.248236Z  INFO avm_trace: Substr of NaN--0.3:
      2026-01-22T19:05:52.248241Z  INFO avm_trace: Substr of NaN-4: 1234
      2026-01-22T19:05:52.248246Z  INFO avm_trace: Substr of NaN-1: 1
      2026-01-22T19:05:52.248251Z  INFO avm_trace: Substr of NaN--1: 12345678
      2026-01-22T19:05:52.248257Z  INFO avm_trace: Substr of NaN-1e+21: 123456789
      2026-01-22T19:05:52.248262Z  INFO avm_trace: Substr of NaN: 123456789
      2026-01-22T19:05:52.248267Z  INFO avm_trace: Substr of NaN-0:
      2026-01-22T19:05:52.248273Z  INFO avm_trace: Substr of NaN--0.01:
      2026-01-22T19:05:52.248278Z  INFO avm_trace: Substr of NaN-Infinity: 123456789
      2026-01-22T19:05:52.248284Z  INFO avm_trace: Substr of NaN--Infinity:
      2026-01-22T19:05:52.248288Z  INFO avm_trace: Substr of NaN-NaN:
      2026-01-22T19:05:52.248293Z  INFO avm_trace: Substr of NaN-NaN:
      2026-01-22T19:05:52.248298Z  INFO avm_trace: Substr of NaN-1.001: 1
      2026-01-22T19:05:52.248304Z  INFO avm_trace: Substr of NaN--0.6:
      2026-01-22T19:05:52.248309Z  INFO avm_trace: Substr of NaN--0.3:
      2026-01-22T19:05:52.248315Z  INFO avm_trace: Substr of NaN-4: 1234
      2026-01-22T19:05:52.248320Z  INFO avm_trace: Substr of NaN-1: 1
      2026-01-22T19:05:52.248325Z  INFO avm_trace: Substr of NaN--1: 12345678
      2026-01-22T19:05:52.248331Z  INFO avm_trace: Substr of NaN-1e+21: 123456789
      2026-01-22T19:05:52.248336Z  INFO avm_trace: Substr of NaN: 123456789
      2026-01-22T19:05:52.248342Z  INFO avm_trace: Substr of 1.001-0:
      2026-01-22T19:05:52.248347Z  INFO avm_trace: Substr of 1.001--0.01:
      2026-01-22T19:05:52.248353Z  INFO avm_trace: Substr of 1.001-Infinity: 23456789
      2026-01-22T19:05:52.248359Z  INFO avm_trace: Substr of 1.001--Infinity:
      2026-01-22T19:05:52.248364Z  INFO avm_trace: Substr of 1.001-NaN:
      2026-01-22T19:05:52.248370Z  INFO avm_trace: Substr of 1.001-NaN:
      2026-01-22T19:05:52.248375Z  INFO avm_trace: Substr of 1.001-1.001: 2
      2026-01-22T19:05:52.248381Z  INFO avm_trace: Substr of 1.001--0.6:
      2026-01-22T19:05:52.248387Z  INFO avm_trace: Substr of 1.001--0.3:
      2026-01-22T19:05:52.248392Z  INFO avm_trace: Substr of 1.001-4: 2345
      2026-01-22T19:05:52.248398Z  INFO avm_trace: Substr of 1.001-1: 2
      2026-01-22T19:05:52.248403Z  INFO avm_trace: Substr of 1.001--1:
      2026-01-22T19:05:52.248409Z  INFO avm_trace: Substr of 1.001-1e+21: 23456789
      2026-01-22T19:05:52.248415Z  INFO avm_trace: Substr of 1.001: 23456789
      2026-01-22T19:05:52.248421Z  INFO avm_trace: Substr of -0.6-0:
      2026-01-22T19:05:52.248427Z  INFO avm_trace: Substr of -0.6--0.01:
      2026-01-22T19:05:52.248433Z  INFO avm_trace: Substr of -0.6-Infinity: 123456789
      2026-01-22T19:05:52.248439Z  INFO avm_trace: Substr of -0.6--Infinity:
      2026-01-22T19:05:52.248444Z  INFO avm_trace: Substr of -0.6-NaN:
      2026-01-22T19:05:52.248449Z  INFO avm_trace: Substr of -0.6-NaN:
      2026-01-22T19:05:52.248455Z  INFO avm_trace: Substr of -0.6-1.001: 1
      2026-01-22T19:05:52.248461Z  INFO avm_trace: Substr of -0.6--0.6:
      2026-01-22T19:05:52.248467Z  INFO avm_trace: Substr of -0.6--0.3:
      2026-01-22T19:05:52.248474Z  INFO avm_trace: Substr of -0.6-4: 1234
      2026-01-22T19:05:52.248479Z  INFO avm_trace: Substr of -0.6-1: 1
      2026-01-22T19:05:52.248484Z  INFO avm_trace: Substr of -0.6--1: 12345678
      2026-01-22T19:05:52.248491Z  INFO avm_trace: Substr of -0.6-1e+21: 123456789
      2026-01-22T19:05:52.248496Z  INFO avm_trace: Substr of -0.6: 123456789
      2026-01-22T19:05:52.248502Z  INFO avm_trace: Substr of -0.3-0:
      2026-01-22T19:05:52.248509Z  INFO avm_trace: Substr of -0.3--0.01:
      2026-01-22T19:05:52.248514Z  INFO avm_trace: Substr of -0.3-Infinity: 123456789
      2026-01-22T19:05:52.248520Z  INFO avm_trace: Substr of -0.3--Infinity:
      2026-01-22T19:05:52.248526Z  INFO avm_trace: Substr of -0.3-NaN:
      2026-01-22T19:05:52.248531Z  INFO avm_trace: Substr of -0.3-NaN:
      2026-01-22T19:05:52.248538Z  INFO avm_trace: Substr of -0.3-1.001: 1
      2026-01-22T19:05:52.248543Z  INFO avm_trace: Substr of -0.3--0.6:
      2026-01-22T19:05:52.248549Z  INFO avm_trace: Substr of -0.3--0.3:
      2026-01-22T19:05:52.248555Z  INFO avm_trace: Substr of -0.3-4: 1234
      2026-01-22T19:05:52.248560Z  INFO avm_trace: Substr of -0.3-1: 1
      2026-01-22T19:05:52.248566Z  INFO avm_trace: Substr of -0.3--1: 12345678
      2026-01-22T19:05:52.248572Z  INFO avm_trace: Substr of -0.3-1e+21: 123456789
      2026-01-22T19:05:52.248577Z  INFO avm_trace: Substr of -0.3: 123456789
      2026-01-22T19:05:52.248583Z  INFO avm_trace: Substr of 4-0:
      2026-01-22T19:05:52.248588Z  INFO avm_trace: Substr of 4--0.01:
      2026-01-22T19:05:52.248593Z  INFO avm_trace: Substr of 4-Infinity: 56789
      2026-01-22T19:05:52.248599Z  INFO avm_trace: Substr of 4--Infinity:
      2026-01-22T19:05:52.248603Z  INFO avm_trace: Substr of 4-NaN:
      2026-01-22T19:05:52.248621Z  INFO avm_trace: Substr of 4-NaN:
      2026-01-22T19:05:52.248626Z  INFO avm_trace: Substr of 4-1.001: 5
      2026-01-22T19:05:52.248632Z  INFO avm_trace: Substr of 4--0.6:
      2026-01-22T19:05:52.248637Z  INFO avm_trace: Substr of 4--0.3:
      2026-01-22T19:05:52.248642Z  INFO avm_trace: Substr of 4-4: 5678
      2026-01-22T19:05:52.248647Z  INFO avm_trace: Substr of 4-1: 5
      2026-01-22T19:05:52.248652Z  INFO avm_trace: Substr of 4--1:
      2026-01-22T19:05:52.248658Z  INFO avm_trace: Substr of 4-1e+21: 56789
      2026-01-22T19:05:52.248663Z  INFO avm_trace: Substr of 4: 56789
      2026-01-22T19:05:52.248669Z  INFO avm_trace: Substr of 1-0:
      2026-01-22T19:05:52.248674Z  INFO avm_trace: Substr of 1--0.01:
      2026-01-22T19:05:52.248679Z  INFO avm_trace: Substr of 1-Infinity: 23456789
      2026-01-22T19:05:52.248684Z  INFO avm_trace: Substr of 1--Infinity:
      2026-01-22T19:05:52.248689Z  INFO avm_trace: Substr of 1-NaN:
      2026-01-22T19:05:52.248694Z  INFO avm_trace: Substr of 1-NaN:
      2026-01-22T19:05:52.248699Z  INFO avm_trace: Substr of 1-1.001: 2
      2026-01-22T19:05:52.248704Z  INFO avm_trace: Substr of 1--0.6:
      2026-01-22T19:05:52.248710Z  INFO avm_trace: Substr of 1--0.3:
      2026-01-22T19:05:52.248715Z  INFO avm_trace: Substr of 1-4: 2345
      2026-01-22T19:05:52.248720Z  INFO avm_trace: Substr of 1-1: 2
      2026-01-22T19:05:52.248724Z  INFO avm_trace: Substr of 1--1:
      2026-01-22T19:05:52.248730Z  INFO avm_trace: Substr of 1-1e+21: 23456789
      2026-01-22T19:05:52.248735Z  INFO avm_trace: Substr of 1: 23456789
      2026-01-22T19:05:52.248740Z  INFO avm_trace: Substr of -1-0:
      2026-01-22T19:05:52.248746Z  INFO avm_trace: Substr of -1--0.01:
      2026-01-22T19:05:52.248752Z  INFO avm_trace: Substr of -1-Infinity: 9
      2026-01-22T19:05:52.248757Z  INFO avm_trace: Substr of -1--Infinity:
      2026-01-22T19:05:52.248762Z  INFO avm_trace: Substr of -1-NaN:
      2026-01-22T19:05:52.248767Z  INFO avm_trace: Substr of -1-NaN:
      2026-01-22T19:05:52.248772Z  INFO avm_trace: Substr of -1-1.001: 9
      2026-01-22T19:05:52.248778Z  INFO avm_trace: Substr of -1--0.6:
      2026-01-22T19:05:52.248783Z  INFO avm_trace: Substr of -1--0.3:
      2026-01-22T19:05:52.248788Z  INFO avm_trace: Substr of -1-4: 9
      2026-01-22T19:05:52.248793Z  INFO avm_trace: Substr of -1-1: 9
      2026-01-22T19:05:52.248799Z  INFO avm_trace: Substr of -1--1:
      2026-01-22T19:05:52.248804Z  INFO avm_trace: Substr of -1-1e+21: 9
      2026-01-22T19:05:52.248809Z  INFO avm_trace: Substr of -1: 9
      2026-01-22T19:05:52.248815Z  INFO avm_trace: Substr of 1e+21-0:
      2026-01-22T19:05:52.248821Z  INFO avm_trace: Substr of 1e+21--0.01:
      2026-01-22T19:05:52.248827Z  INFO avm_trace: Substr of 1e+21-Infinity:
      2026-01-22T19:05:52.248833Z  INFO avm_trace: Substr of 1e+21--Infinity:
      2026-01-22T19:05:52.248838Z  INFO avm_trace: Substr of 1e+21-NaN:
      2026-01-22T19:05:52.248844Z  INFO avm_trace: Substr of 1e+21-NaN:
      2026-01-22T19:05:52.248850Z  INFO avm_trace: Substr of 1e+21-1.001:
      2026-01-22T19:05:52.248857Z  INFO avm_trace: Substr of 1e+21--0.6:
      2026-01-22T19:05:52.248863Z  INFO avm_trace: Substr of 1e+21--0.3:
      2026-01-22T19:05:52.248869Z  INFO avm_trace: Substr of 1e+21-4:
      2026-01-22T19:05:52.248874Z  INFO avm_trace: Substr of 1e+21-1:
      2026-01-22T19:05:52.248880Z  INFO avm_trace: Substr of 1e+21--1:
      2026-01-22T19:05:52.248886Z  INFO avm_trace: Substr of 1e+21-1e+21:
      2026-01-22T19:05:52.248891Z  INFO avm_trace: Substr of 1e+21:
      '''

   def assertSubstring(self, string, sidx, eidx, check):
      self.assertEqual(string.substring(sidx, eidx), check)

   def test_substring(self):
      s = String('')
      self.assertEqual(s.substring(), '')
      # trace( typeof s.substr()) -> string
      self.assertSubstring(s, false, true, '')
      self.assertSubstring(s, 25, 29, '')

      s = String('123456789')
      self.assertEqual(s.substring(), '123456789')
      # trace(typeof s.slice()) -> string
      self.assertSubstring(s, false, true, '1')
      self.assertSubstring(s, 4, -3, '1234')
      self.assertSubstring(s, 25, 29, '')
      self.assertSubstring(s, -5, 9, '123456789')
      self.assertSubstring(s, 2, NaN, '12')
      self.assertSubstring(s, NaN, 2, '12')
      self.assertSubstring(s, 2, undefined, '12')
      self.assertSubstring(s, undefined, 2, '12')
      self.assertSubstring(s, -0.01, 0, '')
      self.assertSubstring(s, s.length, s.length, '')
      self.assertSubstring(s, s.length + 1, 0, '123456789')
      self.assertSubstring(s, Infinity, 5, '6789')
      self.assertSubstring(s, 5, Infinity, '6789')
      self.assertSubstring(s, Infinity, Infinity, '')
      self.assertSubstring(s, -Infinity, -Infinity, '')
      self.assertSubstring(s, -Infinity, Infinity, '123456789')
      self.assertSubstring(s, Infinity, -Infinity, '123456789')
      self.assertSubstring(s, NaN, Infinity, '123456789')
      self.assertSubstring(s, Infinity, NaN, '123456789')
      self.assertSubstring(s, NaN, -Infinity, '')
      self.assertSubstring(s, -Infinity, NaN, '')


class uintTests(NumberTestsBase):
   def test_constructor(self):
      self.assertEqual(uint(), 0)
      self.assertEqual(uint(true), 1)
      self.assertEqual(uint(false), 0)
      self.assertEqual(uint(null), 0)
      self.assertEqual(uint(undefined), 0)
      self.assertEqual(uint(String('')), 0)

      self.assertEqual(uint(''), 0)
      self.assertEqual(uint(String('str')), 0)
      self.assertEqual(uint('str'), 0)
      self.assertEqual(uint(String('true')), 0)
      self.assertEqual(uint('true'), 0)
      self.assertEqual(uint(String('false')), 0)
      self.assertEqual(uint('false'), 0)

      self.assertEqual(uint(Number(0.0)), 0)
      self.assertEqual(uint(0.0), 0)
      self.assertEqual(uint(NaN), 0)
      self.assertEqual(uint(Number(-0.0)), 0)
      self.assertEqual(uint(-0.0), 0)
      self.assertEqual(uint(Infinity), 0)
      self.assertEqual(uint(Number(1.0)), 1)
      self.assertEqual(uint(1.0), 1)
      self.assertEqual(uint(Number(-1.0)), 4294967295)
      self.assertEqual(uint(-1.0), 4294967295)

      self.assertEqual(uint(0xFF1306), 16716550)
      self.assertEqual(uint(1.2315e2), 123)
      self.assertEqual(uint(0x7FFFFFFF), 2147483647)
      self.assertEqual(uint(0x80000000), 2147483648)
      self.assertEqual(uint(0x80000001), 2147483649)
      self.assertEqual(uint(0x180000001), 2147483649)
      self.assertEqual(uint(0x100000001), 1)
      self.assertEqual(uint(-0x7FFFFFFF), 2147483649)
      self.assertEqual(uint(-0x80000000), 2147483648)
      self.assertEqual(uint(-0x80000001), 2147483647)
      self.assertEqual(uint(-0x180000001), 2147483647)
      self.assertEqual(uint(-0x100000001), 4294967295)

      # Parse Tests
      self.assertEqual(uint(String('0.0')), 0)
      self.assertEqual(uint(String('NaN')), 0)
      self.assertEqual(uint(String('-0.0')), 0)
      self.assertEqual(uint(String('Infinity')), 0)
      self.assertEqual(uint(String('1.0')), 1)
      self.assertEqual(uint(String('-1.0')), 4294967295)
      self.assertEqual(uint(String('0xFF1306')), 16716550)
      self.assertEqual(uint(String('1.2315e2')), 123)
      self.assertEqual(uint(String('0x7FFFFFFF')), 2147483647)
      self.assertEqual(uint(String('0x80000000')), 2147483648)
      self.assertEqual(uint(String('0x80000001')), 2147483649)
      self.assertEqual(uint(String('0x180000001')), 2147483649)
      self.assertEqual(uint(String('0x100000001')), 1)
      self.assertEqual(uint(String('-0x7FFFFFFF')), 2147483649)
      self.assertEqual(uint(String('-0x80000000')), 2147483648)
      self.assertEqual(uint(String('-0x80000001')), 2147483647)
      self.assertEqual(uint(String('-0x180000001')), 2147483647)
      self.assertEqual(uint(String('-0x100000001')), 4294967295)

      self.assertEqual(uint(Object()), 0)

   def assertToExponential(self, value, check):
      val = uint(value)
      self._assertToExponential(val, check)

   def test_toExponential(self):
      asrt_1 = ('1', '1.0', '1.00', '1.000', '1.0000', '1.00000', '1.000000',
                '1.0000000', '1.00000000', '1.000000000', '1.0000000000',
                '1.00000000000000000000')

      asrt_0 = ('1e-15', '0.0e-16', '0.00e-16', '0.000e-16', '0.0000e-16',
                '0.00000e-16', '0.000000e-16', '0.0000000e-16',
                '0.00000000e-16', '0.000000000e-16', '0.0000000000e-16',
                '0.00000000000000000000e-16')

      asrt_4294967295 = ('4e+9', '4.3e+9', '4.29e+9', '4.295e+9', '4.2950e+9',
                         '4.29497e+9', '4.294967e+9', '4.2949673e+9',
                         '4.29496730e+9', '4.294967295e+9', '4.2949672950e+9',
                         '4.29496729500000000000e+9')

      asrt_16716550 = ('2e+7', '1.7e+7', '1.67e+7', '1.672e+7', '1.6717e+7',
                       '1.67166e+7', '1.671655e+7', '1.6716550e+7',
                       '1.67165500e+7', '1.671655000e+7', '1.6716550000e+7',
                       '1.67165500000000000000e+7')

      asrt_123 = ('1e+2', '1.2e+2', '1.23e+2', '1.230e+2', '1.2300e+2',
                  '1.23000e+2', '1.230000e+2', '1.2300000e+2',
                  '1.23000000e+2', '1.230000000e+2', '1.2300000000e+2',
                  '1.23000000000000000000e+2')

      asrt_2147483647 = ('2e+9', '2.1e+9', '2.15e+9', '2.147e+9', '2.1475e+9',
                         '2.14748e+9', '2.147484e+9', '2.1474836e+9',
                         '2.14748365e+9', '2.147483647e+9', '2.1474836470e+9',
                         '2.14748364700000000000e+9')

      asrt_2147483648 = ('2e+9', '2.1e+9', '2.15e+9', '2.147e+9', '2.1475e+9',
                         '2.14748e+9', '2.147484e+9', '2.1474836e+9',
                         '2.14748365e+9', '2.147483648e+9', '2.1474836480e+9',
                         '2.14748364800000000000e+9')

      asrt_2147483649 = ('2e+9', '2.1e+9', '2.15e+9', '2.147e+9', '2.1475e+9',
                         '2.14748e+9', '2.147484e+9', '2.1474836e+9',
                         '2.14748365e+9', '2.147483649e+9', '2.1474836490e+9',
                         '2.14748364900000000000e+9')

      self.assertToExponential(true, asrt_1)

      self.assertToExponential(false, asrt_0)
      self.assertToExponential(null, asrt_0)
      self.assertToExponential(undefined, asrt_0)

      self.assertToExponential(String(''), asrt_0)
      self.assertToExponential('', asrt_0)

      self.assertToExponential(String('str'), asrt_0)
      self.assertToExponential('str', asrt_0)

      self.assertToExponential(String('true'), asrt_0)
      self.assertToExponential('true', asrt_0)

      self.assertToExponential(String('false'), asrt_0)
      self.assertToExponential('false', asrt_0)

      self.assertToExponential(Number(0.0), asrt_0)
      self.assertToExponential(0.0, asrt_0)

      self.assertToExponential(NaN, asrt_0)

      self.assertToExponential(Number(-0.0), asrt_0)
      self.assertToExponential(-0.0, asrt_0)

      self.assertToExponential(Infinity, asrt_0)

      self.assertToExponential(Number(1.0), asrt_1)
      self.assertToExponential(1.0, asrt_1)

      self.assertToExponential(Number(-1.0), asrt_4294967295)
      self.assertToExponential(-1.0, asrt_4294967295)

      self.assertToExponential(Number(0xFF1306), asrt_16716550)
      self.assertToExponential(0xFF1306, asrt_16716550)

      self.assertToExponential(Number(1.2315e2), asrt_123)
      self.assertToExponential(1.2315e2, asrt_123)

      self.assertToExponential(Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToExponential(0x7FFFFFFF, asrt_2147483647)

      self.assertToExponential(Number(0x80000000), asrt_2147483648)
      self.assertToExponential(0x80000000, asrt_2147483648)

      self.assertToExponential(Number(0x80000001), asrt_2147483649)
      self.assertToExponential(0x80000001, asrt_2147483649)

      self.assertToExponential(Number(0x180000001), asrt_2147483649)
      self.assertToExponential(0x180000001, asrt_2147483649)

      self.assertToExponential(Number(0x100000001), asrt_1)
      self.assertToExponential(0x100000001, asrt_1)

      self.assertToExponential(Number(-0x7FFFFFFF), asrt_2147483649)
      self.assertToExponential(-0x7FFFFFFF, asrt_2147483649)

      self.assertToExponential(Number(-0x80000000), asrt_2147483648)
      self.assertToExponential(-0x80000000, asrt_2147483648)

      self.assertToExponential(Number(-0x80000001), asrt_2147483647)
      self.assertToExponential(-0x80000001, asrt_2147483647)

      self.assertToExponential(Number(-0x180000001), asrt_2147483647)
      self.assertToExponential(-0x180000001, asrt_2147483647)

      self.assertToExponential(Number(-0x100000001), asrt_4294967295)
      self.assertToExponential(-0x100000001, asrt_4294967295)

      self.assertToExponential(Object(), asrt_0)

      # Parse tests
      self.assertToExponential(String('0.0'), asrt_0)
      self.assertToExponential('0.0', asrt_0)
      self.assertToExponential(String('NaN'), asrt_0)
      self.assertToExponential('NaN', asrt_0)
      self.assertToExponential(String('-0.0'), asrt_0)
      self.assertToExponential('-0.0', asrt_0)
      self.assertToExponential(String('Infinity'), asrt_0)
      self.assertToExponential('Infinity', asrt_0)
      self.assertToExponential(String('1.0'), asrt_1)
      self.assertToExponential('1.0', asrt_1)
      self.assertToExponential(String('-1.0'), asrt_4294967295)
      self.assertToExponential('-1.0', asrt_4294967295)
      self.assertToExponential(String('0xFF1306'), asrt_16716550)
      self.assertToExponential('0xFF1306', asrt_16716550)
      self.assertToExponential(String('1.2315e2'), asrt_123)
      self.assertToExponential('1.2315e2', asrt_123)
      self.assertToExponential(String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToExponential('0x7FFFFFFF', asrt_2147483647)
      self.assertToExponential(String('0x80000000'), asrt_2147483648)
      self.assertToExponential('0x80000000', asrt_2147483648)
      self.assertToExponential(String('0x80000001'), asrt_2147483649)
      self.assertToExponential('0x80000001', asrt_2147483649)
      self.assertToExponential(String('0x180000001'), asrt_2147483649)
      self.assertToExponential('0x180000001', asrt_2147483649)
      self.assertToExponential(String('0x100000001'), asrt_1)
      self.assertToExponential('0x100000001', asrt_1)
      self.assertToExponential(String('-0x7FFFFFFF'), asrt_2147483649)
      self.assertToExponential('-0x7FFFFFFF', asrt_2147483649)
      self.assertToExponential(String('-0x80000000'), asrt_2147483648)
      self.assertToExponential('-0x80000000', asrt_2147483648)
      self.assertToExponential(String('-0x80000001'), asrt_2147483647)
      self.assertToExponential('-0x80000001', asrt_2147483647)
      self.assertToExponential(String('-0x180000001'), asrt_2147483647)
      self.assertToExponential('-0x180000001', asrt_2147483647)
      self.assertToExponential(String('-0x100000001'), asrt_4294967295)
      self.assertToExponential('-0x100000001', asrt_4294967295)

   def assertToFixed(self, value, check):
      val = uint(value)
      self._assertToFixed(val, check)

   def test_toFixed(self):
      asrt_1 = ('1', '1.0', '1.00', '1.000', '1.0000', '1.00000', '1.000000',
                '1.0000000', '1.00000000', '1.000000000', '1.0000000000',
                '1.00000000000000000000')

      asrt_0 = ('0', '0.0', '0.00', '0.000', '0.0000', '0.00000', '0.000000',
                '0.0000000', '0.00000000', '0.000000000', '0.0000000000',
                '0.00000000000000000000')

      asrt_4294967295 = ('4294967295', '4294967295.0', '4294967295.00',
                         '4294967295.000', '4294967295.0000',
                         '4294967295.00000', '4294967295.000000',
                         '4294967295.0000000', '4294967295.00000000',
                         '4294967295.000000000', '4294967295.0000000000',
                         '4294967295.00000000000000000000')

      asrt_16716550 = ('16716550', '16716550.0', '16716550.00',
                       '16716550.000', '16716550.0000', '16716550.00000',
                       '16716550.000000', '16716550.0000000',
                       '16716550.00000000', '16716550.000000000',
                       '16716550.0000000000', '16716550.00000000000000000000')

      asrt_123 = ('123', '123.0', '123.00', '123.000', '123.0000',
                  '123.00000', '123.000000', '123.0000000', '123.00000000',
                  '123.000000000', '123.0000000000',
                  '123.00000000000000000000')

      asrt_2147483647 = ('2147483647', '2147483647.0', '2147483647.00',
                         '2147483647.000', '2147483647.0000',
                         '2147483647.00000', '2147483647.000000',
                         '2147483647.0000000', '2147483647.00000000',
                         '2147483647.000000000', '2147483647.0000000000',
                         '2147483647.00000000000000000000')

      asrt_2147483648 = ('2147483648', '2147483648.0', '2147483648.00',
                         '2147483648.000', '2147483648.0000',
                         '2147483648.00000', '2147483648.000000',
                         '2147483648.0000000', '2147483648.00000000',
                         '2147483648.000000000', '2147483648.0000000000',
                         '2147483648.00000000000000000000')

      asrt_2147483649 = ('2147483649', '2147483649.0', '2147483649.00',
                         '2147483649.000', '2147483649.0000',
                         '2147483649.00000', '2147483649.000000',
                         '2147483649.0000000', '2147483649.00000000',
                         '2147483649.000000000', '2147483649.0000000000',
                         '2147483649.00000000000000000000')

      self.assertToFixed(true, asrt_1)

      self.assertToFixed(false, asrt_0)
      self.assertToFixed(null, asrt_0)
      self.assertToFixed(undefined, asrt_0)

      self.assertToFixed(String(''), asrt_0)
      self.assertToFixed('', asrt_0)

      self.assertToFixed(String('str'), asrt_0)
      self.assertToFixed('str', asrt_0)

      self.assertToFixed(String('true'), asrt_0)
      self.assertToFixed('true', asrt_0)

      self.assertToFixed(String('false'), asrt_0)
      self.assertToFixed('false', asrt_0)

      self.assertToFixed(Number(0.0), asrt_0)
      self.assertToFixed(0.0, asrt_0)

      self.assertToFixed(NaN, asrt_0)

      self.assertToFixed(Number(-0.0), asrt_0)
      self.assertToFixed(-0.0, asrt_0)

      self.assertToFixed(Infinity, asrt_0)

      self.assertToFixed(Number(1.0), asrt_1)
      self.assertToFixed(1.0, asrt_1)

      self.assertToFixed(Number(-1.0), asrt_4294967295)
      self.assertToFixed(-1.0, asrt_4294967295)

      self.assertToFixed(Number(0xFF1306), asrt_16716550)
      self.assertToFixed(0xFF1306, asrt_16716550)

      self.assertToFixed(Number(1.2315e2), asrt_123)
      self.assertToFixed(1.2315e2, asrt_123)

      self.assertToFixed(Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToFixed(0x7FFFFFFF, asrt_2147483647)

      self.assertToFixed(Number(0x80000000), asrt_2147483648)
      self.assertToFixed(0x80000000, asrt_2147483648)

      self.assertToFixed(Number(0x80000001), asrt_2147483649)
      self.assertToFixed(0x80000001, asrt_2147483649)

      self.assertToFixed(Number(0x180000001), asrt_2147483649)
      self.assertToFixed(0x180000001, asrt_2147483649)

      self.assertToFixed(Number(0x100000001), asrt_1)
      self.assertToFixed(0x100000001, asrt_1)

      self.assertToFixed(Number(-0x7FFFFFFF), asrt_2147483649)
      self.assertToFixed(-0x7FFFFFFF, asrt_2147483649)

      self.assertToFixed(Number(-0x80000000), asrt_2147483648)
      self.assertToFixed(-0x80000000, asrt_2147483648)

      self.assertToFixed(Number(-0x80000001), asrt_2147483647)
      self.assertToFixed(-0x80000001, asrt_2147483647)

      self.assertToFixed(Number(-0x180000001), asrt_2147483647)
      self.assertToFixed(-0x180000001, asrt_2147483647)

      self.assertToFixed(Number(-0x100000001), asrt_4294967295)
      self.assertToFixed(-0x100000001, asrt_4294967295)

      self.assertToFixed(Object(), asrt_0)

      # Parse tests
      self.assertToFixed(String('0.0'), asrt_0)
      self.assertToFixed('0.0', asrt_0)
      self.assertToFixed(String('NaN'), asrt_0)
      self.assertToFixed('NaN', asrt_0)
      self.assertToFixed(String('-0.0'), asrt_0)
      self.assertToFixed('-0.0', asrt_0)
      self.assertToFixed(String('Infinity'), asrt_0)
      self.assertToFixed('Infinity', asrt_0)
      self.assertToFixed(String('1.0'), asrt_1)
      self.assertToFixed('1.0', asrt_1)
      self.assertToFixed(String('-1.0'), asrt_4294967295)
      self.assertToFixed('-1.0', asrt_4294967295)
      self.assertToFixed(String('0xFF1306'), asrt_16716550)
      self.assertToFixed('0xFF1306', asrt_16716550)
      self.assertToFixed(String('1.2315e2'), asrt_123)
      self.assertToFixed('1.2315e2', asrt_123)
      self.assertToFixed(String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToFixed('0x7FFFFFFF', asrt_2147483647)
      self.assertToFixed(String('0x80000000'), asrt_2147483648)
      self.assertToFixed('0x80000000', asrt_2147483648)
      self.assertToFixed(String('0x80000001'), asrt_2147483649)
      self.assertToFixed('0x80000001', asrt_2147483649)
      self.assertToFixed(String('0x180000001'), asrt_2147483649)
      self.assertToFixed('0x180000001', asrt_2147483649)
      self.assertToFixed(String('0x100000001'), asrt_1)
      self.assertToFixed('0x100000001', asrt_1)
      self.assertToFixed(String('-0x7FFFFFFF'), asrt_2147483649)
      self.assertToFixed('-0x7FFFFFFF', asrt_2147483649)
      self.assertToFixed(String('-0x80000000'), asrt_2147483648)
      self.assertToFixed('-0x80000000', asrt_2147483648)
      self.assertToFixed(String('-0x80000001'), asrt_2147483647)
      self.assertToFixed('-0x80000001', asrt_2147483647)
      self.assertToFixed(String('-0x180000001'), asrt_2147483647)
      self.assertToFixed('-0x180000001', asrt_2147483647)
      self.assertToFixed(String('-0x100000001'), asrt_4294967295)
      self.assertToFixed('-0x100000001', asrt_4294967295)

   def assertToPrecision(self, value, check):
      val = uint(value)
      self._assertToPrecision(val, check)

   def test_toPrecision(self):
      asrt_1 = ('1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1')

      asrt_0 = ('0e+1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0')

      asrt_4294967295 = ('3.9999999999999996e+9', '4.2e+9', '4.29e+9',
                         '4.294e+9', '4.294899999999999e+9', '4.29496e+9',
                         '4.294967e+9', '4.2949672e+9', '4.29496729e+9',
                         '4294967295', '4294967295', '4294967295')

      asrt_16716550 = ('1e+7', '1.6e+7', '1.6699999999999997e+7', '1.671e+7',
                       '1.6716e+7', '1.67165e+7', '1.671655e+7', '16716550',
                       '16716550', '16716550', '16716550',
                       '16716550.000000002')

      asrt_123 = ('1e+2', '1.2e+2', '123', '123', '123', '123', '123', '123',
                  '123', '123', '123', '123')

      asrt_2147483647 = ('1.9999999999999998e+9', '2.1e+9', '2.14e+9',
                         '2.147e+9', '2.1473999999999998e+9', '2.14748e+9',
                         '2.147483e+9', '2.1474836e+9', '2.14748364e+9',
                         '2147483647', '2147483647', '2147483647')

      asrt_2147483648 = ('1.9999999999999998e+9', '2.1e+9', '2.14e+9',
                         '2.147e+9', '2.1473999999999998e+9', '2.14748e+9',
                         '2.147483e+9', '2.1474836e+9', '2.14748364e+9',
                         '2147483648', '2147483648', '2147483648')

      asrt_2147483649 = ('1.9999999999999998e+9', '2.1e+9', '2.14e+9',
                         '2.147e+9', '2.1473999999999998e+9', '2.14748e+9',
                         '2.147483e+9', '2.1474836e+9', '2.14748364e+9',
                         '2147483649', '2147483649', '2147483649')

      self.assertToPrecision(true, asrt_1)

      self.assertToPrecision(false, asrt_0)
      self.assertToPrecision(null, asrt_0)
      self.assertToPrecision(undefined, asrt_0)

      self.assertToPrecision(String(''), asrt_0)
      self.assertToPrecision('', asrt_0)

      self.assertToPrecision(String('str'), asrt_0)
      self.assertToPrecision('str', asrt_0)

      self.assertToPrecision(String('true'), asrt_0)
      self.assertToPrecision('true', asrt_0)

      self.assertToPrecision(String('false'), asrt_0)
      self.assertToPrecision('false', asrt_0)

      self.assertToPrecision(Number(0.0), asrt_0)
      self.assertToPrecision(0.0, asrt_0)

      self.assertToPrecision(NaN, asrt_0)

      self.assertToPrecision(Number(-0.0), asrt_0)
      self.assertToPrecision(-0.0, asrt_0)

      self.assertToPrecision(Infinity, asrt_0)

      self.assertToPrecision(Number(1.0), asrt_1)
      self.assertToPrecision(1.0, asrt_1)

      self.assertToPrecision(Number(-1.0), asrt_4294967295)
      self.assertToPrecision(-1.0, asrt_4294967295)

      self.assertToPrecision(Number(0xFF1306), asrt_16716550)
      self.assertToPrecision(0xFF1306, asrt_16716550)

      self.assertToPrecision(Number(1.2315e2), asrt_123)
      self.assertToPrecision(1.2315e2, asrt_123)

      self.assertToPrecision(Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToPrecision(0x7FFFFFFF, asrt_2147483647)

      self.assertToPrecision(Number(0x80000000), asrt_2147483648)
      self.assertToPrecision(0x80000000, asrt_2147483648)

      self.assertToPrecision(Number(0x80000001), asrt_2147483649)
      self.assertToPrecision(0x80000001, asrt_2147483649)

      self.assertToPrecision(Number(0x180000001), asrt_2147483649)
      self.assertToPrecision(0x180000001, asrt_2147483649)

      self.assertToPrecision(Number(0x100000001), asrt_1)
      self.assertToPrecision(0x100000001, asrt_1)

      self.assertToPrecision(Number(-0x7FFFFFFF), asrt_2147483649)
      self.assertToPrecision(-0x7FFFFFFF, asrt_2147483649)

      self.assertToPrecision(Number(-0x80000000), asrt_2147483648)
      self.assertToPrecision(-0x80000000, asrt_2147483648)

      self.assertToPrecision(Number(-0x80000001), asrt_2147483647)
      self.assertToPrecision(-0x80000001, asrt_2147483647)

      self.assertToPrecision(Number(-0x180000001), asrt_2147483647)
      self.assertToPrecision(-0x180000001, asrt_2147483647)

      self.assertToPrecision(Number(-0x100000001), asrt_4294967295)
      self.assertToPrecision(-0x100000001, asrt_4294967295)

      self.assertToPrecision(Object(), asrt_0)

      # Parse tests
      self.assertToPrecision(String('0.0'), asrt_0)
      self.assertToPrecision('0.0', asrt_0)
      self.assertToPrecision(String('NaN'), asrt_0)
      self.assertToPrecision('NaN', asrt_0)
      self.assertToPrecision(String('-0.0'), asrt_0)
      self.assertToPrecision('-0.0', asrt_0)
      self.assertToPrecision(String('Infinity'), asrt_0)
      self.assertToPrecision('Infinity', asrt_0)
      self.assertToPrecision(String('1.0'), asrt_1)
      self.assertToPrecision('1.0', asrt_1)
      self.assertToPrecision(String('-1.0'), asrt_4294967295)
      self.assertToPrecision('-1.0', asrt_4294967295)
      self.assertToPrecision(String('0xFF1306'), asrt_16716550)
      self.assertToPrecision('0xFF1306', asrt_16716550)
      self.assertToPrecision(String('1.2315e2'), asrt_123)
      self.assertToPrecision('1.2315e2', asrt_123)
      self.assertToPrecision(String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToPrecision('0x7FFFFFFF', asrt_2147483647)
      self.assertToPrecision(String('0x80000000'), asrt_2147483648)
      self.assertToPrecision('0x80000000', asrt_2147483648)
      self.assertToPrecision(String('0x80000001'), asrt_2147483649)
      self.assertToPrecision('0x80000001', asrt_2147483649)
      self.assertToPrecision(String('0x180000001'), asrt_2147483649)
      self.assertToPrecision('0x180000001', asrt_2147483649)
      self.assertToPrecision(String('0x100000001'), asrt_1)
      self.assertToPrecision('0x100000001', asrt_1)
      self.assertToPrecision(String('-0x7FFFFFFF'), asrt_2147483649)
      self.assertToPrecision('-0x7FFFFFFF', asrt_2147483649)
      self.assertToPrecision(String('-0x80000000'), asrt_2147483648)
      self.assertToPrecision('-0x80000000', asrt_2147483648)
      self.assertToPrecision(String('-0x80000001'), asrt_2147483647)
      self.assertToPrecision('-0x80000001', asrt_2147483647)
      self.assertToPrecision(String('-0x180000001'), asrt_2147483647)
      self.assertToPrecision('-0x180000001', asrt_2147483647)
      self.assertToPrecision(String('-0x100000001'), asrt_4294967295)
      self.assertToPrecision('-0x100000001', asrt_4294967295)

   def assertToString(self, value, check):
      val = uint(value)
      self._assertToString(val, check)

   def test_toString(self):
      asrt_1 = ('1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', 1)

      asrt_0 = ('0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 0)

      asrt_4294967295 = ('11111111111111111111111111111111',
                         '102002022201221111210', '3333333333333333',
                         '32244002423140', '1550104015503', '211301422353',
                         '37777777777', '12068657453', '4294967295',
                         '1904440553', '9ba461593', '535a79888', '2ca5b7463',
                         '1a20dcd80', 'ffffffff', 'a7ffda90', '704he7g3',
                         '4f5aff65', '3723ai4f', '281d55i3', '1fj8b183',
                         '1606k7ib', 'mb994af', 'hek2mgk', 'dnchbnl',
                         'b28jpdl', '8pfgih3', '76beigf', '5qmcpqf',
                         '4q0jto3', '3vvvvvv', '3aokq93', '2qhxjlh',
                         '2br45qa', '1z141z3', 4294967295)

      asrt_16716550 = ('111111110001001100000110', '1011110021210111',
                       '333301030012', '13234412200', '1354143234',
                       '262042204', '77611406', '34407714', '16716550',
                       '9488434', '5721b1a', '3603a66', '2312074', '17030ba',
                       'ff1306', 'bd28c8', '8f4654', '6e5348', '549b7a',
                       '41k104', '357k74', '2dgl6c', '2295im', '1hjlc0',
                       '1af2g6', '14c7ld', 'r5e3i', 'nibsm', 'kj3sa', 'i33th',
                       'fu4o6', 'e35c4', 'chan8', 'b4v5p', '9yakm', 16716550)

      asrt_123 = ('1111011', '11120', '1323', '443', '323', '234', '173',
                  '146', '123', '102', 'a3', '96', '8b', '83', '7b', '74',
                  '6f', '69', '63', '5i', '5d', '58', '53', '4n', '4j', '4f',
                  '4b', '47', '43', '3u', '3r', '3o', '3l', '3i', '3f', 123)

      asrt_2147483647 = ('1111111111111111111111111111111',
                         '12112122212110202101', '1333333333333333',
                         '13344223434042', '553032005531', '104134211161',
                         '17777777777', '5478773671', '2147483647',
                         'a02220281', '4bb2308a7', '282ba4aaa', '1652ca931',
                         'c87e66b7', '7fffffff', '53g7f548', '3928g3h1',
                         '27c57h32', '1db1f927', '140h2d91', 'ikf5bf1',
                         'ebelf95', 'b5gge57', '8jmdnkm', '6oj8ion',
                         '5ehncka', '4clm98f', '3hk7987', '2sb6cs7',
                         '2d09uc1', '1vvvvvv', '1lsqtl1', '1d8xqrp',
                         '15v22um', 'zik0zj', 2147483647)

      asrt_2147483648 = ('10000000000000000000000000000000',
                         '12112122212110202102', '2000000000000000',
                         '13344223434043', '553032005532', '104134211162',
                         '20000000000', '5478773672', '2147483648',
                         'a02220282', '4bb2308a8', '282ba4aab', '1652ca932',
                         'c87e66b8', '80000000', '53g7f549', '3928g3h2',
                         '27c57h33', '1db1f928', '140h2d92', 'ikf5bf2',
                         'ebelf96', 'b5gge58', '8jmdnkn', '6oj8ioo',
                         '5ehnckb', '4clm98g', '3hk7988', '2sb6cs8',
                         '2d09uc2', '2000000', '1lsqtl2', '1d8xqrq',
                         '15v22un', 'zik0zk', 2147483648)

      asrt_2147483649 = ('10000000000000000000000000000001',
                         '12112122212110202110', '2000000000000001',
                         '13344223434044', '553032005533', '104134211163',
                         '20000000001', '5478773673', '2147483649',
                         'a02220283', '4bb2308a9', '282ba4aac', '1652ca933',
                         'c87e66b9', '80000001', '53g7f54a', '3928g3h3',
                         '27c57h34', '1db1f929', '140h2d93', 'ikf5bf3',
                         'ebelf97', 'b5gge59', '8jmdnko', '6oj8iop',
                         '5ehnckc', '4clm98h', '3hk7989', '2sb6cs9',
                         '2d09uc3', '2000001', '1lsqtl3', '1d8xqrr',
                         '15v22uo', 'zik0zl', 2147483649)

      self.assertToString(true, asrt_1)

      self.assertToString(false, asrt_0)
      self.assertToString(null, asrt_0)
      self.assertToString(undefined, asrt_0)

      self.assertToString(String(''), asrt_0)
      self.assertToString('', asrt_0)

      self.assertToString(String('str'), asrt_0)
      self.assertToString('str', asrt_0)

      self.assertToString(String('true'), asrt_0)
      self.assertToString('true', asrt_0)

      self.assertToString(String('false'), asrt_0)
      self.assertToString('false', asrt_0)

      self.assertToString(Number(0.0), asrt_0)
      self.assertToString(0.0, asrt_0)

      self.assertToString(NaN, asrt_0)

      self.assertToString(Number(-0.0), asrt_0)
      self.assertToString(-0.0, asrt_0)

      self.assertToString(Infinity, asrt_0)

      self.assertToString(Number(1.0), asrt_1)
      self.assertToString(1.0, asrt_1)

      self.assertToString(Number(-1.0), asrt_4294967295)
      self.assertToString(-1.0, asrt_4294967295)

      self.assertToString(Number(0xFF1306), asrt_16716550)
      self.assertToString(0xFF1306, asrt_16716550)

      self.assertToString(Number(1.2315e2), asrt_123)
      self.assertToString(1.2315e2, asrt_123)

      self.assertToString(Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToString(0x7FFFFFFF, asrt_2147483647)

      self.assertToString(Number(0x80000000), asrt_2147483648)
      self.assertToString(0x80000000, asrt_2147483648)

      self.assertToString(Number(0x80000001), asrt_2147483649)
      self.assertToString(0x80000001, asrt_2147483649)

      self.assertToString(Number(0x180000001), asrt_2147483649)
      self.assertToString(0x180000001, asrt_2147483649)

      self.assertToString(Number(0x100000001), asrt_1)
      self.assertToString(0x100000001, asrt_1)

      self.assertToString(Number(-0x7FFFFFFF), asrt_2147483649)
      self.assertToString(-0x7FFFFFFF, asrt_2147483649)

      self.assertToString(Number(-0x80000000), asrt_2147483648)
      self.assertToString(-0x80000000, asrt_2147483648)

      self.assertToString(Number(-0x80000001), asrt_2147483647)
      self.assertToString(-0x80000001, asrt_2147483647)

      self.assertToString(Number(-0x180000001), asrt_2147483647)
      self.assertToString(-0x180000001, asrt_2147483647)

      self.assertToString(Number(-0x100000001), asrt_4294967295)
      self.assertToString(-0x100000001, asrt_4294967295)

      self.assertToString(Object(), asrt_0)

      # Parse tests
      self.assertToString(String('0.0'), asrt_0)
      self.assertToString('0.0', asrt_0)
      self.assertToString(String('NaN'), asrt_0)
      self.assertToString('NaN', asrt_0)
      self.assertToString(String('-0.0'), asrt_0)
      self.assertToString('-0.0', asrt_0)
      self.assertToString(String('Infinity'), asrt_0)
      self.assertToString('Infinity', asrt_0)
      self.assertToString(String('1.0'), asrt_1)
      self.assertToString('1.0', asrt_1)
      self.assertToString(String('-1.0'), asrt_4294967295)
      self.assertToString('-1.0', asrt_4294967295)
      self.assertToString(String('0xFF1306'), asrt_16716550)
      self.assertToString('0xFF1306', asrt_16716550)
      self.assertToString(String('1.2315e2'), asrt_123)
      self.assertToString('1.2315e2', asrt_123)
      self.assertToString(String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToString('0x7FFFFFFF', asrt_2147483647)
      self.assertToString(String('0x80000000'), asrt_2147483648)
      self.assertToString('0x80000000', asrt_2147483648)
      self.assertToString(String('0x80000001'), asrt_2147483649)
      self.assertToString('0x80000001', asrt_2147483649)
      self.assertToString(String('0x180000001'), asrt_2147483649)
      self.assertToString('0x180000001', asrt_2147483649)
      self.assertToString(String('0x100000001'), asrt_1)
      self.assertToString('0x100000001', asrt_1)
      self.assertToString(String('-0x7FFFFFFF'), asrt_2147483649)
      self.assertToString('-0x7FFFFFFF', asrt_2147483649)
      self.assertToString(String('-0x80000000'), asrt_2147483648)
      self.assertToString('-0x80000000', asrt_2147483648)
      self.assertToString(String('-0x80000001'), asrt_2147483647)
      self.assertToString('-0x80000001', asrt_2147483647)
      self.assertToString(String('-0x180000001'), asrt_2147483647)
      self.assertToString('-0x180000001', asrt_2147483647)
      self.assertToString(String('-0x100000001'), asrt_4294967295)
      self.assertToString('-0x100000001', asrt_4294967295)


class VectorTests(as3libTestCase):
   def test_class(self):
      raise TestNotImplemented

   def test_coercion(self):
      raise TestNotImplemented

   def test_concat(self):
      a_bool = Vector.Boolean([True, False])
      b_bool = Vector.Boolean([False, True, False])
      self.assertEach(a_bool.concat(b_bool), (True, False, False, True, False))

      class Superclass:
         ...

      class Subclass(Superclass):
         ...

      a_class = Vector([], type=Superclass)
      a_class.length = 2
      a_class[0] = Superclass()
      a_class[1] = Subclass()

      b_class = Vector([], type=Subclass)
      b_class.length = 1
      b_class[0] = Subclass()

      c_class = a_class.concat(b_class)

      self.assertEqual(c_class.length, 3)
      self.assertType(c_class[0], Superclass)
      self.assertType(c_class[1], Subclass)
      self.assertType(c_class[2], Subclass)

      c_class_flipped = b_class.concat(Vector([Subclass()], type=Subclass))

      self.assertEqual(c_class_flipped.length, 2)
      self.assertType(c_class_flipped[0], Subclass)
      self.assertType(c_class_flipped[1], Subclass)

      class Interface:
         ...
      raise TestNotImplemented
      '''
      class Implementer implements Interface {

      }

      trace("/// var a_iface: Vector.<Interface> = new <Interface>[];");
      var a_iface:Vector.<Interface> = new <Interface>[];

      trace("/// a_iface.length = 1;");
      a_iface.length = 1;

      trace("/// a_iface[0] = new Implementer();");
      a_iface[0] = new Implementer();

      trace("/// var b_iface: Vector.<Implementer> = new <Implementer>[];");
      var b_iface:Vector.<Implementer> = new <Implementer>[];

      trace("/// b_iface.length = 1;");
      b_iface.length = 1;

      trace("/// b_iface[0] = new Implementer();");
      b_iface[0] = new Implementer();

      trace("/// var c_iface = a_iface.concat(b_iface);");
      var c_iface = a_iface.concat(b_iface);

      trace("/// (contents of c_iface...)");
      trace_vector(c_iface);

      trace("/// var a_int: Vector.<int> = new <int>[1,2];");
      var a_int:Vector.<int> = new <int>[1,2];

      trace("/// var b_int: Vector.<int> = new <int>[5,16];");
      var b_int:Vector.<int> = new <int>[5,16];

      trace("/// var c_int = a_int.concat(b_int);");
      var c_int = a_int.concat(b_int);

      trace("/// (contents of c_int...)");
      trace_vector(c_int);

      trace("/// var a_number: Vector.<Number> = new <Number>[1,2,3,4];");
      var a_number:Vector.<Number> = new <Number>[1,2,3,4];

      trace("/// var b_number: Vector.<Number> = new <Number>[5, NaN, -5, 0];");
      var b_number:Vector.<Number> = new <Number>[5, NaN, -5, 0];

      trace("/// var c_number = a_number.concat(b_number);");
      var c_number = a_number.concat(b_number);

      trace("/// (contents of c_number...)");
      trace_vector(c_number);

      trace("/// var a_string: Vector.<String> = new <String>[\"a\",\"c\",\"d\",\"f\"];");
      var a_string:Vector.<String> = new <String>["a", "c", "d", "f"];

      trace("/// var b_string: Vector.<String> = new <String>[\"986\",\"B4\",\"Q\",\"rrr\"];");
      var b_string:Vector.<String> = new <String>["986", "B4", "Q", "rrr"];

      trace("/// var c_string = a_string.concat(b_string);");
      var c_string = a_string.concat(b_string);

      trace("/// (contents of c_string...)");
      trace_vector(c_string);

      trace("/// var a_uint: Vector.<uint> = new <uint>[1,2];");
      var a_uint:Vector.<uint> = new <uint>[1,2];

      trace("/// var b_uint: Vector.<uint> = new <uint>[5,16];");
      var b_uint:Vector.<uint> = new <uint>[5,16];

      trace("/// var c_uint = a_uint.concat(b_uint);");
      var c_uint = a_uint.concat(b_uint);

      trace("/// (contents of c_uint...)");
      trace_vector(c_uint);

      trace("/// var a_vector:Vector.<Vector.<int>> = new <Vector.<int>>[new <int>[1,2]];");
      var a_vector:Vector.<Vector.<int>> = new <Vector.<int>>[new <int>[1,2]];

      trace("/// var b_vector:Vector.<Vector.<int>> = new <Vector.<int>>[new <int>[5,16]];");
      var b_vector:Vector.<Vector.<int>> = new <Vector.<int>>[new <int>[5,16]];

      trace("/// var c_vector = a_vector.concat(b_vector)");
      var c_vector = a_vector.concat(b_vector);

      trace("/// (contents of c_vector...)");
      trace_vector(c_vector);
      2026-01-04T02:34:08.279886Z  INFO avm_trace: /// var a_iface: Vector.<Interface> = new <Interface>[];
      2026-01-04T02:34:08.279901Z  INFO avm_trace: /// a_iface.length = 1;
      2026-01-04T02:34:08.279913Z  INFO avm_trace: /// a_iface[0] = new Implementer();
      2026-01-04T02:34:08.279926Z  INFO avm_trace: /// var b_iface: Vector.<Implementer> = new <Implementer>[];
      2026-01-04T02:34:08.279942Z  INFO avm_trace: /// b_iface.length = 1;
      2026-01-04T02:34:08.279949Z  INFO avm_trace: /// b_iface[0] = new Implementer();
      2026-01-04T02:34:08.279956Z  INFO avm_trace: /// var c_iface = a_iface.concat(b_iface);
      2026-01-04T02:34:08.279966Z  INFO avm_trace: /// (contents of c_iface...)
      2026-01-04T02:34:08.279974Z  INFO avm_trace: ///length:  2
      2026-01-04T02:34:08.279984Z  INFO avm_trace: [object Implementer]
      2026-01-04T02:34:08.279995Z  INFO avm_trace: [object Implementer]
      2026-01-04T02:34:08.280006Z  INFO avm_trace: /// var a_int: Vector.<int> = new <int>[1,2];
      2026-01-04T02:34:08.280019Z  INFO avm_trace: /// var b_int: Vector.<int> = new <int>[5,16];
      2026-01-04T02:34:08.280031Z  INFO avm_trace: /// var c_int = a_int.concat(b_int);
      2026-01-04T02:34:08.280042Z  INFO avm_trace: /// (contents of c_int...)
      2026-01-04T02:34:08.280056Z  INFO avm_trace: ///length:  4
      2026-01-04T02:34:08.280065Z  INFO avm_trace: 1
      2026-01-04T02:34:08.280072Z  INFO avm_trace: 2
      2026-01-04T02:34:08.280078Z  INFO avm_trace: 5
      2026-01-04T02:34:08.280085Z  INFO avm_trace: 16
      2026-01-04T02:34:08.280091Z  INFO avm_trace: /// var a_number: Vector.<Number> = new <Number>[1,2,3,4];
      2026-01-04T02:34:08.280104Z  INFO avm_trace: /// var b_number: Vector.<Number> = new <Number>[5, NaN, -5, 0];
      2026-01-04T02:34:08.280118Z  INFO avm_trace: /// var c_number = a_number.concat(b_number);
      2026-01-04T02:34:08.280129Z  INFO avm_trace: /// (contents of c_number...)
      2026-01-04T02:34:08.280142Z  INFO avm_trace: ///length:  8
      2026-01-04T02:34:08.280149Z  INFO avm_trace: 1
      2026-01-04T02:34:08.280156Z  INFO avm_trace: 2
      2026-01-04T02:34:08.280162Z  INFO avm_trace: 3
      2026-01-04T02:34:08.280169Z  INFO avm_trace: 4
      2026-01-04T02:34:08.280176Z  INFO avm_trace: 5
      2026-01-04T02:34:08.280183Z  INFO avm_trace: NaN
      2026-01-04T02:34:08.280428Z  INFO avm_trace: -5
      2026-01-04T02:34:08.280453Z  INFO avm_trace: 0
      2026-01-04T02:34:08.280460Z  INFO avm_trace: /// var a_string: Vector.<String> = new <String>["a","c","d","f"];
      2026-01-04T02:34:08.280483Z  INFO avm_trace: /// var b_string: Vector.<String> = new <String>["986","B4","Q","rrr"];
      2026-01-04T02:34:08.280490Z  INFO avm_trace: /// var c_string = a_string.concat(b_string);
      2026-01-04T02:34:08.280496Z  INFO avm_trace: /// (contents of c_string...)
      2026-01-04T02:34:08.280502Z  INFO avm_trace: ///length:  8
      2026-01-04T02:34:08.280506Z  INFO avm_trace: a
      2026-01-04T02:34:08.280510Z  INFO avm_trace: c
      2026-01-04T02:34:08.280514Z  INFO avm_trace: d
      2026-01-04T02:34:08.280518Z  INFO avm_trace: f
      2026-01-04T02:34:08.280521Z  INFO avm_trace: 986
      2026-01-04T02:34:08.280525Z  INFO avm_trace: B4
      2026-01-04T02:34:08.280529Z  INFO avm_trace: Q
      2026-01-04T02:34:08.280533Z  INFO avm_trace: rrr
      2026-01-04T02:34:08.280537Z  INFO avm_trace: /// var a_uint: Vector.<uint> = new <uint>[1,2];
      2026-01-04T02:34:08.280545Z  INFO avm_trace: /// var b_uint: Vector.<uint> = new <uint>[5,16];
      2026-01-04T02:34:08.280550Z  INFO avm_trace: /// var c_uint = a_uint.concat(b_uint);
      2026-01-04T02:34:08.280556Z  INFO avm_trace: /// (contents of c_uint...)
      2026-01-04T02:34:08.280562Z  INFO avm_trace: ///length:  4
      2026-01-04T02:34:08.280566Z  INFO avm_trace: 1
      2026-01-04T02:34:08.280580Z  INFO avm_trace: 2
      2026-01-04T02:34:08.280583Z  INFO avm_trace: 5
      2026-01-04T02:34:08.280587Z  INFO avm_trace: 16
      2026-01-04T02:34:08.280591Z  INFO avm_trace: /// var a_vector:Vector.<Vector.<int>> = new <Vector.<int>>[new <int>[1,2]];
      2026-01-04T02:34:08.280601Z  INFO avm_trace: /// var b_vector:Vector.<Vector.<int>> = new <Vector.<int>>[new <int>[5,16]];
      2026-01-04T02:34:08.280609Z  INFO avm_trace: /// var c_vector = a_vector.concat(b_vector)
      2026-01-04T02:34:08.280614Z  INFO avm_trace: /// (contents of c_vector...)
      2026-01-04T02:34:08.280619Z  INFO avm_trace: ///length:  2
      2026-01-04T02:34:08.280640Z  INFO avm_trace: 1,2
      2026-01-04T02:34:08.280647Z  INFO avm_trace: 5,16
      '''

   def test_constructor(self):
      a_bool = Vector.Boolean(2)
      self.assertEqual(a_bool.length, 2)
      self.assertFalse(a_bool.fixed)

      b_bool = Vector.Boolean(3, True)
      self.assertEqual(b_bool.length, 3)
      self.assertTrue(b_bool.fixed)

      c_bool = Vector.Boolean()
      self.assertEqual(c_bool.length, 0)
      self.assertFalse(c_bool.fixed)

      class Superclass:
         ...

      class Subclass(Superclass):
         ...

      a0_class = Superclass()
      a1_class = Subclass()

      a_class = Vector(2, type=Superclass)
      self.assertEqual(a_class.length, 2)
      self.assertFalse(a_class.fixed)

      b_class = Vector(3, True, type=Superclass)
      self.assertEqual(b_class.length, 3)
      self.assertTrue(b_class.fixed)

      c_class = Vector(type=Superclass)
      self.assertEqual(c_class.length, 0)
      self.assertFalse(c_class.fixed)

      a_int = Vector.int(2)
      self.assertEqual(a_int.length, 2)
      self.assertFalse(a_int.fixed)

      b_int = Vector.int(3, True)
      self.assertEqual(b_int.length, 3)
      self.assertTrue(b_int.fixed)

      c_int = Vector.int()
      self.assertEqual(c_int.length, 0)
      self.assertFalse(c_int.fixed)

      a_number = Vector.Number(2)
      self.assertEqual(a_number.length, 2)
      self.assertFalse(a_number.fixed)

      b_number = Vector.Number(3, True)
      self.assertEqual(b_number.length, 3)
      self.assertTrue(b_number.fixed)

      c_number = Vector.Number()
      self.assertEqual(c_number.length, 0)
      self.assertFalse(c_number.fixed)

      a_string = Vector.String(2)
      self.assertEqual(a_string.length, 2)
      self.assertFalse(a_string.fixed)

      b_string = Vector.String(3, True)
      self.assertEqual(b_string.length, 3)
      self.assertTrue(b_string.fixed)

      c_string = Vector.String()
      self.assertEqual(c_string.length, 0)
      self.assertFalse(c_string.fixed)

      a_uint = Vector.uint(2)
      self.assertEqual(a_uint.length, 2)
      self.assertFalse(a_uint.fixed)

      b_uint = Vector.uint(3, True)
      self.assertEqual(b_uint.length, 3)
      self.assertTrue(b_uint.fixed)

      c_uint = Vector.uint()
      self.assertEqual(c_uint.length, 0)
      self.assertFalse(c_uint.fixed)

      raise MethodNotImplemented('Vector.<Vector>')
      a_vector = Vector(2, type=Vector.int)
      self.assertEqual(a_vector.length, 2)
      self.assertFalse(a_vector.fixed)

      b_vector = Vector.uint(3, True, type=Vector.int)
      self.assertEqual(b_vector.length, 3)
      self.assertTrue(b_vector.fixed)

      c_vector = Vector.uint(type=Vector.int)
      self.assertEqual(c_vector.length, 0)
      self.assertFalse(c_vector.fixed)

   def test_enumeration(self):
      a = Vector.int([1, 2, 3, 4, 5])
      self.assertIter(a, [0, 1, 2, 3, 4])
      self.assertEach(a, [1, 2, 3, 4, 5])

   def test_every(self):
      raise TestNotImplemented

   def test_filter(self):
      raise TestNotImplemented

   def test_null_callback(self):
      # TODO: Make sure this is correct
      v = Vector.int()
      v.push(1)
      self.assertTrue(v.every(null))
      self.assertIs(v.filter(null), None)
      self.assertEqual(v.forEach(null), undefined)
      self.assertEqual(v.map(null), 0)
      self.assertFalse(v.some(null))


class WTFJSTests(as3libTestCase):
   # These tests are inspired by various documents called WTFJS. These things
   # don't make sense at first glance.
   # https://github.com/denysdovhan/wtfjs
   def test_banana(self):
      self.assertEqual(String('b') + String('a') + + String('a') + String('a'), 'baNaNa')

   def test_not_array(self):
      self.assertEqual(+Array(), 0)
      self.assertEqual(not Array(), false)
      self.assertTrue(Array() == (not Array()))

      # Booleans
      self.assertFalse(true == Array())
      self.assertFalse(true == (not Array()))
      self.asserttrue(false == Array())
      self.assertTrue(false == (not Array()))

   def test_string_bools(self):
      self.assertEqual(not not String('false'), not not String('true'))
      self.assertIs(not not String('false'), not not String('true'))

   def test_fail(self):
      # Original (![] + [])[+[]] + (![] + [])[+!+[]] + ([![]] + [][[]])[+!+[] + [+[]]] + (![] + [])[!+[] + !+[]];
      self.assertEqual((not Array() + Array())[+Array()] + (not Array() + Array())[+(not+Array())] + (Array(not Array()) + Array()[Array()])[+(not+Array()) + Array(+Array)] + (not Array() + Array())[not+Array() + (not+Array())], 'fail')

   def test_truthy_arry(self):
      self.assertTrue(not not Array())
      self.assertFalse(Array())

   def test_falsy_null(self):
      self.assertFalse(not not null)
      self.assertFalse(null == false)

   def test_add_array(self):
      self.assertEqual(Array(1, 2, 3) + Array(4, 5, 6), '1,2,34,5,6')

   def test_array_equality(self):
      '''
      [] == ''   // -> true
      [] == 0    // -> true
      [''] == '' // -> true
      [0] == 0   // -> true
      [0] == ''  // -> false
      [''] == 0  // -> true

      [null] == ''      // true
      [null] == 0       // true
      [undefined] == '' // true
      [undefined] == 0  // true

      [[]] == 0  // true
      [[]] == '' // true

      [[[[[[]]]]]] == '' // true
      [[[[[[]]]]]] == 0  // true

      [[[[[[ null ]]]]]] == 0  // true
      [[[[[[ null ]]]]]] == '' // true

      [[[[[[ undefined ]]]]]] == 0  // true
      [[[[[[ undefined ]]]]]] == '' // true
      '''
      self.assertEqual(Array(), String())
      self.assertEqual(Array(), Number(0))
      self.assertEqual(Array(['']), String())
      self.assertEqual(Array([0]), Number(0))
      self.assertNotEqual(Array([0]), String())
      self.assertEqual(Array(['']), Number(0))

      self.assertEqual(Array([null]), String())
      self.assertEqual(Array([null]), Number(0))
      self.assertEqual(Array([undefined]), String())
      self.assertEqual(Array([undefined]), Number(0))

      self.assertEqual(Array(Array(Array(Array(Array(Array()))))), String())
      self.assertEqual(Array(Array(Array(Array(Array(Array()))))), Number(0))

      self.assertEqual(Array(Array(Array(Array(Array(Array(null)))))), String())
      self.assertEqual(Array(Array(Array(Array(Array(Array(null)))))), Number(0))

      self.assertEqual(Array(Array(Array(Array(Array(Array(undefined)))))), String())
      self.assertEqual(Array(Array(Array(Array(Array(Array(undefined)))))), Number(0))

   def test_parseInt_quirks(self):
      self.assertNaN(as3lib.parseInt('f*ck'))
      self.assertEqual(as3lib.parseInt('f*ck', 16), 15)
      self.assertNaN(as3lib.parseInt('Infinity', 10))
      self.assertNaN(as3lib.parseInt('Infinity', 18))
      self.assertEqual(as3lib.parseInt('Infinity', 19), 18)
      self.assertEqual(as3lib.parseInt('Infinity', 24), 151176378)
      self.assertEqual(as3lib.parseInt('Infinity', 29), 385849803)
      self.assertEqual(as3lib.parseInt('Infinity', 30), 13693557269)
      self.assertEqual(as3lib.parseInt('Infinity', 34), 28872273981)
      self.assertEqual(as3lib.parseInt('Infinity', 35), 1201203301724)
      self.assertNaN(as3lib.parseInt('Infinity', 37))
      self.assertEqual(as3lib.parseInt(null, 24), 23)
      self.assertEqual(as3lib.parseInt('06'), 6)
      # parseInt("08"); // 8 if support ECMAScript 5
      # parseInt("08"); // 0 if not support ECMAScript 5
      self.assertEqual(as3lib.parseInt(0.000001), 0)
      self.assertEqual(as3lib.parseInt(0.0000001), 1)
      self.assertEqual(as3lib.parseInt(1 / 1999999), 5)

   def test_funny_math(self):
      '''
       3  - 1  // -> 2
       3  + 1  // -> 4
      '3' - 1  // -> 2
      '3' + 1  // -> '31'

      '' + '' // -> ''
      [] + [] // -> ''
      {} + [] // -> 0
      [] + {} // -> '[object Object]'
      {} + {} // -> '[object Object][object Object]'

      '222' - -'111' // -> 333

      [4] * [4]       // -> 16
      [] * []         // -> 0
      [4, 4] * [4, 4] // NaN
      '''
      self.assertEqual(Number(3) - Number(1), Number(2))
      self.assertEqual(Number(3) + Number(1), Number(4))
      self.assertEqual(String('3') - Number(1), Number(2))
      self.assertEqual(String('3') + Number(1), String('31'))

      self.assertEqual(String('') + String(''), String(''))
      self.assertEqual(Array() + Array(), String(''))
      self.assertEqual(Object() + Array(), Number(0))
      self.assertEqual(Array() + Object(), String('[object Object]'))
      self.assertEqual(Object() + Object(), String('[object Object][object Object]'))

      self.assertEqual(String('222') - -String('111'), Number('333'))

      self.assertEqual(Array([4]) * Array([4]), Number(16))
      self.assertEqual(Array() * Array(), Number(0))
      self.assertEqual(Array([4, 4]) * Array([4, 4]), NaN)

   def test_yield_self(self):
      # The syntax here is a little bit different but it still works
      def f():
         yield f

      self.assertIs(next(next(next(next(next(f())())())())()), f)

   def test_minmax(self):
      self.assertEqual(Math.min(), Infinity)
      self.assertEqual(Math.max(), -Infinity)
      self.assertLess(Math.max(), Math.min())

   def test_infinite_timeout(self):
      # This will execute immediately because Infinity does not fit into a
      # 32bit uint
      # TODO: console.log
      # setTimeout(() => console.log("called"), Infinity)
      # TODO: Make this an assert
      setTimeout(print, Infinity, "called")


class XMLTests(as3libTestCase):
   ...
