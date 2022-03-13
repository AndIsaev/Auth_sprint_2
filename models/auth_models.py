from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from models.mixins import CreatedUpgradeTimeMixin
from utils import constants
from utils.validators import password_validation


class User(CreatedUpgradeTimeMixin):
    __tablename__ = "user"

    username = db.Column(
        db.String(length=constants.USERNAME_MAX_LENGTH), unique=True, nullable=False
    )
    password = db.Column(db.String(length=256), nullable=False)

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


class SuccessHistory(CreatedUpgradeTimeMixin):
    __tablename__ = "success_history"

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"))
    description = db.Column(db.String(length=500), nullable=False)
