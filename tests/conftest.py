import pytest
import pymysql
from app.config import setting
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import Base,get_db
from main import app
import httpx
safe_password = quote_plus(setting.DB_PASSWORD)


TEST_DATABASE_URL = (
    f"mysql+pymysql://{setting.DB_USER}:"
    f"{safe_password}@"
    f"{setting.DB_HOST}:"
    f"{setting.DB_PORT}/"
    f"test_healthcare_db"
)

TEST_ENGINE = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(bind=TEST_ENGINE, autoflush=False)

@pytest.fixture(scope='session',autouse=True)
def setup_test_database():
    connection = pymysql.connect(
    host=setting.DB_HOST,
    user=setting.DB_USER,
    password=setting.DB_PASSWORD,
    port=int(setting.DB_PORT)

)
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS test_healthcare_db;")
    connection.close()

    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)

@pytest.fixture
def db_session():
    connection = TEST_ENGINE.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind = connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
   

@pytest.fixture
async def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = _override_get_db
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as test_client:
        yield test_client
    app.dependency_overrides.clear()
