import jwt
import datetime
import os
import requests
import logging


logger = logging.getLogger(__file__)


class Tokener(object):
    
    def __init__(self, key: str=None):
        """Tokener init
        Create a new Tokener instance. The `key` paramenter supersedes
        the `GHOST_KEY` environment variable. This, allows to create
        connectinos to different (ghost) hosts.
        Args:
            key (str, optional): A ghost key. Defaults to None.

        Raises:
            RuntimeError: It not key provided
        """
        key = os.environ.get("GHOST_KEY", None) if key is None else key
        if not key:
            raise RuntimeError("Missing environment configuration")

        key_id, secret = key.split(":")
        self.id = key_id
        self.secret = secret
        logger.debug("token generated id: {}".format(key_id))

    def generate(self):
        iat = int(datetime.datetime.now().timestamp())
        header = {
            'alg': 'HS256',
            'typ': 'JWT',
            'kid': self.id
        }
        payload = {
            'iat': iat,
            'exp': iat + 5 * 60,
            'aud': '/admin/'
        }
        logger.debug("decoding for id: {}".format(self.id))
        token = jwt.encode(payload, bytes.fromhex(self.secret), algorithm='HS256', headers=header)
        return token
