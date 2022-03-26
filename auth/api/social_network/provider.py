from flask import request, Blueprint

from app import app
from utils.rate_limit import rate_limit

social_net = Blueprint('social_net', __name__)


@rate_limit()
@social_net.route("/login/<provider>/")
def provider_login(provider: str):
    """
    Retdirect user for internal oauth service of social network
    ---
    tags:
      - oauth
    parameters:
      - in: path
        name: provider
        required: true
        description: The social network's name
        type: string
    responses:
      302:
        description: Redirecting for oauth service of social network
      429:
        description: Too many requests. Limit in interval seconds.
    """
    from core.oauth_settings import OAuthSignIn

    provider_oauth = OAuthSignIn.get_provider(provider_name=provider)
    return provider_oauth.get_redirect_url()


@rate_limit()
@social_net.route("/auth/<provider>")
def provider_auth(provider: str):
    """
    Retdirect user for internal oauth service of social network
    ---
    tags:
      - oauth
    parameters:
      - in: path
        name: provider
        required: true
        description: The social network's name
        type: string
    responses:
      200:
        description: Redirecting for oauth service of social network
        schema:
          properties:
            success:
              type: boolean
              description: Response status
              default: True
            message:
              type: string
              description: Response message
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
              default: []
      429:
        description: Too many requests. Limit in interval seconds.
    """
    from core.oauth_settings import OAuthSignIn

    provider_oauth = OAuthSignIn.get_provider(provider_name=provider)
    return provider_oauth.get_profile_data(request=request)
