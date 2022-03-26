from flask import Blueprint
from flask_restful import Api

api_bp_user = Blueprint("user", __name__)
api = Api(api_bp_user)

from . import routes
