# Most of these test cases are based on ones made by the ruffle.rs project
# https://github.com/ruffle-rs/ruffle

import as3lib
from as3lib import Math
from as3lib.tests import as3libTestCase, TestNotImplemented, MethodNotImplemented


class ArrayTests(as3libTestCase):
   # NOTE: prototype is required for some tests
   def assertArray(self, array, check):
      for i, item in enumerate(check):
         self.assertEqual(array[i], item)

   def assertIndices(self, array, check, length=None):
      arr = [i for i in array]
      if length is not None:
         self.assertEqual(len(arr), length)
      for i, item in enumerate(check):
         self.assertEqual(arr[i], item)

   def assertEach(self, array, check, length=None):
      raise MethodNotImplemented('each')
      # TODO: Add a function for this and create a special method that it calls
      arr = [i for i in each(array)]
      if length is not None:
         self.assertEqual(len(arr), length)
      for i, item in enumerate(check):
         self.assertEqual(arr[i], item)

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
      # TODO: This one is broken
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
      self.assertIndices(array, [0, 4], 4)

      self.assertEach(array, ['elem0', 'elem4'], 4)

   def test_enumerationelements(self):
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

   def test_foreach(self):
      a = as3lib.Array(5, 'abc')

      def test(val, index, array):
         self.assertTrue(val in a)
         self.assertLess(index, len(a))
         self.assertIdentical(array, a)

      a.forEach(test)

   def test_hasownproperty(self):
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

   def test_indexmax(self):
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

   def test_indexof(self):
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

   def test_lastindexof(self):
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
      raise TestNotImplemented

   def test_sort_random(self):
      raise TestNotImplemented

   def test_sorton(self):
      raise TestNotImplemented

   def test_sparseops(self):
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
      self.assertIndices(arr, [0, 1, 100, 500], 4)

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
      raise TestNotImplemented

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

   def test_tolocalestring(self):
      # TODO: The answer that ruffle gives looks wrong, check on actual flash player
      a = as3lib.Array(as3lib.String('a'), as3lib.String('b'), as3lib.String('c'))
      b = as3lib.Array(as3lib.Number(1), as3lib.Number(2), as3lib.Number(3))
      c = as3lib.Array(a, b)

      self.assertEqual(a.toLocaleString(), '[object String],[object String],[object String]')
      self.assertEqual(b.toLocaleString(), '1,2,3')
      self.assertEqual(c.toLocaleString(), '[object String],[object String],[object String],1,2,3')

   def test_tostring(self):
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

   def test_valueof(self):
      # TODO: Make sure that valueOf is supposed to return the array
      a = as3lib.Array('a', 'b', 'c')
      self.assertEqual(a.valueOf(), a)

      b = as3lib.Array(1, 2, 3)
      self.assertEqual(b.valueOf(), b)

      c = as3lib.Array(a, b)
      self.assertEqual(c.valueOf(), c)

   def test_nullcallback(self):
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
      self.asserttrue(as3lib.Boolean(as3lib.String('true')))
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

   def test_tostring(self):
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

      self.assertNaNExact(date.fullYear)
      self.assertNaNExact(date.month)
      self.assertNaNExact(date.date)
      self.assertNaNExact(date.day)
      self.assertNaNExact(date.hours)
      self.assertNaNExact(date.minutes)
      self.assertNaNExact(date.seconds)

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

      self.assertNaNExact(date.fullYear)
      self.assertNaNExact(date.month)
      self.assertNaNExact(date.date)
      self.assertNaNExact(date.day)
      self.assertNaNExact(date.hours)
      self.assertNaNExact(date.minutes)
      self.assertNaNExact(date.seconds)

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

   def test_parsefloat(self):
      self.assertNaNExact(as3lib.parseFloat())

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
      self.assertNaNExact(as3lib.parseFloat("e10"))
      self.assertNaNExact(as3lib.parseFloat("10e-"))

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
      self.assertNaNExact(as3lib.parseFloat('Infinitya'))
      self.assertEqual(as3lib.parseFloat('Infinity   a'), as3lib.Infinity)
      self.assertEqual(as3lib.parseFloat(".   Infinity"), as3lib.Infinity)
      self.assertEqual(as3lib.parseFloat("e10   Infinity"), as3lib.Infinity)
      self.assertEqual(as3lib.parseFloat(".e10   Infinity"), as3lib.Infinity)
      self.assertEqual(as3lib.parseFloat("1   Infinity"), as3lib.Number(1))

      # invalid strings
      self.assertNaNExact(as3lib.parseFloat("BADBAD"))
      self.assertNaNExact(as3lib.parseFloat(''))
      self.assertNaNExact(as3lib.parseFloat('-'))
      self.assertEqual(as3lib.parseFloat('0xff'), as3lib.Number(0))
      self.assertNaNExact(as3lib.parseFloat(as3lib.String.fromCharCode(305)))

      # non-string inputs
      ## Booleans
      self.assertNaNExact(as3lib.parseFloat(as3lib.true))
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

   def test_parseint(self):
      self.assertNaNExact(as3lib.parseInt())
      self.assertNaNExact(as3lib.parseInt(as3lib.undefined))
      self.assertEqual(as3lib.parseInt(as3lib.undefined, 32), as3lib.Int(785077))
      self.assertEqual(as3lib.parseInt('undefined', 32), as3lib.Int(33790067563981))
      self.assertNaNExact(as3lib.parseInt(''))
      self.assertEqual(as3lib.parseInt(123), as3lib.Int(123))
      self.assertEqual(as3lib.parseInt(100, 10), as3lib.Int(100))
      self.assertEqual(as3lib.parseInt(100, 0), as3lib.Int(100))
      self.assertNaNExact(as3lib.parseInt(100, 1))
      self.assertEqual(as3lib.parseInt(100, 2), as3lib.Int(4))
      self.assertEqual(as3lib.parseInt(100, 36), as3lib.Int(1296))
      self.assertNaNExact(as3lib.parseInt(100, 37))
      self.assertNaNExact(as3lib.parseInt(100, -1))
      self.assertEqual(as3lib.parseInt(100, as3lib.Object()), as3lib.Int(100))
      self.assertNaNExact(as3lib.parseInt('100', as3lib.true))
      self.assertEqual(as3lib.parseInt('100', as3lib.false), as3lib.Int(100))
      self.assertEqual(as3lib.parseInt('100', as3lib.NaN), as3lib.Int(100))
      self.assertEqual(as3lib.parseInt('100', as3lib.undefined), as3lib.Int(100))
      self.assertEqual(as3lib.parseInt('0x123'), as3lib.Int(291))
      self.assertEqual(as3lib.parseInt('0xabc'), as3lib.Int(2748))
      self.assertEqual(as3lib.parseInt('010'), as3lib.Int(2))
      self.assertEqual(as3lib.parseInt('-0100'), as3lib.Int(-100))
      self.assertEqual(as3lib.parseInt('-0100z'), as3lib.Int(-100))
      self.assertNaNExact(as3lib.parseInt('0x+0X100'))
      n = 123
      self.assertEqual(as3lib.parseInt(n), as3lib.Int(123))
      self.assertEqual(as3lib.parseInt(123, 32), as3lib.Int(1091))
      self.assertNaNExact(as3lib.parseInt('++1'))
      self.assertEqual(as3lib.parseInt('0x100', 36), as3lib.Int(1540944))
      self.assertEqual(as3lib.parseInt(' 0x100', 36), as3lib.Int(1540944))
      self.assertEqual(as3lib.parseInt('0y100', 36), as3lib.Int(1597600))
      self.assertEqual(as3lib.parseInt(' 0y100', 36), as3lib.Int(1597600))
      self.assertEqual(as3lib.parseInt('-0x100', 36), as3lib.Int(-1540944))
      self.assertEqual(as3lib.parseInt(' -0x100', 36), as3lib.Int(-1540944))
      self.assertEqual(as3lib.parseInt('-0y100', 36), as3lib.Int(-1597600))
      self.assertEqual(as3lib.parseInt(' -0y100', 36), as3lib.Int(-1597600))
      self.assertEqual(as3lib.parseInt('-0x100'), as3lib.Int(-256))
      self.assertNaNExact(as3lib.parseInt('0x-100'))
      self.assertNaNExact(as3lib.parseInt(' 0x-100'))
      self.assertNaNExact(as3lib.parseInt('0x -100'))
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
      self.assertNaNExact(as3lib.parseInt('0x  '))
      self.assertNaNExact(as3lib.parseInt('0x'))
      self.assertNaNExact(as3lib.parseInt('0x  ', 16))
      self.assertNaNExact(as3lib.parseInt('0x', 16))
      self.assertEqual(as3lib.parseInt('12aaa'), as3lib.Int(12))
      self.assertEqual(as3lib.parseInt("100000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "000000000000000"), as3lib.Infinity)
      self.assertEqual(as3lib.parseInt("0x1000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "00000000000000000000000000000000000000000000000000000000000000000000" + "000000000000000"), as3lib.Infinity)
      self.assertNaNExact(as3lib.parseInt(as3lib.String.fromCharCode(305)))
      self.assertEqual(as3lib.parseInt(as3lib.String.fromCharCode(0x2000) + "123"), as3lib.Int(123))

   def test_unescape(self):
      raise TestNotImplemented

   def test_trace(self):
      raise TestNotImplemented


class GlobalsTests(as3libTestCase):
   def test_undefined(self):
      # From https://github.com/ruffle-rs/ruffle/tree/master/tests/tests/swfs/from_shumway/avm1/undefined/undefined-swf7
      self.assertEqual(as3lib.undefined.toString(), 'undefined')
      self.assertNaNExact(-as3lib.undefined)  # TODO: Validate this one
      self.assertTrue(not as3lib.undefined)
      self.assertEqual(as3lib.String('s') + as3lib.undefined, 'sundefined')
      self.assertEqual(as3lib.undefined + as3lib.String('s'), 'undefineds')
      self.assertNaNExact(as3lib.Number(0) + as3lib.undefined)
      self.assertNaNExact(as3lib.undefined + as3lib.Number(0))
      self.assertNotEqual(as3lib.String('undefined'), as3lib.undefined)
      self.assertNotEqual(as3lib.undefined, as3lib.String('undefined'))
      '''
      trace("0 == undefined => " + (0 == undefined));
      trace("undefined == 0 => " + (undefined == 0));
      trace("1 == undefined => " + (1 == undefined));
      trace("undefined == 1 => " + (undefined == 1));
      trace("\'undefined\' < undefined => " + ("undefined" < undefined));
      trace("undefined < \'undefined\' => " + (undefined < "undefined"));
      trace("0 < undefined => " + (0 < undefined));
      trace("undefined < 0 => " + (undefined < 0));
      trace("1 < undefined => " + (1 < undefined));
      trace("undefined < 1 => " + (undefined < 1));
      trace("\'undefined\' <= undefined => " + ("undefined" <= undefined));
      trace("undefined <= \'undefined\' => " + (undefined <= "undefined"));
      trace("0 <= undefined => " + (0 <= undefined));
      trace("undefined <= 0 => " + (undefined <= 0));
      trace("1 <= undefined => " + (1 <= undefined));
      trace("undefined <= 1 => " + (undefined <= 1));
      trace("\'undefined\' > undefined => " + ("undefined" > undefined));
      trace("undefined > \'undefined\' => " + (undefined > "undefined"));
      trace("0 > undefined => " + (0 > undefined));
      trace("undefined > 0 => " + (undefined > 0));
      trace("1 > undefined => " + (1 > undefined));
      trace("undefined > 1 => " + (undefined > 1));
      trace("\'undefined\' >= undefined => " + ("undefined" >= undefined));
      trace("undefined >= \'undefined\' => " + (undefined >= "undefined"));
      trace("0 >= undefined => " + (0 >= undefined));
      trace("undefined >= 0 => " + (undefined >= 0));
      trace("1 >= undefined => " + (1 >= undefined));
      trace("undefined >= 1 => " + (undefined >= 1));
      2025-12-30T22:34:35.176280Z  INFO avm_trace: 0 == undefined => false
      2025-12-30T22:34:35.176282Z  INFO avm_trace: undefined == 0 => false
      2025-12-30T22:34:35.176285Z  INFO avm_trace: 1 == undefined => false
      2025-12-30T22:34:35.176287Z  INFO avm_trace: undefined == 1 => false
      2025-12-30T22:34:35.176292Z  INFO avm_trace: 'undefined' < undefined => undefined
      2025-12-30T22:34:35.176295Z  INFO avm_trace: undefined < 'undefined' => undefined
      2025-12-30T22:34:35.176298Z  INFO avm_trace: 0 < undefined => undefined
      2025-12-30T22:34:35.176301Z  INFO avm_trace: undefined < 0 => undefined
      2025-12-30T22:34:35.176303Z  INFO avm_trace: 1 < undefined => undefined
      2025-12-30T22:34:35.176306Z  INFO avm_trace: undefined < 1 => undefined
      2025-12-30T22:34:35.176309Z  INFO avm_trace: 'undefined' <= undefined => true
      2025-12-30T22:34:35.176313Z  INFO avm_trace: undefined <= 'undefined' => true
      2025-12-30T22:34:35.176315Z  INFO avm_trace: 0 <= undefined => true
      2025-12-30T22:34:35.176318Z  INFO avm_trace: undefined <= 0 => true
      2025-12-30T22:34:35.176321Z  INFO avm_trace: 1 <= undefined => true
      2025-12-30T22:34:35.176323Z  INFO avm_trace: undefined <= 1 => true
      2025-12-30T22:34:35.176326Z  INFO avm_trace: 'undefined' > undefined => undefined
      2025-12-30T22:34:35.176329Z  INFO avm_trace: undefined > 'undefined' => undefined
      2025-12-30T22:34:35.176331Z  INFO avm_trace: 0 > undefined => undefined
      2025-12-30T22:34:35.176334Z  INFO avm_trace: undefined > 0 => undefined
      2025-12-30T22:34:35.176337Z  INFO avm_trace: 1 > undefined => undefined
      2025-12-30T22:34:35.176339Z  INFO avm_trace: undefined > 1 => undefined
      2025-12-30T22:34:35.176342Z  INFO avm_trace: 'undefined' >= undefined => true
      2025-12-30T22:34:35.176345Z  INFO avm_trace: undefined >= 'undefined' => true
      2025-12-30T22:34:35.176347Z  INFO avm_trace: 0 >= undefined => true
      2025-12-30T22:34:35.176350Z  INFO avm_trace: undefined >= 0 => true
      2025-12-30T22:34:35.176353Z  INFO avm_trace: 1 >= undefined => true
      2025-12-30T22:34:35.176355Z  INFO avm_trace: undefined >= 1 => true
      '''
   def test_null(self):
      raise TestNotImplemented


class intTests(as3libTestCase):
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
      self.assertEqual(as3lib.Int(as3lib.Object()), 0)

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
      self.assertEqual(as3lib.Int(1.2315e2), 123)
      self.assertEqual(as3lib.Int(as3lib.String('0x7FFFFFFF')), 2147483647)
      self.assertEqual(as3lib.Int(0x7FFFFFFF), 2147483647)
      self.assertEqual(as3lib.Int(as3lib.String('0x80000000')), -2147483648)
      self.assertEqual(as3lib.Int(0x80000000), -2147483648)
      self.assertEqual(as3lib.Int(as3lib.String('0x80000001')), -2147483647)
      self.assertEqual(as3lib.Int(0x80000001), -2147483647)
      self.assertEqual(as3lib.Int(as3lib.String('0x180000001')), -2147483647)
      self.assertEqual(as3lib.Int(0x180000001), -2147483647)
      self.assertEqual(as3lib.Int(as3lib.String('0x100000001')), 1)
      self.assertEqual(as3lib.Int(0x100000001), 1)
      self.assertEqual(as3lib.Int(as3lib.String('-0x7FFFFFFF')), -2147483647)
      self.assertEqual(as3lib.Int(-0x7FFFFFFF), -2147483647)
      self.assertEqual(as3lib.Int(as3lib.String('-0x80000000')), -2147483648)
      self.assertEqual(as3lib.Int(-0x80000000), -2147483648)
      self.assertEqual(as3lib.Int(as3lib.String('-0x80000001')), 2147483647)
      self.assertEqual(as3lib.Int(-0x80000001), 2147483647)
      self.assertEqual(as3lib.Int(as3lib.String('-0x180000001')), 2147483647)
      self.assertEqual(as3lib.Int(-0x180000001), 2147483647)
      self.assertEqual(as3lib.Int(as3lib.String('-0x100000001')), -1)
      self.assertEqual(as3lib.Int(-0x100000001), -1)

   def test_edgecases(self):
      raise TestNotImplemented

   def test_instanceOf(self):
      raise TestNotImplemented

   def test_toexponential(self):
      raise TestNotImplemented

   def test_tofixed(self):
      raise TestNotImplemented

   def test_toprecision(self):
      raise TestNotImplemented

   def test_toString(self):
      raise TestNotImplemented


class MathTests(as3libTestCase):
   def test_constants(self):
      raise TestNotImplemented
      self.assertEqual(Math.E, )
      self.assertEqual(Math.LN10, )
      self.assertEqual(Math.LN2, )
      self.assertEqual(Math.LOG10E, )
      self.assertEqual(Math.LOG2E, )
      self.assertEqual(Math.PI, )
      self.assertEqual(Math.SQRT1_2, )
      self.assertEqual(Math.SQRT2, )
      '''
      var obj = {valueOf: function():Number { return 10.1; }};

      function runTest(name, func, val) {
         trace(name + "(" + val + ") =");
         trace(func(val));
      }

      function test(name, func) {
         runTest(name, func, 0);
         runTest(name, func, 1);
         runTest(name, func, -1);
         runTest(name, func, 1234.5);
         runTest(name, func, -1234.5);
         runTest(name, func, Infinity);
         runTest(name, func, -Infinity);
         runTest(name, func, NaN);
         runTest(name, func, true);
         runTest(name, func, false);
         runTest(name, func, undefined);
         runTest(name, func, null);
         runTest(name, func, "55.5");
         runTest(name, func, obj);
         trace();
      }

      function runTest2(name, func, val1, val2) {
         trace(name + "(" + val1 + ", " + val2 + ") =");
         trace(func(val1, val2));
      }

      function test2(name, func) {
         runTest2(name, func, 0, 0);
         runTest2(name, func, 1, 2);
         runTest2(name, func, 2, -4);
         runTest2(name, func, 4, -2);
         runTest2(name, func, -99, -100);
         runTest2(name, func, Infinity, -Infinity);
         runTest2(name, func, NaN, 100);
         runTest2(name, func, 999, NaN);
         runTest2(name, func, true, false);
         runTest2(name, func, undefined, null);
         runTest2(name, func, "55.5", "-1234");
         runTest2(name, func, obj, obj);
         trace();
      }

      test("Math.abs", Math.abs);
      test("Math.acos", Math.acos);
      test("Math.asin", Math.asin);
      test("Math.atan", Math.atan);
      test2("Math.atan2", Math.atan2);
      test("Math.ceil", Math.ceil);
      test("Math.cos", Math.cos);
      test("Math.exp", Math.exp);
      test("Math.floor", Math.floor);
      test("Math.log", Math.log);
      test2("Math.max", Math.max);
      test2("Math.min", Math.min);
      test2("Math.pow", Math.pow);
      test("Math.round", Math.round);
      test("Math.sin", Math.sin);
      test("Math.sqrt", Math.sqrt);
      test("Math.tan", Math.tan);

      // Test varargs in min/max
      trace("Math.min() =", Math.min());
      trace("Math.min(0) =", Math.min(0));
      trace("Math.min(1, 2, 3) =", Math.min(1, 2, 3));
      trace("Math.min(-1.1, -2.2, -3.3) =", Math.min(-1.1, -2.2, -3.3));
      trace("Math.min(9, NaN, false, true, Infinity, undefined) =", Math.min(9, NaN, false, true, Infinity, undefined));
      trace();

      trace("Math.max() =", Math.max());
      trace("Math.max(0) =", Math.max(0));
      trace("Math.max(1, 2, 3) =", Math.max(1, 2, 3));
      trace("Math.max(-1.1, -2.2, -3.3) =", Math.max(-1.1, -2.2, -3.3));
      trace("Math.max(9, NaN, false, true, Infinity, undefined) =", Math.max(9, NaN, false, true, Infinity, undefined));
      trace();
      '''


class NumberTests(as3libTestCase):
   def test_constructor(self):
      raise TestNotImplemented


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

   def test_tolocalestring(self):
      o = as3lib.Object()
      self.assertEqual(o.toLocaleString(), '[object Object]')

   def test_tostring(self):
      o = as3lib.Object()
      self.assertEqual(o.toString(), '[object Object]')

   def test_valueof(self):
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
      self.assertNaNExact(-as3lib.undefined)
      self.assertEqual(-as3lib.String(''), 0)
      self.assertNaNExact(-as3lib.String('str'))
      self.assertNaNExact(-as3lib.String('true'))
      self.assertNaNExact(-as3lib.String('false'))
      self.assertEqual(-as3lib.Number(0.0), 0)
      self.assertNaNExact(-as3lib.NaN)
      self.assertEqual(--as3lib.Number(0.0), 0)
      self.assertEqual(-as3lib.Infinity, as3lib.NInfinity)
      self.assertEqual(-as3lib.Number(1.0), as3lib.Int(-1))
      self.assertEqual(--as3lib.Number(1.0), as3lib.Int(1))
      self.assertNaNExact(-as3lib.Object())

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


class uintTests(as3libTestCase):
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

      self.assertEqual(as3lib.uint(as3lib.Object()), 0)

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

   def test_toexponential(self):
      raise TestNotImplemented

   def test_tofixed(self):
      raise TestNotImplemented

   def test_toprecision(self):
      raise TestNotImplemented

   def test_tostring(self):
      raise TestNotImplemented


class VectorTests(as3libTestCase):
   def test_nullcallback(self):
      # TODO: Make sure this is correct
      v = as3lib.Vector(int)
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

   def test_notarray(self):
      self.assertEqual(+as3lib.Array(), 0)
      self.assertEqual(not as3lib.Array(), as3lib.false)
      self.assertTrue(as3lib.Array() == (not as3lib.Array()))

      # Booleans
      self.assertFalse(as3lib.true == as3lib.Array())
      self.assertFalse(as3lib.true == (not as3lib.Array()))
      self.asserttrue(as3lib.false == as3lib.Array())
      self.assertTrue(as3lib.false == (not as3lib.Array()))

   def test_stringbools(self):
      self.assertEqual(not not as3lib.String('false'), not not as3lib.String('true'))
      self.assertIs(not not as3lib.String('false'), not not as3lib.String('true'))

   def test_fail(self):
      # Original (![] + [])[+[]] + (![] + [])[+!+[]] + ([![]] + [][[]])[+!+[] + [+[]]] + (![] + [])[!+[] + !+[]];
      self.assertEqual((not as3lib.Array() + as3lib.Array())[+as3lib.Array()] + (not as3lib.Array() + as3lib.Array())[+(not+as3lib.Array())] + (as3lib.Array(not as3lib.Array()) + as3lib.Array()[as3lib.Array()])[+(not+as3lib.Array()) + as3lib.Array(+as3lib.Array)] + (not as3lib.Array() + as3lib.Array())[not+as3lib.Array() + (not+as3lib.Array())], 'fail')

   def test_truthyarry(self):
      self.assertTrue(not not as3lib.Array())
      self.assertFalse(as3lib.Array())

   def test_falsynull(self):
      self.assertFalse(not not as3lib.null)
      self.assertFalse(as3lib.null == as3lib.false)

   def test_addarray(self):
      self.assertEqual(as3lib.Array(1, 2, 3) + as3lib.Array(4, 5, 6), '1,2,34,5,6')

   def test_arrayequality(self):
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
      raise TestNotImplemented

   def test_parseintquirks(self):
      self.assertNaNExact(as3lib.parseInt('f*ck'))
      self.assertEqual(as3lib.parseInt('f*ck', 16), 15)
      self.assertNaNExact(as3lib.parseInt('Infinity', 10))
      self.assertNaNExact(as3lib.parseInt('Infinity', 18))
      self.assertEqual(as3lib.parseInt('Infinity', 19), 18)
      self.assertEqual(as3lib.parseInt('Infinity', 24), 151176378)
      self.assertEqual(as3lib.parseInt('Infinity', 29), 385849803)
      self.assertEqual(as3lib.parseInt('Infinity', 30), 13693557269)
      self.assertEqual(as3lib.parseInt('Infinity', 34), 28872273981)
      self.assertEqual(as3lib.parseInt('Infinity', 35), 1201203301724)
      self.assertNaNExact(as3lib.parseInt('Infinity', 37))
      self.assertEqual(as3lib.parseInt(as3lib.null, 24), 23)
      self.assertEqual(as3lib.parseInt('06'), 6)
      # parseInt("08"); // 8 if support ECMAScript 5
      # parseInt("08"); // 0 if not support ECMAScript 5
      self.assertEqual(as3lib.parseInt(0.000001), 0)
      self.assertEqual(as3lib.parseInt(0.0000001), 1)
      self.assertEqual(as3lib.parseInt(1 / 1999999), 5)

   def test_funnymath(self):
      raise TestNotImplemented
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

   def test_yieldself(self):
      # The syntax here is a little bit different but it still works
      def f():
         yield f

      self.assertIs(next(next(next(next(next(f())())())())()), f)

   def test_minmax(self):
      self.assertIs(Math.min(), as3lib.Infinity)
      self.assertIs(Math.max(), as3lib.NInfinity)
      self.assertLess(Math.max(), Math.min())

   def test_infinitetimeout(self):
      raise TestNotImplemented
      # setTimeout(() => console.log("called"), Infinity)
      # This will execute immediately because Infinity does not fit into a
      # 32bit uint
