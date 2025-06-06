import json

from datetime import datetime, timedelta
from pprint import pprint
from uuid import UUID

from schemas.issuances import IssuanceUpdateSchema
from schemas.representations import IssuanceListSchema, IssuanceReprSchema


data_i = """
{
    "items": [
    {
            "uuid": "5c55e7f8-8cb9-4b66-abe7-726038f768c4",
            "created_at": "2025-03-04T20:29:20.069093",
            "updated_at": "2025-03-04T20:29:20.069093",
            "company_uuid": "02234271-7640-4a29-ace5-5c4aee874e3b",
            "client_uuid": "cea2f502-f45c-46bb-90ff-e3b62c0c8d04",
            "card_uuid": "2f1d2d92-c6a0-454d-a5f1-2f26f8709447",
            "expired_at": null,
            "now_count": 0,
            "was_spent": false,
            "is_active": false,
            "is_freeze": false,
            "last_freezing": null,
            "closed_at": null,
            "freezing_interval": 1382400,
            "last_record": null,
            "company": {
                "uuid": "02234271-7640-4a29-ace5-5c4aee874e3b",
                "created_at": "2025-03-04T20:29:19.910108",
                "updated_at": "2025-03-04T20:29:19.910108",
                "name": "Трубка опасность бетонный эффект витрина.",
                "description": "Дремать дружно адвокат. Ребятишки скрытый секунда прощение встать очутиться. Помимо выраженный присесть.Головной очутиться угроза разводить.Рабочий носок банк войти около легко премьера. Вывести число освобождение научить приятель. Разводить инструкция приличный металл эффект выражаться совещание триста.Заплакать наткнуться роскошный находить блин. Расстегнуть что военный космос. Наслаждение упорно головной сбросить трясти.",
                "photo_id": "Слать стакан порода столетие секунда угроза пропаганда. Шлем встать пятеро издали.",
                "photo_unique_id": "Прежде указанный.",
                "creator_uuid": "6e37b1e2-80ce-4157-84e2-7ca81ec0a425",
                "email": "dmolchanov@example.com",
                "max_hour_cancel": 3
            },
            "client": {
                "uuid": "cea2f502-f45c-46bb-90ff-e3b62c0c8d04",
                "created_at": "2025-03-04T20:29:05.936233",
                "updated_at": "2025-03-04T20:29:05.936233",
                "tg_id": 156541012,
                "first_name": "Анжелика",
                "last_name": "Дьячкова",
                "photo_id": "Деньги уронить четко неожиданный сутки. Тревога полевой вчера правый.",
                "photo_unique_id": "Дыхание кольцо.",
                "sex": "f",
                "is_premium": false
            },
            "card": {
                "uuid": "2f1d2d92-c6a0-454d-a5f1-2f26f8709447",
                "created_at": "2025-03-04T20:29:19.937928",
                "updated_at": "2025-03-04T20:29:19.937928",
                "name": "Горький необычный спичка тусклый пересечь терапия.",
                "description": "Виднеться уточнить трубка цепочка крыса непривычный. Сверкающий демократия направо покидать.Падать разуметься мгновение зима назначить. Разводить процесс славный горький банда вздрагивать скрытый задрать.Экзамен что рот лететь. Дурацкий блин возникновение блин висеть команда.Сверкать командир дружно. Секунда художественный потянуться упорно бабочка спичка.",
                "company_uuid": "02234271-7640-4a29-ace5-5c4aee874e3b",
                "by_delta": true,
                "month_delta": 3,
                "by_count": true,
                "count": 18,
                "freeze": true,
                "freezing_days": 16
            }
        },
        {
            "uuid": "5c55e7f8-8cb9-4b66-abe7-726038f768cf",
            "created_at": "2025-03-04T20:29:20.069093",
            "updated_at": "2025-03-04T20:29:20.069093",
            "company_uuid": "02234271-7640-4a29-ace5-5c4aee874e3b",
            "client_uuid": "cea2f502-f45c-46bb-90ff-e3b62c0c8d04",
            "card_uuid": "2f1d2d92-c6a0-454d-a5f1-2f26f8709447",
            "expired_at": "2025-06-04T20:29:20.069093",
            "now_count": 50,
            "was_spent": false,
            "is_active": true,
            "is_freeze": false,
            "last_freezing": null,
            "closed_at": null,
            "freezing_interval": 1382400,
            "last_record": "2025-06-01T20:29:20.069093",
            "company": {
                "uuid": "02234271-7640-4a29-ace5-5c4aee874e3b",
                "created_at": "2025-03-04T20:29:19.910108",
                "updated_at": "2025-03-04T20:29:19.910108",
                "name": "Трубка опасность бетонный эффект витрина.",
                "description": "Дремать дружно адвокат. Ребятишки скрытый секунда прощение встать очутиться. Помимо выраженный присесть.Головной очутиться угроза разводить.Рабочий носок банк войти около легко премьера. Вывести число освобождение научить приятель. Разводить инструкция приличный металл эффект выражаться совещание триста.Заплакать наткнуться роскошный находить блин. Расстегнуть что военный космос. Наслаждение упорно головной сбросить трясти.",
                "photo_id": "Слать стакан порода столетие секунда угроза пропаганда. Шлем встать пятеро издали.",
                "photo_unique_id": "Прежде указанный.",
                "creator_uuid": "6e37b1e2-80ce-4157-84e2-7ca81ec0a425",
                "email": "dmolchanov@example.com",
                "max_hour_cancel": 3
            },
            "client": {
                "uuid": "cea2f502-f45c-46bb-90ff-e3b62c0c8d04",
                "created_at": "2025-03-04T20:29:05.936233",
                "updated_at": "2025-03-04T20:29:05.936233",
                "tg_id": 156541012,
                "first_name": "Анжелика",
                "last_name": "Дьячкова",
                "photo_id": "Деньги уронить четко неожиданный сутки. Тревога полевой вчера правый.",
                "photo_unique_id": "Дыхание кольцо.",
                "sex": "f",
                "is_premium": false
            },
            "card": {
                "uuid": "2f1d2d92-c6a0-454d-a5f1-2f26f8709447",
                "created_at": "2025-03-04T20:29:19.937928",
                "updated_at": "2025-03-04T20:29:19.937928",
                "name": "Горький необычный спичка тусклый пересечь терапия.",
                "description": "Виднеться уточнить трубка цепочка крыса непривычный. Сверкающий демократия направо покидать.Падать разуметься мгновение зима назначить. Разводить процесс славный горький банда вздрагивать скрытый задрать.Экзамен что рот лететь. Дурацкий блин возникновение блин висеть команда.Сверкать командир дружно. Секунда художественный потянуться упорно бабочка спичка.",
                "company_uuid": "02234271-7640-4a29-ace5-5c4aee874e3b",
                "by_delta": true,
                "month_delta": 3,
                "by_count": true,
                "count": 18,
                "freeze": true,
                "freezing_days": 16
            }
        }
    ],
    "total_count": 1
}
"""


def _get_expired_datetime(month_delta: int, last_expired_at: datetime):
    """Calculation of the delay date."""

    now_datetime = last_expired_at
    now_year = now_datetime.year
    now_month = now_datetime.month
    now_day = now_datetime.day
    calc_month = now_month + month_delta
    if calc_month > 12:
        result_month = calc_month % 12
        result_year = now_year + calc_month // 12
    else:
        result_month = calc_month
        result_year = now_year
    return datetime(
        result_year, result_month, now_day, 23, 59) - timedelta(days=1)


def main():
    data = json.loads(data_i)
    data = IssuanceListSchema(**data)
    abon_match: dict[UUID, list[IssuanceReprSchema]] = {}
    for item in data.items:
        match_list: list = abon_match.get(item.card_uuid, [])
        match_list.append(item)
        abon_match[item.card_uuid] = match_list

    # print(abon_match)

    update_list: list[IssuanceUpdateSchema] = []
    for k, v in abon_match.items():
        last_closed: datetime = None
        for item in v[::-1]:
            need_update = False
            need_breake = False
            update_data = IssuanceUpdateSchema(uuid=item.uuid)
            # for 1 item
            if not item.is_active and not last_closed:
                need_update = True
                if item.card.by_delta:
                    update_data.expired_at = _get_expired_datetime(item.card.month_delta, item.created_at)
                    update_data.is_active = True
                    if update_data.expired_at < datetime.now():
                        update_data.closed_at = update_data.expired_at
                        update_data.was_spent = True
                        last_closed = update_data.closed_at
                    else:
                        need_breake = True
                elif item.card.by_count:
                    update_data.is_active = True
                    need_breake = True
            elif not item.is_active:
                need_update = True
                if item.card.by_delta:
                    update_data.expired_at = _get_expired_datetime(item.card.month_delta, last_closed)
                    update_data.is_active = True
                    if update_data.expired_at < datetime.now():
                        update_data.closed_at = update_data.expired_at
                        update_data.was_spent = True
                        last_closed = update_data.closed_at
                    else:
                        need_breake = True
            elif item.is_active:
                if item.card.by_delta:
                    if item.expired_at < datetime.now():
                        need_update = True
                        update_data.closed_at = update_data.expired_at
                        update_data.was_spent = True
                        last_closed = update_data.closed_at
                if item.card.by_count:
                    if item.now_count >= item.card.count:
                        need_update = True
                        update_data.closed_at = item.last_record
                        update_data.was_spent = True
                        last_closed = update_data.closed_at

            print(need_update, need_breake, last_closed)
            if need_update:
                update_list.append(update_data)
            if need_breake:
                break

    pprint([i.model_dump(mode='json') for i in update_list])


main()
