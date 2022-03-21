import asyncio
from dataclasses import dataclass
from http.client import HTTPResponse

import aiohttp
import pytest
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from multidict import CIMultiDictProxy

from app import app as test_app
from db import db
from models import Role, User, UserRole
from tests.functional.settings import Settings
from utils import constants
import requests_mock

@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_request(session):
    dispatcher: dict = {
        "get": session.get,
        "post": session.post,
        "patch": session.patch,
        "put": session.put,
        "delete": session.delete,
    }

    async def inner(
        http_method: str,
        data=None,
        headers: str = None,
        endpoint: str = None,
    ) -> HTTPResponse:
        """
        :param headers: str
            Дополнительные headers внутри запроса
        :param http_method: str
            HTTP метод который будет использован
        :param endpoint: str
            Путь до нашего конечного url
        :param data: Optional[dict]
            Тело запроса
        :return: HTTPResponse
        """
        if data is None:
            data = {}
        async with dispatcher.get(http_method)(
            url=f"{Settings.SERVICE_URL}{endpoint}",
            headers=headers,
            json=data,
        ) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture(scope="function", autouse=True)
def app():
    JWTManager(test_app)
    db.init_app(app=test_app)

    test_username: str = "UserTestUser"
    test_email: str = "UserTestUser@mail.ru"
    test_password: str = "CoolPassword!1!"

    with test_app.app_context():
        yield test_app
        db.session.commit()
        db.session.remove()
        db.drop_all()
        db.create_all()
        user = User(username=test_username, email=test_email)
        user.set_password(password=test_password)
        user.save_to_db()

        if not Role.by_name_exist(role_name=constants.DEFAULT_ROLE_FOR_ALL_USERS):
            new_role = Role(name=constants.DEFAULT_ROLE_FOR_ALL_USERS)
            new_role.save_to_db()
            new_user_role = UserRole(user_id=user.id, role_id=new_role.id)
            new_user_role.save_to_db()

        if not Role.by_name_exist(role_name=constants.ROLE_FOR_ADMIN):
            new_role_2 = Role(name=constants.ROLE_FOR_ADMIN)
            new_role_2.save_to_db()
            new_user_role_2 = UserRole(user_id=user.id, role_id=new_role_2.id)
            new_user_role_2.save_to_db()


@pytest.fixture
async def user():
    test_username: str = "Test_243f"
    test_email: str = "Test_243f@mail.ru"
    test_password: str = "Test!12345"

    user = User(username=test_username, email=test_email)
    user.set_password(password=test_password)
    user.save_to_db()
    yield user


@pytest.fixture
async def access_token(user) -> dict:
    return {"Authorization": f"Bearer {create_access_token(identity=user.id)}"}


@pytest.fixture
async def refresh_token(user) -> dict:
    return {"Authorization": f"Bearer {create_refresh_token(identity=user.id)}"}


@pytest.fixture
async def get_role_id(make_request, access_token) -> str:
    response_list = await make_request(
        endpoint="/role/", http_method="get", headers=access_token
    )
    return response_list.body.get("data")[0].get("roles")[0].get("id")
