import asyncio
import pytest

from http import HTTPStatus

from ..data.config import settings as st


@pytest.mark.asyncio
async def test_update_user(
    patch_request
):
    path = 'api/v1/users'
    body = {
        'uuid': st.admin_uuid,
        'description': 'update_description'
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await patch_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_user(
    get_request
):
    path = 'api/v1/users/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.admin_uuid
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('uuid') == st.admin_uuid
    assert body.get('description') == 'update_description'


@pytest.mark.asyncio
async def test_get_all_users(
    get_request
):
    path = 'api/v1/users'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.admin_uuid
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('total_count') == 2
    assert len(body.get('items')) == 2


@pytest.mark.asyncio
async def test_delete_user(
    delete_request
):
    path = 'api/v1/users'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.admin_uuid
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.admin_uuid


@pytest.mark.asyncio
async def test_sleep_users_1(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_user_after_delete(
    get_request
):
    path = 'api/v1/users/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.admin_uuid
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_many_users(
    post_request
):
    path = 'api/v1/users/get_many'
    body = {
        'uuid_list': [st.admin_uuid, st.superuser_uuid],
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    assert body.get('total_count') == 1
    assert len(body.get('items')) == 1
