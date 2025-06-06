import asyncio
import pytest

from http import HTTPStatus

from ..data.config import settings as st


@pytest.mark.asyncio
async def test_create_card(
    post_request
):
    path = 'api/v1/cards'
    body = {
        'company_uuid': st.storage['company_uuid'],
        'name': 'test',
        'description': 'test',
        'by_delta': True,
        'month_delta': 1,
        'by_count': True,
        'count': 2,
        'by_limit': False,
        'freeze': True,
        'freezing_days': 2,
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['card_uuid'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_update_card(
    patch_request
):
    path = 'api/v1/cards'
    body = {
        'uuid': st.storage['card_uuid'],
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
async def test_add_events_card(
    post_request
):
    path = 'api/v1/cards/add_events'
    body = {
        'company_uuid': st.storage['company_uuid'],
        'card_uuid': st.storage['card_uuid'],
        'event_uuid_list': [
            st.storage['event_uuid'], st.storage['event_uuid_personal']],
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    print(body)
    assert status == HTTPStatus.OK
    assert len(body['items']) == 2


@pytest.mark.asyncio
async def test_sleep_cards_1(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_card(
    get_request
):
    path = 'api/v1/cards/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['card_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('uuid') == st.storage['card_uuid']
    assert body.get('name') == 'update_test'
    assert len(body.get('events')) == 2


@pytest.mark.asyncio
async def test_get_all_cards(
    get_request
):
    path = 'api/v1/cards'
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
async def test_archive_card(
    delete_request
):
    path = 'api/v1/cards/archive'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['card_uuid']
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['card_uuid']


@pytest.mark.asyncio
async def test_sleep_cards_2(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_card_after_delete(
    get_request
):
    path = 'api/v1/cards/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['card_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_card(
    delete_request
):
    path = 'api/v1/cards'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['card_uuid']
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['card_uuid']


@pytest.mark.asyncio
async def test_get_many_cards(
    post_request
):
    path = 'api/v1/cards/get_many'
    body = {
        'uuid_list': [st.storage['card_uuid'], ],
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
async def test_create_card_final(
    post_request
):
    path = 'api/v1/cards'
    body = {
        'company_uuid': st.storage['company_uuid'],
        'name': 'test',
        'description': 'test',
        'by_delta': True,
        'month_delta': 1,
        'by_count': True,
        'count': 2,
        'by_limit': False,
        'freeze': True,
        'freezing_days': 2,
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['card_uuid'] = body['item']['uuid']
