from as3lib.tests import as3libTestCase, TestNotImplemented
from as3lib.flash.text import TextField, TextFormat


class TextFieldTests(as3libTestCase):
    def test_event(self):
        raise TestNotImplemented

    def test_focusin_event(self):
        raise TestNotImplemented

    def test_input_dead_keys_windows(self):
        raise TestNotImplemented

    def test_input_events(self):
        raise TestNotImplemented

    def test_unload(self):
        raise TestNotImplemented


class TextFormatTests(as3libTestCase):
    def test_1(self):
        raise TestNotImplemented

    def test_display(self):
        raise TestNotImplemented

    def test_font_max_length(self):
        tf = TextFormat('some  very,very,very,very,very,very,very,very,very,very,very,very,very, long font')
        self.assertEqual(tf.font, 'some  very,very,very,very,very,very,very,very,very,very,very,ver')

        # Setter
        tf.font = 'some 2 very,very,very,very,very,very,very,very,very,very,very,very,very, long font'
        self.assertEqual(tf.font, 'some 2 very,very,very,very,very,very,very,very,very,very,very,ve')

        # Setter 2
        tf.font = 'some not too long font'
        self.assertEqual(tf.font, 'some not too long font')

        # HTML TextField
        field = TextField()
        # NOTE: This spits out some errors (Maybe because my system has non-ttf default fonts?)
        field.htmlText = "<font face='some 3 very,very,very,very,very,very,very,very,very,very,very,very,very, long font'>x</font>"
        self.assertEqual(field.getTextFormat(0, 1).font, 'some 3 very,very,very,very,very,very,very,very,very,very,very,very,very, long font')
