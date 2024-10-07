import asyncio
from contextlib import contextmanager

import fakeredis
import pytest
from fakeredis import aioredis as fake_aioredis
from redis import asyncio as aioredis
from sqlalchemy import NullPool, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.testclient import TestClient

from core import settings
from core.db import queries
from core.db.models import BaseModel
from core.main import app

DB_URL = f"{settings.DB_URL}_test"


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_db_url():
    return DB_URL


@pytest.fixture(scope="session")
def setup_db(event_loop, test_db_url):
    if database_exists(test_db_url):
        drop_database(test_db_url)
    create_database(test_db_url)
    yield
    drop_database(test_db_url)


@pytest.fixture(scope="function")
def setup_db_tables(setup_db, test_db_url):
    create_db_engine = create_engine(test_db_url)
    BaseModel.metadata.create_all(bind=create_db_engine)
    yield
    BaseModel.metadata.drop_all(bind=create_db_engine)


@pytest.fixture(scope="function")
def sync_db_engine(setup_db_tables, test_db_url):
    return create_engine(
        test_db_url,
        echo=False,
        echo_pool=False,
    )


@pytest.fixture(scope="function")
def sync_db_session(sync_db_engine):
    session = sessionmaker(autocommit=False, autoflush=False, bind=sync_db_engine)
    return session


@pytest.fixture(scope="function")
def test_db_session(sync_db_session):
    session = sync_db_session()
    yield session
    session.close()


def get_test_session():
    test_engine = create_engine(
        DB_URL,
        poolclass=NullPool,
    )
    test_session = sessionmaker(
        autoflush=False,
        bind=test_engine,
        expire_on_commit=False,
    )
    return test_session


@contextmanager
def db_test_session():
    test_session = get_test_session()
    with test_session() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


@pytest.fixture()
def sync_redis_client(request, monkeypatch):
    # Create a FakeStrictRedis instance
    redis_client = fakeredis.FakeStrictRedis()

    # Overwrite the Redis connection where it is used
    monkeypatch.setattr("path to redis", redis_client)

    # Teardown steps to be executed after the tests
    def fin():
        # Clean up resources
        redis_client.flushall()

    request.addfinalizer(fin)

    return redis_client


@pytest.fixture()
def async_redis_client(request, monkeypatch):
    # Create a FakeStrictRedis instance
    redis_client = fake_aioredis.FakeRedis()

    # Overwrite the global Redis connection
    monkeypatch.setattr(aioredis, "from_url", lambda *args, **kwargs: redis_client)

    # Teardown steps to be executed after the tests
    def fin():
        # Clean up resources
        asyncio.get_event_loop().run_until_complete(redis_client.flushall())

    request.addfinalizer(fin)

    return redis_client


@pytest.fixture(scope="function")
def fastapi_test_client(
    request,
    sync_db_session,
):
    with TestClient(app) as client:
        queries.sync_session = sync_db_session

        yield client
