from marshmallow import fields

from app import ma
from models import Role


class RoleSchema(ma.SQLAlchemyAutoSchema):
    created_at = fields.Function(lambda obj: obj.created_at.strftime("%Y-%m-%d %H:%M"))
    updated_at = fields.Function(lambda obj: obj.updated_at.strftime("%Y-%m-%d %H:%M"))

    class Meta:
        model = Role
        fields = ("id", "name", "created_at", "updated_at")
        load_instance = True
        # include_fk = True


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
