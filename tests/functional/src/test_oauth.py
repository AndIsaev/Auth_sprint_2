import http

import pytest

from core.oauth_service import register_social_account

pytestmark = pytest.mark.asyncio


async def test_api():
    email: str = "test@gmail.com"
    username: str = "baltazar"
    data, code = register_social_account(
        social_name="facebook", social_id="7777777", email=email, username=username
    )
    assert data.get("message") == f"Logged in as {username} - {email}"
    assert type(data.get("access_token")) == str
    assert code == http.HTTPStatus.OK
