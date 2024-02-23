from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import requests
import requests_mock

from database import Base
from main import app, get_db, get_user

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_user():
    return {'id': '1', 'name': 'Test User'}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_user] = override_get_user

client = TestClient(app)


def test_create_order():
    json = {'user_id': 1,
            'item_description': 'Test Description',
            'item_quantity': 2,
            'item_price': 5}

    response = client.post("/orders/", json=json)
    assert response.status_code == 201, response.text
    response_dict = response.json()

    assert response_dict['user_id'] == 1
    assert response_dict['item_description'] == "Test Description"
    assert response_dict['item_quantity'] == 2
    assert response_dict['item_price'] == 5
    assert response_dict['total_value'] == 10
    assert response_dict['updated_at'] is None
    assert response_dict['created_at'] is not None
    assert "id" in response_dict
    order_id = response_dict['id']

    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200, response.text
    response_dict = response.json()
    assert response_dict['user_id'] == 1
    assert response_dict['item_description'] == "Test Description"
    assert response_dict['item_quantity'] == 2
    assert response_dict['item_price'] == 5
    assert response_dict['total_value'] == 10
    assert response_dict['updated_at'] is None
    assert response_dict['created_at'] is not None
    assert response_dict["id"] == order_id


def test_create_order_without_description():
    json = {'user_id': 1,
            'item_quantity': 2,
            'item_price': 5}

    response = client.post("/orders/", json=json)
    assert response.status_code == 500, response.text
    response_dict = response.json()
    assert response_dict['detail'] == 'Item description could not be empty!'


def test_create_order_without_quantity():
    json = {'user_id': 1,
            'item_description': 'Test Description',
            'item_price': 5}

    response = client.post("/orders/", json=json)
    assert response.status_code == 500, response.text
    response_dict = response.json()
    assert response_dict['detail'] == 'Quantity could not be empty!'


def test_create_order_without_price():
    json = {'user_id': 1,
            'item_description': 'Test Description',
            'item_quantity': 2}

    response = client.post("/orders/", json=json)
    assert response.status_code == 500, response.text
    response_dict = response.json()
    assert response_dict['detail'] == 'Item price could not be empty!'


def test_update_order():
    json = {'user_id': 1,
            'item_description': 'Test Description',
            'item_quantity': 2,
            'item_price': 5}

    response = client.post("/orders/", json=json)
    assert response.status_code == 201, response.text
    response_dict = response.json()

    assert response_dict['user_id'] == 1
    assert response_dict['item_description'] == "Test Description"
    assert response_dict['item_quantity'] == 2
    assert response_dict['item_price'] == 5
    assert response_dict['total_value'] == 10
    assert response_dict['created_at'] is not None
    assert "id" in response_dict
    order_id = response_dict['id']

    json = {'item_description': 'Test Description 2',
            'item_quantity': 3,
            'item_price': 6}

    response = client.patch(f"/orders/{order_id}", json=json)
    assert response.status_code == 200, response.text
    response_dict = response.json()
    assert response_dict['user_id'] == 1
    assert response_dict['item_description'] == "Test Description 2"
    assert response_dict['item_quantity'] == 3
    assert response_dict['item_price'] == 6
    assert response_dict['total_value'] == 18
    assert response_dict['updated_at'] is not None
    assert response_dict['created_at'] is not None
    assert response_dict["id"] == order_id


def teste_delete_order():
    json = {'user_id': 1,
            'item_description': 'Test Description',
            'item_quantity': 2,
            'item_price': 5}

    response = client.post("/orders/", json=json)
    assert response.status_code == 201, response.text
    response_dict = response.json()
    order_id = response_dict['id']

    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200, response.text
    response_dict = response.json()
    assert response_dict['detail'] == "Order deleted!"

    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 404, response.text
    response_dict = response.json()
    assert response_dict['detail'] == "Order not found!"

























