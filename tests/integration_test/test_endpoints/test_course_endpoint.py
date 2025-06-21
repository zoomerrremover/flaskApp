from faker import Faker
from http import HTTPStatus
from urllib.parse import urlencode


# GET /course/ (by ID)
def test_get_course_successful(client, registered_course):
    created_course, user_data = next(registered_course(num_courses=1))
    params = {"id": created_course["id"]}
    response = client.get(f"/course/?{urlencode(params)}")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert response_json["id"] == created_course["id"]
    assert response_json["title"] == created_course["title"]
    assert response_json["text_content"] == created_course["text_content"]
    assert response_json["category"] == created_course["category"]
    assert response_json["user_id"] == created_course["user_id"]


def test_get_course_not_found(client):
    params = {"id": 999999}
    response = client.get(f"/course/?{urlencode(params)}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_course_invalid_id_param(client):
    params = {"id": "invalid"}
    response = client.get(f"/course/?{urlencode(params)}")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_course_missing_id_param(client):
    response = client.get("/course/")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "id" in response.text


# GET /course/by_user
def test_get_course_by_user_successful(client, registered_user, registered_course):
    # Register two courses for the same user
    course_gen = registered_course(num_courses=2)
    course2, _ = next(course_gen)
    course1, user_data1 = next(course_gen)

    # Register a course for a different user
    params = {"id": user_data1["id"], "limit": 10}
    response = client.get(f"/course/by_user?{urlencode(params)}")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) == 2
    assert any(c["id"] == course1["id"] for c in response_json)
    assert any(c["id"] == course2["id"] for c in response_json)


def test_get_course_by_user_no_courses(client, registered_user):
    user_info = next(registered_user(num_users=1))
    params = {"id": user_info["id"], "limit": 10}
    response = client.get(f"/course/by_user?{urlencode(params)}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_course_by_user_invalid_user_id_param(client):
    params = {"id": "invalid", "limit": 10}
    response = client.get(f"/course/by_user?{urlencode(params)}")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_course_by_user_non_existent_user(client):
    params = {"id": 9999999, "limit": 10}
    response = client.get(f"/course/by_user?{urlencode(params)}")
    assert response.status_code == HTTPStatus.NO_CONTENT


# GET /course/by_category
def test_get_course_by_category_successful(client, registered_course, generate_course_data):
    user_with_courses = next(registered_course(num_courses=1))
    created_course1, user1_data = user_with_courses
    course_data_cat1_b = next(generate_course_data(user_id=user1_data["id"]))
    course_data_cat1_b['category'] = created_course1['category']
    headers = {"Authorization": f"Bearer {user1_data['access_token']}"}
    response_b = client.post("/course/",
                             json=course_data_cat1_b,
                             headers=headers)
    assert response_b.status_code == HTTPStatus.OK
    created_course2 = response_b.json

    # Create a course with a different category
    user_with_diff_course = next(registered_course(num_courses=1))
    created_course3, _ = user_with_diff_course

    params = {"search_query": created_course1["category"], "limit": 10}
    response = client.get(f"/course/by_category?{urlencode(params)}")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) == 2
    assert any(c["id"] == created_course1["id"] for c in response_json)
    assert any(c["id"] == created_course2["id"] for c in response_json)
    assert all(c["category"] == created_course1["category"] for c in response_json)


def test_get_course_by_category_no_courses(client):
    params = {"search_query": "nonexistent_category", "limit": 10}
    response = client.get(f"/course/by_category?{urlencode(params)}")
    print(f"Response content: {response.json}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_course_by_category_invalid_category_param(client):
    params = {"search_query": "", "limit": 10}
    response = client.get(f"/course/by_category?{urlencode(params)}")
    assert response.status_code == HTTPStatus.NO_CONTENT
    params_missing = {"limit": 10}
    response_missing = client.get(f"/course/by_category?{urlencode(params_missing)}")
    print(f"Content {response_missing.json}")
    assert response_missing.status_code == HTTPStatus.BAD_REQUEST


# POST /course/
def test_create_course_successful_user(client, registered_user, course_data):
    user_info = next(registered_user(num_users=1))
    headers = {"Authorization": f"Bearer {user_info['access_token']}"}
    response = client.post("/course/", json=course_data, headers=headers)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert response_json["title"] == course_data["title"]
    assert response_json["user_id"] == user_info["id"]
    assert response_json["date_posted"] is None # Assuming this is still None initially


def test_create_course_forbiden(client, course_data):
    response = client.post("/course/", json=course_data)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_create_course_missing_fields(client, registered_user, course_data):
    user_info = next(registered_user(num_users=1))
    headers = {"Authorization": f"Bearer {user_info['access_token']}"}

    payload = course_data.copy()
    del payload["title"]
    response = client.post("/course/", json=payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "title" in response.text

    payload = course_data.copy()
    del payload["text_content"]
    response = client.post("/course/", json=payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "text_content" in response.text

    payload = course_data.copy()
    del payload["category"]
    response = client.post("/course/", json=payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "category" in response.text


def test_create_course_duplicate_title(client, registered_course, course_data):
    first_course, user_info = next(registered_course(num_courses=1))
    payload = course_data.copy()
    payload["title"] = first_course["title"]
    headers = {"Authorization": f"Bearer {user_info['access_token']}"}
    response = client.post("/course/", json=payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_course_invalid_data_types(client, registered_user, course_data):
    user_info = next(registered_user(num_users=1))
    headers = {"Authorization": f"Bearer {user_info['access_token']}"}

    payload = course_data.copy()
    payload["title"] = 123
    response = client.post("/course/", json=payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST

    payload = course_data.copy()
    payload["text_content"] = ["list", "of", "strings"]
    response = client.post("/course/", json=payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


# PATCH /course/
def test_update_course_successful(client, registered_course, generate_course_data):
    created_course, user_info = next(registered_course(num_courses=1))
    headers = {"Authorization": f"Bearer {user_info['access_token']}"}
    new_course_data = next(generate_course_data(user_id=user_info["id"])) # Ensure user_id matches
    
    update_params = {
        "id": created_course["id"],
        "title": new_course_data["title"],
        "text_content": new_course_data["text_content"],
        "category": new_course_data["category"]
    }
    response = client.patch(f"/course/?{urlencode(update_params)}",
                            headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.data == b""

    get_params = {"id": created_course["id"]}
    get_response = client.get(f"/course/?{urlencode(get_params)}")
    assert get_response.status_code == HTTPStatus.OK
    updated_course = get_response.json
    assert updated_course["title"] == new_course_data["title"]
    assert updated_course["text_content"] == new_course_data["text_content"]
    assert updated_course["category"] == new_course_data["category"]


def test_update_course_successful_editor_admin(client,
                                               registered_course,
                                               generate_course_data,
                                               registered_user):
    initial_course, regular_user_info = next(registered_course(num_courses=1, user_role="user"))
    editor_user_data_gen = registered_user(role="editor", num_users=1)
    editor_user_data = next(editor_user_data_gen)
    editor_access_token = editor_user_data["access_token"]
    headers = {"Authorization": f"Bearer {editor_access_token}"}
    update_params = next(generate_course_data())
    update_params["id"] = initial_course["id"]
    response = client.patch(f"/course/?{urlencode(update_params)}",
                            headers=headers)
    assert response.status_code == HTTPStatus.OK
    get_params = {"id": initial_course["id"]}
    get_response = client.get(f"/course/?{urlencode(get_params)}")
    assert get_response.status_code == HTTPStatus.OK
    updated_course = get_response.json
    assert updated_course["title"] == update_params["title"]


def test_update_course_unauthorized(client, registered_course, generate_course_data):
    created_course, _ = next(registered_course(num_courses=1))
    new_course_data = next(generate_course_data(user_id=created_course["user_id"]))
    update_params = {"id": created_course["id"],
                     "title": new_course_data["title"]}
    response = client.patch(f"/course/?{urlencode(update_params)}")
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_course_not_found(client, registered_user, generate_course_data):
    user_info = next(registered_user(num_users=1))
    headers = {"Authorization": f"Bearer {user_info['access_token']}"}
    new_course_data = next(generate_course_data(user_id=user_info["id"]))
    update_params = {"id": 999999, "title": new_course_data["title"]}
    response = client.patch(f"/course/?{urlencode(update_params)}",
                            headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST # Or NOT_FOUND, depending on API behavior


def test_update_course_unauthorized_not_owner(client,
                                               registered_course,
                                               registered_user,
                                               generate_course_data):
    course, _ = next(registered_course(num_courses=1,))
    other_user_info = next(registered_user(num_users=1))
    headers = {"Authorization": f"Bearer {other_user_info['access_token']}"}
    new_course_data = next(generate_course_data(user_id=other_user_info["id"]))
    new_course_data["id"] = course["id"]
    response = client.patch(f"/course/?{urlencode(new_course_data)}",
                            headers=headers)
    print(f" Repsone data: {response.text}")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_course_invalid_id_param(client, registered_user, generate_course_data):
    user_info = next(registered_user(num_users=1))
    headers = {"Authorization": f"Bearer {user_info['access_token']}"}
    new_course_data = next(generate_course_data(user_id=user_info["id"]))
    update_params = {"id": "invalid", "title": new_course_data["title"]}
    response = client.patch(f"/course/?{urlencode(update_params)}",
                            headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_course_duplicate_title_conflict(client, registered_course, generate_course_data):
    # Create two courses by the same user
    user_with_multiple_courses = next(registered_course(num_courses=1))
    course1, user_info = user_with_multiple_courses
    
    course2_data_gen = generate_course_data(user_id=user_info["id"])
    course2_data = next(course2_data_gen)
    
    headers = {"Authorization": f"Bearer {user_info['access_token']}"}
    response_create2 = client.post("/course/",
                                   json=course2_data,
                                   headers=headers)
    assert response_create2.status_code == HTTPStatus.OK
    course2 = response_create2.json
    
    # Attempt to update course2's title to course1's title
    update_params = {"id": course2["id"], "title": course1["title"]}
    response_update = client.patch(f"/course/?{urlencode(update_params)}",
                                   headers=headers)
    assert response_update.status_code == HTTPStatus.BAD_REQUEST


# DELETE /course/
def test_delete_course_successful(client, registered_course):
    created_course, user_info = next(registered_course(num_courses=1))
    headers = {"Authorization": f"Bearer {user_info['access_token']}"}
    delete_params = {"id": created_course["id"]}
    response = client.delete(f"/course/?{urlencode(delete_params)}",
                             headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.data == b""

    get_params = {"id": created_course["id"]}
    get_response = client.get(f"/course/?{urlencode(get_params)}")
    assert get_response.status_code == HTTPStatus.NO_CONTENT


def test_delete_course_successful_editor_admin(client, registered_course, registered_user, app):
    initial_course, regular_user_info = next(registered_course(num_courses=1, user_role="user"))
    editor_user = next(registered_user("editor"))
    editor_access_token = editor_user["access_token"]
    headers = {"Authorization": f"Bearer {editor_access_token}"}
    delete_params = {"id": initial_course["id"]}
    response = client.delete(f"/course/?{urlencode(delete_params)}",
                             headers=headers)
    assert response.status_code == HTTPStatus.OK
    get_params = {"id": initial_course["id"]}
    get_response = client.get(f"/course/?{urlencode(get_params)}")
    assert get_response.status_code == HTTPStatus.NO_CONTENT


def test_delete_course_forbiden(client, registered_course):
    created_course, _ = next(registered_course(num_courses=1))
    delete_params = {"id": created_course["id"]}
    response = client.delete(f"/course/?{urlencode(delete_params)}")
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_course_not_found(client, registered_user):
    user_info = next(registered_user(num_users=1))
    headers = {"Authorization": f"Bearer {user_info['access_token']}"}
    delete_params = {"id": 999999}
    response = client.delete(f"/course/?{urlencode(delete_params)}",
                             headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_course_unauthorized_not_owner(client, registered_course, registered_user):
    course, _ = next(registered_course())
    other_user_info = next(registered_user())
    headers = {"Authorization": f"Bearer {other_user_info['access_token']}"}
    delete_params = {"id": course["id"]}
    response = client.delete(f"/course/?{urlencode(delete_params)}",
                             headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_course_invalid_id_param(client, registered_user):
    user_info = next(registered_user(num_users=1))
    headers = {"Authorization": f"Bearer {user_info['access_token']}"}
    delete_params = {"id": "invalid"}
    response = client.delete(f"/course/?{urlencode(delete_params)}",
                             headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST
