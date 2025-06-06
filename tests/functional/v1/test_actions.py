import asyncio
import pytest

from http import HTTPStatus

from ..data.config import settings as st


@pytest.mark.asyncio
async def test_create_action(
    post_request
):
    path = 'api/v1/actions'
    body = {
        'name': 'test',
        'description': 'test',
        'photo_id': 'test',
        'photo_unique_id': 'test',
        'company_uuid': st.storage['company_uuid'],
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['action_uuid'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_update_action(
    patch_request
):
    path = 'api/v1/actions'
    body = {
        'uuid': st.storage['action_uuid'],
        'photo_id': 'update_test'
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
async def test_sleep_actions_1(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_action(
    get_request
):
    path = 'api/v1/actions/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['action_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('uuid') == st.storage['action_uuid']
    assert body.get('photo_id') == 'update_test'


@pytest.mark.asyncio
async def test_get_all_actions(
    get_request
):
    path = 'api/v1/actions'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await get_request(
        path=path, headers=headers)
    assert status == HTTPStatus.OK
    assert body.get('total_count') == 1
    assert len(body.get('items')) == 1


@pytest.mark.asyncio
async def test_archive_action(
    delete_request
):
    path = 'api/v1/actions/archive'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['action_uuid']
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['action_uuid']


@pytest.mark.asyncio
async def test_sleep_actions_2(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_action_after_delete(
    get_request
):
    path = 'api/v1/actions/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['action_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_action(
    delete_request
):
    path = 'api/v1/actions'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['action_uuid']
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['action_uuid']


@pytest.mark.asyncio
async def test_get_many_actions(
    post_request
):
    path = 'api/v1/actions/get_many'
    body = {
        'uuid_list': [st.storage['action_uuid'], ],
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    assert body.get('total_count') == 0
    assert len(body.get('items')) == 0


@pytest.mark.asyncio
async def test_create_action_final(
    post_request
):
    path = 'api/v1/actions'
    body = {
        'name': 'test',
        'description': 'test',
        'photo_id': 'test',
        'photo_unique_id': 'test',
        'company_uuid': st.storage['company_uuid'],
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['action_uuid'] = body['item']['uuid']
