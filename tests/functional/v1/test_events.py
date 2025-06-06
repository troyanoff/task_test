import asyncio
import pytest

from http import HTTPStatus

from ..data.config import settings as st


@pytest.mark.asyncio
async def test_create_event1(
    post_request
):
    path = 'api/v1/events'
    body = {
        'action_uuid': st.storage['action_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'location_uuid': st.storage['location_uuid'],
        'is_personal': False
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['event_uuid'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_create_event2(
    post_request
):
    path = 'api/v1/events'
    body = {
        'action_uuid': st.storage['action_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'location_uuid': st.storage['location_uuid'],
        'is_personal': True
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['event_uuid_personal'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_update_event(
    patch_request
):
    path = 'api/v1/events'
    body = {
        'uuid': st.storage['event_uuid'],
        'is_personal': True
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await patch_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_sleep_events_1(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_event(
    get_request
):
    path = 'api/v1/events/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['event_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('uuid') == st.storage['event_uuid']
    assert body.get('is_personal') is False


@pytest.mark.asyncio
async def test_get_all_events(
    get_request
):
    path = 'api/v1/events'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await get_request(
        path=path, headers=headers)
    assert status == HTTPStatus.OK
    assert body.get('total_count') == 2
    assert len(body.get('items')) == 2


@pytest.mark.asyncio
async def test_delete_event(
    delete_request
):
    path = 'api/v1/events'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['event_uuid']
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['event_uuid']


@pytest.mark.asyncio
async def test_sleep_events_2(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_event_after_delete(
    get_request
):
    path = 'api/v1/events/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['event_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_many_events(
    post_request
):
    path = 'api/v1/events/get_many'
    body = {
        'uuid_list': [st.storage['event_uuid'], ],
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
async def test_create_event_final(
    post_request
):
    path = 'api/v1/events'
    body = {
        'action_uuid': st.storage['action_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'location_uuid': st.storage['location_uuid'],
        'is_personal': False
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['event_uuid'] = body['item']['uuid']
