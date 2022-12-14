from slugify import slugify
from typing import Union, Any, Tuple, List
from requests import Response
from .models import Post, Tag
from .tokener import Tokener
import datetime
import logging
import requests
import urllib


logger = logging.getLogger(__file__)







class HttpCli(object):
    def __init__(self, url: str, headers: dict):
        self.url = url
        self.headers = headers

    def get(self, path: str, filter: str) -> Union[Response, None]:
        url = f"{self.url}/{path}?{filter}"
        logger.debug(f"{url}")
        try:
            r = requests.get(url, headers=self.headers)
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

    def _get_payload(self, res: Response) -> Union[Any, None]:
        try:
            payload = res.json()
        except Exception as e:
            logger.error(f"Exception: {e}")
            return None
        if 'errors' in payload:
            logger.error(payload['errors'])
            return None
        key = list(payload.keys())[0]
        return payload[key]

    def get_post_by_title(self, title: str) -> Tuple[Union[Post, None], Response]:
        quoted = urllib.parse.quote(title)
        logger.debug(f"{title} -> {quoted}")
        my_filter = f"filter=title:'{quoted}'&limit=1"
        res = self.get('posts', my_filter)
        data = self._get_payload(res) or []
        data = Post(**data[0]) if len(data) > 0 else None
        return data, res

    def get_post(self, attr: str, value: Any) -> Tuple[Union[Post, None], Response]:
        logger.debug(f"{attr}: {value}")
        value = value if attr != "title" else f"'{value}'"
        my_filter = f"filter={attr}:{value}&limit=1"
        res = self.get('posts', my_filter)
        data = self._get_payload(res) or []
        data = Post(**data[0]) if len(data) > 0 else None
        return data, res

    def get_posts(
        self, page: int=1, limit: int=15, formats: str="html,mobiledoc", order: str="publisihed_at desc"
    ) -> Tuple[Union[List[Post], None], Response]:
        q = {
            'include': 'tags',
            'status': 'all',
            'formats': formats,
            'page': page,
            'limit': limit,
            'order': order
        }
        my_filter = urllib.parse.urlencode(q)
        res = self.get('posts', my_filter)
        data = self._get_payload(res)
        data = None if data is None else [Post(**d) for d in data]
        return data, res

    def get_tag_by_name(self, name: str) -> Tuple[Union[Tag, None], Response]:
        quoted = urllib.parse.quote(name)
        logger.debug(f"{name} -> {quoted}")
        my_filter = f"filter=name:'{quoted}'&limit=1"
        res = self.get('tags', my_filter)
        data = self._get_payload(res) or []
        data = Tag(**data[0]) if len(data) > 0 else None
        return data, res

    def get_tag(self, attr: str, value: Any) -> Tuple[Union[Tag, None], Response]:
        logger.debug(f"{attr}: {value}")
        value = value if attr != "name" else f"'{value}'"
        my_filter = f"filter={attr}:{value}&limit=1"
        res = self.get('tags', my_filter)
        data = self._get_payload(res) or []
        data = Tag(**data[0]) if len(data) > 0 else None
        return data, res

    def get_tags(self, page: int=1, limit: int=15) -> Tuple[Union[List[Tag], None], Response]:
        q = {
            'status': 'all',
            'page': page,
            'limit': limit
        }
        my_filter = urllib.parse.urlencode(q)
        res = self.get('tags', my_filter)
        data = self._get_payload(res)
        data = None if data is None else [Tag(**d) for d in data]
        return data, res

    def create_post(self, **kwargs) -> Tuple[bool, Response]:
        body = {'posts': [kwargs]}
        res = self.post('posts', body)
        result = res.status_code == 201 if res is not None else False
        return result, res

    def update_post(self, id: str, **kwargs) -> Tuple[bool, Response]:
        body = {'posts': [kwargs]}
        res = self.put(f'posts/{id}', body)
        if res is not None:
            logger.debug(res.__dict__)
        result = res.status_code == 200 if res is not None else False
        return result, res

    def delete_post(self, id: str) -> Tuple[bool, Response]:
        res = self.delete(f'posts/{id}')
        if res is not None:
            logger.debug(res.__dict__)
        result = res.status_code == 204 if res is not None else False
        return result, res

    def create_tag(self, **kwargs) -> Tuple[bool, Response]:
        body = {'tags': [kwargs]}
        res = self.post('tags', body)
        if res is not None:
            logger.debug(res.__dict__)
        result = res.status_code == 201 if res is not None else False
        return result, res

    def delete_tag(self, id: str) -> Tuple[bool, Response]:
        res = self.delete(f'tags/{id}')
        if res is not None:
            logger.debug(res.__dict__)
        result = res.status_code == 204 if res is not None else False
        return result, res

    def create_author(self, **kwargs) -> Tuple[bool, Response]:
        body = {'authors': [kwargs]}
        res = self.post('authors', body)
        if res is not None:
            logger.debug(res.__dict__)
        result = res.status_code == 201 if res is not None else False
        return result, res

    def delete_author(self, id: str) -> Tuple[bool, Response]:
        res = self.delete(f'authors/{id}')
        if res is not None:
            logger.debug(res.__dict__)
        result = res.status_code == 204 if res is not None else False
        return result, res



class GhostPy(object):
    def __init__(self, url: str, t: Tokener):
        url = url[:-1] if url.endswith("/") else url
        self.endpoint = f"{url}/ghost/api/admin"
        self.tokener = t
        self.headers = {'Authorization': 'Ghost {}'.format(t.generate())}

    def auth(self):
        self.headers = {'Authorization': 'Ghost {}'.format(self.tokener.generate())}
