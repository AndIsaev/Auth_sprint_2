import http

import pytest

pytestmark = pytest.mark.asyncio


async def test_change_user_role(make_request, access_token, user, get_role_id):
    """change user's role"""
    response = await make_request(
        endpoint="/user_role/change",
        http_method="post",
        headers=access_token,
        data={"user_id": f"{user.id}", "role_id": get_role_id},
    )
    assert response.status == http.HTTPStatus.OK


async def test_delete_user_role(make_request, access_token, user, get_role_id):
    """delete user's role"""
    response = await make_request(
        endpoint="/user_role/remove",
        http_method="delete",
        headers=access_token,
        data={"user_id": f"{user.id}", "role_id": get_role_id},
    )
    assert response.status == http.HTTPStatus.BAD_REQUEST
    assert response.body.get("message") == "You can not delete own role"
