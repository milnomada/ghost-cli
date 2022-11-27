from slugify import slugify
from typing import Union, Any, Tuple
from requests import Response
from .models import Post, Tag
import datetime
import logging
import requests


logger = logging.getLogger(__file__)


class HttpCli(object):
    def __init__(self, url: str, headers: dict):
        self.url = url
        self.headers = headers

    def get(self, path: str, filter: str) -> Union[Response, None]:
        url = f"{self.url}/{path}{filter}"
        logger.debug(f"{url}")
        try:
            r = requests.get(url, headers=self.headers)
            logger.debug(r.json())
            return r
        except Exception as e:
            logger.error(f"Exception: {e}")
            return None

    def post(self, path: str, data: dict) -> Union[Response, None]:
        url = f"{self.url}/{path}/"
        logger.debug(f"{url}")
        try:
            r = requests.post(url, json=data, headers=self.headers)
            logging.debug(r.json())
            return r
        except Exception as e:
            logger.error(f"Exception: {e}")
            return None

    def put(self, path: str, data: dict) -> Union[Response, None]:
        url = f"{self.url}/{path}/"
        logger.debug(f"{url}")
        try:
            r = requests.put(url, json=data, headers=self.headers)
            logging.debug(r.json())
            return r
        except Exception as e:
            logger.error(f"Exception: {e}")
            return None

    def delete(self, path: str) -> Union[Response, None]:
        url = f"{self.url}/{path}/"
        logger.debug(f"{url}")
        try:
            r = requests.delete(url, headers=self.headers)
            logging.debug(r.__dict__)
            return r
        except Exception as e:
            logger.error(f"Exception: {e}")
            return None


class GhostCli(HttpCli):
    def __init__(self, url, token):
        url = url[:-1] if url.endswith("/") else url
        url = f"{url}/ghost/api/admin"
        headers = {'Authorization': 'Ghost {}'.format(token)}
        super(GhostCli, self).__init__(url, headers)

        logger.debug(headers)
        logger.info(f"GhostCli started at {url}")

    def get_post_by_title(self, title: str) -> Union[Post, None]:
        slug = slugify(title)
        logger.debug(f"slug: {slug}")
        my_filter = f"?filter=title:'{title}'&limit=1"
        res = self.get('posts', my_filter)
        data = res.json()['posts']
        return Post(**data[0]) if len(data) > 0 else None

    def get_post(self, attr: str, value: Any) -> Union[Post, None]:
        logger.debug(f"{attr}: {value}")
        my_filter = f"?filter={attr}:{value}&limit=1"
        res = self.get('posts', my_filter)
        data = res.json()['posts']
        return Post(**data[0]) if len(data) > 0 else None

    def get_posts(self, attr: str, value: Any, page: int=1, limit: int=15) -> Union[list[Post], None]:
        logger.debug(f"{attr}: {value}")
        my_filter = f"?filter={attr}:{value}&page={page}&limit={limit}"
        res = self.get('posts', my_filter)
        data = res.json()['posts']
        data = None if data is None else [Post(**d) for d in data]
        return data

    def get_tag_by_name(self, name: str) -> Union[Tag, None]:
        slug = slugify(name)
        logger.debug(f"slug: {slug}")
        my_filter = f"?filter=name:'{name}'&limit=1"
        res = self.get('tags', my_filter)
        data = res.json()
        return Tag(**data[0]) if len(data) > 0 else None

    def get_tag(self, attr: str, value: Any) -> Union[Tag, None]:
        logger.debug(f"{attr}: {value}")
        my_filter = f"?filter={attr}:{value}&limit=1"
        res = self.get('tags', my_filter)
        data = res.json()['tags']
        return Tag(**data[0]) if len(data) > 0 else None

    def create_post(self, **kwargs) -> bool:
        body = {'posts': [kwargs]}
        res = self.post('posts', body)
        return res.status_code == 201 if res is not None else False

    def update_post(self, id: str, **kwargs):
        body = {'posts': [kwargs]}
        res = self.put(f'posts/{id}', body)
        logger.debug(res.__dict__)
        return res.status_code == 200 if res is not None else False

    def delete_post(self, id: str):
        res = self.delete(f'posts/{id}')
        logger.debug(res.__dict__)
        return res.status_code == 204 if res is not None else False

    def create_tag(self, tag: Tag) -> bool:
        body = {'tags': [tag.__dict__]}
        res = self.post('tags', body)
        logger.debug(res.__dict__)
        return res.status_code == 201 if res is not None else False

    def delete_tag(self, id: str):
        res = self.delete(f'tags/{id}')
        logger.debug(res.__dict__)
        return res.status_code == 204 if res is not None else False
