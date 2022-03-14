import http

import pytest

pytestmark = pytest.mark.asyncio


async def test_success_change_password(make_request, access_token):
    response = await make_request(
        endpoint="/change_password",
        http_method="post",
        headers=access_token,
        data={"password": "Tesla!123!", "password_confirm": "Tesla!123!"},
    )
    assert response.status == http.HTTPStatus.OK


async def test_unsuccessful_change_change_password(make_request, access_token):
    response = await make_request(
        endpoint="/change_password",
        http_method="post",
        headers=access_token,
        data={"password": "Tes"},
    )
    assert response.status == http.HTTPStatus.BAD_REQUEST
