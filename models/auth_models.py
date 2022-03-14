from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from models.mixins import CreatedUpgradeTimeMixin
from utils import constants
from utils.validators import password_validation


def create_partition(target, connection, **kw) -> None:
    """ creating partition by success_history """
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "success_history_windows" PARTITION OF "success_history" FOR VALUES IN ('windows')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "success_history_linux" PARTITION OF "success_history" FOR VALUES IN ('linux')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "success_history_other" PARTITION OF "success_history" FOR VALUES IN ('other')"""
    )


class User(CreatedUpgradeTimeMixin):
    __tablename__ = "user"

    username = db.Column(
        db.String(length=constants.USERNAME_MAX_LENGTH), unique=True, nullable=False
    )

    password = db.Column(db.String(length=256), nullable=False)
    email = db.Column(db.String(length=255), nullable=False, unique=True)

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
    __table_args__ = (
        UniqueConstraint('id', 'platform'),
        {
            'postgresql_partition_by': 'LIST (platform)',
            'listeners': [('after_create', create_partition)],
        }
    )

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"))
    description = db.Column(db.String(length=500), nullable=False)
    ip_address = db.Column(db.String(100))
    user_agent = db.Column(db.Text, nullable=False)
    platform = db.Column(db.Text, primary_key=True)
    browser = db.Column(db.Text)
