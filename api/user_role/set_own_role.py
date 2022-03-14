import http

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from core import config
from models import UserRole
from utils.decorators import api_response_wrapper

parser = reqparse.RequestParser()
parser.add_argument(
    "role_id", trim=True, type=str, help="send correct id", required=True
)


# TODO: DELETE IT, not for production
class SetOwnUserRole(Resource):
    """For debug method to get role"""

    @api_response_wrapper()
    @jwt_required()
    def post(self):
        if config.TESTING:
            data = parser.parse_args()
            user_id: str = get_jwt_identity()
            role_id: str = data.get("role_id")
            if not UserRole.is_row_exist(user_id=user_id, role_id=role_id):
                new_user_role = UserRole(user_id=user_id, role_id=role_id)
                new_user_role.save_to_db()
            return {"success": True}, http.HTTPStatus.OK
        return {}, http.HTTPStatus.FORBIDDEN
