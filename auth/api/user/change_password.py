import http

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from db import db
from models import User
from utils.decorators import api_response_wrapper
from utils.rate_limit import rate_limit

parser = reqparse.RequestParser()
parser.add_argument(
    "current_password", help="This field cannot be blank", required=True
)
parser.add_argument("password", help="This field cannot be blank", required=True)
parser.add_argument(
    "password_confirm", help="This field cannot be blank", required=True
)


class ChangePassword(Resource):
    @rate_limit()
    @api_response_wrapper()
    @jwt_required()
    def post(self):
        """
        Change password method for users
        ---
        tags:
          - user
        parameters:
          - in: body
            name: body
            schema:
              id: ChangePassword
              required:
                - current_password
                - password
                - password_confirm
              properties:
                current_password:
                  type: string
                  desctription: The user's current password
                  default: "Qwerty123"
                password:
                  type: string
                  description: The user's password.
                  default: "Qwerty_updated123"
                password_confirm:
                  type: string
                  description: Password confirmation
                  default: "Qwerty_updated123"
        responses:
          200:
            description: Message that user was created
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
                    default: ...
                  default: []
                message:
                  type: string
                  description: Response message
          400:
            description: Bad request response
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
                errors:
                  type: array
                  description: Data with error validation messages
                  items:
                    type: object
                    default: ...
                  default: []
                message:
                  type: string
                  description: Response message
          429:
            description: Too many requests. Limit in interval seconds.
        """
        data = parser.parse_args()
        current_password: str = data.get("current_password")
        password: str = data.get("password")
        password_confirm: str = data.get("password_confirm")
        # check that current password and new password not equal
        if current_password == password:
            return {
                "message": "wrong data",
                "errors": [
                    {"current_password": "passwords are equal"},
                    {"password": "passwords are equal"},
                ],
            }, http.HTTPStatus.BAD_REQUEST
        # check that passwords are equal
        if password != password_confirm:
            return {
                "message": "wrong data",
                "errors": [
                    {"password": "passwords are not equal"},
                    {"password_confirm": "passwords are not equal"},
                ],
            }, http.HTTPStatus.BAD_REQUEST
        # get current user
        current_user = User.query.filter_by(id=get_jwt_identity()).first()
        # compair current_password with password in DB
        if not current_user.check_password(password=current_password):
            return {
                "message": "wrong data",
                "errors": [
                    {"current_password": "incorrect password"},
                ],
            }, http.HTTPStatus.BAD_REQUEST
        try:
            current_user.set_password(password=password)
            current_user.save_to_db()
            return {
                "message": "Successful password change by the user"
            }, http.HTTPStatus.OK
        except Exception:
            db.session.rollback()
            return {"message": "Something went wrong"}, http.HTTPStatus.BAD_REQUEST
