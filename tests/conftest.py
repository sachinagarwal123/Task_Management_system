import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from main import app
from database import Base, get_db

# Test database URL for PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/task_management_test"

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """Create test database if it doesn't exist"""
    if not database_exists(SQLALCHEMY_DATABASE_URL):
        create_database(SQLALCHEMY_DATABASE_URL)
    
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    
    yield  # Run the tests
    
    drop_database(SQLALCHEMY_DATABASE_URL)

@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database session for a test"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Clean up tables after test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_client(test_db):
    """Create a test client with database session override"""
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()