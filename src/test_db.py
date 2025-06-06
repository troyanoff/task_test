import asyncio
import functools
import os
import random
import uuid
import time

from contextlib import contextmanager
from faker import Faker
from sqlalchemy import Table, and_, String, select, MetaData, Column, func, or_, not_
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker
)
from sqlalchemy.orm import joinedload, lazyload, load_only
from sqlalchemy.orm.attributes import InstrumentedAttribute
from dotenv import load_dotenv
from pprint import pprint

from models.users import User
from models.clients import Client
from models.companies import Company
from models.locations import Location
from models.cards import Card
from models.actions import Action
from models.instructors import Instructor
from models.subscriptions import Subscription
from models.timeslots import Timeslot
from models.records import Record
from models.issuances import Issuance


load_dotenv()

dbname = os.environ.get('POSTGRES_DB')
user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
host = 'localhost'  # os.environ.get('POSTGRES_HOST', '127.0.0.1')
port = os.environ.get('POSTGRES_PORT', 5432)

dsn = (
    f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}'
)

fake = Faker('ru_RU')


superuser_login = os.environ.get('SUPERUSER_LOGIN')
superuser_password = os.environ.get('SUPERUSER_PASSWORD')
superuser_uuid = os.environ.get('SUPERUSER_UUID')
superrole_name = os.environ.get('SUPERROLE_NAME')


def duration(func):
    @contextmanager
    def wrapping_logic():
        start_ts = time.time()
        yield
        dur = time.time() - start_ts
        print('{} took {:.2} seconds'.format(func.__name__, dur))

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            with wrapping_logic():
                return func(*args, **kwargs)
        else:
            async def tmp():
                with wrapping_logic():
                    return (await func(*args, **kwargs))
            return tmp()
    return wrapper


@duration
async def test_query1(session: async_sessionmaker[AsyncSession]):
    query = select(Company).options(joinedload(Company.cards))
    # print(query)
    result = await session.execute(query)
    result = result.scalars().unique()
    for i in result:
        pprint(i.__dict__)


@duration
async def test_query2(session: async_sessionmaker[AsyncSession]):
    query = select(Card).options(joinedload(Card))
    print(query)
    result = await session.execute(query)
    result = result.scalars().unique()
    for i in result:
        pprint(i.__dict__)


async def create_query(model):
    relations = ['actions', 'locations']
    query = select(model)
    for rel in relations:
        query = query.options(
            joinedload(getattr(model, rel))
        )
    return query


@duration
async def test_query3(session: AsyncSession):
    # kwargs = {'uuid': 'cdca1acb-eb5a-4efe-a2e6-f1cbff0def80', '123': None}
    # where_clauses = [getattr(Card, key) == value for (key, value) in kwargs.items() if value is not None]
    # query_abon = select(Card).where(and_(*where_clauses)).options(joinedload(Card.actions))
    # print(query_abon)
    # result_abon = await session.execute(query_abon)
    # abon = result_abon.scalars().first()
    # # abon = await session.get(Card, 'cdca1acb-eb5a-4efe-a2e6-f1cbff0def80', options=joinedload(Card.actions))
    # if abon:
    #     print(abon.__dict__)
    # else:
    #     print('EMPTY RESPONSE')
    # query_tr = select(Action)
    # result_tr = await session.execute(query_tr)
    # tr = result_tr.scalars().first()
    # abon.actions.remove(tr)
    # await session.commit()

    # query = select(Company).options(
    #     joinedload(Company.timeslots)
    # ).limit(1)
    # result = await session.execute(query)
    # result = result.scalars().unique()
    # for i in result:
    #     pprint(i.__dict__)

    # query = select(Timeslot, func.count(Record.uuid).label('records_count')).join(Record, Timeslot.records, isouter=True).group_by(Timeslot.uuid)
    # print(func.now)

    # query = select(func.count(Issuance.uuid)).where(
    #         and_(
    #             Issuance.company_uuid == '1b47e945-f082-4daa-a68d-dfc8bfcdbada',
    #             or_(
    #                 and_(
    #                     Issuance.expired_at.is_not(None),
    #                     Issuance.expired_at > func.now(),
    #                     not_(Issuance.was_spent)
    #                 ),
    #                 and_(
    #                     Issuance.expired_at.is_(None),
    #                     not_(Issuance.was_spent)
    #                 )
    #             )
    #         )
    #     )

    # subquery_cards = (
    #     select(location_action.c.action_uuid)
    #     .where(location_action.c.location_uuid == '3ad11e47-dc33-4ba4-ad6b-d5ca85c7a5d7')
    #     # .subquery()
    # )
    # query = select(func.count(Action.uuid)).where(
    #     and_(
    #         Action.company_uuid == '9d59a51f-d7ce-4d52-b085-3e6f9242562f',
    #         Action.uuid.in_(subquery_cards)
    #     )
    # )


    # subquery_cards = (
    #     select(Issuance.uuid, func.count(Record.uuid).label('record_count'))
    #     .where(Record.issuance_uuid == Issuance.uuid)
    #     .group_by(Issuance.uuid)
    #     # .correlate(Issuance)
    #     .subquery()
    # )
    # print(subquery_cards)
    # query = select(
    #     Issuance.uuid, Card.count, subquery_cards.c.record_count
    # ).join(
    #     Card, Issuance.card_uuid == Card.uuid
    # ).join(
    #     subquery_cards, Issuance.uuid == subquery_cards.c.uuid
    # ).where(
    #     Card.count < subquery_cards.c.record_count
    # )
    # result = await session.execute(query)
    # result = result.first()
    # # for i in result:
    # pprint(result)
    #     # break

    query = select(Issuance).join(Card).where(Card.uuid == Issuance.card_uuid).where(not_(Issuance.was_spent), Issuance.client_uuid == '2f2537c0-698d-44f6-b399-101cb94724fd', Issuance.company_uuid == 'a3eecc4e-1223-449b-9eba-378097479001').order_by(Issuance.created_at.desc()).limit(20)
    result = await session.execute(query)
    # count = await session.execute(query.with_entities())
    result = result.scalars().unique()
    # pprint(result.was_spent)
    # result = set(result)
    # pprint([i.__dict__ for i in result])
    final = []
    for i in result:
        i_dict = i.__dict__
        card = i_dict.pop('card').__dict__
        client = i_dict.pop('client').__dict__
        company = i_dict.pop('company').__dict__
        final.append(dict(company=company, card=card, client=client, **i_dict))
    pprint(final)
    # pprint([(i.was_spent, i.expired_at) for i in result])
    # pprint([dir(i) for i in result])




    # value = '3e074769-1bd7-466c-b9c4-38b9db8b663e'
    # pprint(vars(Card))
    # query = await create_query(Card)
    # query = query.where(Card.actions.any(Action.uuid == value))
    # result = await session.execute(query)
    # result = result.scalars().unique()
    # for i in result:
    #     pprint(i.__dict__)

    # values = [
    #     'f45d8851-ac81-497a-8557-cce72fb40433',
    #     'efe1fddd-3aad-4e44-9df8-f6b3cbb88f51'
    # ]
    # query = select(Card).where(
    #     Card.uuid.in_(values))
    # result = await session.execute(query)
    # result = result.scalars().unique()
    # for i in result:
    #     pprint(i.__dict__)


    # result = result.scalars().first()
    # tr_uuid = '3e074769-1bd7-466c-b9c4-38b9db8b663e'
    # pprint(result.__dict__)
    # obj = await session.get(Action, tr_uuid)
    # result.actions.append(obj)
    # session.add(result)
    # await session.commit()


async def async_main() -> None:
    engine = create_async_engine(dsn)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        # await test_query1(session)
        # await test_query2(session)
        await test_query3(session)

    # async with engine.connect() as conn:
    #     await test_query(conn)

    await engine.dispose()


asyncio.run(async_main())
