import asyncio
import pytest

from http import HTTPStatus

from ..data.config import settings as st


@pytest.mark.asyncio
async def test_create_record(
    post_request
):
    path = 'api/v1/records'
    body = {
        'client_uuid': st.storage['client_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'timeslot_uuid': st.storage['timeslot_uuid'],
        'issuance_uuid': st.storage['issuance_uuid'],
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    print(body)
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    print(body)
    assert status == HTTPStatus.OK
    st.storage['record_uuid'] = body['item']['uuid']


# @pytest.mark.asyncio
# async def test_update_record(
#     patch_request
# ):
#     path = 'api/v1/records'
#     body = {
#         'uuid': st.storage['record_uuid'],
#         'photo_id': 'update_test'
#     }
#     headers = {
#         'Content-type': 'application/json',
#         'Accept': 'application/json',
#         'Authorization': f'Bearer {st.access_token_superuser}'
#     }
#     body, _, status = await patch_request(
#         path=path, body=body, headers=headers)
#     assert status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_sleep_records_1(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_record(
    get_request
):
    path = 'api/v1/records/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['record_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('uuid') == st.storage['record_uuid']


@pytest.mark.asyncio
async def test_get_all_records(
    get_request
):
    path = 'api/v1/records'
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
async def test_delete_record(
    delete_request
):
    path = 'api/v1/records'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['record_uuid']
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['record_uuid']


@pytest.mark.asyncio
async def test_sleep_records_2(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_record_after_delete(
    get_request
):
    path = 'api/v1/records/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['record_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_many_records(
    post_request
):
    path = 'api/v1/records/get_many'
    body = {
        'uuid_list': [st.storage['record_uuid'], ],
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
async def test_create_record_final(
    post_request
):
    path = 'api/v1/records'
    body = {
        'client_uuid': st.storage['client_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'timeslot_uuid': st.storage['timeslot_uuid'],
        'issuance_uuid': st.storage['issuance_uuid'],
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['record_uuid'] = body['item']['uuid']
