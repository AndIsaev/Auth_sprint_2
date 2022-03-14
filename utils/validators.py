import re
from http import HTTPStatus

from flask_restful import abort

from . import codes, constants, messages


def username_validation(value: str) -> str:
    """Validate username's value for database"""
    """ Check which symbols username contains """
    if not re.match(constants.REGEX_FOR_FIRST_SYMBOL, value):
        abort(
            http_status_code=HTTPStatus.BAD_REQUEST,
            success=False,
            data=[],
            message=codes.INVALID_USERNAME_ERROR,
            errors={"username": messages.USERNAME_FIRST_SYMBOL},
        )
    if not re.match(constants.REGEX_FOR_LOGIN, value):
        abort(
            http_status_code=HTTPStatus.BAD_REQUEST,
            success=False,
            data=[],
            message=codes.INVALID_USERNAME_ERROR,
            errors={"username": messages.USERNAME_OTHER_SYMBOLS},
        )
    """ Check username's length """
    if len(value) < constants.USERNAME_MIN_LENGTH:
        abort(
            http_status_code=HTTPStatus.BAD_REQUEST,
            success=False,
            data=[],
            message=codes.INVALID_USERNAME_ERROR,
            errors={"username": messages.USERNAME_MIN_INVALID},
        )
    elif len(value) > constants.USERNAME_MAX_LENGTH:
        abort(
            http_status_code=HTTPStatus.BAD_REQUEST,
            success=False,
            data=[],
            message=codes.INVALID_USERNAME_ERROR,
            errors={"username": messages.USERNAME_MAX_INVALID},
        )
    """ Return validated username """
    return value


def password_validation(value: str) -> str:
    """Validate password's value for database"""
    """ Check which symbols password contains """
    if re.match(constants.REGEX_ALPHABET_IN_PASSWORD, value):
        if not re.findall(constants.REGEX_UPPER_LATTER_IN_PASSWORD, value):
            abort(
                http_status_code=HTTPStatus.BAD_REQUEST,
                success=False,
                data=[],
                message=codes.INVALID_PASSWORD_ERROR,
                errors={"password": messages.PASSWORD_UPPER_LATTER},
            )
        elif not re.findall(constants.REGEX_LOWER_LATTER_IN_PASSWORD, value):
            abort(
                http_status_code=HTTPStatus.BAD_REQUEST,
                success=False,
                data=[],
                message=codes.INVALID_PASSWORD_ERROR,
                errors={"password": messages.PASSWORD_LOWER_LATTER},
            )
        elif not re.findall(constants.REGEX_PASSWORD_INT_SYMBOL, value):
            abort(
                http_status_code=HTTPStatus.BAD_REQUEST,
                success=False,
                data=[],
                message=codes.INVALID_PASSWORD_ERROR,
                errors={"password": messages.PASSWORD_INTEGER_SYMBOL},
            )
    else:
        abort(
            http_status_code=HTTPStatus.BAD_REQUEST,
            success=False,
            data=[],
            message=codes.INVALID_PASSWORD_ERROR,
            errors={"password": messages.PASSWORD_ALPHABET},
        )
    """ Check password's length """
    if len(value) < constants.PASSWORD_MIN_LENGTH:
        abort(
            http_status_code=HTTPStatus.BAD_REQUEST,
            success=False,
            data=[],
            message=codes.INVALID_PASSWORD_ERROR,
            errors={"password": messages.PASSWORD_MIN_LENGTH},
        )
    elif len(value) > constants.PASSWORD_MAX_LENGTH:
        abort(
            http_status_code=HTTPStatus.BAD_REQUEST,
            success=False,
            data=[],
            message=codes.INVALID_PASSWORD_ERROR,
            errors={"password": messages.PASSWORD_MAX_LENGTH},
        )
    """ Return validated password """
    return value
