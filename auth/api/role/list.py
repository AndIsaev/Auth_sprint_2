from flask_restful import Resource

from models import Role
from utils.decorators import api_response_wrapper
from utils.rate_limit import rate_limit


class RoleList(Resource):
    @rate_limit()
    @api_response_wrapper()
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
          429:
            description: Too many requests. Limit in interval seconds.
        """
        from schemas.role import roles_schema

        return {"roles": roles_schema.dump(Role.query.all())}
