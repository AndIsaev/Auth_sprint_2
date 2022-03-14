from calendar import c
import os
from re import S

from requests.auth import HTTPBasicAuth
import requests

from dotenv import load_dotenv
from flask import url_for

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
        "id": os.getenv("MAIL_ID"),
        "secret": os.getenv("MAIL_SECRET"),
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

    def get_profile_data(self, request=None):
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

    def get_profile_data(self, request=None):
        token = self.service.authorize_access_token()
        resp = self.service.get(
            "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
        )
        user = resp.json()
        return user


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

    def get_profile_data(self, request=None):
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
            display="page",
            response_type="code",
            # client_kwargs={"scope": "email"},
            scope="email",
            base_url="https://api.vk.com/method/",
            request_token_url=None,
            access_token_url="https://oauth.vk.com/access_token",
        )

    def get_redirect_url(self) -> str:
        redirect_uri: str = url_for(
            "provider_auth", _external=True, provider=self.provider_name
        )
        return self.service.authorize_redirect(redirect_uri=redirect_uri)

    def get_profile_data(self, request=None):

        # resp = self.service.get(
        #     "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
        # )
        # print(resp.json())
        return "test"


class MailSignIn(OAuthSignIn):
    def __init__(self):
        super(MailSignIn, self).__init__(provider_name="mail")
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token_params=None,
            authorize_url="https://oauth.mail.ru/login",
            authorize_params=None,
            response_type="token",
            scope='userinfo',
        )

    def get_redirect_url(self) -> str:
        redirect_uri: str = url_for(
            "provider_auth", _external=True, provider=self.provider_name
        )
        print(redirect_uri)
        return self.service.authorize_redirect(redirect_uri=redirect_uri)

    def get_profile_data(self, request=None):
        # token = self.service.authorize_access_token()
        # print(token)
        print(request.data)
        print(request.args)
        code: str = request.args.get("code")
        print(code)
        """ authorize in mail """
        mail_response = requests.post(
            url="https://oauth.mail.ru/token",
            params={"client_id": self.client_id, "client_secret": self.client_secret},
            data={
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:5000/auth/mail"
            }
        )
        access_token: str = mail_response.json().get("access_token")
        print(access_token)
        """ get user's info """
        user_info_response = requests.get(
            url="https://oauth.mail.ru/userinfo",
            params={"access_token": access_token}
        )
        print(user_info_response.json())
        demo_data: dict = {'nickname': 'Бернар Бердикул', 'client_id': '7e5f4707292443fca607873f9f545752', 'id': '1734604429', 'image': 'https://filin.mail.ru/pic?d=-B4YYVzU7KpFhQxz0p1xQ2jGf2hc-VbER21vH7dV-OQteB3PDmmLxgU2MIzWIeJducomlZY~&width=180&height=180', 'first_name': 'Бернар', 'email': 'bernar.berdikul@mail.ru', 'locale': 'ru_RU', 'name': 'Бернар Бердикул', 'last_name': 'Бердикул', 'birthday': '22.04.2000', 'gender': 'm'}

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
