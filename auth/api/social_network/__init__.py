from flask import Blueprint
from flask_restful import Api

api_bp_role = Blueprint("role", __name__)
api = Api(api_bp_role)

from . import routes