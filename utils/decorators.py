import http
from functools import wraps
from typing import Optional, Union

from flask import Response, request
from flask_restful import abort
from redis.exceptions import ConnectionError


def remote_oauth_api_error_handler(func):
    """Decorator to catch remote oauth service's api errors"""

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError:
            message: dict[str, Union[str, list]] = {
                "message": "Redis error",
                "description": "try again later...",
                "errors": [],
            }
            abort(http_status_code=http.HTTPStatus.BAD_REQUEST, message=message)
        except Exception as e:
            message: dict[str, Union[str, list]] = {
                "message": "Oauth error",
                "description": "Try another social network or try again later...",
                "errors": [],
            }
            abort(http_status_code=http.HTTPStatus.BAD_REQUEST, message=message)

    return inner


def requires_basic_auth(func):
    """Decorator to require HTTP Basic Auth for your endpoint."""

    def check_auth(username: str, password: str):
        return username == "guest" and password == "secret"

    def authenticate():
        return Response(
            "Authentication required.",
            http.HTTPStatus.UNAUTHORIZED,
            {"WWW-Authenticate": "Basic realm='Login Required'"},
        )

    @wraps(func)
    def decorated(*args, **kwargs):
        # NOTE: This example will require Basic Auth only when you run the
        # app directly. For unit tests, we can't block it from getting the
        # Swagger specs so we just allow it to go thru without auth.
        # The following two lines of code wouldn't be needed in a normal
        # production environment.
        if __name__ != "__main__":
            return func(*args, **kwargs)

        auth = request.authorization
        if not auth or not check_auth(username=auth.username, password=auth.password):
            return authenticate()
        return func(*args, **kwargs)

    return decorated


def param_error_handler():
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                message: dict[str, Union[str, list]] = {
                    "message": "Wrong params",
                    "description": "Check that you send correct data",
                    "errors": [],
                }
                abort(http_status_code=http.HTTPStatus.BAD_REQUEST, message=message)

        return inner

    return decorator


def api_response_wrapper():
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs) -> tuple:
            result = func(*args, **kwargs)

            response, status_code = (
                result if isinstance(result, tuple) else (result, 200)
            )

            message: Optional[str] = (
                response.pop("message") if "message" in response else None
            )
            description: Optional[str] = (
                response.pop("description") if "description" in response else None
            )
            errors: Optional[list] = (
                response.pop("errors") if "errors" in response else []
            )
            """ prepare wrapped response """
            data: list = []
            if isinstance(response, list):
                data = response
            elif response:
                data.append(response)
            wrapped_response: dict[str, Union[str, list, bool]] = {
                "success": True
                if str(status_code.numerator).startswith("2")
                else False,
                "data": data,
            }
            if message:
                wrapped_response["message"] = message
            if description:
                wrapped_response["description"] = description
            if errors:
                wrapped_response["errors"] = errors
            return wrapped_response, status_code

        return inner

    return decorator
