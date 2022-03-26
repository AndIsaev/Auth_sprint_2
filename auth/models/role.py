import http

from flask_restful import abort

from db import db
from models.mixins import CreatedUpgradeTimeMixin
from utils import codes
from utils.decorators import param_error_handler


class Role(CreatedUpgradeTimeMixin):
    __tablename__ = "role"

    name = db.Column(db.String(length=30), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Role {self.name} {self.id}"

    @classmethod
    @param_error_handler()
    def find_by_role_id(cls, role_id: str):
        return cls.query.filter(cls.id == role_id).first()

    @classmethod
    @param_error_handler()
    def find_by_role_name(cls, role_name: str):
        return cls.query.filter(cls.name == role_name).first()

    @classmethod
    def delete_by_id(cls, role_id: str):
        role = cls.query.filter(cls.id == role_id).first()
        if role:
            db.session.delete(role)
            db.session.commit()
        else:
            message: dict = {"message": codes.OBJECT_NOT_FOUND, "errors": []}
            abort(http_status_code=http.HTTPStatus.NOT_FOUND, message=message)

    @classmethod
    def by_name_exist(cls, role_name: str) -> bool:
        return db.session.query(
            cls.query.filter(cls.name == role_name).exists()
        ).scalar()
