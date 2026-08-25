from as3lib import Number, Object, undefined
from as3lib.flash.net import SharedObject
from as3lib.tests import as3libTestCase, TestNotImplemented


class SharedObjectTests(as3libTestCase):
    # NOTE: SharedObject serialisation order will differ between flash player,
    #       ruffle, and as3lib.
    def test_1(self):
        raise TestNotImplemented

    def test_no_root(self):
        so = SharedObject.getLocal('testObject')
        self.assertTrue(isinstance(so.data, Object))
        self.assertIs(so.data.A, undefined)
        so.data.A = Number(1)
        self.assertEqual(so.data.A, 1)
