import http

import pytest

pytestmark = pytest.mark.asyncio


async def test_success_registration(make_request, access_token):
    response = await make_request(
        endpoint="/registration",
        http_method="post",
        headers=access_token,
        data={
            "username": "UserTestUser_1",
            "password": "CoolPassword!1!",
            "password_confirm": "CoolPassword!1!",
        },
    )
    assert response.status == http.HTTPStatus.CREATED


async def test_success_login(make_request):
    response = await make_request(
        endpoint="/login",
        http_method="post",
        data={
            "username": "UserTestUser",
            "password": "CoolPassword!1!",
        },
    )
    assert response.status == http.HTTPStatus.OK
    access_token = response.body.get("data")[0].get("access_token")
    response = await make_request(
        endpoint="/access_history",
        http_method="get",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status == http.HTTPStatus.OK
    assert len(response.body.get("data")) == 1


async def test_logout_access_login(make_request, access_token):
    response = await make_request(
        endpoint="/logout/access", http_method="post", headers=access_token
    )
    assert response.status == http.HTTPStatus.OK


async def test_logout_refresh_login(make_request, refresh_token):
    response = await make_request(
        endpoint="/logout/refresh", http_method="post", headers=refresh_token
    )
    assert response.status == http.HTTPStatus.OK
