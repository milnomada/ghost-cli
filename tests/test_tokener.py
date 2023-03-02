import datetime
import sys
import os
import json
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from slugify import slugify
from ghost_cli import Tokener
from unittest.mock import Mock, MagicMock, patch, PropertyMock


response = Mock()
my_mock = Mock()
my_mock.get = MagicMock(return_value=response)
my_mock.post = MagicMock(return_value=response)


class TestTokener(unittest.TestCase):

    def test_tokener(self):
        t = Tokener(key="a034f3:bcf8a7")
        token = t.generate(expire=10)
        print(token)
        assert token is not None

    def test_tokener_raises(self):
        with self.assertRaises(RuntimeError):
            t = Tokener()
            token = t.generate(expire=10)
            print(token)


    def test_tokener_raises_value_error(self):
        with self.assertRaises(ValueError):
            t = Tokener(key="a034f3-bcf8a7")
            token = t.generate(expire=10)
