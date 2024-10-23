from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from models import Base, Todos
from main import app
from fastapi.testclient import TestClient
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db" #sqlite

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def ovveride_get_current_user():
    return {'username':'test', 'id': 1, 'role': 'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Test Todo",
        description="Test Description",
        priority=4,
        completed=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as con:
        con.execute(text("DELETE FROM todos;"))
        con.commit()