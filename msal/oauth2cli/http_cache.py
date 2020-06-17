"""This module documents an http client with cache behavior, used by this package.
"""
import memorize

from .http import HttpClient, Response


def key_maker(args, kwds, typed, **kwargs):
    return memorize.core._make_key(args, kwds, typed, **kwargs)


class CacheEnabledHttpClient(HttpClient):
    # We considered
    # https://docs.python.org/3/library/functools.html#functools.lru_cache
    # Its counterpart for Python 2 https://github.com/saporitigianni/memorize

    def __init__(self, http_client):
        self._http_client = http_client  # A raw http_client
        self._cache = {}

    def _request(
            self, method, url, params=None, data=None, headers=None, **kwargs):
        _method = {}
        response = self._http_client.

    def post(self, cache_key, url, params=None, data=None, headers=None, **kwargs):
        now = time.time()
        hit = self._cache.get(cache_key, {})
        if hit and hit.get("expire_at", 0) > now:
            return hit["payload"]

        resp = self._request(
            "POST", url, params=None, data=None, headers=None, **kwargs)

        if resp.status_code >=500:
            # Naively retry once. It might fix majority of intermittent errors
            resp = self._request(
                "POST", url, params=None, data=None, headers=None, **kwargs)

        if resp.status_code >=500 or resp.status_code == 429:
            self._cache[cache_key] = {
                "payload": NormalizedResponse(  # raw resp might be volative
                    raw_resp=resp),
                "expire_at":
                    now + getattr(resp, "headers", {}).get("Retry-After", 123),
                }
        self._cache = {  # One of the hardest thing in CS: cache invalidation :)
            k: v for k, v in self._cache().items() if v["expire_at"] > now}

        return resp

    @memorize(maxsize=128, timeout=0, key=foo)
    def get(self, url, params=None, headers=None, **kwargs):
        """HTTP get.

        :param dict params: A dict to be url-encoded and sent as query-string.
        :param dict headers: A dict representing headers to be sent via request.

        It returns an :class:`~Response`-like object.

        Note: In its async counterpart, this method would be defined as async.
        """
        return Response()


class NormalizedResponse(Response):
    def __init__(self, raw_resp=None, status_code=None, text=None):
        self.status_code = status_code or raw_resp.status_code
        self.text = text or raw_resp.text
        self._raw_resp = raw_resp

    def raise_for_status(self):
        if self._raw_resp:
            self._raw_resp.raise_for_status()
        if self.status_code >=400:
            raise RuntimeError("TBD")  # TODO

