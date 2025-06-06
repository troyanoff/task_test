from async_fastapi_jwt_auth.exceptions import AuthJWTException
from datetime import datetime, timedelta


def get_expired_datetime(
    month_delta: int | None, last_expired_at: datetime | None
):
    """Calculation of the delay date."""
    if not month_delta or not last_expired_at:
        return None
    now_year = last_expired_at.year
    now_month = last_expired_at.month
    now_day = last_expired_at.day
    calc_month = now_month + month_delta
    if calc_month > 12:
        result_month = calc_month % 12
        result_year = now_year + calc_month // 12
    else:
        result_month = calc_month
        result_year = now_year
    return datetime(
        result_year, result_month, now_day, 23, 59) - timedelta(days=1)


class AuthException(AuthJWTException):

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
