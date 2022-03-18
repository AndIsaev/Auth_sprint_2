import http

from flask_restful import Resource, reqparse

from models import User
from utils.decorators import api_response_wrapper
from utils.rate_limit import rate_limit

from .registration_service import create_new_user

parser = reqparse.RequestParser()
parser.add_argument(
    "username", type=str, help="This field cannot be blank", required=True, trim=True
)
parser.add_argument(
    "password", type=str, help="This field cannot be blank", required=True, trim=True
)
parser.add_argument(
    "email", type=str, help="This field cannot be blank", required=True, trim=True
)
parser.add_argument(
    "password_confirm",
    type=str,
    help="This field cannot be blank",
    required=True,
    trim=True,
)


class UserRegistration(Resource):
    @rate_limit()
    @api_response_wrapper()
    def post(self):
        """
        Registration method for users
        ---
        tags:
          - user
        parameters:
          - in: body
            name: body
            schema:
              id: UserRegistration
              required:
                - username
                - email
                - password
                - password_confirm
              properties:
                username:
                  type: string
                  description: The user's username.
                  default: "JohnDoe"
                email:
                  type: string
                  description: The user's email.
                  default: "mail@mail.ru"
                password:
                  type: string
                  description: The user's password.
                  default: "Qwerty123"
                password_confirm:
                  type: string
                  description: Password confirmation
                  default: "Qwerty123"
        responses:
          201:
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
        username: str = data.get("username")
        email: str = data.get("email")
        password: str = data.get("password")
        password_confirm: str = data.get("password_confirm")
        """ check username in DB """
        if User.find_by_username(username=username):
            return {
                "message": "wrong data",
                "errors": [
                    {"username": f"User {username} already exists"},
                ],
            }, http.HTTPStatus.BAD_REQUEST
        """ check email in DB """
        if User.find_by_email(email=email):
            return {
                "message": "wrong data",
                "errors": [
                    {"username": f"User's email {email} already exists"},
                ],
            }, http.HTTPStatus.BAD_REQUEST
        """ check that passwords are equal """
        if password != password_confirm:
            return {
                "message": "wrong data",
                "errors": [
                    {"password": "passwords are not equal"},
                    {"password_confirm": "passwords are not equal"},
                ],
            }, http.HTTPStatus.BAD_REQUEST
        create_new_user(username=username, email=email, password=password)
        return {"message": f"User {username} was created"}, http.HTTPStatus.CREATED
