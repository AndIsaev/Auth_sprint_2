import http

from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort, reqparse

from core.permissions import is_admin_permissions
from db import db
from models import Role
from utils.decorators import api_response_wrapper

parser = reqparse.RequestParser()
parser.add_argument(
    "name", trim=True, type=str, help="This field cannot be blank", required=True
)


def return_or_abort_if_role_not_exist(role_id: str) -> Role:
    role = Role.find_by_role_id(role_id=role_id)
    if not role:
        message: dict = {"message": f"Role '{role_id}' doesn't exist"}
        abort(http_status_code=http.HTTPStatus.NOT_FOUND, message=message)
    return role


class RoleDetail(Resource):
    @api_response_wrapper()
    @jwt_required()
    def get(self, role_id):
        """
        Return detail of specific role by role_id
        ---
        tags:
          - role
        parameters:
          - in: path
            name: role_id
            required: true
            description: The ID of user's role
            type: string
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
          401:
            description: Authorization error response
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
                description:
                  type: string
                  description: Response description
                message:
                  type: string
                  description: Response message
        """
        from schemas.role import role_schema

        role = return_or_abort_if_role_not_exist(role_id=role_id)
        return role_schema.dump(role), http.HTTPStatus.OK

    @api_response_wrapper()
    @jwt_required()
    @is_admin_permissions()
    def patch(self, role_id):
        """
        Update data of specific role by role_id
        ---
        tags:
          - role
        parameters:
          - in: path
            name: role_id
            required: true
            description: The ID of user's role
            type: string
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

        new_name: str = parser.parse_args().get("name")
        if Role.by_name_exist(role_name=new_name):
            return {
                "message": f"Role '{role_id}' already exist"
            }, http.HTTPStatus.BAD_REQUEST
        else:
            role = return_or_abort_if_role_not_exist(role_id=role_id)
            role.name = new_name
            role.save_to_db()
            return role_schema.dump(role), http.HTTPStatus.OK

    @api_response_wrapper()
    @jwt_required()
    @is_admin_permissions()
    def delete(self, role_id: str):
        """
        Delete specific role by role_id
        ---
        tags:
          - role
        parameters:
          - in: path
            name: role_id
            required: true
            description: The ID of user's role
            type: string
        responses:
          202:
            description: The Role deleted
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
                message:
                  type: string
                  description: Response message
        """
        role = return_or_abort_if_role_not_exist(role_id=role_id)
        if role:
            db.session.delete(role)
            db.session.commit()
        return {
            "message": f"Role '{role_id}' has been deleted"
        }, http.HTTPStatus.ACCEPTED
