import pytest
import requests
import time

from http import HTTPStatus
from uuid import uuid4

from ..data.config import settings as st
from ..data.items import (
    create_tasks_items, flag_status_items, list_params_items,
    comparison_time_priority_items
)
from ..data.schemas import (
    CreateTaskResponse, TaskPriority, StatusTaskResponse, InfoTaskSchema,
    ListTaskSchema, TaskStatus
)


@pytest.mark.parametrize(
    'name, params, priority, status_code, flag',
    create_tasks_items
)
def test_create_task(
    name: str, params: dict, priority: TaskPriority | str,
    status_code: int, flag: str
):
    """Test creating tasks."""
    priority_value = (
        priority.name if isinstance(priority, TaskPriority) else priority
    )
    body = {
        'name': name,
        'params': params,
        'priority': priority_value
    }
    response = requests.post(
        url=st.service_url + 'api/v1/tasks',
        json=body,
        timeout=20
    )

    assert response.status_code == status_code
    if status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        return

    response_data = response.json()
    try:
        response_schema = CreateTaskResponse.model_validate(response_data)
        match_response_schema = True
    except Exception:
        match_response_schema = False
    assert match_response_schema
    task_id = response_schema.uuid.__str__()
    list_uuid: list = st.storage.get('list_uuid', [])
    list_uuid.append(task_id)
    st.storage['list_uuid'] = list_uuid
    if flag != 'none':
        st.storage[flag] = task_id


def test_cancel_task():
    """Canceling some previously created tasks."""
    for flag in st.canceled_task_flags:
        response = requests.delete(
            url=st.service_url + 'api/v1/tasks/' + st.storage[flag],
            timeout=20
        )
        assert response.status_code == HTTPStatus.NO_CONTENT


def test_cancel_not_exist_task():
    """Canceling a non-existent task."""
    not_exist_uuid = str(uuid4())
    response = requests.delete(
        url=st.service_url + f'api/v1/tasks/{not_exist_uuid}',
        timeout=20
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_cancel_in_progress_task():
    """Canceling an ongoing task."""
    in_progress_task_id = st.storage['cancel_slow_io']
    response = requests.delete(
        url=st.service_url + f'api/v1/tasks/{in_progress_task_id}',
        timeout=20
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize(
    'flag, task_status',
    flag_status_items
)
def test_status_task(flag: str, task_status: TaskStatus):
    """Checking the status of created tasks."""
    task_id = st.storage[flag]
    response = requests.get(
        url=st.service_url + f'api/v1/tasks/{task_id}/status',
        timeout=20
    )

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    try:
        response_schema = StatusTaskResponse.model_validate(response_data)
        match_response_schema = True
    except Exception:
        match_response_schema = False

    assert match_response_schema

    assert response_schema.status == task_status


def test_status_not_exist_task():
    """Checking the status of a non-existent task."""
    not_exist_uuid = str(uuid4())
    response = requests.get(
        url=st.service_url + f'api/v1/tasks/{not_exist_uuid}/status',
        timeout=20
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_task_info():
    """Checking the task structure."""
    list_uuid = st.storage['list_uuid']
    for task_id in list_uuid:
        response = requests.get(
            url=st.service_url + f'api/v1/tasks/{task_id}',
            timeout=20
        )
        assert response.status_code == HTTPStatus.OK

        response_data = response.json()
        try:
            InfoTaskSchema.model_validate(response_data)
            match_response_schema = True
        except Exception:
            match_response_schema = False
        assert match_response_schema


def test_task_info_not_found():
    """Checking the structure of a non-existent task."""
    not_exist_uuid = str(uuid4())
    response = requests.get(
        url=st.service_url + f'api/v1/tasks/{not_exist_uuid}',
        timeout=20
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_task_list():
    """Checking the structure of the task list."""
    if not st.storage.get('total_task_count'):
        st.storage['total_task_count'] = len(st.storage['list_uuid'])

    params = {
        'limit': st.storage['total_task_count']
    }
    response = requests.get(
        url=st.service_url + 'api/v1/tasks',
        params=params,
        timeout=20
    )
    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    try:
        response_schema = ListTaskSchema.model_validate(response_data)
        match_response_schema = True
    except Exception:
        match_response_schema = False
    assert match_response_schema

    assert len(response_schema.items) == st.storage['total_task_count']
    # for clean table
    # assert response_schema.total_count == st.storage['total_task_count']


@pytest.mark.parametrize(
    'params, status_code',
    list_params_items
)
def test_task_list_with_filters(params: dict, status_code: int):
    """Checking the structure of the task list with filters."""
    response = requests.get(
        url=st.service_url + 'api/v1/tasks',
        params=params,
        timeout=20
    )
    assert response.status_code == status_code

    response_data = response.json()
    try:
        response_schema = ListTaskSchema.model_validate(response_data)
        match_response_schema = True
    except Exception:
        match_response_schema = False
    assert match_response_schema

    priority = params.get('priority')
    status = params.get('status')
    for task in response_schema.items:
        if priority:
            assert task.priority.name == priority
        if status:
            assert task.status.name == status


def test_wait_comleted_tasks():
    """Waiting for the completion of created tasks."""
    time.sleep(st.default_task_compled_timeout * 2)


@pytest.mark.parametrize(
    'low_flag, high_flag',
    comparison_time_priority_items
)
def test_task_priority(low_flag: str, high_flag: str):
    """Checking the operation of prioritization."""
    task_id_1 = st.storage[low_flag]
    task_id_2 = st.storage[high_flag]

    response_1 = requests.get(
        url=st.service_url + f'api/v1/tasks/{task_id_1}',
        timeout=20
    )
    assert response_1.status_code == HTTPStatus.OK

    response_data_1 = response_1.json()
    try:
        task_schema_1 = InfoTaskSchema.model_validate(response_data_1)
        match_response_schema_1 = True
    except Exception:
        match_response_schema_1 = False
    assert match_response_schema_1

    response_2 = requests.get(
        url=st.service_url + f'api/v1/tasks/{task_id_2}',
        timeout=20
    )
    assert response_2.status_code == HTTPStatus.OK

    response_data_2 = response_2.json()
    try:
        task_schema_2 = InfoTaskSchema.model_validate(response_data_2)
        match_response_schema_2 = True
    except Exception:
        match_response_schema_2 = False
    assert match_response_schema_2

    assert task_schema_1.started_at > task_schema_2.started_at
