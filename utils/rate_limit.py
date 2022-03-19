import datetime
from functools import wraps
from http import HTTPStatus

from flask import request

from db import cache


def rate_limit(limit=1000, interval=60):
    """Rate limit for API endpoints.
    If the user has exceeded the limit, then return the response 429.
    """

    def rate_limit_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key: str = f"Limit::{request.remote_addr}:{datetime.datetime.now().minute}"
            current_request_count = cache.get(key=key)

            if current_request_count and int(current_request_count) >= limit:
                return {
                    "message": f"Too many requests. Limit {limit} in {interval} seconds",
                }, HTTPStatus.TOO_MANY_REQUESTS

            else:
                pipe = cache.pipeline()
                pipe.incr(key, 1)
                pipe.expire(key, interval + 1)
                pipe.execute()

                return func(*args, **kwargs)

        return wrapper

    return rate_limit_decorator
