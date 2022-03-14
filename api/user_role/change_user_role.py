from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from core.permissions import is_admin_permissions
from models import UserRole
from utils.decorators import api_response_wrapper

parser = reqparse.RequestParser()
parser.add_argument(
    "user_id", trim=True, type=str, help="send correct id", required=True
)
parser.add_argument(
    "role_id", trim=True, type=str, help="send correct id", required=True
)


class ChangeUserRole(Resource):
    @api_response_wrapper()
    @jwt_required()
    @is_admin_permissions()
    def post(self):
        """
        Create user's role for specific user
        ---
        tags:
          - user_role
        parameters:
          - in: body
            name: body
            schema:
              id: UserRole
              required:
                - user_id
                - role_id
              properties:
                user_id:
                  type: string
                  description: The user's id.
                  default: 28b28c98-926b-45aa-826c-5ea495ecbfa5
                role_id:
                  type: string
                  description: The role's id.
                  default: 6e14280c-48fe-4bf9-94c0-94083e9eec55
        responses:
          200:
            description: The User's role created
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: True
                data:
                  type: array
                  description: Response data
                  items:
                      type: object
                  default: []
        """
        data = parser.parse_args()
        user_id: str = data.get("user_id")
        role_id: str = data.get("role_id")
        if not UserRole.is_row_exist(user_id=user_id, role_id=role_id):
            new_user_role = UserRole(user_id=user_id, role_id=role_id)
            new_user_role.save_to_db()
        return {}
