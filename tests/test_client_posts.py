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
from ghost_cli.models import Post
from unittest.mock import Mock, MagicMock, patch, PropertyMock


response = Mock()
my_mock = Mock()
my_mock.get = MagicMock(return_value=response)
my_mock.post = MagicMock(return_value=response)


class TestClient():

    def test_post_model(self):
        post_title = "Hello World"
        post_slug = slugify(post_title)
        
        my_post = {
            "title": post_title,
            "slug": post_slug,
            "non_existent": 3
        }
        p = Post(**my_post)
        assert p.title == post_title
        assert p.slug == post_slug
        with pytest.raises(AttributeError):
            print(p.non_existent, flush=False)

    def test_get_post(self, mocker):
        post_title = "Hello World"
        post_slug = slugify(post_title)
        my_posts = {'posts': [{
            "title": post_title,
            "slug": post_slug
        }]}
        response.json = MagicMock(return_value=my_posts)
        mocker.patch('requests.get', return_value=response)

        cli = GhostCli("http://localhost", "")
        post, _ = cli.get_post('slug', post_slug)
        assert post.title == post_title
        assert post.slug == post_slug

    def test_get_post_fail(self, mocker):
        post_title = "Hello World"
        post_slug = slugify(post_title)
        my_posts = {'posts': [{
            "title": post_title,
            "slug": post_slug
        }]}
        response.json = MagicMock(return_value=my_posts)
        mocker.patch('requests.get', side_effect=Exception("my exception"))
        cli = GhostCli("http://localhost", "")
        post, _ = cli.get_post('slug', post_slug)
        assert post is None

    def test_get_post_fail_json(self, mocker):
        post_title = "Hello World"
        post_slug = slugify(post_title)
        my_posts = {'posts': [{
            "title": post_title,
            "slug": post_slug
        }]}
        response.json = MagicMock(side_effect=Exception("my exception"))
        mocker.patch('requests.get', return_value=response)
        cli = GhostCli("http://localhost", "")
        post, _ = cli.get_post('slug', post_slug)
        assert post is None

    def test_get_post_fail_errors(self, mocker):
        post_title = "Hello World"
        post_slug = slugify(post_title)
        my_error = {'errors': [{
            "message": "my error message"
        }]}
        response.json = MagicMock(return_value=my_error)
        mocker.patch('requests.get', return_value=response)
        cli = GhostCli("http://localhost", "")
        post, _ = cli.get_post('slug', post_slug)
        assert post is None

    def test_get_post_by_title(self, mocker):
        post_title = "Hello World"
        post_slug = slugify(post_title)
        my_posts = {'posts': [{
            "title": post_title,
            "slug": post_slug
        }]}
        response.json = MagicMock(return_value=my_posts)
        mocker.patch('requests.get', return_value=response)
        cli = GhostCli("http://localhost", "")
        post, _ = cli.get_post_by_title(post_title)
        assert post.title == post_title
        assert post.slug == post_slug

    def test_get_posts(self, mocker):
        post_title = "Hello World"
        post_slug = slugify(post_title)
        post_title_2 = "Hello World Two"
        post_slug_2 = slugify(post_title_2)

        my_posts = {'posts': [{
            "title": post_title,
            "slug": post_slug
        }, {
            "title": post_title_2,
            "slug": post_slug_2
        }]}

        response.json = MagicMock(return_value=my_posts)
        mocker.patch('requests.get', return_value=response)

        cli = GhostCli("http://localhost", "")
        posts, _ = cli.get_posts()
        post_1 = posts[0]
        assert len(posts) == 2
        assert post_1.title == post_title
        assert post_1.slug == post_slug

    def test_create_post(self, mocker):
        post_title = "Hello World"
        post_slug = slugify(post_title)
        my_post = {
            "title": post_title,
            "slug": post_slug
        }
        response.status_code = 201
        mocker.patch('ghost_cli.client.HttpCli.post', return_value=response)
        cli = GhostCli("http://localhost", "")
        status, _  = cli.create_post(**my_post)
        assert status == True

    def test_create_post_requests(self, mocker):
        post_title = "Hello World"
        post_slug = slugify(post_title)
        my_post = {
            "title": post_title,
            "slug": post_slug
        }
        response.status_code = 201
        mocker.patch('requests.post', return_value=response)
        cli = GhostCli("http://localhost", "")
        status, _ = cli.create_post(**my_post)
        assert status == True

    def test_create_post_failed(self, mocker):
        post_title = "Hello World"
        post_slug = slugify(post_title)
        my_post = {
            "title": post_title,
            "slug": post_slug
        }
        response.status_code = 400
        mocker.patch('requests.post', side_effect=Exception("my exception"))
        cli = GhostCli("http://localhost", "")
        status, _ = cli.create_post(**my_post)
        assert status == False

    def test_update_post(self, mocker):
        post_id = 1
        post_title = "New Hello World"
        post_slug = slugify(post_title)
        my_post = {
            "title": post_title,
        }
        response.status_code = 200
        mocker.patch('ghost_cli.client.HttpCli.put', return_value=response)
        cli = GhostCli("http://localhost", "")
        status, _ = cli.update_post(post_id, **my_post)
        assert status == True

    def test_update_post_requests(self, mocker):
        post_id = 1
        post_title = "New Hello World"
        post_slug = slugify(post_title)
        my_post = {
            "title": post_title,
        }
        response.status_code = 200
        mocker.patch('requests.put', return_value=response)
        cli = GhostCli("http://localhost", "")
        status, _ = cli.update_post(post_id, **my_post)
        assert status == True

    def test_update_post_failed(self, mocker):
        post_id = 1
        post_title = "New Hello World"
        post_slug = slugify(post_title)
        my_post = {
            "title": post_title,
        }
        mocker.patch('requests.put', side_effect=Exception("my exception"))
        cli = GhostCli("http://localhost", "")
        status, _ = cli.update_post(post_id, **my_post)
        assert status == False

    def test_delete_post(self, mocker):
        post_id = 1
        response.status_code = 204
        mocker.patch('ghost_cli.client.HttpCli.delete', return_value=response)
        cli = GhostCli("http://localhost", "")
        status, _ = cli.delete_post(post_id)
        assert status == True

    def test_delete_post_request(self, mocker):
        post_id = 1
        response.status_code = 204
        mocker.patch('requests.delete', return_value=response)
        cli = GhostCli("http://localhost", "")
        status, _ = cli.delete_post(post_id)
        assert status == True
        