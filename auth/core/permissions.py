import http
from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from core import config
from models import Role, UserRole
from utils import constants


def is_admin_permissions():
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id: str = get_jwt_identity()
            roles: list[str] = [
                i.name
                for i in Role.query.join(UserRole)
                .filter(UserRole.user_id == user_id)
                .all()
            ]
            if constants.ROLE_FOR_ADMIN in roles or config.TESTING:
                return func(*args, **kwargs)
            else:
                return {
                    "message": "permission error",
                    "description": "Only for users, who has 'admin' role!",
                    "errors": [],
                }, http.HTTPStatus.FORBIDDEN

        return decorator

    return wrapper
