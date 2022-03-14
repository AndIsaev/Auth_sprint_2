from flask import Blueprint
from flask_restful import Api

api_bp_auth = Blueprint('auth', __name__)
api = Api(api_bp_auth)

from . import routes
