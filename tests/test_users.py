# from .database import client, session
from app import schemas
from jose import jwt
from app.config import settings
import pytest

def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'Hello World'

# @pytest.fixture()
# def test_user(client):
#     res = client.post("/users/", json = {"email":"test@user.com", "password":"123"})
#     assert res.status_code == 201
#     new_user = res.json()
#     new_user['password'] = "123"
#     return new_user
    
def test_create_user(client):

    res = client.post("/users/", json = {"email":"test@user.com", "password":"123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@user.com"
    assert res.status_code == 201

def test_user_login(client, test_user):
    res = client.post(
        "/login", data = {"username":test_user['email'], "password":test_user['password']}
    )
    login_res = schemas.Token(**res.json())
    paylod = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = paylod.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("test@user.com", "wrongPassword", 403),
    ("wrongEmail@user.com", "1234", 403),
    ("wrongEmail@user.com", "wrongPassword", 403),
    (None, "1234", 422),
    ("test@user.com", None, 422)
])
def incorrect_user_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login", data = {"username":email, "password":password}
    )
    assert res.status == status_code
    # assert res.json().get("detail") == "Invalid Credentials"