from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models import Role
from utils.decorators import api_response_wrapper


class RoleList(Resource):
    @api_response_wrapper()
    @jwt_required()
    def get(self) -> dict:
        """
        Return list of user's roles
        ---
        tags:
          - role
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
                      roles:
                        type: array
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
                  default: []
                message:
                  type: string
                  description: Response message
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
                  description: Response data
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
        from schemas.role import roles_schema

        return {"roles": roles_schema.dump(Role.query.all())}
