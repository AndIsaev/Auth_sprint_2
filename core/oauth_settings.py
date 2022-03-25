import os

import requests
from dotenv import load_dotenv
from flask import url_for

from app import oauth
from utils.constants import OAUTH_SERVICES
from utils.decorators import remote_oauth_api_error_handler

from .oauth_service import register_social_account

load_dotenv()


OAUTH_CREDENTIALS: dict[str, dict[str, str]] = {
    "facebook": {
        "id": os.getenv("FACEBOOK_APP_ID"),
        "secret": os.getenv("FACEBOOK_APP_SECRET"),
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
        self.service = None

    def get_redirect_url(self) -> str:
        redirect_uri: str = url_for(
            "provider_auth", _external=True, provider=self.provider_name
        )
        return self.service.authorize_redirect(redirect_uri=redirect_uri)

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
        super(FacebookSignIn, self).__init__(provider_name=OAUTH_SERVICES.facebook)
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token_url=os.getenv("FACEBOOK_ACCESS_TOKEN_URL"),
            authorize_url=os.getenv("FACEBOOK_AUTHORIZE_URL"),
            api_base_url=os.getenv("FACEBOOK_API_BASE_URL"),
            client_kwargs={"scope": "email"},
        )

    @remote_oauth_api_error_handler
    def get_profile_data(self, request=None):
        token = self.service.authorize_access_token()
        user_info_response = self.service.get(os.getenv("FACEBOOK_PROFILE_URL")).json()
        # get user's info
        social_id: str = user_info_response.get("id")
        email: str = user_info_response.get("email")
        username: str = user_info_response.get("name")
        return register_social_account(
            request=request,
            social_name=self.provider_name,
            social_id=social_id,
            email=email,
            username=username,
        )


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__(provider_name=OAUTH_SERVICES.google)
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            server_metadata_url=os.getenv("GOOGLE_SERVER_METADATA_URL"),
            client_kwargs={"scope": "openid email profile"},
        )

    @remote_oauth_api_error_handler
    def get_profile_data(self, request=None):
        token = self.service.authorize_access_token()
        user_info_response = self.service.parse_id_token(token=token)
        # get user's info
        social_id: str = user_info_response.get("sub")
        email: str = user_info_response.get("email")
        username: str = user_info_response.get("name")
        return register_social_account(
            request=request,
            social_name=self.provider_name,
            social_id=social_id,
            email=email,
            username=username,
        )


class VKSignIn(OAuthSignIn):
    def __init__(self):
        super(VKSignIn, self).__init__(provider_name=OAUTH_SERVICES.vk)
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorize_url=os.getenv("VK_AUTHORIZE_URL"),
            scope="email",
            base_url=os.getenv("VK_API_BASE_URL"),
        )

    @remote_oauth_api_error_handler
    def get_profile_data(self, request=None):
        code: str = request.args.get("code")
        # authorize in vk
        vk_response = requests.get(
            url=os.getenv("VK_ACCESS_TOKEN_URL"),
            params={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": os.getenv("VK_REDIRECT_URI"),
                "fields": "email",
                "code": code,
            },
        ).json()
        # get user's info
        social_id: str = f"{vk_response.get('user_id')}"
        email: str = vk_response.get("email")
        username: str = f"{self.provider_name}-{social_id}"
        return register_social_account(
            request=request,
            social_name=self.provider_name,
            social_id=social_id,
            email=email,
            username=username,
        )


class MailSignIn(OAuthSignIn):
    def __init__(self):
        super(MailSignIn, self).__init__(provider_name=OAUTH_SERVICES.mail)
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorize_url=os.getenv("MAIL_AUTHORIZE_URL"),
            response_type="code",
            scope="userinfo",
        )

    @remote_oauth_api_error_handler
    def get_profile_data(self, request=None):
        code: str = request.args.get("code")
        # authorize in mail
        mail_response = requests.post(
            url=os.getenv("MAIL_TOKEN_URL"),
            params={"client_id": self.client_id, "client_secret": self.client_secret},
            data={
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": os.getenv("MAIL_REDIRECT_URI"),
            },
        ).json()
        access_token: str = mail_response.get("access_token")
        user_info_response = requests.get(
            url=os.getenv("MAIL_PROFILE_URL"), params={"access_token": access_token}
        ).json()
        # get user's info
        social_id: str = user_info_response.get("id")
        email: str = user_info_response.get("email")
        username: str = user_info_response.get("nickname")
        return register_social_account(
            request=request,
            social_name=self.provider_name,
            social_id=social_id,
            email=email,
            username=username,
        )


class YandexSignIn(OAuthSignIn):
    def __init__(self):
        super(YandexSignIn, self).__init__(provider_name=OAUTH_SERVICES.yandex)
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorize_url=os.getenv("YANDEX_AUTHORIZE_URL"),
            response_type="code",
            display="popup",
            scope="login:info login:email",
        )

    @remote_oauth_api_error_handler
    def get_profile_data(self, request=None):
        code: str = request.args.get("code")
        # authorize in yandex
        yandex_response = requests.post(
            url=os.getenv("YANDEX_TOKEN_URL"),
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
            },
        ).json()
        access_token: str = yandex_response.get("access_token")
        user_info_response = requests.get(
            url=os.getenv("YANDEX_PROFILE_URL"),
            params={
                "format": "json",
                "with_openid_identity": 1,
                "oauth_token": access_token,
            },
        ).json()
        # get user's info
        social_id: str = user_info_response.get("id")
        email: str = user_info_response.get("default_email")
        username: str = user_info_response.get("login")
        return register_social_account(
            request=request,
            social_name=self.provider_name,
            social_id=social_id,
            email=email,
            username=username,
        )
