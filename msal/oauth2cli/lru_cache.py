from functools import wraps

import lru  # pip install py_lru_cache


# The LRUCachedFunction and lru_cache_function from py_lru_cache package
# can decorate only functions, but not class methods. That is because:
# https://stackoverflow.com/questions/41032224/python-class-decorator-does-not-work


def conditional_cache(func):
    return ConditionalCache()(func)


class ConditionalCache(object):
    """A cache decorator that allows per-item decision on whether to cache an item.
    """
    # The code structure below can decorate both function and method.
    # It is inspired by https://stackoverflow.com/a/9417088
    # We may potentially switch to build upon
    # https://github.com/micheles/decorator/blob/master/docs/documentation.md#statement-of-the-problem
    def __init__(self, cache=lru.LRUCacheDict(), key_maker=None, cacheable=None):
        self._cache = cache
        self._key_maker = key_maker or (lambda function, args, kwargs: (
                function.__name__,  # So different decorators could share same cache
                args, kwargs,
                ))
        self._cacheable = cacheable or (lambda result, args, kwargs: True)

    def __call__(self, function):

        @wraps(function)
        def wrapper(*args, **kwargs):
            key = self._key_maker(function, args, kwargs)
            if key is None:  # Then bypass the cache
                return function(*args, **kwargs)
            try:
                return self._cache[key]
            except KeyError:
                # We choose to NOT call function(...) in this block, otherwise
                # potential exception from function(...) would become a confusing
                # "During handling of the above exception, another exception occurred"
                pass
            value = function(*args, **kwargs)
            if self._cacheable(value, args, kwargs):
                self._cache[key] = value
            return value

        return wrapper

