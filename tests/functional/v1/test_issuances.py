import asyncio
import pytest

from http import HTTPStatus

from ..data.config import settings as st


@pytest.mark.asyncio
async def test_create_issuance1(
    post_request
):
    path = 'api/v1/issuances'
    body = {
        'card_uuid': st.storage['card_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'client_uuid': st.storage['client_uuid'],
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    print(st.storage)
    print(body)
    assert status == HTTPStatus.OK
    st.storage['issuance_uuid'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_update_issuance(
    patch_request
):
    path = 'api/v1/issuances'
    body = {
        'uuid': st.storage['issuance_uuid'],
        'is_freeze': True
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
async def test_sleep_issuances_1(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_issuance(
    get_request
):
    path = 'api/v1/issuances/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['issuance_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('uuid') == st.storage['issuance_uuid']
    assert body.get('is_freeze') is True


@pytest.mark.asyncio
async def test_get_all_issuances(
    get_request
):
    path = 'api/v1/issuances'
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
async def test_delete_issuance(
    delete_request
):
    path = 'api/v1/issuances'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['issuance_uuid']
    }
    print('params', params)
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['issuance_uuid']


@pytest.mark.asyncio
async def test_sleep_issuances_2(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_issuance_after_delete(
    get_request
):
    path = 'api/v1/issuances/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['issuance_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    print(body)
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_many_issuances(
    post_request
):
    path = 'api/v1/issuances/get_many'
    body = {
        'uuid_list': [st.storage['issuance_uuid'], ],
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
async def test_create_issuance_final(
    post_request
):
    path = 'api/v1/issuances'
    body = {
        'card_uuid': st.storage['card_uuid'],
        'company_uuid': st.storage['company_uuid'],
        'client_uuid': st.storage['client_uuid'],
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['issuance_uuid'] = body['item']['uuid']
