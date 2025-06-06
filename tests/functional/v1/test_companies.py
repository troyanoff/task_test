import asyncio
import pytest

from http import HTTPStatus

from ..data.config import settings as st


@pytest.mark.asyncio
async def test_create_company(
    post_request
):
    path = 'api/v1/companies'
    body = {
        'name': 'test',
        'description': 'test',
        'photo_id': 'test',
        'photo_unique_id': 'test',
        'creator_uuid': st.storage['creator_uuid'],
        'email': 'test@test.ru',
        'max_hour_cancel': 1,
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['company_uuid'] = body['item']['uuid']


@pytest.mark.asyncio
async def test_create_second_company(
    post_request
):
    path = 'api/v1/companies'
    body = {
        'name': 'test',
        'description': 'test',
        'photo_id': 'test',
        'photo_unique_id': 'test',
        'creator_uuid': st.storage['creator_uuid'],
        'email': 'test@test.ru',
        'max_hour_cancel': 1,
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
async def test_update_company(
    patch_request
):
    path = 'api/v1/companies'
    body = {
        'uuid': st.storage['company_uuid'],
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
async def test_sleep_companies_1(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_company(
    get_request
):
    path = 'api/v1/companies/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['company_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('uuid') == st.storage['company_uuid']
    assert body.get('name') == 'update_test'


@pytest.mark.asyncio
async def test_get_all_companies(
    get_request
):
    path = 'api/v1/companies'
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
async def test_delete_company(
    delete_request
):
    path = 'api/v1/companies'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['company_uuid']
    }
    body, _, status = await delete_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.OK
    assert body.get('item').get('uuid') == st.storage['company_uuid']


@pytest.mark.asyncio
async def test_sleep_companies_2(
):
    await asyncio.sleep(st.default_cache_ttl)
    assert 1 == 1


@pytest.mark.asyncio
async def test_get_company_after_delete(
    get_request
):
    path = 'api/v1/companies/get'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    params = {
        'uuid': st.storage['company_uuid']
    }
    body, _, status = await get_request(
        path=path, headers=headers, params=params)
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_many_companies(
    post_request
):
    path = 'api/v1/companies/get_many'
    body = {
        'uuid_list': [st.storage['company_uuid'], ],
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
async def test_create_company_final(
    post_request
):
    path = 'api/v1/companies'
    body = {
        'name': 'test',
        'description': 'test',
        'photo_id': 'test',
        'photo_unique_id': 'test',
        'creator_uuid': st.storage['creator_uuid'],
        'email': 'test@test.ru',
        'max_hour_cancel': 1,
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_superuser}'
    }
    body, _, status = await post_request(
        path=path, body=body, headers=headers)
    assert status == HTTPStatus.OK
    st.storage['company_uuid'] = body['item']['uuid']
