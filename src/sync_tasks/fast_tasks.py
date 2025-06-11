import time


def calc_price(*args, **kwargs):
    time.sleep(5)
    if 'failed' in kwargs.keys():
        2 / 0
    return {'result': 'Done'}
