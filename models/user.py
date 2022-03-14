from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from models.mixins import CreatedUpgradeTimeMixin
from utils import constants
from utils.validators import password_validation


class User(CreatedUpgradeTimeMixin):
    """
    username:
        псевдоним для пользователя. Должен быть определен для всех пользователей и
        обязательно должен быть уникальным.
    email:
        адрес электронной почты пользователя. Этот столбец не является обязательным.
    """

    __tablename__ = "user"

    username = db.Column(
        db.String(length=constants.USERNAME_MAX_LENGTH), nullable=False, unique=True
    )
    password = db.Column(db.String(length=256), nullable=False)
    social_id = db.Column(db.String(length=64), nullable=True, unique=True)
    email = db.Column(db.String(length=64), nullable=True)

    def __repr__(self) -> str:
        return f"<Username: {self.username}>"

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    def set_password(self, password: str):
        password: str = password_validation(value=password)
        self.password = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(pwhash=self.password, password=password)
