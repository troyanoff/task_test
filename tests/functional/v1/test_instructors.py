import asyncio
import pytest

from http import HTTPStatus

from ..data.config import settings as st


@pytest.mark.asyncio
async def test_create_instructor(
    post_request
):
    path = 'api/v1/instructors'
    body = {
        'photo_id': 'test',
        'photo_unique_id': 'test',
        'client_uuid': st.storage['trainer_uuid'],
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
    st.storage['instructor_uuid'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_update_instructor(
    patch_request
):
    path = 'api/v1/instructors'
    body = {
        'uuid': st.storage['instructor_uuid'],
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
async def test_sleep_instructors_1(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_instructor(
    get_request
):
    path = 'api/v1/instructors/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['instructor_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('uuid') == st.storage['instructor_uuid']
    assert body.get('photo_id') == 'update_test'


@pytest.mark.asyncio
async def test_get_all_instructors(
    get_request
):
    path = 'api/v1/instructors'
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
async def test_archive_instructor(
    delete_request
):
    path = 'api/v1/instructors/archive'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['instructor_uuid']
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['instructor_uuid']


@pytest.mark.asyncio
async def test_sleep_instructors_2(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_instructor_after_delete(
    get_request
):
    path = 'api/v1/instructors/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['instructor_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_instructor(
    delete_request
):
    path = 'api/v1/instructors'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['instructor_uuid']
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['instructor_uuid']


@pytest.mark.asyncio
async def test_get_many_instructors(
    post_request
):
    path = 'api/v1/instructors/get_many'
    body = {
        'uuid_list': [st.storage['instructor_uuid'], ],
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
async def test_create_instructor_final(
    post_request
):
    path = 'api/v1/instructors'
    body = {
        'photo_id': 'test',
        'photo_unique_id': 'test',
        'client_uuid': st.storage['trainer_uuid'],
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
    st.storage['instructor_uuid'] = body['item']['uuid']
