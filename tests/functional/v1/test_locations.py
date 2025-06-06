import asyncio
import pytest

from http import HTTPStatus

from ..data.config import settings as st


@pytest.mark.asyncio
async def test_create_location(
    post_request
):
    path = 'api/v1/locations'
    body = {
        'name': 'test',
        'description': 'test',
        'photo_id': 'test',
        'photo_unique_id': 'test',
        'creator_uuid': st.storage['creator_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'city': 'test@test.ru',
        'street': 'test@test.ru',
        'house': 'test@test.ru',
        'flat': 'test@test.ru',
        'timezone': 3,
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['location_uuid'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_create_second_location(
    post_request
):
    path = 'api/v1/locations'
    body = {
        'name': 'test',
        'description': 'test',
        'photo_id': 'test',
        'photo_unique_id': 'test',
        'creator_uuid': st.storage['creator_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'city': 'test@test.ru',
        'street': 'test@test.ru',
        'house': 'test@test.ru',
        'flat': 'test@test.ru',
        'timezone': 3,
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
async def test_update_location(
    patch_request
):
    path = 'api/v1/locations'
    body = {
        'uuid': st.storage['location_uuid'],
        'name': 'update_test'
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
async def test_sleep_locations_1(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_location(
    get_request
):
    path = 'api/v1/locations/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['location_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('uuid') == st.storage['location_uuid']
    assert body.get('name') == 'update_test'


@pytest.mark.asyncio
async def test_get_all_locations(
    get_request
):
    path = 'api/v1/locations'
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
async def test_delete_location(
    delete_request
):
    path = 'api/v1/locations'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['location_uuid']
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['location_uuid']


@pytest.mark.asyncio
async def test_sleep_locations_2(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_location_after_delete(
    get_request
):
    path = 'api/v1/locations/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['location_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_many_locations(
    post_request
):
    path = 'api/v1/locations/get_many'
    body = {
        'uuid_list': [st.storage['location_uuid'], ],
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
async def test_create_location_final(
    post_request
):
    path = 'api/v1/locations'
    body = {
        'name': 'test',
        'description': 'test',
        'photo_id': 'test',
        'photo_unique_id': 'test',
        'creator_uuid': st.storage['creator_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'city': 'test@test.ru',
        'street': 'test@test.ru',
        'house': 'test@test.ru',
        'flat': 'test@test.ru',
        'timezone': 3,
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['location_uuid'] = body['item']['uuid']
