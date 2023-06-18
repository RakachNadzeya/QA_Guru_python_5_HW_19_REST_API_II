import requests
from jsonschema.validators import validate

from helper import load_json_schema, CustomSession, reqres_session


def test_requested_page_number():
    page = 2

    response = reqres_session.get("/api/users", params={"page": page})

    assert response.status_code == 200
    assert response.json()["page"] == page


def test_get_requested_page_number_schema_validation():
    schema = load_json_schema("get_page_number.json")

    response = reqres_session.get("/api/users")

    validate(instance=response.json(), schema=schema)


def test_users_list_default_length():
    default_users_count = 6

    response = reqres_session.get("/api/users")

    assert len(response.json()["data"]) == default_users_count


def test_get_user_list_schema_validation():
    schema = load_json_schema("get_user_list.json")

    response = reqres_session.get("/api/users")

    validate(instance=response.json(), schema=schema)


def test_single_user_not_found():
    response = reqres_session.get("/api/users/23")

    assert response.status_code == 404
    assert response.text == "{}"


def test_get_single_user_not_found_schema_validation():
    schema = load_json_schema("get_single_user_not_found.json")

    response = reqres_session.get("/api/users/23")

    validate(instance=response.json(), schema=schema)


def test_create_user():
    name = "jane"
    job = "job"

    response = reqres_session.post("/api/users", json={"name": name, "job": job})

    assert response.status_code == 201
    assert response.json()["name"] == name


def test_post_create_user_schema_validation():
    name = "jane"
    job = "job"
    schema = load_json_schema("post_create_user.json")

    response = reqres_session.post("/api/users", json={"name": name, "job": job})

    validate(instance=response.json(), schema=schema)


def test_update_user():
    name = "Kate"
    job = "leader"

    response = reqres_session.put("/api/users/23", json={"name": name, "job": job})

    assert response.status_code == 200
    assert response.json()["name"] == name
    assert response.json()["job"] == job


def test_put_update_user_schema_validation():
    name = "Kate"
    job = "leader"

    schema = load_json_schema("put_update_user_schema.json")

    response = reqres_session.put("/api/users/23", json={"name": name, "job": job})

    validate(instance=response.json(), schema=schema)


def test_user_register_successful():
    email = "eve.holt@reqres.in"
    password = "pistol"

    response = reqres_session.post(
        "/api/register", json={"email": email, "password": password}
    )

    assert response.status_code == 200
    assert response.json()["token"] == "QpwL5tke4Pnpja7X4"


def test_post_user_register_successful_schema_validation():
    email = "eve.holt@reqres.in"
    password = "pistol"

    schema = load_json_schema("post_user_register_successful.json")

    response = reqres_session.post(
        "/api/register", json={"email": email, "password": password}
    )

    validate(instance=response.json(), schema=schema)


def test_user_register_unsuccessful():
    email = "sydney@fife"

    response = reqres_session.post("/api/register", json={"email": email})

    assert response.status_code == 400
    assert response.text == '{"error":"Missing password"}'


def test_post_user_register_unsuccessful_schema_validation():
    email = "sydney@fife"

    schema = load_json_schema("post_user_register_unsuccessful.json")

    response = reqres_session.post("/api/register", json={"email": email})

    validate(instance=response.json(), schema=schema)


def test_login_successful():
    email = "eve.holt@reqres.in"
    password = "pistol"

    response = reqres_session.post("/api/login", json={"email": email, "password": password})

    assert response.status_code == 200
    assert response.json()["token"] != ''


def test_post_login_successful_schema_validation():
    email = "eve.holt@reqres.in"
    password = "pistol"

    schema = load_json_schema("post_login_successful.json")

    response = reqres_session.post("/api/login", json={"email": email, "password": password})

    validate(instance=response.json(), schema=schema)


def test_list_resources():
    response = reqres_session.get("/api/unknown")

    assert response.status_code == 200
    assert response.json()['data'][0]['id'] != ''
    assert response.json()['data'][0]['name'] != ''


def test_get_list_resources_schema_validation():
    schema = load_json_schema("get_list_resources.json")

    response = reqres_session.get("/api/unknown")

    validate(instance=response.json(), schema=schema)


def test_single_resource():
    id = 2
    response = reqres_session.get(f"/api/unknown/{id}")

    assert response.status_code == 200
    assert response.json()['data']['id'] != ''
    assert response.json()['data']['name'] != ''


def test_get_single_resource_schema_validation():
    id = 2

    schema = load_json_schema("get_single_resource.json")

    response = reqres_session.get(f"/api/unknown/{id}")

    validate(instance=response.json(), schema=schema)