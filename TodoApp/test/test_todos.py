from models import Base, Todos
from routers.todos import get_db, get_current_user
from main import app
from fastapi import status
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = ovveride_get_current_user

def test_read_all_authenticated():
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'completed': False, 'description': 'Test Description', 'id': 1, 'owner_id': 1, "priority": 4, 'title': 'Test Todo'}]

def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'completed': False, 'description': 'Test Description', 'id': 1, 'owner_id': 1, "priority": 4, 'title': 'Test Todo'}

def test_read_one_authenticated_not_found():
    response = client.get("/todos/todo/99999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}

def test_create_todo(test_todo):
    request_data = {
        "title": "New Todo",
        "description": "New Todo Description",
        "priority": 3,
        "completed": False
    }

    response = client.post("/todos/todo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.completed == request_data.get('completed')

def test_update_todo(test_todo):
    request_data = {
        "title": "Updated Todo",
        "description": "Updated Todo Description",
        "priority": 1,
        "completed": True
    }

    response = client.put("/todos/todo/1", json=request_data)
    assert response.status_code == status.HTTP_200_OK

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.completed == request_data.get('completed')

def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "Updated Todo",
        "description": "Updated Todo Description",
        "priority": 1,
        "completed": True
    }

    response = client.put("/todos/todo/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}

def test_delete_todo(test_todo):
    response = client.delete("/todos/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo():
    response = client.delete("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}