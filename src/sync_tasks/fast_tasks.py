import time


def calc_price(*args, **kwargs):
    time.sleep(10)
    if 'failed' in kwargs.keys():
        2 / 0
    return {'result': 'Done'}
