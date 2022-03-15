import os

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
        self.service = None

    def get_redirect_url(self) -> str:
        print(self.service)
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
            authorize_url="https://oauth.vk.com/authorize",
            # display="page",
            # response_type="code",
            scope="email",
            base_url="https://api.vk.com/method/",
            # access_token_url="https://oauth.vk.com/access_token",
        )

    def get_profile_data(self, request=None):
        code: str = request.args.get("code")
        print(code)
        """ authorize in mail """
        vk_response = requests.get(
            url="https://oauth.vk.com/access_token",
            params={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": "http://localhost:5000/auth/vk",
                "fields": "email",
                "code": code,
            },
        )
        print(vk_response.json())
        email: str = vk_response.json().get("email")
        user_id: int = vk_response.json().get("user_id")
        """ get user's info """
        # user_info_response = requests.get(
        #     url="https://api.vk.com/method/users.get", params={
        #         "user_id": user_id,
        #         "access_token": access_token,
        #         "fields": "email",
        #         "v": 5.131
        #     }
        # )
        # print(user_info_response.json())
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
            response_type="code",
            scope="userinfo",
        )

    def get_profile_data(self, request=None):
        code: str = request.args.get("code")
        print(code)
        """ authorize in mail """
        mail_response = requests.post(
            url="https://oauth.mail.ru/token",
            params={"client_id": self.client_id, "client_secret": self.client_secret},
            data={
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:5000/auth/mail",
            },
        )
        access_token: str = mail_response.json().get("access_token")
        print(access_token)
        """ get user's info """
        user_info_response = requests.get(
            url="https://oauth.mail.ru/userinfo", params={"access_token": access_token}
        )
        print(user_info_response.json())
        """ example data """
        demo_data: dict = {
            "nickname": "Бернар Бердикул",
            "client_id": "7e5f4707292443fca607873f9f545752",
            "id": "1734604429",
            "image": "https://filin.mail.ru/pic?d=-B4YYVzU7KpFhQxz0p1xQ2jGf2hc-VbER21vH7dV-OQteB3PDmmLxgU2MIzWIeJducomlZY~&width=180&height=180",
            "first_name": "Бернар",
            "email": "bernar.berdikul@mail.ru",
            "locale": "ru_RU",
            "name": "Бернар Бердикул",
            "last_name": "Бердикул",
            "birthday": "22.04.2000",
            "gender": "m",
        }

        # resp = self.service.get(
        #     "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
        # )
        # print(resp.json())
        return "test"


class YandexSignIn(OAuthSignIn):
    def __init__(self):
        super(YandexSignIn, self).__init__(provider_name="yandex")
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token_params=None,
            authorize_url="https://oauth.yandex.ru/authorize",
            authorize_params=None,
            response_type="code",
            display="popup",
            scope="login:email",
        )

    def get_profile_data(self, request=None):
        code: str = request.args.get("code")
        print(code)
        return "test"
