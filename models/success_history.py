from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import UniqueConstraint

from db import db
from models.mixins import CreatedUpgradeTimeMixin

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
