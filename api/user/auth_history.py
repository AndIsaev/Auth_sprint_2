import http

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from models import SuccessHistory
from schemas.history import history_schema
from utils.decorators import api_response_wrapper
from utils.rate_limit import rate_limit


class AuthHistory(Resource):
    @rate_limit()
    @api_response_wrapper()
    @jwt_required()
    def get(self) -> tuple[dict[str, str], int]:
        """
        Return list of user's login history
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
                    type: string
          429:
            description: Too many requests. Limit in interval seconds.
        """
        user_id: str = get_jwt_identity()
        history = SuccessHistory.query.filter_by(user_id=user_id)
        return {"history": history_schema.dump(history)}, http.HTTPStatus.OK
        # return pagination.paginate(SuccessHistory, history_schema)
