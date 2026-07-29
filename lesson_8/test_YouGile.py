import uuid
import time
import pytest
from ProjectsAPI import ProjectsAPI
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "https://ru.yougile.com"
api = ProjectsAPI(BASE_URL)


@pytest.fixture(scope="session")
def auth_token():
    login = os.getenv("login")
    password = os.getenv("password")

    assert login and password, "Переменные login/password не найдены в .env файле"

    api._authenticate(login, password)
    token = api.token
    assert token is not None
    return token


@pytest.fixture
def unique_project(auth_token):
    base_title = f"Auto Test {uuid.uuid4()}"

    response, returned_id = api.create_project(base_title, auth_token)
    assert response.ok, f"Создание упало: {response.text}"

    list_resp = api.get_project_list(auth_token)
    list_resp.raise_for_status()

    found_proj = None
    data = list_resp.json()
    possible_keys = ["content", "result", "items", "projects", "project", "data"]

    for key in possible_keys:
        items = data.get(key)
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and item.get("title") == base_title:
                    found_proj = item
                    break

    assert found_proj is not None, "Созданный проект не найден в системе"

    yield {"id": found_proj["id"], "title": found_proj["title"]}

    if found_proj.get("id"):
        try:
            api.delete_project(found_proj["id"], auth_token)
        except Exception:
            pass


# --- МЕТОД: Получение списка ---


def test_get_project_list_positive(auth_token):
    response = api.get_project_list(auth_token)
    assert response.ok
    data = response.json()
    has_array = any(
        isinstance(data.get(k), list) for k in ["content", "result", "items"]
    )
    assert has_array


# --- МЕТОД: Создание проекта ---


def test_create_project_positive(auth_token):
    title = f"New Project {uuid.uuid4()}"
    response, proj_id = api.create_project(title, auth_token)
    assert response.ok
    assert proj_id is not None


def test_create_project_negative_empty_title(auth_token):
    response, _ = api.create_project("", auth_token)
    assert response.status_code == 400


def test_create_project_negative_no_auth():
    fake_api = ProjectsAPI(BASE_URL)
    response, _ = fake_api.create_project("Test", "")
    assert response.status_code == 401 or response.status_code == 403


# --- МЕТОД: Обновление проекта ---


def test_update_project_positive(unique_project, auth_token):
    new_title = f"Updated Title {uuid.uuid4()}"

    response = api.update_project(unique_project["id"], new_title, auth_token)

    time.sleep(1)

    verify_resp = api.get_project_id(unique_project["id"], auth_token)
    assert verify_resp.status_code == 200

    assert api._contains_project(verify_resp.json(), unique_project["id"])


def test_update_project_negative_not_found(auth_token):
    fake_id = str(uuid.uuid4())
    response = api.update_project(fake_id, "Some Name", auth_token)
    assert response.status_code == 404


# --- МЕТОД: Получение проекта по ID ---


def test_get_project_by_id_positive(unique_project, auth_token):
    response = api.get_project_id(unique_project["id"], auth_token)
    assert response.status_code == 200
    assert api._contains_project(response.json(), unique_project["id"])


def test_get_project_by_id_negative(auth_token):
    response = api.get_project_id("invalid-format-id", auth_token)
    assert response.status_code == 404
