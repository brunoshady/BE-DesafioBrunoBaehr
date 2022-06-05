from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app, get_db

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


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    json = {'name': 'User Test',
            'cpf': '123.456.789-00',
            'email': 'test_email@email.com',
            'phone_number': '(47) 9999-9999'}

    response = client.post("/users/", json=json)
    assert response.status_code == 201, response.text
    response_dict = response.json()
    assert response_dict['name'] == "User Test"
    assert response_dict['cpf'] == "123.456.789-00"
    assert response_dict['email'] == "test_email@email.com"
    assert response_dict['phone_number'] == "(47) 9999-9999"
    assert response_dict['updated_at'] is None
    assert response_dict['created_at'] is not None
    assert "id" in response_dict
    user_id = response_dict['id']

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    response_dict = response.json()
    assert response_dict['name'] == "User Test"
    assert response_dict['cpf'] == "123.456.789-00"
    assert response_dict['email'] == "test_email@email.com"
    assert response_dict['phone_number'] == "(47) 9999-9999"
    assert response_dict['updated_at'] is None
    assert response_dict['created_at'] is not None
    assert response_dict["id"] == user_id


def test_create_user_without_name():
    json = {'cpf': '123.456.789-00',
            'email': 'test_email@email.com',
            'phone_number': '(47) 9999-9999'}

    response = client.post("/users/", json=json)
    assert response.status_code == 500, response.text
    response_dict = response.json()
    assert response_dict['detail'] == 'Name could not be empty!'


def test_create_user_without_cpf():
    json = {'name': 'User Test',
            'email': 'test_email@email.com',
            'phone_number': '(47) 9999-9999'}

    response = client.post("/users/", json=json)
    assert response.status_code == 500, response.text
    response_dict = response.json()
    assert response_dict['detail'] == "CPF could not be empty!"


def test_update_user():
    json = {'name': 'User Test',
            'cpf': '123.456.789-00'}

    response = client.post("/users/", json=json)
    assert response.status_code == 201, response.text
    response_dict = response.json()
    user_id = response_dict['id']

    json = {'email': 'test_email@email.com',
            'phone_number': '(47) 9999-9999'}

    response = client.patch(f"/users/{user_id}", json=json)
    assert response.status_code == 200, response.text
    response_dict = response.json()

    assert response_dict['email'] == "test_email@email.com"
    assert response_dict['phone_number'] == "(47) 9999-9999"
    assert response_dict['updated_at'] is not None


def test_delete_user():
    json = {'name': 'User Test',
            'cpf': '123.456.789-00'}

    response = client.post("/users/", json=json)
    assert response.status_code == 201, response.text
    response_dict = response.json()
    user_id = response_dict['id']

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    response_dict = response.json()
    assert response_dict['detail'] == "User deleted!"

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404, response.text
    response_dict = response.json()
    assert response_dict['detail'] == "User not found!"
