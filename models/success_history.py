from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.mixins import CreatedUpgradeTimeMixin


class SuccessHistory(CreatedUpgradeTimeMixin):
    __tablename__ = "success_history"

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"))
    description = db.Column(db.String(length=500), nullable=False)

    def __repr__(self) -> str:
        return f"<SuccessHistory: {self.user_id} - {self.description}>"
