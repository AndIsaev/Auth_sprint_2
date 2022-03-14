import http

from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from core.permissions import is_admin_permissions
from models import Role
from utils.decorators import api_response_wrapper

parser = reqparse.RequestParser()
parser.add_argument(
    "name", type=str, help="This field cannot be blank", required=True, trim=True
)


class RoleCreate(Resource):
    @api_response_wrapper()
    @jwt_required()
    @is_admin_permissions()
    def post(self):
        """
        Create new role in project
        ---
        tags:
          - role
        parameters:
          - in: body
            name: body
            schema:
              id: Role
              required:
                - name
              properties:
                name:
                  type: string
                  description: The role's name.
                  default: "super_admin"
        responses:
          200:
            description: The Role data
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
                      properties:
                        id:
                          type: string
                          default: a1c0eaa1-6255-40cc-83fc-1e33ed14f4c3
                        name:
                          type: string
                          default: simple_user
                        created_at:
                          type: string
                          default: 2022-02-27 14:12
                        updated_at:
                          type: string
                          default: 2022-02-27 14:12
                  default: []
          400:
            description: Bad request, already existed role name
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: False
                errors:
                  type: array
                  description: Data with error validation messages
                  items:
                    type: object
                    default: ...
                  default: []
                data:
                  type: array
                  description: Response data
                  items:
                    type: object
                    default: ...
                  default: []
                message:
                  type: string
                  description: Response message
        """
        from schemas.role import role_schema

        data = parser.parse_args()
        role_name: str = data.get("name")
        if not Role.by_name_exist(role_name=role_name):
            new_role = Role(name=role_name)
            new_role.save_to_db()
            return role_schema.dump(new_role), http.HTTPStatus.CREATED
        return {
            "message": "wrong data",
            "errors": [{"name": f"Role name <{role_name}> already exist"}],
        }, http.HTTPStatus.BAD_REQUEST
