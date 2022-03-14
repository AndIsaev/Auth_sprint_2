import http

from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from core import config
from db import cache, db
from models.auth_models import User
from utils import codes
from utils.decorators import api_response_wrapper

parser = reqparse.RequestParser()
parser.add_argument(
    "username", type=str, help="This field cannot be blank", trim=True, required=True
)


class Profile(Resource):
    @api_response_wrapper()
    @jwt_required()
    def get(self):
        """
        Get own profile method for users
        ---
        tags:
          - profile
        responses:
          200:
            description: Success user's login
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
                      username:
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
        """
        from schemas.user import user_schema

        user_id: str = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user_schema.dump(user), http.HTTPStatus.OK
        return {"message": codes.OBJECT_NOT_FOUND}, http.HTTPStatus.NOT_FOUND

    @api_response_wrapper()
    @jwt_required()
    def patch(self):
        """
        Update profile method for users
        ---
        tags:
          - profile
        parameters:
          - in: body
            name: body
            schema:
              id: Profile
              required:
                - username
              properties:
                username:
                  type: string
                  description: The user's username.
                  default: "JohnDoe"
        responses:
          200:
            description: Success user's login
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
                      username:
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
        """
        from schemas.user import user_schema

        data = parser.parse_args()
        user_id: str = get_jwt_identity()
        new_username: str = data.get("username")
        if not new_username:
            return {
                "message": "Something went wrong",
                "username": "This field cannot be blank",
            }, http.HTTPStatus.BAD_REQUEST
        try:
            profile = User.query.filter_by(id=user_id).first()
            profile.username = new_username
            profile.save_to_db()
            return user_schema.dump(profile), http.HTTPStatus.OK
        except Exception:
            db.session.rollback()
            return {"message": "Something went wrong"}, http.HTTPStatus.BAD_REQUEST

    @api_response_wrapper()
    @jwt_required()
    def delete(self):
        """
        Delete profile method for users
        ---
        tags:
          - profile
        responses:
          200:
            description: Successfully deletion user
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: True
                message:
                  type: string
                  description: Response message
          400:
            description: Unsuccessfully deletion user
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: False
                message:
                  type: string
                  description: Response message
        """
        jti: str = get_jwt().get("jti")
        user_id: str = get_jwt_identity()
        try:
            profile = User.query.filter_by(id=user_id).first()
            db.session.delete(profile)
            db.session.commit()
            """ revoke token """
            cache.add_token(
                key=jti, expire=config.JWT_ACCESS_TOKEN_EXPIRES, value=user_id
            )
            return {"message": "success deleted"}, http.HTTPStatus.OK
        except Exception:
            db.session.rollback()
            return {"message": "Something went wrong"}, http.HTTPStatus.BAD_REQUEST


class GetSuccessHistory(Resource):
    @api_response_wrapper()
    @jwt_required()
    def get(self) -> tuple[dict[str, str], int]:
        """
        Return list of user's login history
        ---
        tags:
          - profile
        responses:
          200:
            description: Success user's login
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
                    type: string
        """
        from schemas.history import history_schema
        from models.auth_models import SuccessHistory
        user_id: str = get_jwt_identity()
        history = SuccessHistory.query.filter_by(user_id=user_id)
        return {"history": history_schema.dump(history)}, http.HTTPStatus.OK
        # return pagination.paginate(SuccessHistory, history_schema)
