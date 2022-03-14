import http
import uuid

from flask_restful import abort
from sqlalchemy.dialects.postgresql import UUID

from db import db


class IdMixin(db.Model):
    __abstract__ = True

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            abort(
                http_status_code=http.HTTPStatus.BAD_REQUEST,
                message={"message": "Something went wrong"},
            )


class CreatedUpgradeTimeMixin(IdMixin):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
