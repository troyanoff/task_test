import asyncio
import functools
import random
import os
import uuid
import time

from datetime import datetime, timedelta
from contextlib import contextmanager
from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker
)
from dotenv import load_dotenv

from models.base import Base
from core.config import settings
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
from models.events import Event
from models.relations import CardEvent


load_dotenv()

dbname = os.environ.get('POSTGRES_DB')
user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
host = os.environ.get('POSTGRES_HOST', '127.0.0.1')
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
async def create_superuser(
    session: AsyncSession
):
    user = User(
        login=superuser_login,
        password=superuser_password,
        description='maksimalno krutoj chel',
        role=superrole_name
    )
    session.add(user)
    await session.commit()


@duration
async def create_clients(
    session: AsyncSession,
    count: int = 10000
):
    objs = []
    uuid_list = []
    tg_id_list = []
    for _ in range(count):
        client_uuid = uuid.uuid4()
        tg_id = random.randint(100000000, 999999999)
        client = Client(
            uuid=client_uuid,
            tg_id=tg_id,
            photo_id=fake.text(settings.tg_media_id_len),
            photo_unique_id=fake.text(settings.tg_media_unique_id_len),
            first_name=fake.first_name_female(),
            last_name=fake.last_name_female(),
            sex=random.choice(['f', 'm'])
        )
        objs.append(client)
        uuid_list.append(client_uuid)
        tg_id_list.append(tg_id)
    session.add_all(objs)
    await session.commit()
    return objs


@duration
async def create_company_relations(
    session: AsyncSession,
    clients: list[Client]
):
    """Filling out company data."""
    creator = random.choice(clients)
    client_uuid_list = [i.uuid for i in clients]
    loc_list = []
    actions_list = []
    abon_list = []
    instr_list = []
    sub_list = []
    timeslot_list = []
    record_list = []

    company_uuid = uuid.uuid4()
    company = Company(
        uuid=company_uuid,
        name=fake.text(settings.short_field_len),
        creator_uuid=creator.uuid,
        description=fake.text(settings.long_field_len),
        photo_id=fake.text(settings.tg_media_id_len),
        photo_unique_id=fake.text(settings.tg_media_unique_id_len),
        email=fake.email(),
        max_hour_cancel=random.randint(2, 12)
    )

    session.add(company)
    await session.commit()

    for _ in range(5):
        loc = Location(
            uuid=uuid.uuid4(),
            name=fake.text(settings.short_field_len),
            description=fake.text(settings.long_field_len),
            photo_id=fake.text(settings.tg_media_id_len),
            photo_unique_id=fake.text(settings.tg_media_unique_id_len),
            company_uuid=company_uuid,
            city=fake.city(),
            street=fake.text(settings.short_field_len),
            house=str(random.randint(1, 200)),
            flat=str(random.randint(1, 80)),
            timezone=random.randint(2, 12),
        )
        loc_list.append(loc)

    session.add_all(loc_list)
    await session.commit()

    for _ in range(3):
        action = Action(
            uuid=uuid.uuid4(),
            company_uuid=company_uuid,
            name=fake.text(settings.short_field_len),
            description=fake.text(settings.long_field_len),
            photo_id=fake.text(settings.tg_media_id_len),
            photo_unique_id=fake.text(settings.tg_media_unique_id_len),
        )
        actions_list.append(action)

    session.add_all(actions_list)
    await session.commit()

    for _ in range(5):
        freeze = random.choice([True, False])
        abon = Card(
            uuid=uuid.uuid4(),
            company_uuid=company_uuid,
            name=fake.text(settings.short_field_len),
            description=fake.text(settings.long_field_len),
            by_delta=random.choice([True, False]),
            month_delta=random.randint(1, 24),
            by_count=random.choice([True, False]),
            count=random.choice([random.randint(10, 30), None]),
            freeze=freeze,
            freezing_days=random.randint(10, 40) if freeze else 0
        )
        abon_list.append(abon)

    session.add_all(abon_list)
    await session.commit()

    unique_list_ins = []
    for _ in range(5):
        client_uuid = random.choice(client_uuid_list)
        if (client_uuid, company_uuid) in unique_list_ins:
            continue
        instr = Instructor(
            uuid=uuid.uuid4(),
            client_uuid=client_uuid,
            photo_id=fake.text(settings.tg_media_id_len),
            photo_unique_id=fake.text(settings.tg_media_unique_id_len),
            company_uuid=company_uuid,
        )
        instr_list.append(instr)
        unique_list_ins.append((client_uuid, company_uuid))

    session.add_all(instr_list)
    await session.commit()

    unique_list_sub = []
    for i in clients:
        if (i.uuid, company_uuid) in unique_list_sub:
            continue
        sub = Subscription(
            uuid=uuid.uuid4(),
            client_uuid=i.uuid,
            company_uuid=company_uuid,
            role=random.choice([
                'customer', 'staff', 'instructor', 'client'])
        )
        sub_list.append(sub)
        unique_list_sub.append((i.uuid, company_uuid))

    session.add_all(sub_list)
    await session.commit()

    events_list = []
    for loc in loc_list:
        for trn in actions_list:
            event = Event(
                uuid=uuid.uuid4(),
                company_uuid=company_uuid,
                location_uuid=loc.uuid,
                action_uuid=trn.uuid,
                is_personal=random.choice([True, False])
            )
            events_list.append(event)

    session.add_all(events_list)
    await session.commit()

    unique_list_ts = []
    for _ in range(600):
        start_time = datetime(
            2025,
            random.randint(1, 12),
            random.randint(1, 28),
            random.randint(9, settings.tg_media_unique_id_len),
            0
        )
        ev = random.choice(events_list).uuid
        instructor = random.choice(instr_list).uuid
        if (ev, instructor, start_time) not in unique_list_ts:
            ts = Timeslot(
                uuid=uuid.uuid4(),
                company_uuid=company_uuid,
                event_uuid=ev,
                instructor_uuid=instructor,
                start_time=start_time,
                end_time=start_time + timedelta(hours=1),
                by_count=random.choice([True, False]),
                max_count=random.choice([random.randint(10, 30), 0])
            )
            timeslot_list.append(ts)
            unique_list_ts.append((ev, instructor, start_time))

    session.add_all(timeslot_list)
    await session.commit()

    issuance_list = []
    for i in clients:
        random_start_at = datetime(
            random.randint(2024, 2025),
            random.randint(1, 12),
            random.randint(1, 28),
            random.randint(9, 20),
            0
        )
        random_abon = random.choice(abon_list)
        issue = Issuance(
            uuid=uuid.uuid4(),
            company_uuid=company_uuid,
            client_uuid=i.uuid,
            card_uuid=random_abon.uuid,
            start_at=random_start_at,
            expired_at=(
                random_start_at + timedelta(days=30 * random_abon.month_delta)
                if random_abon.month_delta else None
            ),
            freezing_interval=(
                int(timedelta(days=random_abon.freezing_days).total_seconds())
                if random_abon.freeze else 0
            )
        )
        issuance_list.append(issue)

    session.add_all(issuance_list)
    await session.commit()

    unique_list_rec = []
    for _ in range(10000):
        client = random.choice(clients).uuid
        timeslot = random.choice(timeslot_list).uuid
        issuance = random.choice(issuance_list).uuid
        if (client, timeslot) not in unique_list_rec:
            rec = Record(
                uuid=uuid.uuid4(),
                client_uuid=client,
                timeslot_uuid=timeslot,
                company_uuid=company_uuid,
                issuance_uuid=issuance
            )
            unique_list_rec.append((client, timeslot))
            record_list.append(rec)

    session.add_all(record_list)
    await session.commit()

    query = select(
        Card
    ).where(
        Card.company_uuid == company_uuid
    )

    result = await session.execute(query)
    cards = result.scalars().unique()

    card_event_list = []
    for ab in cards:
        rand_events = random.sample(events_list, k=int(len(events_list) / 3))
        for event in rand_events:
            rel = CardEvent(
                card_uuid=ab.uuid,
                event_uuid=event.uuid,
                company_uuid=company_uuid
            )
            card_event_list.append(rel)
    session.add_all(card_event_list)
    await session.commit()


async def async_main() -> None:
    engine = create_async_engine(dsn)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        print('-' * 100)
        print(', '.join(Base.metadata.tables.keys()))
        print('-' * 100)
        print('creating super user')
        await create_superuser(session)
        print('creating clients')
        clients = await create_clients(session, 10000)
        print('creating companies')
        for i in range(4):
            print(f'company {i + 1}')
            random_clients = random.sample(clients, k=200)
            await create_company_relations(session, random_clients)

    await engine.dispose()


asyncio.run(async_main())
