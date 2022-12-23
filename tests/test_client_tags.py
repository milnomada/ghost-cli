import datetime
import sys
import os
import json
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from slugify import slugify
from ghost_cli import GhostCli
from ghost_cli.client import HttpCli
from unittest.mock import Mock, MagicMock, patch, PropertyMock


response = Mock()
my_mock = Mock()
my_mock.get = MagicMock(return_value=response)
my_mock.post = MagicMock(return_value=response)


class TestClientTags():

    def test_get_tag(self, mocker):
        tag_name = "Last news"
        tag_slug = slugify(tag_name)
        my_tags = {'tags': [{
            "name": tag_name,
            "slug": tag_slug
        }]}
        response.json = MagicMock(return_value=my_tags)
        mocker.patch('ghost_cli.client.HttpCli.get', return_value=response)

        cli = GhostCli("http://localhost", "")
        tag, _ = cli.get_tag('slug', tag_slug)
        assert tag.name == tag_name
        assert tag.slug == tag_slug

    def test_get_tag_by_name(self, mocker):
        tag_name = "Last news"
        tag_slug = slugify(tag_name)
        my_tags = {'tags': [{
            "name": tag_name,
            "slug": tag_slug
        }]}
        response.json = MagicMock(return_value=my_tags)
        mocker.patch('ghost_cli.client.HttpCli.get', return_value=response)

        cli = GhostCli("http://localhost", "")
        tag, _ = cli.get_tag_by_name(tag_name)
        assert tag.name == tag_name
        assert tag.slug == tag_slug

    def test_get_posts(self, mocker):
        tag_name = "Last news"
        tag_slug = slugify(tag_name)
        my_tags = {'tags': [{
            "name": tag_name,
            "slug": tag_slug
        }]}
        response.json = MagicMock(return_value=my_tags)
        mocker.patch('ghost_cli.client.HttpCli.get', return_value=response)

        cli = GhostCli("http://localhost", "")
        tags, _ = cli.get_tags()
        tag = tags[0]
        assert len(tags) == 1
        assert tag.name == tag_name
        assert tag.slug == tag_slug

    def test_create_tag(self, mocker):
        tag_name = "Last news"
        tag_slug = slugify(tag_name)
        my_tag = {
            "name": tag_name,
            "slug": tag_slug
        }
        response.status_code = 201
        mocker.patch('ghost_cli.client.HttpCli.post', return_value=response)
        cli = GhostCli("http://localhost", "")
        status, _ = cli.create_tag(**my_tag)
        assert status == True

    def test_create_tag_failed(self, mocker):
        tag_name = "Last news"
        tag_slug = slugify(tag_name)
        my_tag = {
            "name": tag_name,
            "slug": tag_slug
        }
        response.status_code = 400
        mocker.patch('requests.post', side_effect=Exception("my exception"))
        mocker.patch('ghost_cli.client.HttpCli.post', return_value=response)

        cli = GhostCli("http://localhost", "")
        status, _ = cli.create_tag(**my_tag)
        assert status == False

    def test_delete_tag(self, mocker):
        tag_id = 1
        response.status_code = 204
        mocker.patch('ghost_cli.client.HttpCli.delete', return_value=response)
        cli = GhostCli("http://localhost", "")
        status, res = cli.delete_tag(tag_id)
        assert status == True
 