import http

import pytest

pytestmark = pytest.mark.asyncio


async def test_role_list_and_detail(make_request, access_token):
    """Check role's detail & list methods"""
    """ List """
    response_list = await make_request(
        endpoint="/role/", http_method="get", headers=access_token
    )
    assert response_list.status == http.HTTPStatus.OK
    """ Detail """
    role_id: str = response_list.body.get("data")[0].get("roles")[0].get("id")
    response_detail = await make_request(
        endpoint=f"/role/{role_id}", http_method="get", headers=access_token
    )
    response_detail_id: str = response_detail.body.get("data")[0].get("id")
    assert response_detail.status == http.HTTPStatus.OK
    assert response_detail_id == role_id


async def test_role_create(make_request, access_token):
    """Check creating role"""
    test_role: str = "test_role"
    response = await make_request(
        endpoint="/role/",
        http_method="post",
        headers=access_token,
        data={"name": test_role},
    )
    response_name: str = response.body.get("data")[0].get("name")
    assert response.status == http.HTTPStatus.CREATED
    assert test_role == response_name
    """ Detail """
    role_id: str = response.body.get("data")[0].get("id")
    response_detail = await make_request(
        endpoint=f"/role/{role_id}", http_method="get", headers=access_token
    )
    response_detail_id: str = response_detail.body.get("data")[0].get("id")
    response_detail_name: str = response_detail.body.get("data")[0].get("name")
    assert response_detail.status == http.HTTPStatus.OK
    assert response_detail_id == role_id
    assert test_role == response_detail_name


async def test_role_update(make_request, access_token, get_role_id):
    """Check updating role"""
    updated_role: str = "updated_role"
    response = await make_request(
        endpoint=f"/role/{get_role_id}",
        http_method="patch",
        headers=access_token,
        data={"name": updated_role},
    )
    response_name: str = response.body.get("data")[0].get("name")
    assert response.status == http.HTTPStatus.OK
    assert response_name == updated_role
