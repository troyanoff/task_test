from sync_tasks.fast_tasks import calc_price
from sync_tasks.normal_tasks import calc_prices
from sync_tasks.slow_tasks import calc_report


task_list = {
    'calc_price': calc_price,
    'calc_prices': calc_prices,
    'calc_report': calc_report,
}
