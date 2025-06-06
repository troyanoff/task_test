from datetime import datetime, timedelta


def week_borders(year: int, week_number: int):
    year_start = datetime(year, 1, 1, 0, 0)
    print(year_start.isocalendar())
    second_week_start = year_start + timedelta(days=(8 - year_start.isocalendar()[2]))
    print(second_week_start)
    next_monday = second_week_start + timedelta(days=(week_number - 1) * 7)
    print(next_monday)
    print('left_border', next_monday - timedelta(days=7))
    print('right_border', (next_monday - timedelta(days=1)).replace(hour=23, minute=59))


week_borders(2025, 1)

