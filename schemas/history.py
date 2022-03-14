from marshmallow import fields

from app import ma
from models import SuccessHistory


class HistorySchema(ma.SQLAlchemyAutoSchema):
    created_at = fields.Function(lambda obj: obj.created_at.strftime("%Y-%m-%d %H:%M"))
    updated_at = fields.Function(lambda obj: obj.updated_at.strftime("%Y-%m-%d %H:%M"))

    class Meta:
        model = SuccessHistory
        fields = ("description", "created_at", "updated_at")
        load_instance = True
        # include_fk = True


history_schema = HistorySchema(many=True)
