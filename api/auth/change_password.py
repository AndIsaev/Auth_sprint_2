import http

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from db import db
from models import User
from utils.decorators import api_response_wrapper

parser = reqparse.RequestParser()
parser.add_argument("password", help="This field cannot be blank", required=True)
parser.add_argument(
    "password_confirm", help="This field cannot be blank", required=True
)


class ChangePassword(Resource):
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
                - password
                - password_confirm
              properties:
                password:
                  type: string
                  description: The user's password.
                  default: "Qwerty123"
                password_confirm:
                  type: string
                  description: Password confirmation
                  default: "Qwerty123"
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
        """
        data = parser.parse_args()
        password: str = data.get("password")
        password_confirm: str = data.get("password_confirm")
        """ check that passwords are equal """
        if password != password_confirm:
            return {
                "message": "wrong data",
                "errors": [
                    {"password": "passwords are not equal"},
                    {"password_confirm": "passwords are not equal"},
                ],
            }, 400
        user_id: str = get_jwt_identity()
        try:
            current_user = User.query.filter_by(id=user_id).first()
            current_user.set_password(password=password)
            current_user.save_to_db()
            return {
                "message": "Successful password change by the user"
            }, http.HTTPStatus.OK
        except Exception:
            db.session.rollback()
            return {"message": "Something went wrong"}, http.HTTPStatus.BAD_REQUEST
