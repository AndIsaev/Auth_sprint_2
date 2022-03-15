import http

from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from core import config
from db import cache, db
from models import User
from utils import codes
from utils.decorators import api_response_wrapper
from utils.validators import email_validation, username_validation

parser = reqparse.RequestParser()
parser.add_argument(
    "username", type=str, help="This field cannot be blank", trim=True, required=False
)
parser.add_argument(
    "email", type=str, help="This field cannot be blank", trim=True, required=False
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
        new_email: str = data.get("email")
        """ Check if nothing need to update """
        if not new_username and not new_email:
            return {}, http.HTTPStatus.OK
        """ check values in database """
        if new_username and User.find_by_username(
            username=username_validation(value=new_username)
        ):
            return {
                "message": "Unique constraint",
                "username": "This username already in use",
            }, http.HTTPStatus.BAD_REQUEST
        if new_email and User.find_by_email(email=email_validation(value=new_email)):
            return {
                "message": "Unique constraint",
                "email": "This email already in use",
            }, http.HTTPStatus.BAD_REQUEST
        """ Try update profile """
        try:
            profile = User.query.filter_by(id=user_id).first()
            if new_username:
                profile.username = new_username
            if new_email:
                profile.email = new_email
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
