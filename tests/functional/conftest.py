import asyncio
import json
import pytest
import pytest_asyncio
import os

from aiohttp import ClientSession, RequestInfo, FormData

from .data.config import settings as st


# @pytest_asyncio.fixture(scope='session')
# async def event_loop():
#     # loop = asyncio.get_event_loop_policy().new_event_loop()
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()


# @pytest_asyncio.fixture(scope='session')
# async def http_session():
#     sess = ClientSession()
#     yield sess
#     await sess.close()


@pytest_asyncio.fixture
async def get_request():
    async def inner(
        path: str, params: dict = {}, headers: dict = {}
    ) -> RequestInfo:
        url = os.path.join(await st.get_service_url(), path)
        async with ClientSession() as session:
            async with session.get(
                    url, params=params, headers=headers) as response:
                body = await response.json(content_type=None)
                headers = response.headers
                status = response.status
        return body, headers, status

    return inner


@pytest_asyncio.fixture
def post_request():
    async def inner(
        path: str, params: dict = {}, headers: dict = {}, body: dict = {}
    ) -> RequestInfo:
        url = os.path.join(await st.get_service_url(), path)
        body = json.dumps(body)
        async with ClientSession() as session:
            async with session.post(
                url, params=params, headers=headers, data=body
            ) as response:
                body = await response.json(content_type=None)
                headers = response.headers
                status = response.status
        return body, headers, status

    return inner


@pytest_asyncio.fixture
def patch_request():
    async def inner(
        path: str, params: dict = {}, headers: dict = {}, body: dict = {}
    ) -> RequestInfo:
        url = os.path.join(await st.get_service_url(), path)
        body = json.dumps(body)
        async with ClientSession() as session:
            async with session.patch(
                url, params=params, headers=headers, data=body
            ) as response:
                body = await response.json(content_type=None)
                headers = response.headers
                status = response.status
        return body, headers, status

    return inner


@pytest_asyncio.fixture
def delete_request():
    async def inner(
        path: str, params: dict = {}, headers: dict = {}
    ) -> RequestInfo:
        url = os.path.join(await st.get_service_url(), path)
        async with ClientSession() as session:
            async with session.delete(
                url, params=params, headers=headers
            ) as response:
                body = await response.json(content_type=None)
                headers = response.headers
                status = response.status
        return body, headers, status

    return inner


def pytest_collection_modifyitems(items):
    MODULE_ORDER = [
        'functional.v1.test_auth',
        'functional.v1.test_users',
        'functional.v1.test_protect',
        'functional.v1.test_clients',
        'functional.v1.test_companies',
        'functional.v1.test_locations',
        'functional.v1.test_subscriptions',
        'functional.v1.test_instructors',
        'functional.v1.test_actions',
        'functional.v1.test_events',
        'functional.v1.test_cards',
        'functional.v1.test_issuances',
        'functional.v1.test_timeslots',
        'functional.v1.test_records',
    ]
    module_mapping = {item: item.module.__name__ for item in items}

    sorted_items = items.copy()

    for module in MODULE_ORDER[::-1]:
        sorted_items = [
            it for it in sorted_items if module_mapping[it] == module
        ] + [
            it for it in sorted_items if module_mapping[it] != module
        ]

    items[:] = sorted_items


def write_error_to_file(error_message):
    with open(st.error_file, 'a') as f:
        f.write(error_message + '\n')


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    if report.failed:
        error_message = (
            f'Test {report.nodeid} completed with an error.\n'
            f'Error msg: {report.longreprtext}\n'
            f'{"=" * 80}\n'
        )
        write_error_to_file(error_message)


async def send_notification_async(success, len_passed, len_failed):
    if success:
        msg = (
            f'{st.project_name}\n'
            f'tests passed successfully.\n{len_passed=}, {len_failed=}'
        )
    else:
        msg = (
            f'{st.project_name}\n'
            'tests failed, the details are in the file.\n'
            f'{len_passed=}, {len_failed=}'
        )
    url_text = (
        f'https://api.telegram.org/'
        f'bot{st.bot_token}/'
        f'sendMessage'
    )
    url_file = (
        f'https://api.telegram.org/'
        f'bot{st.bot_token}/'
        f'sendDocument'
    )
    for chat_id in await st.get_tg_id_list():
        params = {
            'chat_id': int(chat_id),
            'text': msg
        }
        async with ClientSession() as session:
            async with session.get(url_text, params=params):
                pass
        if not success:
            with open('test_errors.log', 'rb') as file:
                form_data = FormData()
                form_data.add_field(
                    'document', file, filename=os.path.basename(st.error_file))
                async with ClientSession() as session:
                    async with session.post(
                        url_file, data=form_data, params={'chat_id': chat_id}
                    ):
                        pass


def send_notification(success, len_passed, len_failed):
    asyncio.run(send_notification_async(success, len_passed, len_failed))


@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):

    len_passed = len(terminalreporter.stats.get('passed', []))
    len_failed = len(terminalreporter.stats.get('failed', []))
    if exitstatus == 0:
        send_notification(True, len_passed, len_failed)
    else:
        send_notification(False, len_passed, len_failed)
