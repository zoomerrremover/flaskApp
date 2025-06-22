from http import HTTPStatus
import json
from urllib.parse import urlencode
from src.constants import UserRolesEnum # Required for checking roles
from src.db import Course


def test_get_article_successful_by_id(client, registered_article):
    article_info, _, _ = next(registered_article())
    params = urlencode({"id": article_info["id"]})
    response = client.get(f"/article/?{params}")
    print(f"The error is :{response.text} ")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert response_json["id"] == article_info["id"]
    assert response_json["title"] == article_info["title"]
    assert response_json["course_id"] == article_info["course_id"]
    assert response_json["user_id"] == article_info["user_id"]
    # Check date_posted only if it was set (e.g., for editor/admin)
    if article_info["date_posted"]:
        assert response_json["date_posted"] is not None


def test_get_article_not_found(client):
    params = urlencode({"id": 99999})  # Non-existent ID
    response = client.get(f"/article/?{params}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_articles_by_user_successful(client, registered_article):
    article_info, user_data, course_data = next(registered_article(num_articles=3)) # Get 3 articles
    params = urlencode({"id": user_data["id"], "limit": 5})
    response = client.get(f"/article/by_user?{params}")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) >= 1 # At least one article should be returned
    assert any(article["id"] == article_info["id"] for article in response_json)


def test_get_articles_by_user_not_found(client, registered_user):
    # Create a user who won't have any articles
    no_article_user_data = next(registered_user())
    params = urlencode({"id": no_article_user_data["id"], "limit": 5})
    response = client.get(f"/article/by_user?{params}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_articles_by_non_existent_user(client):
    params = urlencode({"id": 999999, "limit": 5}) # Non-existent user ID
    response = client.get(f"/article/by_user?{params}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_articles_by_course_successful(client, registered_article):
    # Create a user, a course, and a few articles for that course
    article_info, user_data, course_data = next(registered_article(num_articles=2))
    params = urlencode({"id": course_data["id"], "limit": 5})
    response = client.get(f"/article/by_course?{params}")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) >= 1 # At least one article should be returned
    assert any(article["id"] == article_info["id"] for article in response_json)


def test_get_articles_by_course_not_found(client, registered_course):
    # Create a course that won't have any articles linked
    _, course_data = next(registered_course())
    params = urlencode({"id": course_data["id"], "limit": 5})
    response = client.get(f"/article/by_course?{params}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_articles_by_non_existent_course(client):
    params = urlencode({"id": 999999, "limit": 5}) # Non-existent course ID
    response = client.get(f"/article/by_course?{params}")
    assert response.status_code == HTTPStatus.NO_CONTENT


## POST /article/ Tests
def test_create_article_successful_user_role(client, registered_user, generate_course_data):
    user_data = next(registered_user(role="user"))
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    course_data = next(generate_course_data(user_id=user_data["id"]))
    with client.application.app_context():
        created_course_db = Course(**course_data).save()
        course_id = created_course_db.id
    article_payload = {
        "title": "My New Article",
        "text_content": "This is the content of my new article.",
        "course_id": course_id,
        "next_article": None,
        "previous_article": None,
    }
    response = client.post("/article/", json=article_payload, headers=headers)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert response_json["title"] == article_payload["title"]
    assert response_json["user_id"] == user_data["id"]
    assert response_json["course_id"] == course_id
    assert response_json["date_posted"] is None # Regular user should have date_posted as None


def test_create_article_successful_editor_role(client, registered_user, generate_course_data):
    editor_data = next(registered_user(role=UserRolesEnum.editor.value))
    access_token = editor_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Create a course first
    course_data = next(generate_course_data(user_id=editor_data["id"]))
    with client.application.app_context():
        created_course_db = Course(**course_data).save()
        course_id = created_course_db.id

    article_payload = {
        "title": "Editor's Approved Article",
        "text_content": "This article is posted by an editor.",
        "course_id": course_id,
    }
    response = client.post("/article/", json=article_payload, headers=headers)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert response_json["title"] == article_payload["title"]
    assert response_json["user_id"] == editor_data["id"]
    assert response_json["date_posted"] is not None # Editor should have date_posted set


def test_create_article_unauthorized(client, generate_course_data, registered_user):
    user_data = next(registered_user())
    course_data = next(generate_course_data(user_id=user_data["id"]))
    with client.application.app_context():
        created_course_db = Course(**course_data).save()
        course_id = created_course_db.id

    article_payload = {
        "title": "Unauthorized Article",
        "text_content": "Attempting to create without token.",
        "course_id": course_id,
    }
    response = client.post("/article/", json=article_payload) # No headers
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_create_article_missing_title(client, registered_user, generate_course_data):
    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    course_data = next(generate_course_data(user_id=user_data["id"]))
    with client.application.app_context():
        created_course_db = Course(**course_data).save()
        course_id = created_course_db.id

    article_payload = {
        "text_content": "Content without title.",
        "course_id": course_id,
    }
    response = client.post("/article/", json=article_payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_article_invalid_data_title_too_long(client, registered_course, article_data):
    course_info, user_data = next(registered_course())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    article_payload = next(article_data(1, user_data["id"], course_info["id"]))
    article_payload["title"] = 200 * "a"
    response = client.post("/article/", json=article_payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_article_invalid_data_text_content_too_long(client, registered_course, article_data):
    course_info, user_data = next(registered_course())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    article_payload = next(article_data(1, user_data["id"], course_info["id"]))
    article_payload["course_id"] = 6000 * "a"
    response = client.post("/article/", json=article_payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_article_invalid_course_id(client, registered_course, article_data):
    course_info, user_data = next(registered_course())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    article_payload = next(article_data(1, user_data["id"], 9999999))
    response = client.post("/article/", json=article_payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_article_successful_by_owner(client, registered_article, article_data):
    article_info, user_data, _ = next(registered_article(role="user"))
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    new_params = next(article_data())
    new_params["id"] = article_info["id"]
    update_params = urlencode(new_params)
    response = client.patch(f"/article/?{update_params}", headers=headers)
    print(f"Error result {response.text}")
    assert response.status_code == HTTPStatus.OK
    assert response.data == b""
    get_params = urlencode({"id": article_info["id"]})
    get_response = client.get(f"/article/?{get_params}")
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json["title"] == new_params["title"]


def test_update_article_successful_by_editor(client, registered_article, article_data):
    # Editor creates the article, then updates it
    article_info, editor_data, _ = next(registered_article(role=UserRolesEnum.editor.value))
    access_token = editor_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    new_data = next(article_data())
    new_data["id"] = article_info["id"]
    update_params = urlencode(new_data)
    response = client.patch(f"/article/?{update_params}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.data == b""
    get_params = urlencode({"id": article_info["id"]})
    get_response = client.get(f"/article/?{get_params}")
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json["title"] == new_data["title"]


def test_update_article_unauthorized(client, registered_article, article_data):
    article_info, _, _ = next(registered_article())
    update_params = next(article_data())
    update_params["id"] = article_info["id"]
    update_params = urlencode(update_params)
    response = client.patch(f"/article/?{update_params}")
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_article_forbidden_not_owner_or_editor(client, registered_article, registered_user, article_data):
    article_info, owner_user_data, _ = next(registered_article(role="user"))
    other_user_data = next(registered_user(role="user"))
    other_user_token = other_user_data["access_token"]
    headers = {"Authorization": f"Bearer {other_user_token}"}
    update_params = next(article_data())
    update_params["id"] = article_info["id"]
    update_params = urlencode(update_params)
    response = client.patch(f"/article/?{update_params}", headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_article_not_found(client, registered_user, article_data):
    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    update_params = next(article_data())
    update_params["id"] = 99999999
    update_params = urlencode(update_params)
    response = client.patch(f"/article/?{update_params}", headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_article_invalid_data_title_too_long(client, registered_article, article_data):
    article_info, user_data, _ = next(registered_article())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    update_params = next(article_data())
    update_params["id"] = article_info["id"]
    update_params["title"] = 200 * "a"
    update_params = urlencode(update_params)
    response = client.patch(f"/article/?{update_params}", headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_article_no_payload(client, registered_article):
    article_info, user_data, _ = next(registered_article())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    update_params = urlencode({"id": article_info["id"]})
    response = client.patch(f"/article/?{update_params}", headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_article_successful_by_owner(client, registered_article):
    article_info, user_data, _ = next(registered_article(role="user"))
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    delete_params = urlencode({"id": article_info["id"]})
    response = client.delete(f"/article/?{delete_params}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.data == b""

    # Verify deletion
    get_params = urlencode({"id": article_info["id"]})
    get_response = client.get(f"/article/?{get_params}")
    assert get_response.status_code == HTTPStatus.NO_CONTENT


def test_delete_article_successful_by_editor(client, registered_article):
    # Editor creates the article, then deletes it
    article_info, editor_data, _ = next(registered_article(role=UserRolesEnum.editor.value))
    access_token = editor_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    delete_params = urlencode({"id": article_info["id"]})
    response = client.delete(f"/article/?{delete_params}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.data == b""

    # Verify deletion
    get_params = urlencode({"id": article_info["id"]})
    get_response = client.get(f"/article/?{get_params}")
    assert get_response.status_code == HTTPStatus.NO_CONTENT


def test_delete_article_unauthorized(client, registered_article):
    article_info, _, _ = next(registered_article())
    delete_params = urlencode({"id": article_info["id"]})
    response = client.delete(f"/article/?{delete_params}") # No headers
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_article_forbidden_not_owner_or_editor(client, registered_article, registered_user):
    # User 1 creates article
    article_info, owner_user_data, _ = next(registered_article(role="user"))
    # User 2 tries to delete User 1's article
    other_user_data = next(registered_user(role="user"))
    other_user_token = other_user_data["access_token"]
    headers = {"Authorization": f"Bearer {other_user_token}"}

    delete_params = urlencode({"id": article_info["id"]})
    response = client.delete(f"/article/?{delete_params}", headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_article_not_found(client, registered_user):
    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    delete_params = urlencode({"id": 99999}) # Non-existent article ID
    response = client.delete(f"/article/?{delete_params}", headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

