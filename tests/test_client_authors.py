import datetime
import sys
import os
import json
import unittest
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from slugify import slugify
from ghost_cli import GhostCli
from ghost_cli.client import HttpCli
from ghost_cli.models import Author
from unittest.mock import Mock, MagicMock, patch, PropertyMock


response = Mock()
my_mock = Mock()
my_mock.get = MagicMock(return_value=response)
my_mock.post = MagicMock(return_value=response)


class TestClientAuthors():

    def test_author_model(self, mocker):
        author_name = "John Foo"
        author_slug = slugify(author_name)
        
        my_author = {
            "name": author_name,
            "slug": author_slug,
            "my_foo_attr": ""
        }
        a = Author(**my_author)
        assert a.name == author_name
        assert a.slug == author_slug
        with pytest.raises(AttributeError):
            print(a.my_foo_attr, flush=False)

    def test_create_author(self, mocker):
        author_name = "John Foo"
        author_slug = slugify(author_name)
        my_author = {
            "name": author_name,
            "slug": author_slug
        }
        response.status_code = 201
        mocker.patch('ghost_cli.client.HttpCli.post', return_value=response)
        cli = GhostCli("http://localhost", "")
        res = cli.create_author(**my_author)
        assert res == True

    def test_create_author_failed(self, mocker):
        author_name = "John Foo"
        author_slug = slugify(author_name)
        my_author = {
            "name": author_name,
            "slug": author_slug
        }
        response.status_code = 400
        mocker.patch('requests.post', side_effect=Exception("my exception"))
        mocker.patch('ghost_cli.client.HttpCli.post', return_value=response)

        cli = GhostCli("http://localhost", "")
        res = cli.create_author(**my_author)
        assert res == False