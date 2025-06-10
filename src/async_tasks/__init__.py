from async_tasks.fast_tasks import send_email
from async_tasks.normal_tasks import send_emails
from async_tasks.slow_tasks import send_files


task_list = {
    'send_email': send_email,
    'send_emails': send_emails,
    'send_files': send_files,
}
