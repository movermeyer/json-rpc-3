""" Test utility functionality."""
from datetime import datetime
import json
import unittest

from jsonrpc.utils import json_datetime_hook, FixedOffset, json_datetime_default
from jsonrpc.base import JSONSerializable

class TestJSONSerializable(unittest.TestCase):
    """ Test JSONSerializable functionality."""

    def setUp(self):
        self._class = JSONSerializable

    def test_definse_serialize_deserialize(self):
        """ Test classmethods of inherited class."""
        self.assertEqual(self._class().serialize({}), "{}")
        self.assertEqual(self._class().deserialize("{}"), {})


class TestDatetimeEncoderDecoder(unittest.TestCase):
    """ Test DatetimeEncoder and json_datetime_hook functionality."""

    def test_datetime(self):
        obj = datetime.now()

        with self.assertRaises(TypeError):
            json.dumps(obj)

        string = json.dumps(obj, default=json_datetime_default)

        self.assertEqual(obj, json.loads(string, object_hook=json_datetime_hook))

    def test_complex(self):
        obj = {'id': '1', 'params': (datetime(2014, 6, 17, 9, 38, 39, 911853),), 'jsonrpc': 2.0, 'method': 'w'}
        json.dumps(obj, default=json_datetime_default)

    def test_skip_nondt_obj(self):
        obj = {'__weird__': True}
        string = json.dumps(obj, default=json_datetime_default)
        self.assertEqual(obj, json.loads(string, object_hook=json_datetime_hook))

    def test_datetime_tzinfo(self):
        obj = datetime.now().replace(tzinfo=FixedOffset(3600))

        with self.assertRaises(TypeError):
            json.dumps(obj)

        string = json.dumps(obj, default=json_datetime_default)

        self.assertEqual(obj, json.loads(string, object_hook=json_datetime_hook))
