from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.mixins import CreatedUpgradeTimeMixin
from utils.decorators import param_error_handler

from models import Role, User


class UserRole(CreatedUpgradeTimeMixin):
    __tablename__ = "user_role"

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey("role.id"), nullable=False)

    user = db.relationship(User, backref=db.backref('user_roles', lazy=True))
    role = db.relationship(Role, backref=db.backref('user_roles', lazy=True))

    __table_args__ = (db.UniqueConstraint("user_id", "role_id", name="user_role_pk"),)

    def __repr__(self) -> str:
        return f"<UserRole {self.user_id}:{self.role_id}>"

    @classmethod
    @param_error_handler()
    def get_row_by_ids(cls, user_id: str, role_id: str) -> bool:
        return cls.query.filter(cls.user_id == user_id, cls.role_id == role_id).first()

    @classmethod
    @param_error_handler()
    def is_row_exist(cls, user_id: str, role_id: str) -> bool:
        return db.session.query(
            cls.query.filter(cls.user_id == user_id, cls.role_id == role_id).exists()
        ).scalar()
