from as3lib import Error, null, Number, Object, undefined
from as3lib.flash.net import (FileFilter, getClassByAlias, registerClassAlias,
                              SharedObject)
from as3lib.tests import as3libTestCase, TestNotImplemented


class FileFilterTests(as3libTestCase):
    def test_properties(self):
        fileFilter = FileFilter('Images', '*.jpg;*.gif;*.png')
        self.assertEqual(fileFilter.description, 'Images')
        self.assertEqual(fileFilter.extension, '*.jpg;*.gif;*.png')
        self.assertEqual(fileFilter.macType, null)


class FileReferenceTests(as3libTestCase):
    def test_browse_cancel(self):
        raise TestNotImplemented

    def test_browse_select(self):
        raise TestNotImplemented

    def test_load(self):
        raise TestNotImplemented

    def test_save(self):
        raise TestNotImplemented

    def test_save_and_browse(self):
        raise TestNotImplemented

    def test_save_and_load(self):
        raise TestNotImplemented

    def test_uninitialized(self):
        raise TestNotImplemented

    def test_list_browse_cancel(self):
        raise TestNotImplemented

    def test_list_browse_select(self):
        raise TestNotImplemented


class FunctionTests(as3libTestCase):
    def test_getClassByAlias(self):
        raise TestNotImplemented
        try:
            getClassByAlias('toString')
        except Error as e:
            ...  # => ReferenceError: Error #1014: Class toString could not be found.

        try:
            getClassByAlias('MyClass')
        except Error as e:
            ...  # => ReferenceError: Error #1014: Class MyClass could not be found.

        class TestClass:
            ...

        registerClassAlias('MyClass', TestClass)
        self.assertIs(getClassByAlias("MyClass"), TestClass)

    def test_navigateToURL(self):
        raise TestNotImplemented


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
