from models import Base, Todos
from routers.todos import get_db, get_current_user
from main import app
from fastapi import status
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = ovveride_get_current_user

def test_return_users():
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'id': 1, 'username': 'test', 'role': 'admin'}]