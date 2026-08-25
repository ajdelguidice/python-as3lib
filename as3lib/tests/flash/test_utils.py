from as3lib import (ArgumentError, Array, delete, each, false, Infinity, NaN,
                    null, Number, Object, true, String, TypeError, undefined)
from as3lib.flash.errors import EOFError, IOError
from as3lib.flash.events import TimerEvent
from as3lib.flash.geom import Point
from as3lib.flash.utils import ByteArray, Dictionary, Timer
from as3lib.tests import as3libTestCase, TestNotImplemented
from time import sleep


class ByteArrayTests(as3libTestCase):
    def setUp(self):
        self.defEncode = ByteArray.defaultObjectEncoding

    def tearDown(self):
        ByteArray.defaultObjectEncoding = self.defEncode

    def assertAtStart(self, ba):
        self.assertEqual(ba.position, 0)

    def assertAtEnd(self, ba):
        self.assertEqual(ba.position, ba.length)

    def test_compress(self):
        # TODO: Add tests for compressed bytes
        def createByteArray():
            result = ByteArray()
            for i in range(100):
                result.writeByte(i)
            return result

        def readByteArray(ba):
            ba.position = 0
            return [ba.readUnsignedByte() for i in range(ba.length)]

        ba = createByteArray()

        ba.compress()
        self.assertAtEnd(ba)

        ba.uncompress()
        self.assertAtStart(ba)
        asrt = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65,
                66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81,
                82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97,
                98, 99)
        self.assertArray(readByteArray(ba), asrt)

        # ba.compress("lzma")
        # print("compressed (lzma)", ba, false)

        # ba.uncompress("lzma")
        # print("uncompressed (lzma)", ba, true)

        ba.compress("deflate")
        self.assertAtEnd(ba)

        ba.uncompress("deflate")
        self.assertAtStart(ba)
        self.assertArray(readByteArray(ba), asrt)

        ba.deflate()
        self.assertAtEnd(ba)

        ba.inflate()
        self.assertAtStart(ba)
        self.assertArray(readByteArray(ba), asrt)

        ba.compress("zlib")
        self.assertAtEnd(ba)

        ba.uncompress("zlib")
        self.assertAtStart(ba)
        self.assertArray(readByteArray(ba), asrt)

        # Check zlib header
        ba = createByteArray()
        ba.compress("zlib")
        ba.position = 0
        self.assertEqual
        self.assertEqual(ba.readUnsignedByte(), 120)
        self.assertEqual(ba.readUnsignedByte(), 218)

    def test_errors(self):
        ba = ByteArray()
        self.assertRaisesAS3(TypeError, 2007, None, ba.compress, null)
        self.assertRaisesAS3(IOError, 2058, None, ba.compress, 'abcdef')

        self.assertRaisesAS3(TypeError, 2007, None, ba.uncompress, null)
        self.assertRaisesAS3(IOError, 2058, None, ba.uncompress, 'abcdef')
        ba.uncompress('zlib')  # Doesn't raise an error

        def setEndian(barr, endian):
            barr.endian = endian

        self.assertRaisesAS3(TypeError, 2007, None, setEndian, ba, null)
        self.assertRaisesAS3(ArgumentError, 2008, None, setEndian, ba, 'abcdef')

        self.assertRaisesAS3(TypeError, 2007, None, ba.writeUTF, null)
        self.assertRaisesAS3(TypeError, 2007, None, ba.writeUTFBytes, null)
        self.assertRaisesAS3(TypeError, 2007, None, ba.writeUTF, null)
        self.assertRaisesAS3(TypeError, 2007, None, ba.writeUTF, null)

        ba.writeMultiByte('abcd', 'utf-8')
        ba.writeMultiByte('abcd', 'aisjdasd')
        self.assertRaisesAS3(TypeError, 2007, None, ba.writeMultiByte, null, 'utf-8')
        self.assertRaisesAS3(TypeError, 2007, None, ba.writeMultiByte, null, 'aisjdasd')
        self.assertRaisesAS3(TypeError, 2007, None, ba.writeMultiByte, null, null)

        ba.readMultiByte(0, '')
        self.assertRaisesAS3(EOFError, 2030, None, ba.readMultiByte, 20, '')
        self.assertRaisesAS3(TypeError, 2007, None, ba.readMultiByte, 0, null)
        self.assertRaisesAS3(TypeError, 2007, None, ba.readMultiByte, 20, null)
        ba.readMultiByte(0, 'aisjdasd')
        self.assertRaisesAS3(EOFError, 2030, None, ba.readMultiByte, 20, 'aisjdasd')
        ba.readMultiByte(0, 'utf-8')
        self.assertRaisesAS3(EOFError, 2030, None, ba.readMultiByte, 20, 'utf-8')

    def test_method_serialization(self):
        p = Point(4.5, 5.5)
        b = ByteArray()
        b.writeObject(p)
        self.assertEqual(b.length, 25)

    def test_oom(self):
        # This is not supposed to fail
        b = ByteArray()
        b.length = 0xFFFFFFFF

    def test_readobject_amf0(self):
        raise TestNotImplemented

    def test_readobject_amf3(self):
        raise TestNotImplemented

    def test_readUTFBytes_bom(self):
        ba = ByteArray()
        ba.writeByte(0xEF)
        ba.writeByte(0xBB)
        ba.writeByte(0xBF)
        ba.writeUTFBytes('Text')
        ba.position = 0
        text = ba.readUTFBytes(ba.length)
        self.assertEqual(text, 'Text')
        self.assertEqual(len(text), 4)

    def test_readUTFBytes_null_bom(self):
        ba = ByteArray()
        ba.writeByte(0xEF)
        ba.writeByte(0xBB)
        ba.writeByte(0xBF)
        ba.writeUTFBytes('Text')
        ba.writeByte(0)
        ba.position = 0
        text = ba.readUTFBytes(ba.length)
        self.assertEqual(text, 'Text')
        self.assertEqual(len(text), 4)

    def test_readUTF_bom(self):
        ba = ByteArray()
        ba.writeShort(3 + 4)  # length of BOM + text
        ba.writeByte(0xEF)
        ba.writeByte(0xBB)
        ba.writeByte(0xBF)
        ba.writeUTFBytes('Text')
        ba.position = 0
        text = ba.readUTF()
        self.assertEqual(text, 'Text')
        self.assertEqual(len(text), 4)

    def test_readUTF_null_bom(self):
        ba = ByteArray()
        ba.writeShort(3 + 4)  # length of BOM + text
        ba.writeByte(0xEF)
        ba.writeByte(0xBB)
        ba.writeByte(0xBF)
        ba.writeUTFBytes('Text')
        ba.writeByte(0)
        ba.position = 0
        text = ba.readUTF()
        self.assertEqual(text, 'Text')
        self.assertEqual(len(text), 4)

    def test_serialization(self):
        raise TestNotImplemented

    def test_string_null(self):
        raise TestNotImplemented

    def test_toString(self):
        ba = ByteArray()
        ba.writeUTFBytes(String('\uFEFFabc'))

        self.assertEqual(ba.toString(), 'abc')
        self.assertEqual(ba.toString().length, 3)
        self.assertEqual(ba.position, 6)

        ba.position = 0
        self.assertEqual(ba.position, 0)
        self.assertEqual(ba.toString(), 'abc')
        self.assertEqual(ba.toString().length, 3)
        self.assertEqual(ba.position, 0)

        # Verify BOM was written.
        self.assertEqual(ba.readUnsignedByte().toString(16), 'ef')
        self.assertEqual(ba.readUnsignedByte().toString(16), 'bb')
        self.assertEqual(ba.readUnsignedByte().toString(16), 'bf')

        ba2 = ByteArray()
        ba2.writeUTFBytes(String("hello"))
        ba2.writeByte(0x00)
        ba2.writeUTFBytes(String("world"))

        # Flash's trace seems to strip \u0000, but the length is correct.
        # trace("ba2.toString():", ba2.toString());
        self.assertEqual(ba2.toString().length, 11)
        self.assertEqual(ba2.position, 11)

        ba2.position = 0
        self.assertEqual(ba2.position, 0)
        # trace("ba2.toString():", ba2.toString());
        self.assertEqual(ba2.toString().length, 11)
        self.assertEqual(ba2.position, 0)

    def test_utf16(self):
        raise TestNotImplemented

    def test_writeObject(self):
        def assert_readObject(value):
            ba = ByteArray()
            ba.writeObject(value)
            ba.position = 0
            self.assertEqual(ba.readObject(), value)

        TESTS = Array(
            undefined,
            null,
            false,
            true,
            Number(4),
            Number(4.5),
            Infinity,
            -Infinity,
            NaN,
            String("test")
        )

        def runTests():
            for var in each(TESTS):
                assert_readObject(var)

            assert_readObject(TESTS)

        # AMF3 TESTS
        ByteArray.defaultObjectEncoding = 3
        runTests()

        # AMF0 TESTS
        ByteArray.defaultObjectEncoding = 0
        runTests()


class DictionaryTests(as3libTestCase):
    def assertKeyAmount(self, d, amount):
        count = 0
        for i in each(d):
            count += 1

        self.assertEqual(count, amount)

    def assertIterSorted(self, obj, values, length=None):
        self.assertArray([i for i in obj].sort(), values, length)

    def assertEachSorted(self, obj, values, length=None):
        self.assertArray([i for i in each(obj)].sort(), values, length)

    def test_access(self):
        a = Dictionary()
        a['key'] = 5
        self.assertEqual(a['key'], 5)

        a['key'] = 6

        class Test:
            ...

        key2 = Test()
        a[key2] = 23

        key3 = Test()
        a[key3] = 'Key3 True Value'

        a['key3'] = 'Key3 False Value'

        class testobj:
            def toString(*args):
                return 'key4'
        key4 = testobj()

        a[key4] = 'Key4 True Value'

        a['key4'] = 'Key4 False Value'

        a[13] = "i've been found!"
        a['13'] = "no I haven't"

        a[1.123] = 'this violates Rust!'
        a['1.123'] = 'this is perfectly acceptable'

        a[undefined] = 'oh no'
        a['undefined'] = 'uh huh...'

        a[null] = 'oh YES!'
        a['null'] = 'yeah sure'

        a[true] = 'true'
        a['true'] = 'stringy true'

        a[false] = 'false'
        a['false'] = 'stringy false'

        self.assertEqual(a['key'], 6)
        self.assertEqual(a[key2], 23)
        self.assertEqual(a[key3], 'Key3 True Value')
        self.assertEqual(a['key3'], 'Key3 False Value')
        self.assertEqual(a[key4], 'Key4 True Value')
        self.assertEqual(a['key4'], 'Key4 False Value')
        self.assertEqual(a[13], "no I haven't")
        self.assertEqual(a[1.123], 'this is perfectly acceptable')
        self.assertEqual(a['1.123'], 'this is perfectly acceptable')
        self.assertEqual(a[undefined], 'uh huh...')
        self.assertEqual(a['undefined'], 'uh huh...')
        self.assertEqual(a[null], 'yeah sure')
        self.assertEqual(a['null'], 'yeah sure')
        self.assertEqual(a[true], 'stringy true')
        self.assertEqual(a['true'], 'stringy true')
        self.assertEqual(a[false], 'stringy false')
        self.assertEqual(a['false'], 'stringy false')

        a[a] = a

        # TODO: Make sure this is correct
        self.assertEqual(a[a], a)

    def test_delete(self):
        a = Dictionary()
        a['key'] = 5
        self.assertEqual(a['key'], 5)

        a['key'] = 6

        class Test:
            ...

        key2 = Test()
        a[key2] = 23

        key3 = Test()
        a[key3] = 'Key3 True Value'
        a['key3'] = 'Key3 False Value'

        key4 = Object()
        key4.toString = lambda: 'key4'
        a[key4] = 'Key4 True Value'
        a['key4'] = 'Key4 False Value'

        a[13] = "i've been found!"
        a['13'] = "no I haven't"

        a[1.123] = 'this violates Rust!'
        a['1.123'] = 'this is perfectly acceptable'

        a[undefined] = 'oh no'
        a['undefined'] = 'uh huh...'

        a[null] = 'oh YES!'
        a['null'] = 'yeah sure'

        a[true] = 'true'
        a['true'] = 'stringy true'

        a[false] = 'false'

        self.assertTrue(delete(a['key']))
        self.assertEqual(a['key'], undefined)

        self.assertTrue(delete(a[key2]))
        self.assertEqual(a[key2], undefined)

        self.assertTrue(delete(a[key3]))
        self.assertEqual(a[key3], undefined)
        self.assertEqual(a['key3'], 'Key3 False Value')

        self.assertTrue(delete(a['key3']))
        self.assertEqual(a[key3], undefined)
        self.assertEqual(a['key3'], undefined)

        self.assertTrue(delete(a[key4]))
        self.assertEqual(a[key4], undefined)
        self.assertEqual(a['key4'], 'Key4 False Value')

        self.assertTrue(delete(a['key4']))
        self.assertEqual(a[key4], undefined)
        self.assertEqual(a['key4'], undefined)

        self.assertTrue(delete(a[13]))
        self.assertEqual(a[13], undefined)

        self.assertTrue(delete(a[1.123]))
        self.assertEqual(a[1.123], undefined)
        self.assertEqual(a['1.123'], undefined)

        self.assertTrue(delete(a[undefined]))
        self.assertEqual(a[undefined], undefined)
        self.assertEqual(a['undefined'], undefined)

        self.assertTrue(delete(a[null]))
        self.assertEqual(a[null], undefined)
        self.assertEqual(a['null'], undefined)

        self.assertTrue(delete(a[true]))
        self.assertEqual(a[true], undefined)
        self.assertEqual(a[true], undefined)

        self.assertTrue(delete(a[false]))
        self.assertEqual(a[false], undefined)
        self.assertEqual(a[false], undefined)

        a[a] = a
        self.assertEqual(a[a], a)

        self.assertTrue(delete(a[a]))
        self.assertEqual(a[a], undefined)

        key5 = Object()
        key5.toString = lambda: 'key5'

        self.assertTrue(delete(a[key5]))

    def test_forEach(self):
        a = Dictionary()

        a[String('foo')] = 'The value'
        self.assertEqual(a[String('foo')], 'The value')

        firstKey = Object()
        a[firstKey] = 'Testing'
        a[1234567] = true
        a.setPropertyIsEnumerable(1234567, false)
        self.assertTrue(a.propertyIsEnumerable(1234567))
        self.assertFalse(a.propertyIsEnumerable(Object()))

        a.setPropertyIsEnumerable(firstKey, false)
        self.assertIterSorted(a, ['1234567', firstKey, 'foo'], 3)

        a['key'] = 5
        self.assertEqual(a['key'], 5)

        a['key'] = 6

        class Test:
            ...

        key2 = Test()
        a[key2] = 23

        key3 = Test()
        a[key3] = 'Key3 True Value'

        a['key3'] = 'Key3 False Value'

        class testobj:
            def toString(*args):
                return 'key4'
        key4 = testobj()

        a[key4] = 'Key4 True Value'

        a['key4'] = 'Key4 False Value'

        a[13] = "i've been found!"
        a['13'] = "no I haven't"

        a[1.123] = 'this violates Rust!'
        a['1.123'] = 'this is perfectly acceptable'

        a[undefined] = 'oh no'
        a['undefined'] = 'uh huh...'

        a[null] = 'oh YES!'
        a['null'] = 'yeah sure'

        a[true] = 'true'
        a['true'] = 'stringy true'

        a[false] = 'false'
        a['false'] = 'stringy false'

        a[a] = a

        asrt1 = ('1.123', '1234567', '13', a, firstKey, key2, key3, 'false',
                 'foo', 'key', 'key3', key4, 'key4', 'null', 'true',
                 'undefined')
        asrt2 = ('23', '6', 'Key3 False Value', 'Key3 True Value',
                 'Key4 False Value', 'Key4 True Value', 'Testing',
                 'The value', a, "no I haven't", 'stringy false',
                 'stringy true', 'this is perfectly acceptable', true,
                 'uh huh...', 'yeah sure')

        self.assertIterSorted(a, asrt1)
        self.assertEachSorted(a, asrt2)

        a.setPropertyIsEnumerable(key2, false)
        a.setPropertyIsEnumerable(key3, false)
        a.setPropertyIsEnumerable(key4, false)

        self.assertIterSorted(a, asrt1)
        self.assertEachSorted(a, asrt2)

    def test_hasOwnProperty(self):
        a = Dictionary()
        a['key'] = 5
        self.assertEqual(a['key'], 5)

        a['key'] = 6

        class Test:
            ...

        key2 = Test()
        a[key2] = 23

        key3 = Test()
        a[key3] = 'Key3 True Value'
        a['key3'] = 'Key3 False Value'

        key4 = Object()
        key4.toString = lambda: 'key4'
        a[key4] = 'Key4 True Value'
        a['key4'] = 'Key4 False Value'

        a[13] = "i've been found!"
        a['13'] = "no I haven't"

        a[1.123] = 'this violates Rust!'
        a['1.123'] = 'this is perfectly acceptable'

        a[undefined] = 'oh no'
        a['undefined'] = 'uh huh...'

        a[null] = 'oh YES!'
        a['null'] = 'yeah sure'

        a[true] = 'true'
        a['true'] = 'stringy true'

        a[false] = 'false'

        self.assertTrue(a.hasOwnProperty("key"))
        self.assertFalse(a.hasOwnProperty(key2))
        self.assertFalse(a.hasOwnProperty(key3))
        self.assertTrue(a.hasOwnProperty("key3"))
        self.assertTrue(a.hasOwnProperty(key4))
        self.assertTrue(a.hasOwnProperty("key4"))
        self.assertTrue(a.hasOwnProperty(13))
        self.assertTrue(a.hasOwnProperty(1.123))
        self.assertTrue(a.hasOwnProperty("1.123"))
        self.assertTrue(a.hasOwnProperty(undefined))
        self.assertTrue(a.hasOwnProperty("undefined"))
        self.assertTrue(a.hasOwnProperty(null))
        self.assertTrue(a.hasOwnProperty("null"))
        self.assertTrue(a.hasOwnProperty(true))
        self.assertTrue(a.hasOwnProperty("true"))
        self.assertTrue(a.hasOwnProperty(false))
        self.assertTrue(a.hasOwnProperty("false"))
        self.assertFalse(a.hasOwnProperty(Test()))
        a[a] = a
        self.assertTrue(a.hasOwnProperty(a))

    def test_in(self):
        a = Dictionary()
        a['key'] = 5
        a['key'] = 6

        class Test:
            ...

        key2 = Test()
        a[key2] = 23

        key3 = Test()
        a[key3] = 'Key3 True Value'

        a['key3'] = 'Key3 False Value'

        class testobj:
            def toString(*args):
                return 'key4'
        key4 = testobj()

        a[key4] = 'Key4 True Value'

        a['key4'] = 'Key4 False Value'

        a[13] = "i've been found!"
        a['13'] = "no I haven't"

        a[1.123] = 'this violates Rust!'
        a['1.123'] = 'this is perfectly acceptable'

        a[undefined] = 'oh no'
        a['undefined'] = 'uh huh...'

        a[null] = 'oh YES!'
        a['null'] = 'yeah sure'

        a[true] = 'true'
        a['true'] = 'stringy true'

        a[false] = 'false'
        a['false'] = 'stringy false'

        self.assertTrue('key' in a)
        self.assertTrue(key2 in a)
        self.assertTrue(key3 in a)
        self.assertTrue('key3' in a)
        self.assertTrue(key4 in a)
        self.assertTrue('key4' in a)
        self.assertTrue(13 in a)
        self.assertTrue(1.123 in a)
        self.assertTrue('1.123' in a)
        self.assertTrue(undefined in a)
        self.assertTrue('undefined' in a)
        self.assertTrue(null in a)
        self.assertTrue('null' in a)
        self.assertTrue(true in a)
        self.assertTrue('true' in a)
        self.assertTrue(false in a)
        self.assertTrue('false' in a)

        a[a] = a
        self.assertTrue(a in a)

    def test_iter_modify(self):
        # NOTE: Should work fine once Object works properly
        def runTest(obj, check_during, check_after):
            for i in range(100):
                obj[f'Key {i}'] = i

            toDelete = []
            seen = []
            for key in obj:
                seen.append(f"Key: '{key}' Value: {obj[key]}")

                if (len(seen) < 94):
                    toDelete.append(key)

                if (len(seen) == 95):
                    for j in range(len(toDelete)):
                        newKey = toDelete[j]
                        if (j % 2 == 0):
                            delete(obj[newKey])
                        else:
                            obj.setPropertyIsEnumerable(newKey, false)

            seen.sort()
            self.assertEqual(seen, check_during)

            seenAfter = []
            for newKey in obj:
                seenAfter.append(f"Key: '{newKey}' Value: {obj[newKey]}")

            seenAfter.sort()
            self.assertEqual(len(seenAfter), check_after)

        check = ["Key: 'Key 0' Value: 0", "Key: 'Key 1' Value: 1", "Key: 'Key 10' Value: 10", "Key: 'Key 11' Value: 11", "Key: 'Key 12' Value: 12", "Key: 'Key 13' Value: 13", "Key: 'Key 14' Value: 14", "Key: 'Key 15' Value: 15", "Key: 'Key 16' Value: 16", "Key: 'Key 17' Value: 17", "Key: 'Key 18' Value: 18", "Key: 'Key 19' Value: 19", "Key: 'Key 2' Value: 2", "Key: 'Key 20' Value: 20", "Key: 'Key 21' Value: 21", "Key: 'Key 22' Value: 22", "Key: 'Key 23' Value: 23", "Key: 'Key 24' Value: 24", "Key: 'Key 25' Value: 25", "Key: 'Key 26' Value: 26", "Key: 'Key 27' Value: 27", "Key: 'Key 28' Value: 28", "Key: 'Key 29' Value: 29", "Key: 'Key 3' Value: 3", "Key: 'Key 30' Value: 30", "Key: 'Key 31' Value: 31", "Key: 'Key 32' Value: 32", "Key: 'Key 33' Value: 33", "Key: 'Key 34' Value: 34", "Key: 'Key 35' Value: 35", "Key: 'Key 36' Value: 36", "Key: 'Key 37' Value: 37", "Key: 'Key 38' Value: 38", "Key: 'Key 39' Value: 39", "Key: 'Key 4' Value: 4", "Key: 'Key 40' Value: 40", "Key: 'Key 41' Value: 41", "Key: 'Key 42' Value: 42", "Key: 'Key 43' Value: 43", "Key: 'Key 44' Value: 44", "Key: 'Key 45' Value: 45", "Key: 'Key 46' Value: 46", "Key: 'Key 47' Value: 47", "Key: 'Key 48' Value: 48", "Key: 'Key 49' Value: 49", "Key: 'Key 5' Value: 5", "Key: 'Key 50' Value: 50", "Key: 'Key 51' Value: 51", "Key: 'Key 52' Value: 52", "Key: 'Key 53' Value: 53", "Key: 'Key 54' Value: 54", "Key: 'Key 55' Value: 55", "Key: 'Key 56' Value: 56", "Key: 'Key 57' Value: 57", "Key: 'Key 58' Value: 58", "Key: 'Key 59' Value: 59", "Key: 'Key 6' Value: 6", "Key: 'Key 60' Value: 60", "Key: 'Key 61' Value: 61", "Key: 'Key 62' Value: 62", "Key: 'Key 63' Value: 63", "Key: 'Key 64' Value: 64", "Key: 'Key 65' Value: 65", "Key: 'Key 66' Value: 66", "Key: 'Key 67' Value: 67", "Key: 'Key 68' Value: 68", "Key: 'Key 69' Value: 69", "Key: 'Key 7' Value: 7", "Key: 'Key 70' Value: 70", "Key: 'Key 71' Value: 71", "Key: 'Key 72' Value: 72", "Key: 'Key 73' Value: 73", "Key: 'Key 74' Value: 74", "Key: 'Key 75' Value: 75", "Key: 'Key 76' Value: 76", "Key: 'Key 77' Value: 77", "Key: 'Key 78' Value: 78", "Key: 'Key 79' Value: 79", "Key: 'Key 8' Value: 8", "Key: 'Key 80' Value: 80", "Key: 'Key 81' Value: 81", "Key: 'Key 82' Value: 82", "Key: 'Key 83' Value: 83", "Key: 'Key 84' Value: 84", "Key: 'Key 85' Value: 85", "Key: 'Key 86' Value: 86", "Key: 'Key 87' Value: 87", "Key: 'Key 88' Value: 88", "Key: 'Key 89' Value: 89", "Key: 'Key 9' Value: 9", "Key: 'Key 90' Value: 90", "Key: 'Key 91' Value: 91", "Key: 'Key 92' Value: 92", "Key: 'Key 93' Value: 93", "Key: 'Key 94' Value: 94", "Key: 'Key 95' Value: 95", "Key: 'Key 96' Value: 96", "Key: 'Key 97' Value: 97", "Key: 'Key 98' Value: 98", "Key: 'Key 99' Value: 99"]

        array = Array()
        array.push("First normal entry")
        array.push("Second normal entry")
        # runTest(array)

        d = Dictionary()
        # d[Object()] = "First distinct object key"
        # d[Object()] = "Second distinct object key"
        runTest(d, check, 53)

        runTest(Object(), check, 53)

    def test_namespace(self):
        raise TestNotImplemented

    def test_primativeKeys(self):
        raise TestNotImplemented

    def test_weakKeys(self):
        d = Dictionary(true)

        obj1 = Object()
        obj2 = Object()
        obj3 = Object()
        obj4 = Object()
        obj5 = Object()
        d[obj1] = 0
        d[obj2] = 1
        d[obj3] = 2
        d[obj4] = 3
        d[obj5] = 4

        d = d
        self.assertKeyAmount(d, 5)

        obj1 = null
        obj3 = null
        obj5 = null
        self.assertKeyAmount(d, 2)


class TimerTests(as3libTestCase):
    # TODO: Find a way to properly test Timer because it is async
    def test_1(self):
        raise TestNotImplemented

    def test_events(self):
        self.eventOrder = ''

        def timer(e):
            self.eventOrder += 'T'
            self.assertEvent(e, TimerEvent, 'timer', false, false)
            self.assertEqual(e.eventPhase, 2)

        def timerComplete(e):
            self.eventOrder += 'C'
            self.assertEvent(e, TimerEvent, 'timerComplete', false, false)
            self.assertEqual(e.eventPhase, 2)

        t = Timer(100, 2)
        t.addEventListener('timer', timer)
        t.addEventListener('timerComplete', timerComplete)
        t.start()

        sleep(0.3)  # Wait for timer to finish

        self.assertEqual(self.eventOrder, 'TTC')

        del self.eventOrder

    def test_finish(self):
        raise TestNotImplemented

    def test_reset(self):
        raise TestNotImplemented

    def test_setdelay(self):
        raise TestNotImplemented
