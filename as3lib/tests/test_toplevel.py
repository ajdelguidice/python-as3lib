# Most of these test cases are based on ones made by the ruffle.rs project
# https://github.com/ruffle-rs/ruffle

import as3lib
from as3lib import (ArgumentError, Error, EvalError, Math, RangeError,
                    ReferenceError, URIError, VerifyError)
from as3lib._toplevel.Keywords import each
from as3lib.flash.errors import (EOFError, IllegalOperationError,
                                 InvalidSWFError, IOError, MemoryError,
                                 ScriptTimeoutError, StackOverflowError)
from as3lib.flash.utils import setTimeout
from as3lib.tests import as3libTestCase, TestNotImplemented, MethodNotImplemented

# TODO: Clear prototypes after every test

class ArrayTests(as3libTestCase):
   # NOTE: prototype is required for some tests
   def assertIndex(self, index, length, hasprop):
      arr = as3lib.Array()
      arr[index] = 0
      self.assertEqual(arr.length, length)
      self.assertEqual(arr.hasOwnProperty(index), hasprop)
      self.assertEqual(arr[index], 0)

   def test_access(self):
      # TODO: Add more of this test
      a = as3lib.Array('a', 'b', 'c')
      self.assertEqual(a[0], 'a')
      self.assertEqual(a[1], 'b')
      self.assertEqual(a[2], 'c')

      a = as3lib.Array(5)
      self.assertEqual(a.length, 5)
      a[0] = 'First'
      a[2] = 'Second'
      a[3] = 'Third'
      self.assertEqual(a.removeAt(1), as3lib.undefined)
      self.assertEqual(a.length, 4)

   def test_concat(self):
      a = as3lib.Array('a', 'b', 'c')
      b = as3lib.Array('d', 'e', 'f')
      c = a.concat(b)
      self.assertEqual(c, ['a', 'b', 'c', 'd', 'e', 'f'])
      d = a.concat('d', 'e', 'f')
      self.assertEqual(d, ['a', 'b', 'c', 'd', 'e', 'f'])
      e = a.concat('g', b, 'h')
      self.assertEqual(e, ['a', 'b', 'c', 'g', 'd', 'e', 'f', 'h'])
      f = a.concat(b, b)
      self.assertEqual(f, ['a', 'b', 'c', 'd', 'e', 'f', 'd', 'e', 'f'])
      g = a.concat(as3lib.null, as3lib.undefined)
      self.assertEqual(g, ['a', 'b', 'c', as3lib.null, as3lib.undefined])

   def test_constructor(self):
      self.assertEqual(as3lib.Array().length, 0)
      self.assertEqual(as3lib.Array(5).length, 5)
      self.assertEqual(as3lib.Array('5').length, 1)
      self.assertEqual(as3lib.Array(5, 6).length, 2)
      self.assertEqual(as3lib.Array(5, 'abc').length, 2)

   def test_delete(self):
      raise MethodNotImplemented('delete')
      # TODO: Add a delete function that returns True if successful
      a = as3lib.Array('a', 'b', 'c')

      # Delete a[1]
      self.assertTrue(as3lib.delete(a[1]))
      self.assertEqual(a.length, 3)
      self.assertArray(a, ['a', as3lib.undefined, 'c', as3lib.undefined])
      self.assertFalse(a.hasOwnProperty(1))

      # Delete a[2]
      self.assertTrue(as3lib.delete(a[2]))
      self.assertEqual(a.length, 3)
      self.assertArray(a, ['a', as3lib.undefined, as3lib.undefined, as3lib.undefined])
      self.assertFalse(a.hasOwnProperty(2))

      # Delete a[3]
      self.assertTrue(as3lib.delete(a[3]))
      self.assertEqual(a.length, 3)
      self.assertArray(a, ['a', as3lib.undefined, as3lib.undefined, as3lib.undefined])
      self.assertFalse(a.hasOwnProperty(3))

      # Delete a[4]
      self.assertTrue(as3lib.delete(a[4]))
      self.assertEqual(a.length, 3)
      self.assertArray(a, ['a', as3lib.undefined, as3lib.undefined, as3lib.undefined])
      self.assertFalse(a.hasOwnProperty(4))

   def test_enumeration(self):
      # NOTE: This test seems to prove that Arrays act more like python dictionaries
      a = as3lib.Array(1, 2, 3, 4, 5)
      self.assertArray(a, [1, 2, 3, 4, 5])

      array = as3lib.Array(5)
      array[0] = 'elem0'
      array[4] = 'elem4'
      array.prop = 'property'
      array[-1] = 'elem negative one'

      # TODO: Validate order

      # TODO: This will fail until array is rewritten
      self.assertIter(array, [0, 4], 4)

      self.assertEach(array, ['elem0', 'elem4'], 4)

   def test_enumeration_elements(self):
      a = as3lib.Array(1, 2, 3, 4, 5)
      a.elem = 'test'

      self.assertEach(a, [1, 2, 3, 4, 5, 'test'], 6)

      self.assertTrue(a.propertyIsEnumerable('elem'))
      self.assertFalse(a.propertyIsEnumerable('another'))
      self.assertFalse(a.propertyIsEnumerable('random'))
      self.assertTrue(a.propertyIsEnumerable('3'))
      self.assertFalse(a.propertyIsEnumerable('7'))

   def test_every(self):
      a = as3lib.Array(5, 3, 1, 9, 16)
      self.assertFalse(a.every(lambda val, i, j: val == 5))
      self.assertTrue(a.every(lambda val, i, j: val != 20))

      b = as3lib.Array()
      self.assertTrue(b.every(lambda val, i, j: val == 5))

   def test_filter(self):
      a = as3lib.Array(5, 3, 1, 9, 16)
      b = a.filter(lambda val, i, j: val <= 5)
      self.assertEqual(b, [5, 3, 1])

   def test_forEach(self):
      a = as3lib.Array(5, 'abc')

      def test(val, index, array):
         self.assertTrue(val in a)
         self.assertLess(index, len(a))
         self.assertIdentical(array, a)

      a.forEach(test)

   def test_hasOwnProperty(self):
      a = as3lib.Array(5)

      as3lib.Array.prototype[3] = 'works'
      self.assertFalse(a.hasOwnProperty('2'))
      self.assertFalse(a.hasOwnProperty('3'))

      a[3] = 'nohole'
      self.assertFalse(a.hasOwnProperty('2'))
      self.assertTrue(a.hasOwnProperty('3'))

   def test_holes(self):
      a = as3lib.Array(5)

      as3lib.Array.prototype[3] = 'works'
      self.assertEqual(a[2], as3lib.undefined)
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
      a = as3lib.Array(5, '5', 3, False, 4, 5, as3lib.undefined, 9)
      self.assertEqual(a.indexOf(5), 0)
      self.assertEqual(a.indexOf(5, 1), 5)
      self.assertEqual(a.indexOf(5, 2), 5)
      self.assertEqual(a.indexOf(5, 6), -1)
      self.assertEqual(a.indexOf(5, 10), -1)
      self.assertEqual(a.indexOf(True), -1)
      self.assertEqual(a.indexOf(as3lib.undefined), 6)
      self.assertEqual(a.indexOf('5'), 1)

   def test_join(self):
      a = as3lib.Array('a', 'b', 'c')
      b = as3lib.Array(1, 2, 3)
      c = as3lib.Array(a, b)
      d = as3lib.Array('str', 123, as3lib.undefined, as3lib.null, as3lib.true, as3lib.false)
      self.assertEqual(a.join(), 'a,b,c')
      self.assertEqual(b.join(), '1,2,3')
      self.assertEqual(c.join(), 'a,b,c,1,2,3')
      self.assertEqual(c.join(as3lib.undefined), 'a,b,c,1,2,3')
      self.assertEqual(c.join(as3lib.null), 'a,b,cnull1,2,3')
      self.assertEqual(c.join(as3lib.false), 'a,b,cfalse1,2,3')
      self.assertEqual(a.join(as3lib.NaN), 'aNaNbNaNc')
      self.assertEqual(b.join(5), '15253')
      self.assertEqual(c.join(' + '), 'a,b,c + 1,2,3')
      self.assertEqual(c.join(b), 'a,b,c1,2,31,2,3')
      self.assertEqual(d.join('!'), 'str!123!!!true!false')

   def test_lastIndexOf(self):
      a = as3lib.Array(5, '5', 3, False, 4, 5, as3lib.undefined, 9)
      self.assertEqual(a.lastIndexOf(5), 5)
      self.assertEqual(a.lastIndexOf(5, 1), 0)
      self.assertEqual(a.lastIndexOf(5, 2), 0)
      self.assertEqual(a.lastIndexOf(5, 6), 5)
      self.assertEqual(a.lastIndexOf(5, 10), 5)
      self.assertEqual(a.lastIndexOf(True), -1)
      self.assertEqual(a.lastIndexOf(as3lib.undefined), 6)
      self.assertEqual(a.lastIndexOf('5'), 1)

   def test_length(self):
      self.assertEqual(as3lib.Array().length, 0)
      self.assertEqual(as3lib.Array(0, 1, 2, 3, 4).length, 5)
      self.assertEqual(as3lib.Array(as3lib.undefined).length, 1)
      a = as3lib.Array(0, 1, 2)
      self.assertEqual(a.length, 3)
      a.length = 5
      self.assertEqual(a.length, 5)
      self.assertEqual(a.toString(), '0,1,2,,')
      a.length = 0
      self.assertEqual(a.length, 0)
      self.assertEqual(a.toString(), '')

   def test_literal(self):
      a = as3lib.Array('a', 'b', 'c')
      self.assertEqual(a[0], 'a')
      self.assertEqual(a[1], 'b')
      self.assertEqual(a[2], 'c')

   def test_map(self):
      a = as3lib.Array(5, 3, 1, 9, 16)
      b = a.map(lambda val, i, j: val + 1)
      self.assertEqual(b, [6, 4, 2, 10, 17])

   def test_pop(self):
      a = as3lib.Array(5)
      a[1] = 'other_test'
      a[2] = 'test'
      as3lib.Array.prototype[3] = 'works'

      self.assertEqual(a.toString(), ',other_test,test,works,')
      self.assertEqual(a.length, 5)

      self.assertEqual(a.pop(), 'test')
      self.assertEqual(a.toString(), ',other_test,,works')
      self.assertEqual(a.length, 4)

      self.assertEqual(a.pop(), 'other_test')
      self.assertEqual(a.toString(), ',,')
      self.assertEqual(a.length, 3)

      self.assertEqual(a.pop(), as3lib.undefined)
      self.assertEqual(a.toString(), ',')
      self.assertEqual(a.length, 2)

      self.assertEqual(a.pop(), as3lib.undefined)
      self.assertEqual(a.toString(), '')
      self.assertEqual(a.length, 1)

      self.assertEqual(a.pop(), as3lib.undefined)
      self.assertEqual(a.toString(), '')
      self.assertEqual(a.length, 0)

      self.assertEqual(a.pop(), as3lib.undefined)
      self.assertEqual(a.toString(), '')
      self.assertEqual(a.length, 0)

   def test_push(self):
      a = as3lib.Array(5)
      a[2] = 'test'
      as3lib.Array.prototype[3] = 'works'

      self.assertEqual(a.toString(), ',,test,works,')

      a.push('hi', 'bye')
      self.assertEquals(a.length, 7)
      self.assertEquals(a.toString(), ',,test,works,,hi,bye')

      a.push()
      self.assertEquals(a.length, 7)
      self.assertEquals(a.toString(), ',,test,works,,hi,bye')

   def test_reverse(self):
      a = as3lib.Array(5)
      as3lib.Array.prototype[0] = 0
      a[1] = 1
      a[2] = 2
      a[3] = as3lib.undefined
      as3lib.Array.prototype[4] = 4

      self.assertEqual(a.length, 5)

      b = a.reverse()
      self.assertEqual(a, b)
      self.assertEqual(a.toString(), ',2,1,,4')
      self.assertEqual(b.toString(), ',2,1,,4')

      as3lib.Array.prototype[4] = 999
      self.assertEqual(b.toString(), ',2,1,,999')

   def test_shift(self):
      a = as3lib.Array(5)
      a[2] = 'test'
      as3lib.Array.prototype[3] = 'works'

      self.assertArray(a, [as3lib.undefined, as3lib.undefined, 'test', 'works', as3lib.undefined], 5)

      self.assertEqual(a.shift(), as3lib.undefined)
      self.assertArray(a, [as3lib.undefined, 'test', as3lib.undefined, 'works'], 4)

      self.assertEqual(a.shift(), as3lib.undefined)
      self.assertArray(a, ['test', as3lib.undefined, as3lib.undefined], 3)

      self.assertEqual(a.shift(), 'test')
      self.assertArray(a, [as3lib.undefined, as3lib.undefined], 2)

      self.assertEqual(a.shift(), as3lib.undefined)
      self.assertArray(a, [as3lib.undefined], 1)

      self.assertEqual(a.shift(), as3lib.undefined)
      self.assertArray(a, [], 0)

      self.assertEqual(a.shift(), as3lib.undefined)
      self.assertArray(a, [], 0)

   def test_slice(self):
      a = as3lib.Array(8)

      as3lib.Array.prototype[0] = 999
      as3lib.Array.prototype[1] = 998
      a[2] = 2
      as3lib.Array.prototype[3] = 997
      a[4] = 4
      as3lib.Array.prototype[5] = 996
      a[6] = 6
      as3lib.Array.prototype[7] = 995

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
      a = as3lib.Array(5, 3, 1, 9, 16)
      self.assertTrue(a.some(lambda val, i, j: val == 5))
      self.assertFalse(a.some(lambda val, i, j: val == 20))

      b = as3lib.Array()
      self.assertFalse(b.some(lambda val, i, j: val == 30))

   def test_sort(self):
      def newArray():  # fresh_array
         a = as3lib.Array(5,3,1,'Abc','2','aba',as3lib.false,as3lib.null,'zzz')
         a[11] = 'not a hole'
         return a

      def newArray2():  # fresh_array_b
         b = as3lib.Array(5,3,'2',as3lib.false,as3lib.true,as3lib.NaN)
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
         as3lib.Array.prototype[10] = 'hole10'
         as3lib.Array.prototype[11] = 'hole11'
         as3lib.Array.prototype[12] = 'hole12'

         self.assertArray(a, check)

         # Clean up (used delete)
         del as3lib.Array.prototype[10]
         del as3lib.Array.prototype[11]
         del as3lib.Array.prototype[12]

         as3lib.Array.prototype[9] = as3lib.undefined
         as3lib.Array.prototype[10] = 'hole in slot 10'

      # NOTE: Only returns when 4 or 8 is specified
      a = newArray()
      as3lib.Array.prototype[9] = as3lib.undefined
      as3lib.Array.prototype[10] = 'hole in slot 10'
      s = a.sort(as3lib.Array.UNIQUESORT)
      self.assertNotEqual(s, 0)


      a = newArray()
      s = a.sort(as3lib.Array.RETURNINDEXEDARRAY)
      self.assertArray(s, [2,4,1,0,3,5,6,10,11,7,8,9])

      a.sort()
      self.assertArray(a, [1,'2',3,5,'Abc','aba',as3lib.false,'hole in slot 10','not a hole',as3lib.null,'zzz',as3lib.undefined])

      check_holes(a, [1,'2',3,5,'Abc','aba',as3lib.false,'hole in slot 10','not a hole',as3lib.null,'zzz','hole11'])


      a = newArray()

      s = a.sort(as3lib.Array.CASEINSENSITIVE | as3lib.Array.RETURNINDEXEDARRAY)
      self.assertArray(s, [2,4,1,0,5,3,6,10,11,7,8,9])

      a.sort(as3lib.Array.CASEINSENSITIVE)
      self.assertArray(a, [1,'2',3,5,'aba','Abc',as3lib.false,'hole in slot 10','not a hole',as3lib.null,'zzz',as3lib.undefined])

      check_holes(a, [1,'2',3,5,'aba','Abc',as3lib.false,'hole in slot 10','not a hole',as3lib.null,'zzz','hole11'])


      a = newArray()

      s = a.sort(as3lib.Array.DESCENDING | as3lib.Array.RETURNINDEXEDARRAY)
      self.assertArray(s, [8,7,11,10,6,5,3,0,1,4,2,9])

      a.sort(as3lib.Array.DESCENDING)
      self.assertArray(a, ['zzz',as3lib.null,'not a hole','hole in slot 10',as3lib.false,'aba','Abc',5,3,'2',1,as3lib.undefined])

      check_holes(a, ['zzz',as3lib.null,'not a hole','hole in slot 10',as3lib.false,'aba','Abc',5,3,'2',1,'hole11'])


      a = newArray()

      s = a.sort(as3lib.Array.CASEINSENSITIVE | as3lib.Array.DESCENDING | as3lib.Array.RETURNINDEXEDARRAY)
      self.assertArray(s, [8,7,11,10,6,3,5,0,1,4,2,9])

      a.sort(as3lib.Array.CASEINSENSITIVE | as3lib.Array.DESCENDING)
      self.assertArray(a, ['zzz',as3lib.null,'not a hole','hole in slot 10',as3lib.false,'Abc','aba',5,3,'2',1,as3lib.undefined])

      check_holes(a, ['zzz',as3lib.null,'not a hole','hole in slot 10',as3lib.false,'Abc','aba',5,3,'2',1,'hole11'])


      b = as3lib.Array(5,3,2,1,'2',as3lib.false,as3lib.true,as3lib.NaN)
      s = b.sort(as3lib.Array.NUMERIC | as3lib.Array.UNIQUESORT)
      self.assertEqual(s, 0)


      b = newArray2()

      s = b.sort(as3lib.Array.NUMERIC | as3lib.Array.RETURNINDEXEDARRAY)
      self.assertArray(s, [3,4,2,1,0,5])

      b.sort(as3lib.Array.NUMERIC)
      self.assertArray(b, [as3lib.false,as3lib.true,'2',3,5,as3lib.NaN])

      check_holes(b, [as3lib.false,as3lib.true,'2',3,5,as3lib.NaN])


      b = newArray2()

      b.sort(as3lib.Array.NUMERIC | 1)
      self.assertArray(b, [as3lib.false,as3lib.true,'2',3,5,as3lib.NaN])


      b = newArray2()

      s = b.sort(as3lib.Array.NUMERIC | as3lib.Array.DESCENDING | as3lib.Array.RETURNINDEXEDARRAY)
      self.assertArray(s, [5,0,1,2,4,3])

      b.sort(16 | as3lib.Array.DESCENDING)
      self.assertArray(b, [as3lib.NaN,5,3,'2',as3lib.true,as3lib.false])

      check_holes(b, [as3lib.NaN,5,3,'2',as3lib.true,as3lib.false])


      a = as3lib.Array(7,2,1,'3','4')

      a.sort(sub_comparison)
      self.assertArray(a, [7,'4','3',2,1])

      a.sort(sub_comparison, 2)
      self.assertArray(a, [1,2,'3','4',7])

      s = a.sort(sub_comparison, as3lib.Array.RETURNINDEXEDARRAY)
      self.assertArray(s, [4,3,2,1,0])

      s = a.sort(sub_comparison, as3lib.Array.DESCENDING | 8)
      self.assertArray(s, [0,1,2,3,4])

      s = a.sort(sub_comparison, as3lib.Array.UNIQUESORT)
      self.assertNotEqual(s, 0)


      c = as3lib.Array(3,'abc')

      s = c.sort(sub_comparison, as3lib.Array.UNIQUESORT)
      self.assertEqual(s, 0)

      d = as3lib.Array(3,'4')

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

      array = as3lib.Array(*[i for i in range(50)])

      # "sort" the array using randomly-chosen comparison results.
      def sortfunc(a, b):
         r = next(rng)
         if r % 8 == 0:
            return 0
         if r > 0:
            return 1
         return -1

      array.sort(sortfunc)
      self.assertArray(array, [13,35,24,1,8,33,6,3,9,38,20,7,23,40,19,16,12,15,14,4,22,37,21,18,45,25,41,27,36,32,47,44,43,48,29,5,26,11,10,39,17,42,49,2,31,28,0,30,34,46])


   def test_sortOn(self):
      raise TestNotImplemented

   def test_sparse_ops(self):
      arr = as3lib.Array(1, 2)
      arr[50] = 6
      arr[100] = 10
      arr[500] = 11

      self.assertEqual(arr[0], 1)
      self.assertEqual(arr[50], 6)
      self.assertEqual(arr[100], 10)
      self.assertEqual(arr[500], 11)
      self.assertEqual(arr[1000], as3lib.undefined)
      self.assertEqual(arr.length, 501)

      # Delete
      del arr[50]
      self.assertEqual(arr.length, 501)
      self.assertEqual(arr[50], as3lib.undefined)
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
      self.assertEqual(arr.removeAt(150), as3lib.undefined)
      self.assertEqual(arr.length, 500)
      self.assertEqual(arr[499], 11)
      self.assertEqual(arr[500], as3lib.undefined)

   def test_splice(self):
      # TODO: Ensure that the length asserts are correct
      def constructArray():
         arr = as3lib.Array(8)
         arr[2] = 2
         arr[4] = 4
         arr[6] = 6
         return arr

      as3lib.Array.prototype[0] = 999
      as3lib.Array.prototype[1] = 998
      as3lib.Array.prototype[3] = 997
      as3lib.Array.prototype[5] = 996
      as3lib.Array.prototype[7] = 995

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

      as3lib.Array.prototype[0] = 99
      as3lib.Array.prototype[5] = 96
      as3lib.Array.prototype[7] = 95

      self.assertArray(a, [99, 998, 2, 997, 4, 96, 6, 95], 8)
      self.assertArray(c, [999, 998, 2], 3)
      self.assertArray(d, [995], 1)
      self.assertArray(e, [], 0)
      self.assertArray(f, [2, 997, 4, 996, 6, 995], 6)

   def test_splice2(self):
      raise TestNotImplemented

   def test_splice_types(self):
      raise TestNotImplemented

   def test_storage(self):
      a = as3lib.Array('a', 'b', 'c')

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
      a = as3lib.Array(as3lib.String('a'), as3lib.String('b'), as3lib.String('c'))
      b = as3lib.Array(as3lib.Number(1), as3lib.Number(2), as3lib.Number(3))
      c = as3lib.Array(a, b)

      self.assertEqual(a.toLocaleString(), '[object String],[object String],[object String]')
      self.assertEqual(b.toLocaleString(), '1,2,3')
      self.assertEqual(c.toLocaleString(), '[object String],[object String],[object String],1,2,3')

   def test_toString(self):
      a = as3lib.Array('a', 'b', 'c')
      b = as3lib.Array(1, 2, 3)
      c = as3lib.Array(a, b)
      d = as3lib.Array('str', 123, as3lib.undefined, as3lib.null, as3lib.true, as3lib.false)

      self.assertEqual(a.toString(), 'a,b,c')
      self.assertEqual(b.toString(), '1,2,3')
      self.assertEqual(c.toString(), 'a,b,c,1,2,3')
      self.assertEqual(d.toString(), 'str,123,,,true,false')

   def test_unshift(self):
      a = as3lib.Array(5)
      a[2] = 'test'
      as3lib.Array.prototype[3] = 'works'

      self.asserArray(a, [as3lib.undefined, as3lib.undefined, 'test', 'works', as3lib.undefined])

      a.unshift("hi", "bye")
      self.asserArray(a, ['hi', 'bye', as3lib.undefined, 'works', 'test', as3lib.undefined, as3lib.undefined])

      a.unshift()
      self.asserArray(a, ['hi', 'bye', as3lib.undefined, 'works', 'test', as3lib.undefined, as3lib.undefined])

   def test_valueOf(self):
      # TODO: Make sure that valueOf is supposed to return the array
      a = as3lib.Array('a', 'b', 'c')
      self.assertEqual(a.valueOf(), a)

      b = as3lib.Array(1, 2, 3)
      self.assertEqual(b.valueOf(), b)

      c = as3lib.Array(a, b)
      self.assertEqual(c.valueOf(), c)

   def test_null_callback(self):
      # TODO: Make sure this is correct
      a = as3lib.Array()
      a.push(1)

      self.assertTrue(a.every(as3lib.null))
      self.assertIs(a.filter(as3lib.null), None)
      self.assertEqual(a.forEach(as3lib.null), as3lib.undefined)
      self.assertIs(a.map(as3lib.null), None)
      self.assertFalse(a.some(as3lib.null))


class BooleanTests(as3libTestCase):
   def test_constructor(self):
      self.assertFalse(as3lib.Boolean())
      self.assertTrue(as3lib.Boolean(as3lib.true))
      self.assertTrue(as3lib.Boolean(True))
      self.assertFalse(as3lib.Boolean(as3lib.false))
      self.assertFalse(as3lib.Boolean(False))
      self.assertFalse(as3lib.Boolean(as3lib.null))
      self.assertFalse(as3lib.Boolean(as3lib.undefined))
      self.assertFalse(as3lib.Boolean(as3lib.String('')))
      self.assertFalse(as3lib.Boolean(''))
      self.assertTrue(as3lib.Boolean(as3lib.String('str')))
      self.assertTrue(as3lib.Boolean('str'))
      self.assertTrue(as3lib.Boolean(as3lib.String('true')))
      self.assertTrue(as3lib.Boolean('true'))
      self.assertTrue(as3lib.Boolean(as3lib.String('false')))
      self.assertTrue(as3lib.Boolean('false'))
      self.assertFalse(as3lib.Boolean(as3lib.Number(0.0)))
      self.assertFalse(as3lib.Boolean(0.0))
      self.assertFalse(as3lib.Boolean(as3lib.NaN))
      self.assertFalse(as3lib.Boolean(as3lib.Number(-0.0)))
      self.assertFalse(as3lib.Boolean(-0.0))
      self.assertTrue(as3lib.Boolean(as3lib.Infinity))
      self.assertTrue(as3lib.Boolean(as3lib.Number(1.0)))
      self.assertTrue(as3lib.Boolean(1.0))
      self.assertTrue(as3lib.Boolean(as3lib.Number(-1.0)))
      self.assertTrue(as3lib.Boolean(-1.0))
      self.assertTrue(as3lib.Boolean(as3lib.Object()))

   def test_negation(self):
      self.assertFalse(not as3lib.true)
      self.assertTrue(not as3lib.false)
      self.assertTrue(not as3lib.null)
      self.assertTrue(not as3lib.undefined)
      self.assertTrue(not as3lib.String(''))
      self.assertFalse(not as3lib.String('str'))
      self.assertFalse(not as3lib.String('true'))
      self.assertFalse(not as3lib.String('false'))
      self.assertTrue(not as3lib.Number(0.0))
      self.assertTrue(not as3lib.NaN)
      self.assertTrue(not as3lib.Number(-0.0))
      self.assertFalse(not as3lib.Infinity)
      self.assertFalse(not as3lib.Number(1.0))
      self.assertFalse(not as3lib.Number(-1.0))
      self.assertFalse(not as3lib.Object())

   def test_toString(self):
      # TODO: Make sure assertIs is correct here
      self.assertEqual(as3lib.true.toString(), 'true')
      self.assertIs(as3lib.true.valueOf(), True)
      self.assertEqual(as3lib.false.toString(), 'false')
      self.assertIs(as3lib.false.valueOf(), False)


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
      milliseconds = as3lib.Date.parse(string)
      if as3lib.isNaN(milliseconds) or milliseconds is None:
         self.fail('Date.parse returned NaN')
      newdate = as3lib.Date(milliseconds)
      if useUTC:
         self.assertDateUTC(newdate, *args)
      else:
         self.assertDate(newdate, *args)

   def assertNotParsed(self, string):
      milliseconds = as3lib.Date.parse(string)
      if not as3lib.isNaN(milliseconds) and milliseconds is not None:
         self.fail('Date.parse returned valid date when it wasn\'t supposed to')

   def test_timestamp(self):
      date = as3lib.Date(929156400000)

      self.assertDateUTC(date, 1999, 5, 12, 6, 3, 0, 0)

   def test_arguements(self):
      date = as3lib.Date(2021, 7, 29, 4, 22, 55, 11)

      self.assertDate(date, 2021, 7, 29, 0, 4, 22, 55, 11)

   def test_invalid_string(self):
      date = as3lib.Date('12')

      self.assertNaN(date.fullYear)
      self.assertNaN(date.month)
      self.assertNaN(date.date)
      self.assertNaN(date.day)
      self.assertNaN(date.hours)
      self.assertNaN(date.minutes)
      self.assertNaN(date.seconds)

   def test_object_aruement(self):
      o = as3lib.Object()

      def valueOf():
         return 929156400000

      o.valueOf = valueOf
      date = as3lib.Date(o)

      self.assertDateUTC(date, 1999, 5, 12, 6, 3, 0, 0)

   def test_invalid_object_aruement(self):
      # TODO: Make Date accept objects
      o = as3lib.Object()

      def valueOf():
         return "Tue Feb 1 05:12:30 2005"

      o.valueOf = valueOf
      date = as3lib.Date(o)

      self.assertNaN(date.fullYear)
      self.assertNaN(date.month)
      self.assertNaN(date.date)
      self.assertNaN(date.day)
      self.assertNaN(date.hours)
      self.assertNaN(date.minutes)
      self.assertNaN(date.seconds)

   def test_string_arguement(self):
      date = as3lib.Date("Tue Feb 1 05:12:30 2005")

      self.assertDate(date, 2005, 1, 1, 2, 5, 12, 30)

   def test_setting_values(self):
      # TODO: test UTC properties
      date = as3lib.Date(0)

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
      raise TestNotImplemented

   def test_properties_with_NaN(self):
      date = as3lib.Date(as3lib.NaN)

      self.assertisNaN(date.fullYear)
      self.assertisNaN(date.month)
      self.assertisNaN(date.date)
      self.assertisNaN(date.day)
      self.assertisNaN(date.hours)
      self.assertisNaN(date.minutes)
      self.assertisNaN(date.seconds)

      date.date = 9
      date.fullYear = 1999

      self.assertDate(date, 1999, 0, 1, 5, 0, 0, 0)

      date.time = as3lib.NaN
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
   def escape(self):
      raise TestNotImplemented

   def test_isfinite(self):
      self.assertTrue(as3lib.isFinite(as3lib.true))
      self.assertTrue(as3lib.isFinite(as3lib.false))
      self.assertTrue(as3lib.isFinite(as3lib.Number(10.0)))
      self.assertTrue(as3lib.isFinite(10.0))
      self.assertTrue(as3lib.isFinite(as3lib.Number(-10.0)))
      self.assertTrue(as3lib.isFinite(-10.0))
      self.assertTrue(as3lib.isFinite(as3lib.Number(0.0)))
      self.assertTrue(as3lib.isFinite(0.0))
      self.assertFalse(as3lib.isFinite(as3lib.NaN))
      self.assertFalse(as3lib.isFinite(as3lib.Infinity))
      self.assertFalse(as3lib.isFinite(-as3lib.Infinity))
      self.assertTrue(as3lib.isFinite(as3lib.String('')))
      self.assertTrue(as3lib.isFinite(''))
      self.assertFalse(as3lib.isFinite(as3lib.String('hello')))
      self.assertFalse(as3lib.isFinite('hello'))
      self.assertTrue(as3lib.isFinite(as3lib.String(' ')))
      self.assertTrue(as3lib.isFinite(' '))
      self.assertTrue(as3lib.isFinite(as3lib.String('  5  ')))
      self.assertTrue(as3lib.isFinite('  5  '))
      self.assertTrue(as3lib.isFinite(as3lib.String('0')))
      self.assertTrue(as3lib.isFinite('0'))
      self.assertFalse(as3lib.isFinite(as3lib.String('NaN')))
      self.assertFalse(as3lib.isFinite('NaN'))
      self.assertFalse(as3lib.isFinite(as3lib.String('Infinity')))
      self.assertFalse(as3lib.isFinite('Infinity'))
      self.assertFalse(as3lib.isFinite(as3lib.String('-Infinity')))
      self.assertFalse(as3lib.isFinite('-Infinity'))
      self.assertFalse(as3lib.isFinite(as3lib.String('100a')))
      self.assertFalse(as3lib.isFinite('100a'))
      self.assertTrue(as3lib.isFinite(as3lib.String('0x10')))
      self.assertTrue(as3lib.isFinite('0x10'))
      self.assertFalse(as3lib.isFinite(as3lib.String('0xhello')))
      self.assertFalse(as3lib.isFinite('0xhello'))
      self.assertTrue(as3lib.isFinite(as3lib.String('0x1999999981ffffff')))
      self.assertTrue(as3lib.isFinite('0x1999999981ffffff'))
      self.assertFalse(as3lib.isFinite(as3lib.String('0xUIXUIDFKHJDF012345678')))
      self.assertFalse(as3lib.isFinite('0xUIXUIDFKHJDF012345678'))
      self.assertTrue(as3lib.isFinite(as3lib.String('123e-1')))
      self.assertTrue(as3lib.isFinite('123e-1'))
      self.assertFalse(as3lib.isFinite())

   def test_isNaN(self):
      self.assertFalse(as3lib.isNaN(as3lib.true))
      self.assertFalse(as3lib.isNaN(as3lib.false))
      self.assertFalse(as3lib.isNaN(as3lib.Number(10.0)))
      self.assertFalse(as3lib.isNaN(as3lib.Number(-10.0)))
      self.assertFalse(as3lib.isNaN(as3lib.Number(0.0)))
      self.assertTrue(as3lib.isNaN(as3lib.NaN))
      self.assertFalse(as3lib.isNaN(as3lib.Infinity))
      self.assertFalse(as3lib.isNaN(as3lib.NInfinity))
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
      self.assertEqual(as3lib.parseFloat('12345'), as3lib.Number(12345))

      # decimal point
      self.assertEqual(as3lib.parseFloat('012345.67890'), as3lib.Number(012345.6789))

      # ignore leading/trailing whitespace
      self.assertEqual(as3lib.parseFloat(" \t\r\n99999.99999\t\r\n      "), as3lib.Number(99999.99999))

      # long numbers (more than 15 digits)
      self.assertEqual(as3lib.parseFloat('-22222222222222222'), as3lib.Number(-22222222222222224))
      self.assertEqual(as3lib.parseFloat('-22222222.222222222'), as3lib.Number(-22222222.222222224))

      # subnormal number
      self.assertEqual(as3lib.parseFloat('.0000000000000000000000005').toString(), '4.999999999999999e-25')

      # ignore trailing garbage
      self.assertEqual(as3lib.parseFloat("0000.12345GIBBERISH"), as3lib.Number(0.12345))

      # exponent
      self.assertEqual(as3lib.parseFloat("9e99999"), as3lib.Infinity)
      self.assertEqual(as3lib.parseFloat("+100e-100").toString(), '0.999999999999999e-98')
      self.assertEqual(as3lib.parseFloat("-123.234E+66").toString(), '-1.23234e+68')
      self.assertEqual(as3lib.parseFloat(".2E20E1"), as3lib.Number(20000000000000000000))
      self.assertEqual(as3lib.parseFloat("-034.1+e20"), as3lib.Number(-34.1))
      self.assertEqual(as3lib.parseFloat("10e"), as3lib.Number(10))
      self.assertNaN(as3lib.parseFloat("e10"))
      self.assertNaN(as3lib.parseFloat("10e-"))

      # exponent overflow
      self.assertEqual(as3lib.parseFloat("1e4294967297"), as3lib.Number(10))
      self.assertEqual(as3lib.parseFloat("1e2147483648"), as3lib.Number(0))
      self.assertEqual(as3lib.parseFloat("1e-2147483648"), as3lib.Number(0))

      # multiple dots
      self.assertEqual(as3lib.parseFloat("1.2345.678"), as3lib.Number(1.2345))
      self.assertEqual(as3lib.parseFloat("1.2345.6e50"), as3lib.Number(1.2345))

      # infinity
      self.assertEqual(as3lib.parseFloat('Infinity'), as3lib.Infinity)
      self.assertEqual(as3lib.parseFloat('-Infinity'), as3lib.NInfinity)
      self.assertEqual(as3lib.parseFloat('+Infinity'), as3lib.Infinity)
      self.assertNaN(as3lib.parseFloat('Infinitya'))
      self.assertEqual(as3lib.parseFloat('Infinity   a'), as3lib.Infinity)
      self.assertEqual(as3lib.parseFloat(".   Infinity"), as3lib.Infinity)
      self.assertEqual(as3lib.parseFloat("e10   Infinity"), as3lib.Infinity)
      self.assertEqual(as3lib.parseFloat(".e10   Infinity"), as3lib.Infinity)
      self.assertEqual(as3lib.parseFloat("1   Infinity"), as3lib.Number(1))

      # invalid strings
      self.assertNaN(as3lib.parseFloat("BADBAD"))
      self.assertNaN(as3lib.parseFloat(''))
      self.assertNaN(as3lib.parseFloat('-'))
      self.assertEqual(as3lib.parseFloat('0xff'), as3lib.Number(0))
      self.assertNaN(as3lib.parseFloat(as3lib.String.fromCharCode(305)))

      # non-string inputs
      ## Booleans
      self.assertNaN(as3lib.parseFloat(as3lib.true))
      ## Numbers
      self.assertEqual(as3lib.parseFloat(1.2), as3lib.Number(1.2))
      ## Infinity objects
      self.assertEqual(as3lib.parseFloat(as3lib.Infinity), as3lib.Infinity)
      ## Function that returns a string
      self.assertEqual(as3lib.parseFloat(lambda: '5'), as3lib.Number(5))
      ## Class with toString method

      class C:
         def toString():
            return '6'

      self.assertEqual(as3lib.parseFloat(C()), as3lib.Number(6))

   def test_parseInt(self):
      self.assertNaN(as3lib.parseInt())
      self.assertNaN(as3lib.parseInt(as3lib.undefined))
      self.assertEqual(as3lib.parseInt(as3lib.undefined, 32), as3lib.Int(785077))
      self.assertEqual(as3lib.parseInt('undefined', 32), as3lib.Int(33790067563981))
      self.assertNaN(as3lib.parseInt(''))
      self.assertEqual(as3lib.parseInt(123), as3lib.Int(123))
      self.assertEqual(as3lib.parseInt(100, 10), as3lib.Int(100))
      self.assertEqual(as3lib.parseInt(100, 0), as3lib.Int(100))
      self.assertNaN(as3lib.parseInt(100, 1))
      self.assertEqual(as3lib.parseInt(100, 2), as3lib.Int(4))
      self.assertEqual(as3lib.parseInt(100, 36), as3lib.Int(1296))
      self.assertNaN(as3lib.parseInt(100, 37))
      self.assertNaN(as3lib.parseInt(100, -1))
      self.assertEqual(as3lib.parseInt(100, as3lib.Object()), as3lib.Int(100))
      self.assertNaN(as3lib.parseInt('100', as3lib.true))
      self.assertEqual(as3lib.parseInt('100', as3lib.false), as3lib.Int(100))
      self.assertEqual(as3lib.parseInt('100', as3lib.NaN), as3lib.Int(100))
      self.assertEqual(as3lib.parseInt('100', as3lib.undefined), as3lib.Int(100))
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
      self.assertEqual(as3lib.parseInt('0x12', as3lib.NaN), as3lib.Int(18))
      self.assertNaN(as3lib.parseInt('0x  '))
      self.assertNaN(as3lib.parseInt('0x'))
      self.assertNaN(as3lib.parseInt('0x  ', 16))
      self.assertNaN(as3lib.parseInt('0x', 16))
      self.assertEqual(as3lib.parseInt('12aaa'), as3lib.Int(12))
      self.assertEqual(as3lib.parseInt("100000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "000000000000000"), as3lib.Infinity)
      self.assertEqual(as3lib.parseInt("0x1000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "000000000000000"), as3lib.Infinity)
      self.assertNaN(as3lib.parseInt(as3lib.String.fromCharCode(305)))
      self.assertEqual(as3lib.parseInt(as3lib.String.fromCharCode(0x2000) + "123"), as3lib.Int(123))

   def test_unescape(self):
      raise TestNotImplemented

   def test_trace(self):
      raise TestNotImplemented


class GlobalsTests(as3libTestCase):
   def test_undefined(self):
      # From https://github.com/ruffle-rs/ruffle/tree/master/tests/tests/swfs/from_shumway/avm1/undefined/undefined-swf7
      self.assertEqual(as3lib.undefined.toString(), 'undefined')
      self.assertNaN(-as3lib.undefined)  # TODO: Validate this one
      self.assertTrue(not as3lib.undefined)
      self.assertEqual(as3lib.String('s') + as3lib.undefined, 'sundefined')
      self.assertEqual(as3lib.undefined + as3lib.String('s'), 'undefineds')
      self.assertNaN(as3lib.Number(0) + as3lib.undefined)
      self.assertNaN(as3lib.undefined + as3lib.Number(0))
      self.assertNotEqual(as3lib.String('undefined'), as3lib.undefined)
      self.assertNotEqual(as3lib.undefined, as3lib.String('undefined'))
      self.assertFalse(as3lib.Number(0) == as3lib.undefined)
      self.assertFalse(as3lib.undefined == as3lib.Number(0))
      self.assertFalse(as3lib.Number(1) == as3lib.undefined)
      self.assertFalse(as3lib.undefined == as3lib.Number(1))
      # trace("\'undefined\' < undefined => " + ("undefined" < undefined));
      # trace("undefined < \'undefined\' => " + (undefined < "undefined"));
      # 'undefined' < undefined => undefined
      # undefined < 'undefined' => undefined
      self.assertEqual(as3lib.Number(0) < as3lib.undefined, as3lib.undefined)
      self.assertEqual(as3lib.undefined < as3lib.Number(0), as3lib.undefined)
      self.assertEqual(as3lib.Number(1) < as3lib.undefined, as3lib.undefined)
      self.assertEqual(as3lib.undefined < as3lib.Number(1), as3lib.undefined)
      # trace("\'undefined\' <= undefined => " + ("undefined" <= undefined));
      # trace("undefined <= \'undefined\' => " + (undefined <= "undefined"));
      # 'undefined' <= undefined => true
      # undefined <= 'undefined' => true
      self.assertTrue(as3lib.Number(0) <= as3lib.undefined)
      self.assertTrue(as3lib.undefined <= as3lib.Number(0))
      self.assertTrue(as3lib.Number(1) <= as3lib.undefined)
      self.assertTrue(as3lib.undefined <= as3lib.Number(1))
      # trace("\'undefined\' > undefined => " + ("undefined" > undefined));
      # trace("undefined > \'undefined\' => " + (undefined > "undefined"));
      # 'undefined' > undefined => undefined
      # undefined > 'undefined' => undefined
      self.assertEqual(as3lib.Number(0) > as3lib.undefined, as3lib.undefined)
      self.assertEqual(as3lib.undefined > as3lib.Number(0), as3lib.undefined)
      self.assertEqual(as3lib.Number(1) > as3lib.undefined, as3lib.undefined)
      self.assertEqual(as3lib.undefined > as3lib.Number(1), as3lib.undefined)
      # trace("\'undefined\' >= undefined => " + ("undefined" >= undefined));
      # trace("undefined >= \'undefined\' => " + (undefined >= "undefined"));
      # 'undefined' >= undefined => true
      # undefined >= 'undefined' => true
      self.assertTrue(as3lib.Number(0) >= as3lib.undefined)
      self.assertTrue(as3lib.undefined >= as3lib.Number(0))
      self.assertTrue(as3lib.Number(1) >= as3lib.undefined)
      self.assertTrue(as3lib.undefined >= as3lib.Number(1))

   def test_null(self):
      raise TestNotImplemented


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
      #2, 3, 4, 5, 6, 7, 8, 9, null/10, ..., valueOf
      self.assertEqual(val.toString(), check[8])
      for i in range(35):
         self.assertEqual(val.toString(i + 2), check[i])
      self.assertEqual(val.valueOf(), check[35])


class intTests(NumberTestsBase):
   def test_constructor(self):
      self.assertEqual(as3lib.Int(), 0)
      self.assertEqual(as3lib.Int(as3lib.true), 1)
      self.assertEqual(as3lib.Int(True), 1)
      self.assertEqual(as3lib.Int(as3lib.false), 0)
      self.assertEqual(as3lib.Int(False), 0)
      self.assertEqual(as3lib.Int(as3lib.null), 0)
      self.assertEqual(as3lib.Int(as3lib.undefined), 0)

      self.assertEqual(as3lib.Int(as3lib.String('')), 0)
      self.assertEqual(as3lib.Int(''), 0)
      self.assertEqual(as3lib.Int(as3lib.String('str')), 0)
      self.assertEqual(as3lib.Int('str'), 0)
      self.assertEqual(as3lib.Int(as3lib.String('true')), 0)
      self.assertEqual(as3lib.Int('true'), 0)
      self.assertEqual(as3lib.Int(as3lib.String('false')), 0)
      self.assertEqual(as3lib.Int('false'), 0)

      self.assertEqual(as3lib.Int(as3lib.Number(0.0)), 0)
      self.assertEqual(as3lib.Int(0.0), 0)
      self.assertEqual(as3lib.Int(as3lib.NaN), 0)
      self.assertEqual(as3lib.Int(as3lib.Number(-0.0)), 0)
      self.assertEqual(as3lib.Int(-0.0), 0)
      self.assertEqual(as3lib.Int(as3lib.Infinity), 0)
      self.assertEqual(as3lib.Int(as3lib.Number(1.0)), 1)
      self.assertEqual(as3lib.Int(1.0), 1)
      self.assertEqual(as3lib.Int(as3lib.Number(-1.0)), -1)
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
      self.assertEqual(as3lib.Int(as3lib.String('0.0')), 0)
      self.assertEqual(as3lib.Int('0.0'), 0)
      self.assertEqual(as3lib.Int(as3lib.String('NaN')), 0)
      self.assertEqual(as3lib.Int('NaN'), 0)
      self.assertEqual(as3lib.Int(as3lib.String('-0.0')), 0)
      self.assertEqual(as3lib.Int('-0.0'), 0)
      self.assertEqual(as3lib.Int(as3lib.String('Infinity')), 0)
      self.assertEqual(as3lib.Int('Infinity'), 0)
      self.assertEqual(as3lib.Int(as3lib.String('1.0')), 1)
      self.assertEqual(as3lib.Int('1.0'), 1)
      self.assertEqual(as3lib.Int(as3lib.String('-1.0')), -1)
      self.assertEqual(as3lib.Int('-1.0'), -1)
      self.assertEqual(as3lib.Int(as3lib.String('0xFF1306')), 16716550)
      self.assertEqual(as3lib.Int('0xFF1306'), 16716550)
      self.assertEqual(as3lib.Int(as3lib.String('1.2315e2')), 123)
      self.assertEqual(as3lib.Int('1.2315e2'), 123)
      self.assertEqual(as3lib.Int(as3lib.String('0x7FFFFFFF')), 2147483647)
      self.assertEqual(as3lib.Int('0x7FFFFFFF'), 2147483647)
      self.assertEqual(as3lib.Int(as3lib.String('0x80000000')), -2147483648)
      self.assertEqual(as3lib.Int('0x80000000'), -2147483648)
      self.assertEqual(as3lib.Int(as3lib.String('0x80000001')), -2147483647)
      self.assertEqual(as3lib.Int('0x80000001'), -2147483647)
      self.assertEqual(as3lib.Int(as3lib.String('0x180000001')), -2147483647)
      self.assertEqual(as3lib.Int('0x180000001'), -2147483647)
      self.assertEqual(as3lib.Int(as3lib.String('0x100000001')), 1)
      self.assertEqual(as3lib.Int('0x100000001'), 1)
      self.assertEqual(as3lib.Int(as3lib.String('-0x7FFFFFFF')), -2147483647)
      self.assertEqual(as3lib.Int('-0x7FFFFFFF'), -2147483647)
      self.assertEqual(as3lib.Int(as3lib.String('-0x80000000')), -2147483648)
      self.assertEqual(as3lib.Int('-0x80000000'), -2147483648)
      self.assertEqual(as3lib.Int(as3lib.String('-0x80000001')), 2147483647)
      self.assertEqual(as3lib.Int('-0x80000001'), 2147483647)
      self.assertEqual(as3lib.Int(as3lib.String('-0x180000001')), 2147483647)
      self.assertEqual(as3lib.Int('-0x180000001'), 2147483647)
      self.assertEqual(as3lib.Int(as3lib.String('-0x100000001')), -1)
      self.assertEqual(as3lib.Int('-0x100000001'), -1)

      self.assertEqual(as3lib.Int(as3lib.Object()), 0)

   def test_edge_cases(self):
      raise TestNotImplemented
      # uint doesn't exist
      # trace(getQualifiedClassName(1 as uint));
      # 2026-01-06T18:24:19.825440Z  INFO avm_trace: int
      # trace((1 as uint) is uint);
      # 2026-01-06T18:24:19.825443Z  INFO avm_trace: true
      # trace(getQualifiedClassName(new uint()));
      # 2026-01-06T18:24:19.825446Z  INFO avm_trace: int

      # Int overflow => Number
      self.assertType(as3lib.Int(268435454), as3lib.Int)
      self.assertType(as3lib.Int(268435454 + 1), as3lib.Int)
      self.assertType(as3lib.Int(268435454 + 2), as3lib.Number)

      # Int underflow => Number
      self.assertType(as3lib.Int(-268435454), as3lib.Int)
      self.assertType(as3lib.Int(-268435454 - 1), as3lib.Int)
      self.assertType(as3lib.Int(-268435454 - 2), as3lib.Int)
      self.assertType(as3lib.Int(-268435454 - 3), as3lib.Number)

      # properties declared 'uint' don't underflow at 0
      self.assertEqual(as3lib.Array().length - 1, -1)

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
                          '-2.147483648e+9','-2.1474836480e+9',
                          '-2.14748364800000000000e+9')
      asrt_n2147483647 = ('-2e+9', '-2.1e+9', '-2.15e+9', '-2.147e+9',
                          '-2.1475e+9', '-2.14748e+9', '-2.147484e+9',
                          '-2.1474836e+9', '-2.14748365e+9',
                          '-2.147483647e+9', '-2.1474836470e+9',
                          '-2.14748364700000000000e+9')

      self.assertToExponential(as3lib.true, asrt_1)

      self.assertToExponential(as3lib.false, asrt_0)
      self.assertToExponential(as3lib.null, asrt_0)
      self.assertToExponential(as3lib.undefined, asrt_0)

      self.assertToExponential(as3lib.String(''), asrt_0)
      self.assertToExponential('', asrt_0)

      self.assertToExponential(as3lib.String('str'), asrt_0)
      self.assertToExponential('str', asrt_0)

      self.assertToExponential(as3lib.String('true'), asrt_0)
      self.assertToExponential('true', asrt_0)

      self.assertToExponential(as3lib.String('false'), asrt_0)
      self.assertToExponential('false', asrt_0)

      self.assertToExponential(as3lib.Number(0.0), asrt_0)
      self.assertToExponential(0.0, asrt_0)

      self.assertToExponential(as3lib.NaN, asrt_0)

      self.assertToExponential(as3lib.Number(-0.0), asrt_0)
      self.assertToExponential(-0.0, asrt_0)

      self.assertToExponential(as3lib.Infinity, asrt_0)

      self.assertToExponential(as3lib.Number(1.0), asrt_1)
      self.assertToExponential(1.0, asrt_1)

      self.assertToExponential(as3lib.Number(-1.0), asrt_n1)
      self.assertToExponential(-1.0, asrt_n1)

      self.assertToExponential(as3lib.Number(0xFF1306), asrt_16716550)
      self.assertToExponential(0xFF1306, asrt_16716550)

      self.assertToExponential(as3lib.Number(1.2315e2), asrt_123)
      self.assertToExponential(1.2315e2, asrt_123)

      self.assertToExponential(as3lib.Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToExponential(0x7FFFFFFF, asrt_2147483647)

      self.assertToExponential(as3lib.Number(0x80000000), asrt_n2147483648)
      self.assertToExponential(0x80000000, asrt_n2147483648)

      self.assertToExponential(as3lib.Number(0x80000001), asrt_n2147483647)
      self.assertToExponential(0x80000001, asrt_n2147483647)

      self.assertToExponential(as3lib.Number(0x180000001), asrt_n2147483647)
      self.assertToExponential(0x180000001, asrt_n2147483647)

      self.assertToExponential(as3lib.Number(0x100000001), asrt_1)
      self.assertToExponential(0x100000001, asrt_1)

      self.assertToExponential(as3lib.Number(-0x7FFFFFFF), asrt_n2147483647)
      self.assertToExponential(-0x7FFFFFFF, asrt_n2147483647)

      self.assertToExponential(as3lib.Number(-0x80000000), asrt_n2147483648)
      self.assertToExponential(-0x80000000, asrt_n2147483648)

      self.assertToExponential(as3lib.Number(-0x80000001), asrt_2147483647)
      self.assertToExponential(-0x80000001, asrt_2147483647)

      self.assertToExponential(as3lib.Number(-0x180000001), asrt_2147483647)
      self.assertToExponential(-0x180000001, asrt_2147483647)

      self.assertToExponential(as3lib.Number(-0x100000001), asrt_n1)
      self.assertToExponential(-0x100000001, asrt_n1)

      self.assertToExponential(as3lib.Object(), asrt_0)

      # Parse Tests
      self.assertToExponential(as3lib.String('0.0'), asrt_0)
      self.assertToExponential('0.0', asrt_0)
      self.assertToExponential(as3lib.String('NaN'), asrt_0)
      self.assertToExponential('NaN', asrt_0)
      self.assertToExponential(as3lib.String('-0.0'), asrt_0)
      self.assertToExponential('-0.0', asrt_0)
      self.assertToExponential(as3lib.String('Infinity'), asrt_0)
      self.assertToExponential('Infinity', asrt_0)
      self.assertToExponential(as3lib.String('1.0'), asrt_1)
      self.assertToExponential('1.0', asrt_1)
      self.assertToExponential(as3lib.String('-1.0'), asrt_n1)
      self.assertToExponential('-1.0', asrt_n1)
      self.assertToExponential(as3lib.String('0xFF1306'), asrt_16716550)
      self.assertToExponential('0xFF1306', asrt_16716550)
      self.assertToExponential(as3lib.String('1.2315e2'), asrt_123)
      self.assertToExponential('1.2315e2', asrt_123)
      self.assertToExponential(as3lib.String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToExponential('0x7FFFFFFF', asrt_2147483647)
      self.assertToExponential(as3lib.String('0x80000000'), asrt_n2147483648)
      self.assertToExponential('0x80000000', asrt_n2147483648)
      self.assertToExponential(as3lib.String('0x80000001'), asrt_n2147483647)
      self.assertToExponential('0x80000001', asrt_n2147483647)
      self.assertToExponential(as3lib.String('0x180000001'), asrt_n2147483647)
      self.assertToExponential('0x180000001', asrt_n2147483647)
      self.assertToExponential(as3lib.String('0x100000001'), asrt_1)
      self.assertToExponential('0x100000001', asrt_1)
      self.assertToExponential(as3lib.String('-0x7FFFFFFF'), asrt_n2147483647)
      self.assertToExponential('-0x7FFFFFFF', asrt_n2147483647)
      self.assertToExponential(as3lib.String('-0x80000000'), asrt_n2147483648)
      self.assertToExponential('-0x80000000', asrt_n2147483648)
      self.assertToExponential(as3lib.String('-0x80000001'), asrt_2147483647)
      self.assertToExponential('-0x80000001', asrt_2147483647)
      self.assertToExponential(as3lib.String('-0x180000001'), asrt_2147483647)
      self.assertToExponential('-0x180000001', asrt_2147483647)
      self.assertToExponential(as3lib.String('-0x100000001'), asrt_n1)
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

      self.assertToFixed(as3lib.true, asrt_1)

      self.assertToFixed(as3lib.false, asrt_0)
      self.assertToFixed(as3lib.null, asrt_0)
      self.assertToFixed(as3lib.undefined, asrt_0)

      self.assertToFixed(as3lib.String(''), asrt_0)
      self.assertToFixed('', asrt_0)

      self.assertToFixed(as3lib.String('str'), asrt_0)
      self.assertToFixed('str', asrt_0)

      self.assertToFixed(as3lib.String('true'), asrt_0)
      self.assertToFixed('true', asrt_0)

      self.assertToFixed(as3lib.String('false'), asrt_0)
      self.assertToFixed('false', asrt_0)

      self.assertToFixed(as3lib.Number(0.0), asrt_0)
      self.assertToFixed(0.0, asrt_0)

      self.assertToFixed(as3lib.NaN, asrt_0)

      self.assertToFixed(as3lib.Number(-0.0), asrt_0)
      self.assertToFixed(-0.0, asrt_0)

      self.assertToFixed(as3lib.Infinity, asrt_0)

      self.assertToFixed(as3lib.Number(1.0), asrt_1)
      self.assertToFixed(1.0, asrt_1)

      self.assertToFixed(as3lib.Number(-1.0), asrt_n1)
      self.assertToFixed(-1.0, asrt_n1)

      self.assertToFixed(as3lib.Number(0xFF1306), asrt_16716550)
      self.assertToFixed(0xFF1306, asrt_16716550)

      self.assertToFixed(as3lib.Number(1.2315e2), asrt_123)
      self.assertToFixed(1.2315e2, asrt_123)

      self.assertToFixed(as3lib.Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToFixed(0x7FFFFFFF, asrt_2147483647)

      self.assertToFixed(as3lib.Number(0x80000000), asrt_n2147483648)
      self.assertToFixed(0x80000000, asrt_n2147483648)

      self.assertToFixed(as3lib.Number(0x80000001), asrt_n2147483647)
      self.assertToFixed(0x80000001, asrt_n2147483647)

      self.assertToFixed(as3lib.Number(0x180000001), asrt_n2147483647)
      self.assertToFixed(0x180000001, asrt_n2147483647)

      self.assertToFixed(as3lib.Number(0x100000001), asrt_1)
      self.assertToFixed(0x100000001, asrt_1)

      self.assertToFixed(as3lib.Number(-0x7FFFFFFF), asrt_n2147483647)
      self.assertToFixed(-0x7FFFFFFF, asrt_n2147483647)

      self.assertToFixed(as3lib.Number(-0x80000000), asrt_n2147483648)
      self.assertToFixed(-0x80000000, asrt_n2147483648)

      self.assertToFixed(as3lib.Number(-0x80000001), asrt_2147483647)
      self.assertToFixed(-0x80000001, asrt_2147483647)

      self.assertToFixed(as3lib.Number(-0x180000001), asrt_2147483647)
      self.assertToFixed(-0x180000001, asrt_2147483647)

      self.assertToFixed(as3lib.Number(-0x100000001), asrt_n1)
      self.assertToFixed(-0x100000001, asrt_n1)

      self.assertToFixed(as3lib.Object(), asrt_0)

      # Parse Tests
      self.assertToFixed(as3lib.String('0.0'), asrt_0)
      self.assertToFixed('0.0', asrt_0)
      self.assertToFixed(as3lib.String('NaN'), asrt_0)
      self.assertToFixed('NaN', asrt_0)
      self.assertToFixed(as3lib.String('-0.0'), asrt_0)
      self.assertToFixed('-0.0', asrt_0)
      self.assertToFixed(as3lib.String('Infinity'), asrt_0)
      self.assertToFixed('Infinity', asrt_0)
      self.assertToFixed(as3lib.String('1.0'), asrt_1)
      self.assertToFixed('1.0', asrt_1)
      self.assertToFixed(as3lib.String('-1.0'), asrt_n1)
      self.assertToFixed('-1.0', asrt_n1)
      self.assertToFixed(as3lib.String('0xFF1306'), asrt_16716550)
      self.assertToFixed('0xFF1306', asrt_16716550)
      self.assertToFixed(as3lib.String('1.2315e2'), asrt_123)
      self.assertToFixed('1.2315e2', asrt_123)
      self.assertToFixed(as3lib.String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToFixed('0x7FFFFFFF', asrt_2147483647)
      self.assertToFixed(as3lib.String('0x80000000'), asrt_n2147483648)
      self.assertToFixed('0x80000000', asrt_n2147483648)
      self.assertToFixed(as3lib.String('0x80000001'), asrt_n2147483647)
      self.assertToFixed('0x80000001', asrt_n2147483647)
      self.assertToFixed(as3lib.String('0x180000001'), asrt_n2147483647)
      self.assertToFixed('0x180000001', asrt_n2147483647)
      self.assertToFixed(as3lib.String('0x100000001'), asrt_1)
      self.assertToFixed('0x100000001', asrt_1)
      self.assertToFixed(as3lib.String('-0x7FFFFFFF'), asrt_n2147483647)
      self.assertToFixed('-0x7FFFFFFF', asrt_n2147483647)
      self.assertToFixed(as3lib.String('-0x80000000'), asrt_n2147483648)
      self.assertToFixed('-0x80000000', asrt_n2147483648)
      self.assertToFixed(as3lib.String('-0x80000001'), asrt_2147483647)
      self.assertToFixed('-0x80000001', asrt_2147483647)
      self.assertToFixed(as3lib.String('-0x180000001'), asrt_2147483647)
      self.assertToFixed('-0x180000001', asrt_2147483647)
      self.assertToFixed(as3lib.String('-0x100000001'), asrt_n1)
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

      self.assertToPrecision(as3lib.true, asrt_1)

      self.assertToPrecision(as3lib.false, asrt_0)
      self.assertToPrecision(as3lib.null, asrt_0)
      self.assertToPrecision(as3lib.undefined, asrt_0)

      self.assertToPrecision(as3lib.String(''), asrt_0)
      self.assertToPrecision('', asrt_0)

      self.assertToPrecision(as3lib.String('str'), asrt_0)
      self.assertToPrecision('str', asrt_0)

      self.assertToPrecision(as3lib.String('true'), asrt_0)
      self.assertToPrecision('true', asrt_0)

      self.assertToPrecision(as3lib.String('false'), asrt_0)
      self.assertToPrecision('false', asrt_0)

      self.assertToPrecision(as3lib.Number(0.0), asrt_0)
      self.assertToPrecision(0.0, asrt_0)

      self.assertToPrecision(as3lib.NaN, asrt_0)

      self.assertToPrecision(as3lib.Number(-0.0), asrt_0)
      self.assertToPrecision(-0.0, asrt_0)

      self.assertToPrecision(as3lib.Infinity, asrt_0)

      self.assertToPrecision(as3lib.Number(1.0), asrt_1)
      self.assertToPrecision(1.0, asrt_1)

      self.assertToPrecision(as3lib.Number(-1.0), asrt_n1)
      self.assertToPrecision(-1.0, asrt_n1)

      self.assertToPrecision(as3lib.Number(0xFF1306), asrt_16716550)
      self.assertToPrecision(0xFF1306, asrt_16716550)

      self.assertToPrecision(as3lib.Number(1.2315e2), asrt_123)
      self.assertToPrecision(1.2315e2, asrt_123)

      self.assertToPrecision(as3lib.Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToPrecision(0x7FFFFFFF, asrt_2147483647)

      self.assertToPrecision(as3lib.Number(0x80000000), asrt_n2147483648)
      self.assertToPrecision(0x80000000, asrt_n2147483648)

      self.assertToPrecision(as3lib.Number(0x80000001), asrt_n2147483647)
      self.assertToPrecision(0x80000001, asrt_n2147483647)

      self.assertToPrecision(as3lib.Number(0x180000001), asrt_n2147483647)
      self.assertToPrecision(0x180000001, asrt_n2147483647)

      self.assertToPrecision(as3lib.Number(0x100000001), asrt_1)
      self.assertToPrecision(0x100000001, asrt_1)

      self.assertToPrecision(as3lib.Number(-0x7FFFFFFF), asrt_n2147483647)
      self.assertToPrecision(-0x7FFFFFFF, asrt_n2147483647)

      self.assertToPrecision(as3lib.Number(-0x80000000), asrt_n2147483648)
      self.assertToPrecision(-0x80000000, asrt_n2147483648)

      self.assertToPrecision(as3lib.Number(-0x80000001), asrt_2147483647)
      self.assertToPrecision(-0x80000001, asrt_2147483647)

      self.assertToPrecision(as3lib.Number(-0x180000001), asrt_2147483647)
      self.assertToPrecision(-0x180000001, asrt_2147483647)

      self.assertToPrecision(as3lib.Number(-0x100000001), asrt_n1)
      self.assertToPrecision(-0x100000001, asrt_n1)

      self.assertToPrecision(as3lib.Object(), asrt_0)

      # Parse Tests
      self.assertToPrecision(as3lib.String('0.0'), asrt_0)
      self.assertToPrecision('0.0', asrt_0)
      self.assertToPrecision(as3lib.String('NaN'), asrt_0)
      self.assertToPrecision('NaN', asrt_0)
      self.assertToPrecision(as3lib.String('-0.0'), asrt_0)
      self.assertToPrecision('-0.0', asrt_0)
      self.assertToPrecision(as3lib.String('Infinity'), asrt_0)
      self.assertToPrecision('Infinity', asrt_0)
      self.assertToPrecision(as3lib.String('1.0'), asrt_1)
      self.assertToPrecision('1.0', asrt_1)
      self.assertToPrecision(as3lib.String('-1.0'), asrt_n1)
      self.assertToPrecision('-1.0', asrt_n1)
      self.assertToPrecision(as3lib.String('0xFF1306'), asrt_16716550)
      self.assertToPrecision('0xFF1306', asrt_16716550)
      self.assertToPrecision(as3lib.String('1.2315e2'), asrt_123)
      self.assertToPrecision('1.2315e2', asrt_123)
      self.assertToPrecision(as3lib.String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToPrecision('0x7FFFFFFF', asrt_2147483647)
      self.assertToPrecision(as3lib.String('0x80000000'), asrt_n2147483648)
      self.assertToPrecision('0x80000000', asrt_n2147483648)
      self.assertToPrecision(as3lib.String('0x80000001'), asrt_n2147483647)
      self.assertToPrecision('0x80000001', asrt_n2147483647)
      self.assertToPrecision(as3lib.String('0x180000001'), asrt_n2147483647)
      self.assertToPrecision('0x180000001', asrt_n2147483647)
      self.assertToPrecision(as3lib.String('0x100000001'), asrt_1)
      self.assertToPrecision('0x100000001', asrt_1)
      self.assertToPrecision(as3lib.String('-0x7FFFFFFF'), asrt_n2147483647)
      self.assertToPrecision('-0x7FFFFFFF', asrt_n2147483647)
      self.assertToPrecision(as3lib.String('-0x80000000'), asrt_n2147483648)
      self.assertToPrecision('-0x80000000', asrt_n2147483648)
      self.assertToPrecision(as3lib.String('-0x80000001'), asrt_2147483647)
      self.assertToPrecision('-0x80000001', asrt_2147483647)
      self.assertToPrecision(as3lib.String('-0x180000001'), asrt_2147483647)
      self.assertToPrecision('-0x180000001', asrt_2147483647)
      self.assertToPrecision(as3lib.String('-0x100000001'), asrt_n1)
      self.assertToPrecision('-0x100000001', asrt_n1)

   def assertToString(self, value, check):
      #2, 3, 4, 5, 6, 7, 8, 9, null/10, ..., valueOf
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

      self.assertToString(as3lib.true, asrt_1)

      self.assertToString(as3lib.false, asrt_0)
      self.assertToString(as3lib.null, asrt_0)
      self.assertToString(as3lib.undefined, asrt_0)

      self.assertToString(as3lib.String(''), asrt_0)
      self.assertToString('', asrt_0)

      self.assertToString(as3lib.String('str'), asrt_0)
      self.assertToString('str', asrt_0)

      self.assertToString(as3lib.String('true'), asrt_0)
      self.assertToString('true', asrt_0)

      self.assertToString(as3lib.String('false'), asrt_0)
      self.assertToString('false', asrt_0)

      self.assertToString(as3lib.Number(0.0), asrt_0)
      self.assertToString(0.0, asrt_0)

      self.assertToString(as3lib.NaN, asrt_0)

      self.assertToString(as3lib.Number(-0.0), asrt_0)
      self.assertToString(-0.0, asrt_0)

      self.assertToString(as3lib.Infinity, asrt_0)

      self.assertToString(as3lib.Number(1.0), asrt_1)
      self.assertToString(1.0, asrt_1)

      self.assertToString(as3lib.Number(-1.0), asrt_n1)
      self.assertToString(-1.0, asrt_n1)

      self.assertToString(as3lib.Number(0xFF1306), asrt_16716550)
      self.assertToString(0xFF1306, asrt_16716550)

      self.assertToString(as3lib.Number(1.2315e2), asrt_123)
      self.assertToString(1.2315e2, asrt_123)

      self.assertToString(as3lib.Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToString(0x7FFFFFFF, asrt_2147483647)

      self.assertToString(as3lib.Number(0x80000000), asrt_n2147483648)
      self.assertToString(0x80000000, asrt_n2147483648)

      self.assertToString(as3lib.Number(0x80000001), asrt_n2147483647)
      self.assertToString(0x80000001, asrt_n2147483647)

      self.assertToString(as3lib.Number(0x180000001), asrt_n2147483647)
      self.assertToString(0x180000001, asrt_n2147483647)

      self.assertToString(as3lib.Number(0x100000001), asrt_1)
      self.assertToString(0x100000001, asrt_1)

      self.assertToString(as3lib.Number(-0x7FFFFFFF), asrt_n2147483647)
      self.assertToString(-0x7FFFFFFF, asrt_n2147483647)

      self.assertToString(as3lib.Number(-0x80000000), asrt_n2147483648)
      self.assertToString(-0x80000000, asrt_n2147483648)

      self.assertToString(as3lib.Number(-0x80000001), asrt_2147483647)
      self.assertToString(-0x80000001, asrt_2147483647)

      self.assertToString(as3lib.Number(-0x180000001), asrt_2147483647)
      self.assertToString(-0x180000001, asrt_2147483647)

      self.assertToString(as3lib.Number(-0x100000001), asrt_n1)
      self.assertToString(-0x100000001, asrt_n1)

      self.assertToString(as3lib.Object(), asrt_0)

      # Parse Tests
      self.assertToString(as3lib.String('0.0'), asrt_0)
      self.assertToString('0.0', asrt_0)
      self.assertToString(as3lib.String('NaN'), asrt_0)
      self.assertToString('NaN', asrt_0)
      self.assertToString(as3lib.String('-0.0'), asrt_0)
      self.assertToString('-0.0', asrt_0)
      self.assertToString(as3lib.String('Infinity'), asrt_0)
      self.assertToString('Infinity', asrt_0)
      self.assertToString(as3lib.String('1.0'), asrt_1)
      self.assertToString('1.0', asrt_1)
      self.assertToString(as3lib.String('-1.0'), asrt_n1)
      self.assertToString('-1.0', asrt_n1)
      self.assertToString(as3lib.String('0xFF1306'), asrt_16716550)
      self.assertToString('0xFF1306', asrt_16716550)
      self.assertToString(as3lib.String('1.2315e2'), asrt_123)
      self.assertToString('1.2315e2', asrt_123)
      self.assertToString(as3lib.String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToString('0x7FFFFFFF', asrt_2147483647)
      self.assertToString(as3lib.String('0x80000000'), asrt_n2147483648)
      self.assertToString('0x80000000', asrt_n2147483648)
      self.assertToString(as3lib.String('0x80000001'), asrt_n2147483647)
      self.assertToString('0x80000001', asrt_n2147483647)
      self.assertToString(as3lib.String('0x180000001'), asrt_n2147483647)
      self.assertToString('0x180000001', asrt_n2147483647)
      self.assertToString(as3lib.String('0x100000001'), asrt_1)
      self.assertToString('0x100000001', asrt_1)
      self.assertToString(as3lib.String('-0x7FFFFFFF'), asrt_n2147483647)
      self.assertToString('-0x7FFFFFFF', asrt_n2147483647)
      self.assertToString(as3lib.String('-0x80000000'), asrt_n2147483648)
      self.assertToString('-0x80000000', asrt_n2147483648)
      self.assertToString(as3lib.String('-0x80000001'), asrt_2147483647)
      self.assertToString('-0x80000001', asrt_2147483647)
      self.assertToString(as3lib.String('-0x180000001'), asrt_2147483647)
      self.assertToString('-0x180000001', asrt_2147483647)
      self.assertToString(as3lib.String('-0x100000001'), asrt_n1)
      self.assertToString('-0x100000001', asrt_n1)


class MathTests(as3libTestCase):
   def assertFuncReturns(self, check, func, *args):
      if check is as3lib.NaN:
         self.assertNaN(func(*args))
      else:
         self.assertEqual(func(*args), check)

   def assertFunc1(self, func, *values):
      obj = as3lib.Object()
      obj.valueOf = lambda: as3lib.Number(10.1)
      self.assertFuncReturns(values[0], func, 0)
      self.assertFuncReturns(values[1], func, 1)
      self.assertFuncReturns(values[2], func, -1)
      self.assertFuncReturns(values[3], func, 1234.5)
      self.assertFuncReturns(values[4], func, -1234.5)
      self.assertFuncReturns(values[5], func, as3lib.Infinity)
      self.assertFuncReturns(values[6], func, -as3lib.Infinity)
      self.assertFuncReturns(values[7], func, as3lib.NaN)
      self.assertFuncReturns(values[8], func, as3lib.true)
      self.assertFuncReturns(values[9], func, as3lib.false)
      self.assertFuncReturns(values[10], func, as3lib.undefined)
      self.assertFuncReturns(values[11], func, as3lib.null)
      self.assertFuncReturns(values[12], func, as3lib.String('55.5'))
      self.assertFuncReturns(values[13], func, obj)

   def assertFunc2(self, func, *values):
      obj = as3lib.Object()
      obj.valueOf = lambda: as3lib.Number(10.1)
      self.assertFuncReturns(values[0], func, 0, 0)
      self.assertFuncReturns(values[1], func, 1, 2)
      self.assertFuncReturns(values[2], func, 2, -4)
      self.assertFuncReturns(values[3], func, 4, -2)
      self.assertFuncReturns(values[4], func, -99, -100)
      self.assertFuncReturns(values[5], func, as3lib.Infinity, -as3lib.Infinity)
      self.assertFuncReturns(values[6], func, as3lib.NaN, 100)
      self.assertFuncReturns(values[7], func, 999, as3lib.NaN)
      self.assertFuncReturns(values[8], func, as3lib.true, as3lib.false)
      self.assertFuncReturns(values[9], func, as3lib.undefined, as3lib.null)
      self.assertFuncReturns(values[10], func, as3lib.String('55.5'), as3lib.String('-1234'))
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
      self.assertFunc1(Math.abs, 0, 1, 1, 1234.5, 1234.5, as3lib.Infinity,
                       as3lib.Infinity, as3lib.NaN, 1, 0, as3lib.NaN, 0, 55.5,
                       10.1)

   def test_acos(self):
      self.assertFunc1(Math.acos, 1.5707963267948966, 0, 3.141592653589793,
                       as3lib.NaN, as3lib.NaN, as3lib.NaN, as3lib.NaN,
                       as3lib.NaN, 0, 1.5707963267948966, as3lib.NaN,
                       1.5707963267948966, as3lib.NaN, as3lib.NaN)

   def test_asin(self):
      self.assertFunc1(Math.asin, 0, 1.5707963267948966, -1.5707963267948966,
                       as3lib.NaN, as3lib.NaN, as3lib.NaN, as3lib.NaN,
                       as3lib.NaN, 1.5707963267948966, 0, as3lib.NaN, 0,
                       as3lib.NaN, as3lib.NaN)

   def test_atan(self):
      self.assertFunc1(Math.atan, 0, 0.7853981633974483, -0.7853981633974483,
                       1.5699862824196225, -1.5699862824196225,
                       1.5707963267948966, -1.5707963267948966, as3lib.NaN,
                       0.7853981633974483, 0, as3lib.NaN, 0,
                       1.5527802582408412, 1.47210806614649)

   def test_atan2(self):
      self.assertFunc2(Math.atan2, 0, 0.4636476090008061, 2.677945044588987,
                       2.0344439357957027, -2.361219573523157,
                       2.356194490192345, as3lib.NaN, as3lib.NaN,
                       1.5707963267948966, as3lib.NaN, 3.096647253816438,
                       0.7853981633974483)

   def test_ceil(self):
      self.assertFunc1(Math.ceil, 0, 1, -1, 1235, -1234, as3lib.Infinity,
                       -as3lib.Infinity, as3lib.NaN, 1, 0, as3lib.NaN, 0, 56,
                       11)

   def test_cos(self):
      self.assertFunc1(Math.cos, 1, 0.5403023058681398, 0.5403023058681398,
                       -0.989373592132422, -0.989373592132422, as3lib.NaN,
                       as3lib.NaN, as3lib.NaN, 0.5403023058681398, 1,
                       as3lib.NaN, 1, 0.49872621790648564,
                       -0.7805681801691837)

   def test_exp(self):
      self.assertFunc1(Math.exp, 1, 2.718281828459045, 0.36787944117144233,
                       as3lib.Infinity, 0, as3lib.Infinity, 0, as3lib.NaN,
                       2.718281828459045, 1, as3lib.NaN, 1,
                       1.268655614010956e+24, 24343.00942440838)

   def test_floor(self):
      self.assertFunc1(Math.floor, 0, 1, -1, 1234, -1235, as3lib.Infinity,
                       -as3lib.Infinity, as3lib.NaN, 1, 0, as3lib.NaN, 0, 55,
                       10)

   def test_log(self):
      self.assertFunc1(Math.log, -as3lib.Infinity, 0, as3lib.NaN,
                       7.118421308785234, as3lib.NaN, as3lib.Infinity,
                       as3lib.NaN, as3lib.NaN, 0, -as3lib.Infinity,
                       as3lib.NaN, -as3lib.Infinity, 4.0163830207523885,
                       2.312535423847214)

   def test_max(self):
      self.assertFunc2(Math.max, 0, 2, 2, 4, -99, as3lib.Infinity, as3lib.NaN,
                       as3lib.NaN, 1, as3lib.NaN, 55.5, 10.1)

   def test_min(self):
      self.assertFunc2(Math.min, 0, 1, -4, -2, -100, -as3lib.Infinity,
                       as3lib.NaN, as3lib.NaN, 0, as3lib.NaN, -1234, 10.1)

   def test_pow(self):
      self.assertFunc2(Math.pow, 1, 1, 0.0625, 0.0625,
                       2.7319990264290253e-200, 0, as3lib.NaN, as3lib.NaN, 1,
                       1, 0, 13920212824.565023)

   def test_round(self):
      self.assertFunc1(Math.round, 0, 1, -1, 1235, -1234, as3lib.Infinity,
                       -as3lib.Infinity, as3lib.NaN, 1, 0, as3lib.NaN, 0, 56,
                       10)

   def test_sin(self):
      self.assertFunc1(Math.sin, 0, 0.8414709848078965, -0.8414709848078965,
                       0.14539565052293643, -0.14539565052293643, as3lib.NaN,
                       as3lib.NaN, as3lib.NaN, 0.8414709848078965, 0,
                       as3lib.NaN, 0, -0.8667595742607592,
                       -0.6250706488928821)

   def test_sqrt(self):
      self.assertFunc1(Math.sqrt, 0, 1, as3lib.NaN, 35.13545218152173,
                       as3lib.NaN, as3lib.Infinity, as3lib.NaN, as3lib.NaN, 1,
                       0, as3lib.NaN, 0, 7.44983221287567, 3.1780497164141406)

   def test_tan(self):
      self.assertFunc1(Math.tan, 0, 1.5574077246549023, -1.5574077246549023,
                       -0.14695727850342305, 0.14695727850342305, as3lib.NaN,
                       as3lib.NaN, as3lib.NaN, 1.5574077246549023, 0,
                       as3lib.NaN, 0, -1.7379466792405172, 0.8007893029375109)

   def test_minmax_special_cases(self):
      self.assertEqual(Math.min(), as3lib.Infinity)
      self.assertEqual(Math.min(0), 0)
      self.assertEqual(Math.min(1, 2, 3), 1)
      self.assertEqual(Math.min(-1.1, -2.2, -3.3), -3.3)
      self.assertNaN(Math.min(9, as3lib.NaN, as3lib.false, as3lib.true, as3lib.Infinity, as3lib.undefined))
      self.assertEqual(Math.max(), -as3lib.Infinity)
      self.assertEqual(Math.max(0), 0)
      self.assertEqual(Math.max(1, 2, 3), 3)
      self.assertEqual(Math.max(-1.1, -2.2, -3.3), -1.1)
      self.assertNaN(Math.max(9, as3lib.NaN, as3lib.false, as3lib.true, as3lib.Infinity, as3lib.undefined))


class NumberTests(NumberTestsBase):
   def test_constructor(self):
      self.assertEqual(as3lib.Number(), 0)
      self.assertEqual(as3lib.Number(as3lib.Number()), 0)
      self.assertEqual(as3lib.Number(as3lib.true), 1)
      self.assertEqual(as3lib.Number(as3lib.false), 0)
      self.assertEqual(as3lib.Number(as3lib.null), 0)
      self.assertNaN(as3lib.Number(as3lib.undefined))

      self.assertEqual(as3lib.Number(as3lib.String('')), 0)
      self.assertEqual(as3lib.Number(''), 0)
      self.assertNaN(as3lib.Number(as3lib.String('str')))
      self.assertNaN(as3lib.Number('str'))
      self.assertNaN(as3lib.Number(as3lib.String('true')))
      self.assertNaN(as3lib.Number('true'))
      self.assertNaN(as3lib.Number(as3lib.String('false')))
      self.assertNaN(as3lib.Number('false'))

      self.assertEqual(as3lib.Number(0.0), 0)

      self.assertNaN(as3lib.Number(as3lib.NaN))

      self.assertEqual(as3lib.Number(-0.0), 0)

      self.assertEqual(as3lib.Number(as3lib.Infinity), as3lib.Infinity)

      self.assertEqual(as3lib.Number(1.0), 1)
      self.assertEqual(as3lib.Number(-1.0), -1)
      self.assertEqual(as3lib.Number(0xFF1306), 16716550)
      self.assertEqual(as3lib.Number(1.2315e2), 123.15)
      self.assertEqual(as3lib.Number(0.0), 0)

      self.assertNaN(as3lib.Number(as3lib.Object()))

      self.assertEqual(as3lib.Number(as3lib.String('0.0')), 0)
      self.assertEqual(as3lib.Number('0.0'), 0)
      self.assertNaN(as3lib.Number(as3lib.String('NaN')))
      self.assertNaN(as3lib.Number('NaN'))
      self.assertEqual(as3lib.Number(as3lib.String('-0.0')), 0)
      self.assertEqual(as3lib.Number('-0.0'), 0)
      self.assertEqual(as3lib.Number(as3lib.String('Infinity')), as3lib.Infinity)
      self.assertEqual(as3lib.Number('Infinity'), as3lib.Infinity)
      self.assertEqual(as3lib.Number(as3lib.String('-Infinity')), -as3lib.Infinity)
      self.assertEqual(as3lib.Number('-Infinity'), -as3lib.Infinity)

      self.assertNaN(as3lib.Number(as3lib.String('infinity')))
      self.assertNaN(as3lib.Number('infinity'))
      self.assertNaN(as3lib.Number(as3lib.String('inf')))
      self.assertNaN(as3lib.Number('inf'))

      self.assertEqual(as3lib.Number(as3lib.String('1.0')), 1)
      self.assertEqual(as3lib.Number('1.0'), 1)
      self.assertEqual(as3lib.Number(as3lib.String('-1.0')), -1)
      self.assertEqual(as3lib.Number('-1.0'), -1)
      self.assertEqual(as3lib.Number(as3lib.String('0xFF1306')), 16716550)
      self.assertEqual(as3lib.Number('0xFF1306'), 16716550)
      self.assertEqual(as3lib.Number(as3lib.String('1.2315e2')), 123.15)
      self.assertEqual(as3lib.Number('1.2315e2'), 123.15)


class ObjectTests(as3libTestCase):
   def assertEnumerate(self, obj1, check):
      out = as3lib.Array()
      for name in obj1:
         out.push('%s = %s' % (name, obj1[name]))

      out.sort()
      self.assertEqual(out.toString(), check)

   def test_enumeration(self):
      x = as3lib.Object()
      x.key = 'value'
      x.key2 = 'value2'
      self.assertEnumerate(x, 'key = value,key2 = value2')

      # delete key2
      del x['key2']
      self.assertEnumerate(x, 'key = value')

      # other objects
      self.assertEnumerate(as3lib.Object(), '')
      self.assertEnumerate(as3lib.null, '')
      self.assertEnumerate(as3lib.undefined, '')

   def test_prototype(self):
      obj = as3lib.Object

      self.assertFalse(obj.hasOwnProperty('toString'))
      self.assertTrue(obj.prototype.hasOwnProperty('toString'))

      temp = as3lib.Object.prototype.toString
      o = obj()
      self.assertEqual(o.toString(), '[object Object]')
      as3lib.Object.prototype.toString = lambda: 'Custom toString'
      self.assertEqual(o.toString(), 'Custom toString')

      as3lib.Object.prototype.toString = temp

   def test_toLocaleString(self):
      o = as3lib.Object()
      self.assertEqual(o.toLocaleString(), '[object Object]')

   def test_toString(self):
      o = as3lib.Object()
      self.assertEqual(o.toString(), '[object Object]')

   def test_valueOf(self):
      obj = as3lib.Object()
      self.assertIs(obj.valueOf(), obj)


class OperationTests(as3libTestCase):
   def assertDivide(self, value1, value2, equals):
      n = value1 / value2
      self.assertEqual(n, equals)

   def assertDivideNaN(self, value1, value2, equals):
      n = value1 / value2
      self.assertIs(n, as3lib.NaN)

   def test_add(self):
      raise TestNotImplemented

   def test_subtract(self):
      raise TestNotImplemented

   def test_divide(self):
      # TODO: Add more of this test
      self.assertDivide(as3lib.true, as3lib.true, 1)
      self.assertDivide(as3lib.false, as3lib.true, 0)
      self.assertDivide(as3lib.null, as3lib.true, 0)
      self.assertDivideNaN(as3lib.undefined, as3lib.true)
      self.assertDivide(as3lib.String(''), as3lib.true, 0)
      self.assertDivideNaN(as3lib.String('str'), as3lib.true)
      self.assertDivideNaN(as3lib.String('true'), as3lib.true)
      self.assertDivideNaN(as3lib.String('false'), as3lib.true)
      self.assertDivide(as3lib.Number(0.0), as3lib.true, 0)
      self.assertDivideNaN(as3lib.NaN, as3lib.true)
      self.assertDivide(as3lib.Number(-0.0), as3lib.true, 0)
      self.assertDivide(as3lib.Infinity, as3lib.true, as3lib.Infinity)
      self.assertDivide(as3lib.Number(1.0), as3lib.true, 1)
      self.assertDivide(as3lib.Number(-1.0), as3lib.true, -1)

   def test_lshift(self):
      raise TestNotImplemented

   def test_rshift(self):
      raise TestNotImplemented

   def test_negate(self):
      self.assertEqual(-as3lib.true, -1)
      self.assertEqual(-as3lib.false, 0)
      self.assertEqual(-as3lib.null, 0)
      self.assertNaN(-as3lib.undefined)
      self.assertEqual(-as3lib.String(''), 0)
      self.assertNaN(-as3lib.String('str'))
      self.assertNaN(-as3lib.String('true'))
      self.assertNaN(-as3lib.String('false'))
      self.assertEqual(-as3lib.Number(0.0), 0)
      self.assertNaN(-as3lib.NaN)
      self.assertEqual(--as3lib.Number(0.0), 0)
      self.assertEqual(-as3lib.Infinity, as3lib.NInfinity)
      self.assertEqual(-as3lib.Number(1.0), as3lib.Int(-1))
      self.assertEqual(--as3lib.Number(1.0), as3lib.Int(1))
      self.assertNaN(-as3lib.Object())

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
      self.assertEqual(as3lib.Int(2), as3lib.String('2'))
      self.assertEqual(as3lib.Int(2), as3lib.Int(2))
      self.assertNotEqual(as3lib.Int(2), as3lib.Int(5))
      self.assertEqual(as3lib.true, as3lib.true)
      self.assertEqual(as3lib.false, as3lib.false)
      self.assertEqual(as3lib.true, as3lib.false)
      self.assertEqual(as3lib.Int(1), as3lib.true)
      self.assertEqual(as3lib.Int(0), as3lib.false)
      self.assertEqual(as3lib.String('abc'), as3lib.String('abc'))
      self.assertNotEqual(as3lib.Int(0), as3lib.undefined)
      self.assertEqual(as3lib.undefined, as3lib.undefined)
      self.assertNotEqual(as3lib.NaN, as3lib.NaN)
      self.assertNotEqual(as3lib.undefined, as3lib.NaN)
      self.assertNotEqual(as3lib.Int(0), as3lib.null)
      self.assertEqual(as3lib.null, as3lib.null)
      self.assertEqual(as3lib.undefined, as3lib.null)
      self.assertNotEqual(as3lib.NaN, as3lib.null)

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
      self.assertIsNot(as3lib.Int(2), as3lib.String('2'))
      self.assertIs(as3lib.Int(2), as3lib.Int(2))
      self.assertIsNot(as3lib.Int(2), as3lib.Int(5))
      self.assertIs(as3lib.true, as3lib.true)
      self.assertIs(as3lib.false, as3lib.false)
      self.assertIs(as3lib.true, as3lib.false)
      self.assertIsNot(as3lib.Int(1), as3lib.true)
      self.assertIsNot(as3lib.Int(0), as3lib.false)
      self.assertIs(as3lib.String('abc'), as3lib.String('abc'))
      self.assertIsNot(as3lib.Int(0), as3lib.undefined)
      self.assertIs(as3lib.undefined, as3lib.undefined)
      self.assertIs(as3lib.NaN, as3lib.NaN)
      self.assertIsNot(as3lib.undefined, as3lib.NaN)
      self.assertIsNot(as3lib.Int(0), as3lib.null)
      self.assertIs(as3lib.null, as3lib.null)
      self.assertIsNot(as3lib.undefined, as3lib.null)
      self.assertIsNot(as3lib.NaN, as3lib.null)

   def test_ifstrictne(self):
      raise TestNotImplemented

   def test_in(self):
      raise TestNotImplemented


class uintTests(NumberTestsBase):
   def test_constructor(self):
      self.assertEqual(as3lib.uint(), 0)
      self.assertEqual(as3lib.uint(as3lib.true), 1)
      self.assertEqual(as3lib.uint(as3lib.false), 0)
      self.assertEqual(as3lib.uint(as3lib.null), 0)
      self.assertEqual(as3lib.uint(as3lib.undefined), 0)
      self.assertEqual(as3lib.uint(as3lib.String('')), 0)

      self.assertEqual(as3lib.uint(''), 0)
      self.assertEqual(as3lib.uint(as3lib.String('str')), 0)
      self.assertEqual(as3lib.uint('str'), 0)
      self.assertEqual(as3lib.uint(as3lib.String('true')), 0)
      self.assertEqual(as3lib.uint('true'), 0)
      self.assertEqual(as3lib.uint(as3lib.String('false')), 0)
      self.assertEqual(as3lib.uint('false'), 0)

      self.assertEqual(as3lib.uint(as3lib.Number(0.0)), 0)
      self.assertEqual(as3lib.uint(0.0), 0)
      self.assertEqual(as3lib.uint(as3lib.NaN), 0)
      self.assertEqual(as3lib.uint(as3lib.Number(-0.0)), 0)
      self.assertEqual(as3lib.uint(-0.0), 0)
      self.assertEqual(as3lib.uint(as3lib.Infinity), 0)
      self.assertEqual(as3lib.uint(as3lib.Number(1.0)), 1)
      self.assertEqual(as3lib.uint(1.0), 1)
      self.assertEqual(as3lib.uint(as3lib.Number(-1.0)), 4294967295)
      self.assertEqual(as3lib.uint(-1.0), 4294967295)

      self.assertEqual(as3lib.uint(0xFF1306), 16716550)
      self.assertEqual(as3lib.uint(1.2315e2), 123)
      self.assertEqual(as3lib.uint(0x7FFFFFFF), 2147483647)
      self.assertEqual(as3lib.uint(0x80000000), 2147483648)
      self.assertEqual(as3lib.uint(0x80000001), 2147483649)
      self.assertEqual(as3lib.uint(0x180000001), 2147483649)
      self.assertEqual(as3lib.uint(0x100000001), 1)
      self.assertEqual(as3lib.uint(-0x7FFFFFFF), 2147483649)
      self.assertEqual(as3lib.uint(-0x80000000), 2147483648)
      self.assertEqual(as3lib.uint(-0x80000001), 2147483647)
      self.assertEqual(as3lib.uint(-0x180000001), 2147483647)
      self.assertEqual(as3lib.uint(-0x100000001), 4294967295)

      # Parse Tests
      self.assertEqual(as3lib.uint(as3lib.String('0.0')), 0)
      self.assertEqual(as3lib.uint(as3lib.String('NaN')), 0)
      self.assertEqual(as3lib.uint(as3lib.String('-0.0')), 0)
      self.assertEqual(as3lib.uint(as3lib.String('Infinity')), 0)
      self.assertEqual(as3lib.uint(as3lib.String('1.0')), 1)
      self.assertEqual(as3lib.uint(as3lib.String('-1.0')), 4294967295)
      self.assertEqual(as3lib.uint(as3lib.String('0xFF1306')), 16716550)
      self.assertEqual(as3lib.uint(as3lib.String('1.2315e2')), 123)
      self.assertEqual(as3lib.uint(as3lib.String('0x7FFFFFFF')), 2147483647)
      self.assertEqual(as3lib.uint(as3lib.String('0x80000000')), 2147483648)
      self.assertEqual(as3lib.uint(as3lib.String('0x80000001')), 2147483649)
      self.assertEqual(as3lib.uint(as3lib.String('0x180000001')), 2147483649)
      self.assertEqual(as3lib.uint(as3lib.String('0x100000001')), 1)
      self.assertEqual(as3lib.uint(as3lib.String('-0x7FFFFFFF')), 2147483649)
      self.assertEqual(as3lib.uint(as3lib.String('-0x80000000')), 2147483648)
      self.assertEqual(as3lib.uint(as3lib.String('-0x80000001')), 2147483647)
      self.assertEqual(as3lib.uint(as3lib.String('-0x180000001')), 2147483647)
      self.assertEqual(as3lib.uint(as3lib.String('-0x100000001')), 4294967295)

      self.assertEqual(as3lib.uint(as3lib.Object()), 0)

   def assertToExponential(self, value, check):
      val = as3lib.uint(value)
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

      asrt_2147483649 = ('2e+9','2.1e+9', '2.15e+9', '2.147e+9', '2.1475e+9',
                         '2.14748e+9', '2.147484e+9', '2.1474836e+9',
                         '2.14748365e+9', '2.147483649e+9', '2.1474836490e+9',
                         '2.14748364900000000000e+9')

      self.assertToExponential(as3lib.true, asrt_1)

      self.assertToExponential(as3lib.false, asrt_0)
      self.assertToExponential(as3lib.null, asrt_0)
      self.assertToExponential(as3lib.undefined, asrt_0)

      self.assertToExponential(as3lib.String(''), asrt_0)
      self.assertToExponential('', asrt_0)

      self.assertToExponential(as3lib.String('str'), asrt_0)
      self.assertToExponential('str', asrt_0)

      self.assertToExponential(as3lib.String('true'), asrt_0)
      self.assertToExponential('true', asrt_0)

      self.assertToExponential(as3lib.String('false'), asrt_0)
      self.assertToExponential('false', asrt_0)

      self.assertToExponential(as3lib.Number(0.0), asrt_0)
      self.assertToExponential(0.0, asrt_0)

      self.assertToExponential(as3lib.NaN, asrt_0)

      self.assertToExponential(as3lib.Number(-0.0), asrt_0)
      self.assertToExponential(-0.0, asrt_0)

      self.assertToExponential(as3lib.Infinity, asrt_0)

      self.assertToExponential(as3lib.Number(1.0), asrt_1)
      self.assertToExponential(1.0, asrt_1)

      self.assertToExponential(as3lib.Number(-1.0), asrt_4294967295)
      self.assertToExponential(-1.0, asrt_4294967295)

      self.assertToExponential(as3lib.Number(0xFF1306), asrt_16716550)
      self.assertToExponential(0xFF1306, asrt_16716550)

      self.assertToExponential(as3lib.Number(1.2315e2), asrt_123)
      self.assertToExponential(1.2315e2, asrt_123)

      self.assertToExponential(as3lib.Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToExponential(0x7FFFFFFF, asrt_2147483647)

      self.assertToExponential(as3lib.Number(0x80000000), asrt_2147483648)
      self.assertToExponential(0x80000000, asrt_2147483648)

      self.assertToExponential(as3lib.Number(0x80000001), asrt_2147483649)
      self.assertToExponential(0x80000001, asrt_2147483649)

      self.assertToExponential(as3lib.Number(0x180000001), asrt_2147483649)
      self.assertToExponential(0x180000001, asrt_2147483649)

      self.assertToExponential(as3lib.Number(0x100000001), asrt_1)
      self.assertToExponential(0x100000001, asrt_1)

      self.assertToExponential(as3lib.Number(-0x7FFFFFFF), asrt_2147483649)
      self.assertToExponential(-0x7FFFFFFF, asrt_2147483649)

      self.assertToExponential(as3lib.Number(-0x80000000), asrt_2147483648)
      self.assertToExponential(-0x80000000, asrt_2147483648)

      self.assertToExponential(as3lib.Number(-0x80000001), asrt_2147483647)
      self.assertToExponential(-0x80000001, asrt_2147483647)

      self.assertToExponential(as3lib.Number(-0x180000001), asrt_2147483647)
      self.assertToExponential(-0x180000001, asrt_2147483647)

      self.assertToExponential(as3lib.Number(-0x100000001), asrt_4294967295)
      self.assertToExponential(-0x100000001, asrt_4294967295)

      self.assertToExponential(as3lib.Object(), asrt_0)

      # Parse tests
      self.assertToExponential(as3lib.String('0.0'), asrt_0)
      self.assertToExponential('0.0', asrt_0)
      self.assertToExponential(as3lib.String('NaN'), asrt_0)
      self.assertToExponential('NaN', asrt_0)
      self.assertToExponential(as3lib.String('-0.0'), asrt_0)
      self.assertToExponential('-0.0', asrt_0)
      self.assertToExponential(as3lib.String('Infinity'), asrt_0)
      self.assertToExponential('Infinity', asrt_0)
      self.assertToExponential(as3lib.String('1.0'), asrt_1)
      self.assertToExponential('1.0', asrt_1)
      self.assertToExponential(as3lib.String('-1.0'), asrt_4294967295)
      self.assertToExponential('-1.0', asrt_4294967295)
      self.assertToExponential(as3lib.String('0xFF1306'), asrt_16716550)
      self.assertToExponential('0xFF1306', asrt_16716550)
      self.assertToExponential(as3lib.String('1.2315e2'), asrt_123)
      self.assertToExponential('1.2315e2', asrt_123)
      self.assertToExponential(as3lib.String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToExponential('0x7FFFFFFF', asrt_2147483647)
      self.assertToExponential(as3lib.String('0x80000000'), asrt_2147483648)
      self.assertToExponential('0x80000000', asrt_2147483648)
      self.assertToExponential(as3lib.String('0x80000001'), asrt_2147483649)
      self.assertToExponential('0x80000001', asrt_2147483649)
      self.assertToExponential(as3lib.String('0x180000001'), asrt_2147483649)
      self.assertToExponential('0x180000001', asrt_2147483649)
      self.assertToExponential(as3lib.String('0x100000001'), asrt_1)
      self.assertToExponential('0x100000001', asrt_1)
      self.assertToExponential(as3lib.String('-0x7FFFFFFF'), asrt_2147483649)
      self.assertToExponential('-0x7FFFFFFF', asrt_2147483649)
      self.assertToExponential(as3lib.String('-0x80000000'), asrt_2147483648)
      self.assertToExponential('-0x80000000', asrt_2147483648)
      self.assertToExponential(as3lib.String('-0x80000001'), asrt_2147483647)
      self.assertToExponential('-0x80000001', asrt_2147483647)
      self.assertToExponential(as3lib.String('-0x180000001'), asrt_2147483647)
      self.assertToExponential('-0x180000001', asrt_2147483647)
      self.assertToExponential(as3lib.String('-0x100000001'), asrt_4294967295)
      self.assertToExponential('-0x100000001', asrt_4294967295)

   def assertToFixed(self, value, check):
      val = as3lib.uint(value)
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

      self.assertToFixed(as3lib.true, asrt_1)

      self.assertToFixed(as3lib.false, asrt_0)
      self.assertToFixed(as3lib.null, asrt_0)
      self.assertToFixed(as3lib.undefined, asrt_0)

      self.assertToFixed(as3lib.String(''), asrt_0)
      self.assertToFixed('', asrt_0)

      self.assertToFixed(as3lib.String('str'), asrt_0)
      self.assertToFixed('str', asrt_0)

      self.assertToFixed(as3lib.String('true'), asrt_0)
      self.assertToFixed('true', asrt_0)

      self.assertToFixed(as3lib.String('false'), asrt_0)
      self.assertToFixed('false', asrt_0)

      self.assertToFixed(as3lib.Number(0.0), asrt_0)
      self.assertToFixed(0.0, asrt_0)

      self.assertToFixed(as3lib.NaN, asrt_0)

      self.assertToFixed(as3lib.Number(-0.0), asrt_0)
      self.assertToFixed(-0.0, asrt_0)

      self.assertToFixed(as3lib.Infinity, asrt_0)

      self.assertToFixed(as3lib.Number(1.0), asrt_1)
      self.assertToFixed(1.0, asrt_1)

      self.assertToFixed(as3lib.Number(-1.0), asrt_4294967295)
      self.assertToFixed(-1.0, asrt_4294967295)

      self.assertToFixed(as3lib.Number(0xFF1306), asrt_16716550)
      self.assertToFixed(0xFF1306, asrt_16716550)

      self.assertToFixed(as3lib.Number(1.2315e2), asrt_123)
      self.assertToFixed(1.2315e2, asrt_123)

      self.assertToFixed(as3lib.Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToFixed(0x7FFFFFFF, asrt_2147483647)

      self.assertToFixed(as3lib.Number(0x80000000), asrt_2147483648)
      self.assertToFixed(0x80000000, asrt_2147483648)

      self.assertToFixed(as3lib.Number(0x80000001), asrt_2147483649)
      self.assertToFixed(0x80000001, asrt_2147483649)

      self.assertToFixed(as3lib.Number(0x180000001), asrt_2147483649)
      self.assertToFixed(0x180000001, asrt_2147483649)

      self.assertToFixed(as3lib.Number(0x100000001), asrt_1)
      self.assertToFixed(0x100000001, asrt_1)

      self.assertToFixed(as3lib.Number(-0x7FFFFFFF), asrt_2147483649)
      self.assertToFixed(-0x7FFFFFFF, asrt_2147483649)

      self.assertToFixed(as3lib.Number(-0x80000000), asrt_2147483648)
      self.assertToFixed(-0x80000000, asrt_2147483648)

      self.assertToFixed(as3lib.Number(-0x80000001), asrt_2147483647)
      self.assertToFixed(-0x80000001, asrt_2147483647)

      self.assertToFixed(as3lib.Number(-0x180000001), asrt_2147483647)
      self.assertToFixed(-0x180000001, asrt_2147483647)

      self.assertToFixed(as3lib.Number(-0x100000001), asrt_4294967295)
      self.assertToFixed(-0x100000001, asrt_4294967295)

      self.assertToFixed(as3lib.Object(), asrt_0)

      # Parse tests
      self.assertToFixed(as3lib.String('0.0'), asrt_0)
      self.assertToFixed('0.0', asrt_0)
      self.assertToFixed(as3lib.String('NaN'), asrt_0)
      self.assertToFixed('NaN', asrt_0)
      self.assertToFixed(as3lib.String('-0.0'), asrt_0)
      self.assertToFixed('-0.0', asrt_0)
      self.assertToFixed(as3lib.String('Infinity'), asrt_0)
      self.assertToFixed('Infinity', asrt_0)
      self.assertToFixed(as3lib.String('1.0'), asrt_1)
      self.assertToFixed('1.0', asrt_1)
      self.assertToFixed(as3lib.String('-1.0'), asrt_4294967295)
      self.assertToFixed('-1.0', asrt_4294967295)
      self.assertToFixed(as3lib.String('0xFF1306'), asrt_16716550)
      self.assertToFixed('0xFF1306', asrt_16716550)
      self.assertToFixed(as3lib.String('1.2315e2'), asrt_123)
      self.assertToFixed('1.2315e2', asrt_123)
      self.assertToFixed(as3lib.String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToFixed('0x7FFFFFFF', asrt_2147483647)
      self.assertToFixed(as3lib.String('0x80000000'), asrt_2147483648)
      self.assertToFixed('0x80000000', asrt_2147483648)
      self.assertToFixed(as3lib.String('0x80000001'), asrt_2147483649)
      self.assertToFixed('0x80000001', asrt_2147483649)
      self.assertToFixed(as3lib.String('0x180000001'), asrt_2147483649)
      self.assertToFixed('0x180000001', asrt_2147483649)
      self.assertToFixed(as3lib.String('0x100000001'), asrt_1)
      self.assertToFixed('0x100000001', asrt_1)
      self.assertToFixed(as3lib.String('-0x7FFFFFFF'), asrt_2147483649)
      self.assertToFixed('-0x7FFFFFFF', asrt_2147483649)
      self.assertToFixed(as3lib.String('-0x80000000'), asrt_2147483648)
      self.assertToFixed('-0x80000000', asrt_2147483648)
      self.assertToFixed(as3lib.String('-0x80000001'), asrt_2147483647)
      self.assertToFixed('-0x80000001', asrt_2147483647)
      self.assertToFixed(as3lib.String('-0x180000001'), asrt_2147483647)
      self.assertToFixed('-0x180000001', asrt_2147483647)
      self.assertToFixed(as3lib.String('-0x100000001'), asrt_4294967295)
      self.assertToFixed('-0x100000001', asrt_4294967295)

   def assertToPrecision(self, value, check):
      val = as3lib.uint(value)
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

      self.assertToPrecision(as3lib.true, asrt_1)

      self.assertToPrecision(as3lib.false, asrt_0)
      self.assertToPrecision(as3lib.null, asrt_0)
      self.assertToPrecision(as3lib.undefined, asrt_0)

      self.assertToPrecision(as3lib.String(''), asrt_0)
      self.assertToPrecision('', asrt_0)

      self.assertToPrecision(as3lib.String('str'), asrt_0)
      self.assertToPrecision('str', asrt_0)

      self.assertToPrecision(as3lib.String('true'), asrt_0)
      self.assertToPrecision('true', asrt_0)

      self.assertToPrecision(as3lib.String('false'), asrt_0)
      self.assertToPrecision('false', asrt_0)

      self.assertToPrecision(as3lib.Number(0.0), asrt_0)
      self.assertToPrecision(0.0, asrt_0)

      self.assertToPrecision(as3lib.NaN, asrt_0)

      self.assertToPrecision(as3lib.Number(-0.0), asrt_0)
      self.assertToPrecision(-0.0, asrt_0)

      self.assertToPrecision(as3lib.Infinity, asrt_0)

      self.assertToPrecision(as3lib.Number(1.0), asrt_1)
      self.assertToPrecision(1.0, asrt_1)

      self.assertToPrecision(as3lib.Number(-1.0), asrt_4294967295)
      self.assertToPrecision(-1.0, asrt_4294967295)

      self.assertToPrecision(as3lib.Number(0xFF1306), asrt_16716550)
      self.assertToPrecision(0xFF1306, asrt_16716550)

      self.assertToPrecision(as3lib.Number(1.2315e2), asrt_123)
      self.assertToPrecision(1.2315e2, asrt_123)

      self.assertToPrecision(as3lib.Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToPrecision(0x7FFFFFFF, asrt_2147483647)

      self.assertToPrecision(as3lib.Number(0x80000000), asrt_2147483648)
      self.assertToPrecision(0x80000000, asrt_2147483648)

      self.assertToPrecision(as3lib.Number(0x80000001), asrt_2147483649)
      self.assertToPrecision(0x80000001, asrt_2147483649)

      self.assertToPrecision(as3lib.Number(0x180000001), asrt_2147483649)
      self.assertToPrecision(0x180000001, asrt_2147483649)

      self.assertToPrecision(as3lib.Number(0x100000001), asrt_1)
      self.assertToPrecision(0x100000001, asrt_1)

      self.assertToPrecision(as3lib.Number(-0x7FFFFFFF), asrt_2147483649)
      self.assertToPrecision(-0x7FFFFFFF, asrt_2147483649)

      self.assertToPrecision(as3lib.Number(-0x80000000), asrt_2147483648)
      self.assertToPrecision(-0x80000000, asrt_2147483648)

      self.assertToPrecision(as3lib.Number(-0x80000001), asrt_2147483647)
      self.assertToPrecision(-0x80000001, asrt_2147483647)

      self.assertToPrecision(as3lib.Number(-0x180000001), asrt_2147483647)
      self.assertToPrecision(-0x180000001, asrt_2147483647)

      self.assertToPrecision(as3lib.Number(-0x100000001), asrt_4294967295)
      self.assertToPrecision(-0x100000001, asrt_4294967295)

      self.assertToPrecision(as3lib.Object(), asrt_0)

      # Parse tests
      self.assertToPrecision(as3lib.String('0.0'), asrt_0)
      self.assertToPrecision('0.0', asrt_0)
      self.assertToPrecision(as3lib.String('NaN'), asrt_0)
      self.assertToPrecision('NaN', asrt_0)
      self.assertToPrecision(as3lib.String('-0.0'), asrt_0)
      self.assertToPrecision('-0.0', asrt_0)
      self.assertToPrecision(as3lib.String('Infinity'), asrt_0)
      self.assertToPrecision('Infinity', asrt_0)
      self.assertToPrecision(as3lib.String('1.0'), asrt_1)
      self.assertToPrecision('1.0', asrt_1)
      self.assertToPrecision(as3lib.String('-1.0'), asrt_4294967295)
      self.assertToPrecision('-1.0', asrt_4294967295)
      self.assertToPrecision(as3lib.String('0xFF1306'), asrt_16716550)
      self.assertToPrecision('0xFF1306', asrt_16716550)
      self.assertToPrecision(as3lib.String('1.2315e2'), asrt_123)
      self.assertToPrecision('1.2315e2', asrt_123)
      self.assertToPrecision(as3lib.String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToPrecision('0x7FFFFFFF', asrt_2147483647)
      self.assertToPrecision(as3lib.String('0x80000000'), asrt_2147483648)
      self.assertToPrecision('0x80000000', asrt_2147483648)
      self.assertToPrecision(as3lib.String('0x80000001'), asrt_2147483649)
      self.assertToPrecision('0x80000001', asrt_2147483649)
      self.assertToPrecision(as3lib.String('0x180000001'), asrt_2147483649)
      self.assertToPrecision('0x180000001', asrt_2147483649)
      self.assertToPrecision(as3lib.String('0x100000001'), asrt_1)
      self.assertToPrecision('0x100000001', asrt_1)
      self.assertToPrecision(as3lib.String('-0x7FFFFFFF'), asrt_2147483649)
      self.assertToPrecision('-0x7FFFFFFF', asrt_2147483649)
      self.assertToPrecision(as3lib.String('-0x80000000'), asrt_2147483648)
      self.assertToPrecision('-0x80000000', asrt_2147483648)
      self.assertToPrecision(as3lib.String('-0x80000001'), asrt_2147483647)
      self.assertToPrecision('-0x80000001', asrt_2147483647)
      self.assertToPrecision(as3lib.String('-0x180000001'), asrt_2147483647)
      self.assertToPrecision('-0x180000001', asrt_2147483647)
      self.assertToPrecision(as3lib.String('-0x100000001'), asrt_4294967295)
      self.assertToPrecision('-0x100000001', asrt_4294967295)

   def assertToString(self, value, check):
      val = as3lib.uint(value)
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

      self.assertToString(as3lib.true, asrt_1)

      self.assertToString(as3lib.false, asrt_0)
      self.assertToString(as3lib.null, asrt_0)
      self.assertToString(as3lib.undefined, asrt_0)

      self.assertToString(as3lib.String(''), asrt_0)
      self.assertToString('', asrt_0)

      self.assertToString(as3lib.String('str'), asrt_0)
      self.assertToString('str', asrt_0)

      self.assertToString(as3lib.String('true'), asrt_0)
      self.assertToString('true', asrt_0)

      self.assertToString(as3lib.String('false'), asrt_0)
      self.assertToString('false', asrt_0)

      self.assertToString(as3lib.Number(0.0), asrt_0)
      self.assertToString(0.0, asrt_0)

      self.assertToString(as3lib.NaN, asrt_0)

      self.assertToString(as3lib.Number(-0.0), asrt_0)
      self.assertToString(-0.0, asrt_0)

      self.assertToString(as3lib.Infinity, asrt_0)

      self.assertToString(as3lib.Number(1.0), asrt_1)
      self.assertToString(1.0, asrt_1)

      self.assertToString(as3lib.Number(-1.0), asrt_4294967295)
      self.assertToString(-1.0, asrt_4294967295)

      self.assertToString(as3lib.Number(0xFF1306), asrt_16716550)
      self.assertToString(0xFF1306, asrt_16716550)

      self.assertToString(as3lib.Number(1.2315e2), asrt_123)
      self.assertToString(1.2315e2, asrt_123)

      self.assertToString(as3lib.Number(0x7FFFFFFF), asrt_2147483647)
      self.assertToString(0x7FFFFFFF, asrt_2147483647)

      self.assertToString(as3lib.Number(0x80000000), asrt_2147483648)
      self.assertToString(0x80000000, asrt_2147483648)

      self.assertToString(as3lib.Number(0x80000001), asrt_2147483649)
      self.assertToString(0x80000001, asrt_2147483649)

      self.assertToString(as3lib.Number(0x180000001), asrt_2147483649)
      self.assertToString(0x180000001, asrt_2147483649)

      self.assertToString(as3lib.Number(0x100000001), asrt_1)
      self.assertToString(0x100000001, asrt_1)

      self.assertToString(as3lib.Number(-0x7FFFFFFF), asrt_2147483649)
      self.assertToString(-0x7FFFFFFF, asrt_2147483649)

      self.assertToString(as3lib.Number(-0x80000000), asrt_2147483648)
      self.assertToString(-0x80000000, asrt_2147483648)

      self.assertToString(as3lib.Number(-0x80000001), asrt_2147483647)
      self.assertToString(-0x80000001, asrt_2147483647)

      self.assertToString(as3lib.Number(-0x180000001), asrt_2147483647)
      self.assertToString(-0x180000001, asrt_2147483647)

      self.assertToString(as3lib.Number(-0x100000001), asrt_4294967295)
      self.assertToString(-0x100000001, asrt_4294967295)

      self.assertToString(as3lib.Object(), asrt_0)

      # Parse tests
      self.assertToString(as3lib.String('0.0'), asrt_0)
      self.assertToString('0.0', asrt_0)
      self.assertToString(as3lib.String('NaN'), asrt_0)
      self.assertToString('NaN', asrt_0)
      self.assertToString(as3lib.String('-0.0'), asrt_0)
      self.assertToString('-0.0', asrt_0)
      self.assertToString(as3lib.String('Infinity'), asrt_0)
      self.assertToString('Infinity', asrt_0)
      self.assertToString(as3lib.String('1.0'), asrt_1)
      self.assertToString('1.0', asrt_1)
      self.assertToString(as3lib.String('-1.0'), asrt_4294967295)
      self.assertToString('-1.0', asrt_4294967295)
      self.assertToString(as3lib.String('0xFF1306'), asrt_16716550)
      self.assertToString('0xFF1306', asrt_16716550)
      self.assertToString(as3lib.String('1.2315e2'), asrt_123)
      self.assertToString('1.2315e2', asrt_123)
      self.assertToString(as3lib.String('0x7FFFFFFF'), asrt_2147483647)
      self.assertToString('0x7FFFFFFF', asrt_2147483647)
      self.assertToString(as3lib.String('0x80000000'), asrt_2147483648)
      self.assertToString('0x80000000', asrt_2147483648)
      self.assertToString(as3lib.String('0x80000001'), asrt_2147483649)
      self.assertToString('0x80000001', asrt_2147483649)
      self.assertToString(as3lib.String('0x180000001'), asrt_2147483649)
      self.assertToString('0x180000001', asrt_2147483649)
      self.assertToString(as3lib.String('0x100000001'), asrt_1)
      self.assertToString('0x100000001', asrt_1)
      self.assertToString(as3lib.String('-0x7FFFFFFF'), asrt_2147483649)
      self.assertToString('-0x7FFFFFFF', asrt_2147483649)
      self.assertToString(as3lib.String('-0x80000000'), asrt_2147483648)
      self.assertToString('-0x80000000', asrt_2147483648)
      self.assertToString(as3lib.String('-0x80000001'), asrt_2147483647)
      self.assertToString('-0x80000001', asrt_2147483647)
      self.assertToString(as3lib.String('-0x180000001'), asrt_2147483647)
      self.assertToString('-0x180000001', asrt_2147483647)
      self.assertToString(as3lib.String('-0x100000001'), asrt_4294967295)
      self.assertToString('-0x100000001', asrt_4294967295)


class VectorTests(as3libTestCase):
   def test_constructor(self):
      a_bool = as3lib.Vector.Boolean(2)
      self.assertEqual(a_bool.length, 2)
      self.assertFalse(a_bool.fixed)

      b_bool = as3lib.Vector.Boolean(3, True)
      self.assertEqual(b_bool.length, 3)
      self.assertTrue(b_bool.fixed)

      c_bool = as3lib.Vector.Boolean()
      self.assertEqual(c_bool.length, 0)
      self.assertFalse(c_bool.fixed)

      class Superclass:...

      class Subclass(Superclass):...

      a0_class = Superclass()
      a1_class = Subclass()

      a_class = as3lib.Vector(2, type=Superclass)
      self.assertEqual(a_class.length, 2)
      self.assertFalse(a_class.fixed)

      b_class = as3lib.Vector(3, True, type=Superclass)
      self.assertEqual(b_class.length, 3)
      self.assertTrue(b_class.fixed)

      c_class = as3lib.Vector(type=Superclass)
      self.assertEqual(c_class.length, 0)
      self.assertFalse(c_class.fixed)

      a_int = as3lib.Vector.int(2)
      self.assertEqual(a_int.length, 2)
      self.assertFalse(a_int.fixed)

      b_int = as3lib.Vector.int(3, True)
      self.assertEqual(b_int.length, 3)
      self.assertTrue(b_int.fixed)

      c_int = as3lib.Vector.int()
      self.assertEqual(c_int.length, 0)
      self.assertFalse(c_int.fixed)

      a_number = as3lib.Vector.Number(2)
      self.assertEqual(a_number.length, 2)
      self.assertFalse(a_number.fixed)

      b_number = as3lib.Vector.Number(3, True)
      self.assertEqual(b_number.length, 3)
      self.assertTrue(b_number.fixed)

      c_number = as3lib.Vector.Number()
      self.assertEqual(c_number.length, 0)
      self.assertFalse(c_number.fixed)

      a_string = as3lib.Vector.String(2)
      self.assertEqual(a_string.length, 2)
      self.assertFalse(a_string.fixed)

      b_string = as3lib.Vector.String(3, True)
      self.assertEqual(b_string.length, 3)
      self.assertTrue(b_string.fixed)

      c_string = as3lib.Vector.String()
      self.assertEqual(c_string.length, 0)
      self.assertFalse(c_string.fixed)

      a_uint = as3lib.Vector.uint(2)
      self.assertEqual(a_uint.length, 2)
      self.assertFalse(a_uint.fixed)

      b_uint = as3lib.Vector.uint(3, True)
      self.assertEqual(b_uint.length, 3)
      self.assertTrue(b_uint.fixed)

      c_uint = as3lib.Vector.uint()
      self.assertEqual(c_uint.length, 0)
      self.assertFalse(c_uint.fixed)

      raise MethodNotImplemented('Vector.<Vector>')
      a_vector = as3lib.Vector(2, type=as3lib.Vector.int)
      self.assertEqual(a_vector.length, 2)
      self.assertFalse(a_vector.fixed)

      b_vector = as3lib.Vector.uint(3, True, type=as3lib.Vector.int)
      self.assertEqual(b_vector.length, 3)
      self.assertTrue(b_vector.fixed)

      c_vector = as3lib.Vector.uint(type=as3lib.Vector.int)
      self.assertEqual(c_vector.length, 0)
      self.assertFalse(c_vector.fixed)

   def test_concat(self):
      a_bool = as3lib.Vector.Boolean([True, False])
      b_bool = as3lib.Vector.Boolean([False, True, False])
      self.assertArray(a_bool.concat(b_bool), (True, False, False, True, False))

      class Superclass:...

      class Subclass(Superclass):...

      a_class = as3lib.Vector([], type=Superclass)
      a_class.length = 2
      a_class[0] = Superclass()
      a_class[1] = Subclass()

      b_class = as3lib.Vector([], type=Subclass)
      b_class.length = 1
      b_class[0] = Subclass()

      c_class = a_class.concat(b_class)

      self.assertEqual(c_class.length, 3)
      self.assertType(c_class[0], Superclass)
      self.assertType(c_class[1], Subclass)
      self.assertType(c_class[2], Subclass)

      c_class_flipped = b_class.concat(as3lib.Vector([Subclass()], type=Subclass))

      self.assertEqual(c_class_flipped.length, 2)
      self.assertType(c_class_flipped[0], Subclass)
      self.assertType(c_class_flipped[1], Subclass)

      class Interface:...
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

   def test_null_callback(self):
      # TODO: Make sure this is correct
      v = as3lib.Vector.int()
      v.push(1)
      self.assertTrue(v.every(as3lib.null))
      self.assertIs(v.filter(as3lib.null), None)
      self.assertEqual(v.forEach(as3lib.null), as3lib.undefined)
      self.assertEqual(v.map(as3lib.null), 0)
      self.assertFalse(v.some(as3lib.null))


class WTFJSTests(as3libTestCase):
   # These tests are inspired by various documents called WTFJS. These things
   # don't make sense at first glance.
   # https://github.com/denysdovhan/wtfjs
   def test_banana(self):
      self.assertEqual(as3lib.String('b') + as3lib.String('a') + + as3lib.String('a') + as3lib.String('a'), 'baNaNa')

   def test_not_array(self):
      self.assertEqual(+as3lib.Array(), 0)
      self.assertEqual(not as3lib.Array(), as3lib.false)
      self.assertTrue(as3lib.Array() == (not as3lib.Array()))

      # Booleans
      self.assertFalse(as3lib.true == as3lib.Array())
      self.assertFalse(as3lib.true == (not as3lib.Array()))
      self.asserttrue(as3lib.false == as3lib.Array())
      self.assertTrue(as3lib.false == (not as3lib.Array()))

   def test_string_bools(self):
      self.assertEqual(not not as3lib.String('false'), not not as3lib.String('true'))
      self.assertIs(not not as3lib.String('false'), not not as3lib.String('true'))

   def test_fail(self):
      # Original (![] + [])[+[]] + (![] + [])[+!+[]] + ([![]] + [][[]])[+!+[] + [+[]]] + (![] + [])[!+[] + !+[]];
      self.assertEqual((not as3lib.Array() + as3lib.Array())[+as3lib.Array()] + (not as3lib.Array() + as3lib.Array())[+(not+as3lib.Array())] + (as3lib.Array(not as3lib.Array()) + as3lib.Array()[as3lib.Array()])[+(not+as3lib.Array()) + as3lib.Array(+as3lib.Array)] + (not as3lib.Array() + as3lib.Array())[not+as3lib.Array() + (not+as3lib.Array())], 'fail')

   def test_truthy_arry(self):
      self.assertTrue(not not as3lib.Array())
      self.assertFalse(as3lib.Array())

   def test_falsy_null(self):
      self.assertFalse(not not as3lib.null)
      self.assertFalse(as3lib.null == as3lib.false)

   def test_add_array(self):
      self.assertEqual(as3lib.Array(1, 2, 3) + as3lib.Array(4, 5, 6), '1,2,34,5,6')

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
      self.assertEqual(as3lib.Array(), as3lib.String())
      self.assertEqual(as3lib.Array(), as3lib.Number(0))
      self.assertEqual(as3lib.Array(['']), as3lib.String())
      self.assertEqual(as3lib.Array([0]), as3lib.Number(0))
      self.assertNotEqual(as3lib.Array([0]), as3lib.String())
      self.assertEqual(as3lib.Array(['']), as3lib.Number(0))

      self.assertEqual(as3lib.Array([as3lib.null]), as3lib.String())
      self.assertEqual(as3lib.Array([as3lib.null]), as3lib.Number(0))
      self.assertEqual(as3lib.Array([as3lib.undefined]), as3lib.String())
      self.assertEqual(as3lib.Array([as3lib.undefined]), as3lib.Number(0))

      self.assertEqual(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array()))))), as3lib.String())
      self.assertEqual(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array()))))), as3lib.Number(0))

      self.assertEqual(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.null)))))), as3lib.String())
      self.assertEqual(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.null)))))), as3lib.Number(0))

      self.assertEqual(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.undefined)))))), as3lib.String())
      self.assertEqual(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.Array(as3lib.undefined)))))), as3lib.Number(0))

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
      self.assertEqual(as3lib.parseInt(as3lib.null, 24), 23)
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
      self.assertEqual(as3lib.Number(3) - as3lib.Number(1), as3lib.Number(2))
      self.assertEqual(as3lib.Number(3) + as3lib.Number(1), as3lib.Number(4))
      self.assertEqual(as3lib.String('3') - as3lib.Number(1), as3lib.Number(2))
      self.assertEqual(as3lib.String('3') + as3lib.Number(1), as3lib.String('31'))

      self.assertEqual(as3lib.String('') + as3lib.String(''), as3lib.String(''))
      self.assertEqual(as3lib.Array() + as3lib.Array(), as3lib.String(''))
      self.assertEqual(as3lib.Object() + as3lib.Array(), as3lib.Number(0))
      self.assertEqual(as3lib.Array() + as3lib.Object(), as3lib.String('[object Object]'))
      self.assertEqual(as3lib.Object() + as3lib.Object(), as3lib.String('[object Object][object Object]'))

      self.assertEqual(as3lib.String('222') - -as3lib.String('111'), as3lib.Number('333'))

      self.assertEqual(as3lib.Array([4]) * as3lib.Array([4]), as3lib.Number(16))
      self.assertEqual(as3lib.Array() * as3lib.Array(), as3lib.Number(0))
      self.assertEqual(as3lib.Array([4, 4]) * as3lib.Array([4, 4]), as3lib.NaN)

   def test_yield_self(self):
      # The syntax here is a little bit different but it still works
      def f():
         yield f

      self.assertIs(next(next(next(next(next(f())())())())()), f)

   def test_minmax(self):
      self.assertIs(Math.min(), as3lib.Infinity)
      self.assertIs(Math.max(), as3lib.NInfinity)
      self.assertLess(Math.max(), Math.min())

   def test_infinite_timeout(self):
      # This will execute immediately because Infinity does not fit into a
      # 32bit uint
      # TODO: console.log
      # setTimeout(() => console.log("called"), Infinity)
      # TODO: Make this an assert
      setTimeout(print, as3lib.Infinity, "called")
