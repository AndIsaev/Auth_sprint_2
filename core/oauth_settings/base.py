import json
import os

from dotenv import load_dotenv
from flask import redirect, request, session, url_for

from app import oauth

load_dotenv()

OAUTH_CREDENTIALS: dict[str, dict[str, str]] = {
    "facebook": {
        "id": os.getenv("FACEBOOK_APP_ID"),
        "secret": os.getenv("FACEBOOK_APP_SECRET"),
    },
    "twitter": {
        "id": os.getenv("FACEBOOK_APP_ID"),
        "secret": os.getenv("FACEBOOK_APP_ID"),
    },
    "vk": {"id": os.getenv("VK_ID"), "secret": os.getenv("VK_SECRET")},
    "yandex": {"id": os.getenv("YANDEX_ID"), "secret": os.getenv("YANDEX_SECRET")},
    "mail": {
        "id": os.getenv("FACEBOOK_APP_ID"),
        "secret": os.getenv("FACEBOOK_APP_ID"),
    },
    "google": {
        "id": os.getenv("GOOGLE_CLIENT_ID"),
        "secret": os.getenv("GOOGLE_CLIENT_SECRET"),
    },
}


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name: str):
        self.provider_name: str = provider_name
        credentials: dict[str, str] = OAUTH_CREDENTIALS.get(provider_name)
        self.client_id: str = credentials.get("id")
        self.client_secret: str = credentials.get("secret")

    def get_redirect_url(self):
        pass

    def get_profile_data(self):
        pass

    @classmethod
    def get_provider(cls, provider_name: str):
        if not cls.providers:
            cls.providers: dict[str, object] = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers.get(provider_name)


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__(provider_name="facebook")
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token_url="https://graph.facebook.com/oauth/access_token",
            access_token_params=None,
            authorize_url="https://www.facebook.com/dialog/oauth",
            authorize_params=None,
            api_base_url="https://graph.facebook.com/",
            client_kwargs={"scope": "email"},
        )

    def get_redirect_url(self) -> str:
        redirect_uri: str = url_for(
            "provider_auth", _external=True, provider=self.provider_name
        )
        return self.service.authorize_redirect(redirect_uri=redirect_uri)

    def get_profile_data(self):
        token = self.service.authorize_access_token()
        resp = self.service.get(
            "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
        )
        return resp.json()


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__(provider_name="google")
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )

    def get_redirect_url(self) -> str:
        redirect_uri: str = url_for(
            "provider_auth", _external=True, provider=self.provider_name
        )
        return self.service.authorize_redirect(redirect_uri=redirect_uri)

    def get_profile_data(self):
        token = self.service.authorize_access_token()
        user = self.service.parse_id_token(token=token)
        return user


class VKSignIn(OAuthSignIn):
    def __init__(self):
        super(VKSignIn, self).__init__(provider_name="vk")
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token_params=None,
            authorize_url="https://oauth.vk.com/authorize",
            authorize_params=None,
            display='page',
            response_type="code",
            # client_kwargs={"scope": "email"},
            scope='email',
            base_url='https://api.vk.com/method/',
            request_token_url=None,
            access_token_url='https://oauth.vk.com/access_token',
        )

    def get_redirect_url(self) -> str:
        redirect_uri: str = url_for(
            "provider_auth", _external=True, provider=self.provider_name
        )
        return self.service.authorize_redirect(redirect_uri=redirect_uri)

    def get_profile_data(self):

        # resp = self.service.get(
        #     "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
        # )
        # print(resp.json())
        return 'test'


class SignIn(OAuthSignIn):
    def __init__(self):
        super(VKSignIn, self).__init__(provider_name="vk")
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token_params=None,
            authorize_url="https://oauth.vk.com/authorize",
            authorize_params=None,
            display='page',
            response_type="code",
            # client_kwargs={"scope": "email"},
            scope='email',
            base_url='https://api.vk.com/method/',
            request_token_url=None,
            access_token_url='https://oauth.vk.com/access_token',
        )

    def get_redirect_url(self) -> str:
        redirect_uri: str = url_for(
            "provider_auth", _external=True, provider=self.provider_name
        )
        return self.service.authorize_redirect(redirect_uri=redirect_uri)

    def get_profile_data(self):

        # resp = self.service.get(
        #     "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
        # )
        # print(resp.json())
        return 'test'


# class TwitterSignIn(OAuthSignIn):
#     def __init__(self):
#         super(TwitterSignIn, self).__init__("twitter")
#         self.service = oauth.remote_app(
#             name="twitter",
#             consumer_key=self.consumer_id,
#             consumer_secret=self.consumer_secret,
#             request_token_url="https://api.twitter.com/oauth/request_token",
#             access_token_url="https://api.twitter.com/oauth/access_token",
#             authorize_url="https://api.twitter.com/oauth/authenticate",
#             base_url="https://api.twitter.com/1/",
#         )
#
#     def authorize(self):
#         request_token = self.service.get_request_token(
#             params={"oauth_callback": self.get_callback_url()}
#         )
#         session["request_token"] = request_token
#         return redirect(self.service.get_authorize_url(request_token[0]))
#
#     def callback(self):
#         request_token = session.pop("request_token")
#         if "oauth_verifier" not in request.args:
#             return None, None, None
#         oauth_session = self.service.get_auth_session(
#             request_token[0],
#             request_token[1],
#             data={"oauth_verifier": request.args["oauth_verifier"]},
#         )
#         me = oauth_session.get("account/verify_credentials.json").json()
#         social_id = "twitter$" + str(me.get("id"))
#         username = me.get("screen_name")
#         return social_id, username, None  # Twitter does not provide email
