import http

import pytest

pytestmark = pytest.mark.asyncio


async def test_success_change_password(make_request, access_token):
    response = await make_request(
        endpoint="/change_password",
        http_method="post",
        headers=access_token,
        data={
            "current_password": "Test!12345",
            "password": "Tesla!123!",
            "password_confirm": "Tesla!123!",
        },
    )
    assert response.status == http.HTTPStatus.OK
    assert response.body.get("message") == "Successful password change by the user"


async def test_unsuccessful_change_change_password(make_request, access_token):
    response = await make_request(
        endpoint="/change_password",
        http_method="post",
        headers=access_token,
        data={
            "current_password": "Test!12345",
            "password": "Tesla!123!",
            "password_confirm": "Tesla!1234!",
        },
    )
    assert response.status == http.HTTPStatus.BAD_REQUEST
    assert response.body.get("errors")[0].get("password") == "passwords are not equal"
