import asyncio
import pytest

from http import HTTPStatus

from ..data.config import settings as st


@pytest.mark.asyncio
async def test_create_subscription(
    post_request
):
    path = 'api/v1/subscriptions'
    body = {
        'client_uuid': st.storage['client_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'role': 'client',
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['subscription_uuid'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_update_subscription(
    patch_request
):
    path = 'api/v1/subscriptions'
    body = {
        'uuid': st.storage['subscription_uuid'],
        'role': 'staff'
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
async def test_sleep_subscriptions_1(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_subscription(
    get_request
):
    path = 'api/v1/subscriptions/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['subscription_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('uuid') == st.storage['subscription_uuid']
    assert body.get('role') == 'staff'


@pytest.mark.asyncio
async def test_get_all_subscriptions(
    get_request
):
    path = 'api/v1/subscriptions'
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
async def test_delete_subscription(
    delete_request
):
    path = 'api/v1/subscriptions'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['subscription_uuid']
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['subscription_uuid']


@pytest.mark.asyncio
async def test_sleep_subscriptions_2(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_subscription_after_delete(
    get_request
):
    path = 'api/v1/subscriptions/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['subscription_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_many_subscriptions(
    post_request
):
    path = 'api/v1/subscriptions/get_many'
    body = {
        'uuid_list': [st.storage['subscription_uuid'], ],
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
async def test_create_subscription_final(
    post_request
):
    path = 'api/v1/subscriptions'
    body = {
        'client_uuid': st.storage['client_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'role': 'client',
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['subscription_uuid'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_create_subscription_trainer(
    post_request
):
    path = 'api/v1/subscriptions'
    body = {
        'client_uuid': st.storage['trainer_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'role': 'client',
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['subscription_uuid'] = body['item']['uuid']
