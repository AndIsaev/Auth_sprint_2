from flask import Blueprint
from flask_restful import Api

api_bp_user_role = Blueprint("user_role", __name__)
api = Api(api_bp_user_role)

from . import routes
