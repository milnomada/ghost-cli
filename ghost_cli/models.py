import datetime
import logging

logger = logging.getLogger(__file__)

class Post(object):
    slug: str # "welcome-short",
    id: str # "5ddc9141c35e7700383b2937",
    uuid: str # "a5aa9bd8-ea31-415c-b452-3040dae1e730",
    title: str # "Welcome",
    mobiledoc: str # "{\"version\":\"0.3.1\",\"atoms\":[],\"cards\":[],\"markups\":[],\"sections\":[[1,\"p\",[[0,[],0,\"👋 Welcome, it's great to have you here.\"]]]]}",
    html: str # "<p>👋 Welcome, it's great to have you here.</p>",
    comment_id: str # "5ddc9141c35e7700383b2937",
    feature_image: str # "https://static.ghost.org/v3.0.0/images/welcome-to-ghost.png",
    feature_image_alt: str # null,
    feature_image_caption: str # null,
    featured: bool # false,
    status: str # "published",
    visibility: str # "public",
    created_at: datetime.datetime # "2019-11-26T02:43:13.000Z",
    updated_at: datetime.datetime # "2019-11-26T02:44:17.000Z",
    published_at: datetime.datetime # "2019-11-26T02:44:17.000Z",
    custom_excerpt: str # null,
    codeinjection_head: str # null,
    codeinjection_foot: str # null,
    custom_template: str # null,
    canonical_url: str # null,
    tags: list #
    authors: list #
    primary_author: dict #
    primary_tag: dict #
    url: str # "https://docs.ghost.io/welcome-short/",
    excerpt: str # "👋 Welcome, it's great to have you here.",
    og_image: str # null,
    og_title: str # null,
    og_description: str # null,
    twitter_image: str # null,
    twitter_title: str # null,
    twitter_description: str # null,
    meta_title: str # null,
    meta_description: str # null,
    email_only: str # false,
    newsletter: dict # --
    email: dict # --

    def __init__(self, **kwargs):
        for k in kwargs:
            if k not in self.__annotations__:
                logger.debug(f"Post: drop attribute {k}")
                continue
            setattr(self, k, kwargs[k])


class Tag(object):
    slug: str # "getting-started",
    id: str # "5ddc9063c35e7700383b27e0",
    name: str # "Getting Started",
    description: str # null,
    feature_image: str # null,
    visibility: str # "public",
    meta_title: str # null,
    meta_description: str # null,
    og_image: str # null,
    og_title: str # null,
    og_description: str # null,
    twitter_image: str # null,
    twitter_title: str # null,
    twitter_description: str # null,
    codeinjection_head: str # null,
    codeinjection_foot: str # null,
    canonical_url: str # null,
    accent_color: str # null,
    url: str # "https://docs.ghost.io/tag/getting-started/"

    def __init__(self, **kwargs):
        for k in kwargs:
            if k not in self.__annotations__:
                logger.debug(f"Tag: drop attribute {k}")
                continue
            setattr(self, k, kwargs[k])


class Author(object):
    slug: str # "cameron",
    id: str # "5ddc9b9510d8970038255d02",
    name: str # "Cameron Almeida",
    profile_image: str # "https://docs.ghost.io/content/images/2019/03/1c2f492a-a5d0-4d2d-b350-cdcdebc7e413.jpg",
    cover_image: str # null,
    bio: str # "Editor at large.",
    website: str # "https://example.com",
    location: str # "Cape Town",
    facebook: str # "example",
    twitter: str # "@example",
    meta_title: str # null,
    meta_description: str # null,
    url: str # "https://docs.ghost.io/author/cameron/"

    def __init__(self, **kwargs):
        for k in kwargs:
            if k not in self.__annotations__:
                logger.debug(f"Author: drop attribute {k}")
                continue
            setattr(self, k, kwargs[k])
