from db import db
from models import Role, User, UserRole
from utils import constants
from utils.validators import email_validation, username_validation


def create_new_user(username: str, email: str, password: str) -> User:
    """create new user"""
    new_user: User = User(
        username=username_validation(value=username),
        email=email_validation(value=email),
    )
    new_user.set_password(password=password)
    db.session.add(new_user)
    """ find default role """
    default_role = Role.find_by_role_name(
        role_name=constants.DEFAULT_ROLE_FOR_ALL_USERS
    )
    """ set default role for user """
    new_user_role = UserRole(user_id=new_user.id, role_id=default_role.id)
    new_user_role.save_to_db()
    return new_user
