"""This module implements an http client with cache behavior, used by this package.
"""
from .lru_cache import ConditionalCache
from .http import HttpClient


class CacheEnabledHttpClient(HttpClient):
    # We considered
    # https://docs.python.org/3/library/functools.html#functools.lru_cache
    # Its counterpart for Python 2 https://github.com/saporitigianni/memorize

    def __init__(self, http_client):
        self._http_client = http_client  # A raw http_client

    @ConditionalCache(
        # key_maker=lambda args, kwargs: print(args, kwargs),
        cacheable=lambda resp, args, kwargs: resp.status_code==429)
    def post(self, url, **kwargs):
        return self._http_client.post(url, **kwargs)

    @ConditionalCache()
    def get(self, url, **kwargs):
        return self._http_client.get(url, **kwargs)

