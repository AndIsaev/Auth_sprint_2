import http

import pytest

pytestmark = pytest.mark.asyncio


async def test_unauthorized_get_profile(make_request):
    response = await make_request(endpoint="/me/users", http_method="get")
    assert response.status == http.HTTPStatus.UNAUTHORIZED


async def test_authorized_get_profile(make_request, access_token):
    response = await make_request(
        endpoint="/me/users", http_method="get", headers=access_token
    )
    assert response.status == http.HTTPStatus.OK


async def test_success_authorized_patch_profile(user, make_request, access_token):
    response = await make_request(
        endpoint="/me/users",
        http_method="patch",
        headers=access_token,
        data={"username": "Lord"},
    )
    assert response.status == http.HTTPStatus.OK
    assert response.body.get("data")[0].get("username") == "Lord"


async def test_unsuccessful_authorized_patch_profile(make_request, access_token):
    response = await make_request(
        endpoint="/me/users", http_method="patch", headers=access_token
    )
    assert response.status == http.HTTPStatus.BAD_REQUEST


async def test_authorized_delete_profile(make_request, access_token):
    response = await make_request(
        endpoint="/me/users", http_method="delete", headers=access_token
    )
    assert response.status == http.HTTPStatus.OK
    response = await make_request(
        endpoint="/me/users", http_method="get", headers=access_token
    )
    assert response.status == http.HTTPStatus.UNAUTHORIZED
