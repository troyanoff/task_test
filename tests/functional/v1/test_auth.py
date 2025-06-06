import asyncio
import pytest

from http import HTTPStatus

from ..data.config import settings as st


# @pytest.mark.parametrize(
#         'path, http_method, expected_status', endpoints_v1_protected)
@pytest.mark.asyncio
async def test_login(
    post_request
):
    path = 'api/v1/auth/login'
    body = {
        'login': st.superuser_login,
        'password': st.superuser_password
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    access_token = body.get('access_token')
    refresh_token = body.get('refresh_token')
    assert access_token is not None
    assert refresh_token is not None
    st.access_token_superuser = access_token
    st.refresh_token_superuser = refresh_token


@pytest.mark.asyncio
async def test_refresh(
    get_request
):
    path = 'api/v1/auth/refresh'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.refresh_token_superuser}'
    }
    body, _, status = await get_request(
        path=path, headers=headers)
    assert status == HTTPStatus.OK
    access_token = body.get('access_token')
    assert access_token is not None
    st.access_token_superuser = access_token


@pytest.mark.asyncio
async def test_logout(
    get_request
):
    path = 'api/v1/auth/logout'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await get_request(
        path=path, headers=headers)
    assert status == HTTPStatus.OK
    msg = body.get('msg')
    assert msg == 'success logout'
    body, _, status = await get_request(
        path=path, headers=headers)
    assert status == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_sleep_auth_1(
):
    await asyncio.sleep(st.safe_rate_limit_seconds)
    assert 1 == 1


@pytest.mark.asyncio
async def test_superuser_login(
    post_request
):
    path = 'api/v1/auth/login'
    body = {
        'login': st.superuser_login,
        'password': st.superuser_password
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    access_token = body.get('access_token')
    refresh_token = body.get('refresh_token')
    assert access_token is not None
    assert refresh_token is not None
    st.access_token_superuser = access_token
    st.refresh_token_superuser = refresh_token


@pytest.mark.asyncio
async def test_sleep_auth_2(
):
    await asyncio.sleep(st.safe_rate_limit_seconds)
    assert 1 == 1


@pytest.mark.asyncio
async def test_create_admin(
    post_request
):
    path = 'api/v1/users/'
    body = {
        'login': st.admin_login,
        'password': st.admin_password,
        'description': 'test',
        'role': st.admin_role_name
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.admin_uuid = body['item']['uuid']


@pytest.mark.asyncio
async def test_admin_login(
    post_request
):
    path = 'api/v1/auth/login'
    body = {
        'login': st.admin_login,
        'password': st.admin_password
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    access_token = body.get('access_token')
    refresh_token = body.get('refresh_token')
    assert access_token is not None
    assert refresh_token is not None
    st.access_token_admin = access_token
    st.refresh_token_admin = refresh_token


@pytest.mark.asyncio
async def test_sleep_auth_3(
):
    await asyncio.sleep(st.safe_rate_limit_seconds)
    assert 1 == 1
