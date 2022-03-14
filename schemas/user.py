from app import ma
from models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "username")
        model = User
        load_instance = True
        # include_fk = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)
