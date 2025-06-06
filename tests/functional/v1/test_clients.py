import asyncio
import pytest

from http import HTTPStatus

from ..data.config import settings as st


@pytest.mark.asyncio
async def test_create_client(
    post_request
):
    path = 'api/v1/clients'
    body = {
        'tg_id': 11111111,
        'first_name': 'test',
        'last_name': 'test',
        'photo_id': 'test',
        'photo_unique_id': 'test',
        'sex': 'm',
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['client_uuid'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_update_client(
    patch_request
):
    path = 'api/v1/clients'
    body = {
        'uuid': st.storage['client_uuid'],
        'first_name': 'update_test'
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
async def test_get_client(
    get_request
):
    path = 'api/v1/clients/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['client_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('uuid') == st.storage['client_uuid']
    assert body.get('first_name') == 'update_test'


@pytest.mark.asyncio
async def test_get_all_clients(
    get_request
):
    path = 'api/v1/clients'
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
async def test_delete_client(
    delete_request
):
    path = 'api/v1/clients'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['client_uuid']
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['client_uuid']


@pytest.mark.asyncio
async def test_sleep_clients_1(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_client_after_delete(
    get_request
):
    path = 'api/v1/clients/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['client_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_many_clients(
    post_request
):
    path = 'api/v1/clients/get_many'
    body = {
        'uuid_list': [st.storage['client_uuid'], ],
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
async def test_create_creator(
    post_request
):
    path = 'api/v1/clients'
    body = {
        'tg_id': 11111111,
        'first_name': 'test',
        'last_name': 'test',
        'photo_id': 'test',
        'photo_unique_id': 'test',
        'sex': 'm',
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['creator_uuid'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_create_client_final_1(
    post_request
):
    path = 'api/v1/clients'
    body = {
        'tg_id': 11111112,
        'first_name': 'test',
        'last_name': 'test',
        'photo_id': 'test',
        'photo_unique_id': 'test',
        'sex': 'm',
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['client_uuid'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_create_instructor(
    post_request
):
    path = 'api/v1/clients'
    body = {
        'tg_id': 11111113,
        'first_name': 'test',
        'last_name': 'test',
        'photo_id': 'test',
        'photo_unique_id': 'test',
        'sex': 'm',
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['trainer_uuid'] = body['item']['uuid']
