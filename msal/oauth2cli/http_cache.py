"""This module implements an http client with cache behavior, used by this package.
"""
from .lru_cache import ConditionalCache
from .expiring_dict import ExpiringDict
from .http import HttpClient


class CacheEnabledHttpClient(HttpClient):
    # We considered
    # https://docs.python.org/3/library/functools.html#functools.lru_cache
    # Its counterpart for Python 2 https://github.com/saporitigianni/memorize

    _cache = ExpiringDict(expiry=5)

    def __init__(self, http_client):
        self._http_client = http_client  # A raw http_client

    @ConditionalCache(
        cache=_cache,
        key_maker=lambda func, args, kwargs:  # print(func, args, kwargs),
            (
            "http 429, 5xx, and retry-after",
            args[1],  # The token endpoint url is an approximation of authority
            kwargs.get("data", {}).get("client_id"),
            kwargs.get("data", {}).get("scope"),
            kwargs.get("data", {}).get("refresh_token")
                or kwargs.get("data", {}).get("username"),
            ),
        cacheable=lambda resp, args, kwargs:
            resp.status_code != 429 or resp.status_code >= 500
            or "Retry-After" in resp.headers,  # Supposed to be Case-insensitive
        )
    def post(self, url, **kwargs):
        return self._http_client.post(url, **kwargs)

    @ConditionalCache()
    def get(self, url, **kwargs):
        return self._http_client.get(url, **kwargs)

