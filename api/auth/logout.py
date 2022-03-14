import http

from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource

from core import config
from db import cache
from utils.decorators import api_response_wrapper


class UserLogoutAccess(Resource):
    @api_response_wrapper()
    @jwt_required()
    def post(self):
        """
        Logout access token method for users
        ---
        tags:
          - user
        responses:
          200:
            description: Success user's logout access token
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
        jti: str = get_jwt().get("jti")
        user_id: str = get_jwt_identity()
        try:
            cache.add_token(
                key=jti, expire=config.JWT_ACCESS_TOKEN_EXPIRES, value=user_id
            )
            return {"message": "Access token has been revoked"}, http.HTTPStatus.OK
        except Exception:
            return {"message": "Something went wrong"}, http.HTTPStatus.BAD_REQUEST


class UserLogoutRefresh(Resource):
    @api_response_wrapper()
    @jwt_required(refresh=True)
    def post(self):
        """
        Logout refresh token method for users
        ---
        tags:
          - user
        responses:
          200:
            description: Success user's logout refresh token
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
        jti: str = get_jwt().get("jti")
        try:
            cache.delete_token(key=jti)
            return {"message": "Refresh token has been revoked"}, http.HTTPStatus.OK
        except Exception:
            return {"message": "Something went wrong"}, http.HTTPStatus.BAD_REQUEST
