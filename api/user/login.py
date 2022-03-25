import http

from flask import request
from flask_restful import Resource, reqparse

from models import User
from utils.decorators import api_response_wrapper
from utils.rate_limit import rate_limit

from .login_service import generate_jwt_tokens


parser = reqparse.RequestParser()
parser.add_argument("email", help="This field cannot be blank", required=True)
parser.add_argument("password", help="This field cannot be blank", required=True)


class UserLogin(Resource):
    @rate_limit()
    @api_response_wrapper()
    def post(self):
        """
        Login method for users
        ---
        tags:
          - user
        parameters:
          - in: body
            name: body
            schema:
              id: UserLogin
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  description: The user's email.
                  default: "JohnDoe@mail.ru"
                password:
                  type: string
                  description: The user's password.
                  default: "Qwerty123"
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
                      access_token:
                        type: string
                      refresh_token:
                        type: string
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
                message:
                  type: string
                  description: Response message
          429:
            description: Too many requests. Limit in interval seconds.
        """
        data = parser.parse_args()
        email: str = data.get("email")
        current_user = User.find_by_email(email=email)
        if not current_user:
            return {"message": f"User {email} doesn't exist"}, http.HTTPStatus.NOT_FOUND

        if current_user.check_password(password=data.get("password")):
            jwt_tokens: dict[str, str] = generate_jwt_tokens(
                current_user=current_user, request=request
            )
            return {
                "message": f"Logged in as {current_user.username}",
                "access_token": jwt_tokens.get("access_token"),
                "refresh_token": jwt_tokens.get("refresh_token"),
            }, http.HTTPStatus.OK
        return {"message": "Wrong credentials"}, http.HTTPStatus.BAD_REQUEST
