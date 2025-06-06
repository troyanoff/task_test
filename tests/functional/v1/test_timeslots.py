import asyncio
import pytest

from datetime import datetime, timedelta
from http import HTTPStatus

from ..data.config import settings as st


@pytest.mark.asyncio
async def test_create_timeslot(
    post_request
):
    path = 'api/v1/timeslots'
    body = {
        'instructor_uuid': st.storage['instructor_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'event_uuid': st.storage['event_uuid'],
        'start_time': str(datetime.now() + timedelta(hours=2)),
        'end_time': str(datetime.now() + timedelta(hours=3)),
        'by_count': True,
        'max_count': 15,
        'section': 'test'
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['timeslot_uuid'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_update_timeslot(
    patch_request
):
    path = 'api/v1/timeslots'
    body = {
        'uuid': st.storage['timeslot_uuid'],
        'section': 'update_test'
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
async def test_sleep_timeslots_1(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_timeslot(
    get_request
):
    path = 'api/v1/timeslots/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['timeslot_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('uuid') == st.storage['timeslot_uuid']
    assert body.get('section') == 'update_test'


@pytest.mark.asyncio
async def test_get_all_timeslots(
    get_request
):
    path = 'api/v1/timeslots'
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
async def test_cancel_timeslot(
    delete_request
):
    path = 'api/v1/timeslots/cancel'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['timeslot_uuid']
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['timeslot_uuid']


@pytest.mark.asyncio
async def test_sleep_timeslots_2(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_timeslot_after_delete(
    get_request
):
    path = 'api/v1/timeslots/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['timeslot_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_timeslot(
    delete_request
):
    path = 'api/v1/timeslots'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['timeslot_uuid']
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['timeslot_uuid']


@pytest.mark.asyncio
async def test_get_many_timeslots(
    post_request
):
    path = 'api/v1/timeslots/get_many'
    body = {
        'uuid_list': [st.storage['timeslot_uuid'], ],
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
async def test_create_timeslot_final(
    post_request
):
    path = 'api/v1/timeslots'
    body = {
        'instructor_uuid': st.storage['instructor_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'event_uuid': st.storage['event_uuid'],
        'start_time': str(datetime.now() + timedelta(hours=2)),
        'end_time': str(datetime.now() + timedelta(hours=3)),
        'by_count': True,
        'max_count': 15,
        'section': 'test'
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['timeslot_uuid'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_get_by_filter_timeslots(
    post_request
):
    path = 'api/v1/timeslots/get_by_filter'
    body = {
        'company_uuid': st.storage['company_uuid'],
        'event_uuid_list': [st.storage['event_uuid'], ],
        'min_dt': str(datetime.now()),
        'max_dt': str(datetime.now() + timedelta(hours=3))
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


@pytest.mark.asyncio
async def test_get_by_location_timeslot(
    get_request
):
    path = 'api/v1/timeslots/get_by_location'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'company_uuid': st.storage['company_uuid'],
        'location_uuid': st.storage['location_uuid'],
        'week_number': datetime.now().isocalendar()[1]
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('total_count') == 1
    assert len(body.get('items')) == 1
