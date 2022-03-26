import http

from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_restful import Resource

from db import cache
from models import UserRole
from utils.decorators import api_response_wrapper
from utils.rate_limit import rate_limit


class TokenRefresh(Resource):
    @rate_limit()
    @api_response_wrapper()
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh token method for users
        ---
        tags:
          - user
        responses:
          200:
            description: Success user's token refresh
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
                      access_token:
                        type: string
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
          429:
            description: Too many requests. Limit in interval seconds.
        """
        jti = get_jwt().get("jti")
        user_id: str = get_jwt_identity()
        # user's roles
        additional_claims: dict[str, list] = {
            "roles": [i.role.name for i in UserRole.query.filter_by(user_id=user_id)]
        }
        print(additional_claims)
        # new access token
        access_token: str = create_access_token(
            identity=user_id, additional_claims=additional_claims
        )
        if cache.is_jti_blacklisted(jti=jti):
            return {"access_token": access_token}, http.HTTPStatus.OK
        return {
            "success": False,
            "errors": [],
            "message": "token revoked",
            "description": "The refresh token has been revoked.",
        }, http.HTTPStatus.UNAUTHORIZED
