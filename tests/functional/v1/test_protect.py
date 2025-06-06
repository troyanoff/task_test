import asyncio
import pytest

from ..data.config import settings as st
from ..data.items import (
    endpoints_v1_protected, endpoints_v1_protected_admin
)


@pytest.mark.parametrize(
        'path, http_method, expected_status', endpoints_v1_protected)
@pytest.mark.asyncio
async def test_not_authorization(
    path, http_method, expected_status, get_request, post_request,
    patch_request, delete_request
):
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        # 'Authorization': 'nnn'
    }
    if http_method == 'get':
        _, _, status = await get_request(
            path=path, headers=headers)
    elif http_method == 'patch':
        _, _, status = await patch_request(
            path=path, body={}, headers=headers)
    elif http_method == 'delete':
        _, _, status = await delete_request(
            path=path, headers=headers)
    else:
        _, _, status = await post_request(
            path=path, body={}, headers=headers)
    assert status == expected_status


@pytest.mark.asyncio
async def test_sleep_protect_1(
):
    await asyncio.sleep(st.safe_rate_limit_seconds)
    assert 1 == 1


@pytest.mark.parametrize(
        'path, http_method, expected_status', endpoints_v1_protected_admin)
@pytest.mark.asyncio
async def test_authorization(
    path, http_method, expected_status, get_request, post_request,
    patch_request, delete_request
):
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.access_token_admin}'
    }
    if http_method == 'get':
        _, _, status = await get_request(
            path=path, headers=headers)
    elif http_method == 'patch':
        _, _, status = await patch_request(
            path=path, body={}, headers=headers)
    elif http_method == 'delete':
        _, _, status = await delete_request(
            path=path, headers=headers)
    else:
        _, _, status = await post_request(
            path=path, body={}, headers=headers)
    assert status != expected_status


@pytest.mark.asyncio
async def test_sleep_protect_2(
):
    await asyncio.sleep(st.safe_rate_limit_seconds)
    assert 1 == 1
