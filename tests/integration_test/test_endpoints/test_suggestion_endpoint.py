from http import HTTPStatus
import json
from urllib.parse import urlencode
from src.constants import UserRolesEnum # Required for checking roles
from src.db import Course

def test_get_suggestion_successful(client, registered_suggestion):
    """Test retrieving a single suggestion by its ID successfully."""
    suggestion_info, _, _, _ = next(registered_suggestion())
    params = urlencode({"id": suggestion_info["id"]})
    response = client.get(f"/suggestion/?{params}")
    
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert response_json["id"] == suggestion_info["id"]
    assert response_json["title"] == suggestion_info["title"]
    assert response_json["text_content"] == suggestion_info["text_content"]
    assert response_json["article_id"] == suggestion_info["article_id"]
    assert response_json["user_id"] == suggestion_info["user_id"]
    assert response_json["date_posted"] is not None # Should always be set
    assert response_json["stars_count"] == 0


def test_get_suggestion_not_found(client):
    """Test retrieving a non-existent suggestion."""
    params = urlencode({"id": 999999})  # Non-existent ID
    response = client.get(f"/suggestion/?{params}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_suggestion_invalid_id_param(client):
    """Test retrieving a suggestion with an invalid ID parameter type."""
    params = urlencode({"id": "invalid"})
    response = client.get(f"/suggestion/?{params}")
    assert response.status_code == HTTPStatus.BAD_REQUEST


# GET /suggestion/by_user
def test_get_suggestions_by_user_successful(client, registered_suggestion, suggestion_data, app):
    """Test retrieving suggestions by a specific user successfully."""
    # Register multiple suggestions by the same user
    suggestion_gen = registered_suggestion(num_suggestions=2)
    suggestion1, user_data, article_info, _ = next(suggestion_gen)
    suggestion2, _, _, _ = next(suggestion_gen)
    params = urlencode({"id": user_data["id"], "limit": 10})
    response = client.get(f"/suggestion/by_user?{params}")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) >= 2  # Should have at least two suggestions
    assert all(s["user_id"] == user_data["id"] for s in response_json)


def test_get_suggestions_by_user_no_suggestions(client, registered_user):
    """Test retrieving suggestions for a user who has none."""
    no_suggestion_user_data = next(registered_user())
    params = urlencode({"id": no_suggestion_user_data["id"], "limit": 10})
    response = client.get(f"/suggestion/by_user?{params}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_suggestions_by_non_existent_user(client):
    """Test retrieving suggestions for a non-existent user."""
    params = urlencode({"id": 999999, "limit": 10})  # Non-existent user ID
    response = client.get(f"/suggestion/by_user?{params}")
    assert response.status_code == HTTPStatus.NO_CONTENT


# GET /suggestion/by_article
def test_get_suggestions_by_article_successful(client, registered_suggestion, suggestion_data, app):
    """Test retrieving suggestions for a specific article successfully."""
    # Create multiple suggestions for the same article
    suggestion_gen = registered_suggestion(num_suggestions=2)
    suggestion1, user_data, article_info, _ = next(suggestion_gen)
    suggestion2, _, _, _ = next(suggestion_gen)
    # Create another suggestion for the same article
    params = urlencode({"id": article_info["id"], "limit": 10})
    response = client.get(f"/suggestion/by_article?{params}")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) >= 2  # Should have at least two suggestions
    assert all(s["article_id"] == article_info["id"] for s in response_json)


def test_get_suggestions_by_article_no_suggestions(client, registered_article):
    """Test retrieving suggestions for an article that has none."""
    article_info, _, _ = next(registered_article())
    params = urlencode({"id": article_info["id"], "limit": 10})
    response = client.get(f"/suggestion/by_article?{params}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_suggestions_by_non_existent_article(client):
    """Test retrieving suggestions for a non-existent article."""
    params = urlencode({"id": 999999, "limit": 10})  # Non-existent article ID
    response = client.get(f"/suggestion/by_article?{params}")
    assert response.status_code == HTTPStatus.NO_CONTENT


# POST /suggestion/
def test_create_suggestion_successful_user_role(client, registered_article, suggestion_data):
    """Test creating a suggestion successfully by a regular user."""
    article_info, user_data, _ = next(registered_article(role="user"))
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = next(suggestion_data(article_id=article_info["id"]))
    response = client.post("/suggestion/", json=payload, headers=headers)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert response_json["title"] == payload["title"]
    assert response_json["text_content"] == payload["text_content"]
    assert response_json["article_id"] == article_info["id"]
    assert response_json["user_id"] == user_data["id"]
    assert response_json["date_posted"] is not None  # date_posted should always be set upon creation
    assert response_json["stars_count"] == 0


def test_create_suggestion_successful_editor_role(client, registered_article, suggestion_data):
    """Test creating a suggestion successfully by an editor."""
    article_info, editor_data,  _ = next(registered_article(role=UserRolesEnum.editor.value))
    access_token = editor_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = next(suggestion_data(article_id=article_info["id"]))
    response = client.post("/suggestion/", json=payload, headers=headers)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert response_json["title"] == payload["title"]
    assert response_json["text_content"] == payload["text_content"]
    assert response_json["article_id"] == article_info["id"]
    assert response_json["user_id"] == editor_data["id"]
    assert response_json["date_posted"] is not None
    assert response_json["stars_count"] == 0


def test_create_suggestion_unauthorized(client, registered_article, suggestion_data):
    """Test creating a suggestion without authentication."""
    article_info, user_data, _ = next(registered_article())
    payload = next(suggestion_data(article_id=article_info["id"]))
    response = client.post("/suggestion/", json=payload)  # No headers
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_create_suggestion_missing_title(client, registered_article, suggestion_data):
    article_info, user_data,  _ = next(registered_article())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = next(suggestion_data(article_id=article_info["id"]))
    del payload["title"]
    response = client.post("/suggestion/", json=payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "title" in response.text


def test_create_suggestion_invalid_data_title_too_long(client, registered_article, suggestion_data):
    """Test creating a suggestion with a title exceeding max length."""
    article_info, user_data,  _ = next(registered_article())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = next(suggestion_data(article_id=article_info["id"]))
    payload["title"] = "a" * 33  # Max length is 32
    response = client.post("/suggestion/", json=payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_suggestion_invalid_data_text_content_too_long(client, registered_article, suggestion_data):
    """Test creating a suggestion with text_content exceeding max length."""
    article_info, user_data, _ = next(registered_article())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = next(suggestion_data(article_id=article_info["id"]))
    payload["text_content"] = "a" * 8001  # Max length is 8000
    response = client.post("/suggestion/", json=payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_suggestion_invalid_article_id(client, registered_user, suggestion_data):
    """Test creating a suggestion with a non-existent article ID."""
    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    payload = next(suggestion_data(article_id=999999))  # Non-existent article_id
    response = client.post("/suggestion/", json=payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


# POST /suggestion/star
def test_star_suggestion_successful(client, registered_suggestion):
    """Test starring a suggestion successfully."""
    suggestion_info, user_data, _, _ = next(registered_suggestion())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    params = urlencode({"id": suggestion_info["id"]})
    
    response = client.post(f"/suggestion/star?{params}", headers=headers)
    assert response.status_code == HTTPStatus.OK

    # Verify stars_count incremented
    get_response = client.get(f"/suggestion/?{params}")
    assert get_response.status_code == HTTPStatus.OK
    # Initial stars_count is 0 from fixture, so after starring once it should be 1
    assert get_response.json["stars_count"] == 1


def test_star_suggestion_already_starred(client, registered_suggestion, app):
    """Test attempting to star a suggestion that is already starred by the user."""
    suggestion_info, user_data, _, _ = next(registered_suggestion())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    params = urlencode({"id": suggestion_info["id"]})

    # First star (successful)
    response1 = client.post(f"/suggestion/star?{params}", headers=headers)
    assert response1.status_code == HTTPStatus.OK

    # Attempt to star again
    response2 = client.post(f"/suggestion/star?{params}", headers=headers)
    assert response2.status_code == HTTPStatus.BAD_REQUEST  # Assuming ERROR_ALREDY_REACTED maps to BAD_REQUEST


def test_star_suggestion_unauthorized(client, registered_suggestion):
    """Test starring a suggestion without authentication."""
    suggestion_info, _, _, _ = next(registered_suggestion())
    params = urlencode({"id": suggestion_info["id"]})
    response = client.post(f"/suggestion/star?{params}")  # No headers
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_star_suggestion_not_found(client, registered_user):
    """Test starring a non-existent suggestion."""
    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    params = urlencode({"id": 999999})  # Non-existent suggestion
    response = client.post(f"/suggestion/star?{params}", headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST  # Or NO_CONTENT or NOT_FOUND depending on exact error handling


# POST /suggestion/unstar
def test_unstar_suggestion_successful(client, registered_suggestion, app):
    """Test unstarring a previously starred suggestion successfully."""
    suggestion_info, user_data, _, _ = next(registered_suggestion())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    params = urlencode({"id": suggestion_info["id"]})

    # Star first to ensure there's a reaction to unstar
    star_response = client.post(f"/suggestion/star?{params}", headers=headers)
    assert star_response.status_code == HTTPStatus.OK

    response = client.post(f"/suggestion/unstar?{params}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    
    # Verify stars_count decremented back to initial (0)
    get_response = client.get(f"/suggestion/?{params}")
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json["stars_count"] == 0


def test_unstar_suggestion_not_starred(client, registered_suggestion):
    """Test unstarring a suggestion that was not previously starred by the user."""
    suggestion_info, user_data, _, _ = next(registered_suggestion())  # Not starred initially by this user
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    params = urlencode({"id": suggestion_info["id"]})
    
    response = client.post(f"/suggestion/unstar?{params}", headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST  # Assuming delete_reaction fails if no existing reaction


def test_unstar_suggestion_unauthorized(client, registered_suggestion):
    """Test unstarring a suggestion without authentication."""
    suggestion_info, _, _, _ = next(registered_suggestion())
    params = urlencode({"id": suggestion_info["id"]})
    response = client.post(f"/suggestion/unstar?{params}")  # No headers
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_unstar_suggestion_not_found(client, registered_user):
    """Test unstarring a non-existent suggestion."""
    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    params = urlencode({"id": 999999})  # Non-existent suggestion
    response = client.post(f"/suggestion/unstar?{params}", headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST  # Or NO_CONTENT or NOT_FOUND


# PATCH /suggestion/
def test_update_suggestion_successful_by_owner(client, registered_suggestion, suggestion_data):
    """Test updating a suggestion successfully by its owner."""
    suggestion_info, user_data, _, _ = next(registered_suggestion(user_role="user"))
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    new_data = next(suggestion_data(article_id=suggestion_info["article_id"]))
    new_data["id"] = suggestion_info["id"]
    response = client.patch(f"/suggestion/?{urlencode(new_data)}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.data == b""

    # Verify update
    get_response = client.get(f"/suggestion/?{urlencode({'id': suggestion_info['id']})}")
    assert get_response.status_code == HTTPStatus.OK
    updated_suggestion = get_response.json
    assert updated_suggestion["title"] == new_data["title"]
    assert updated_suggestion["text_content"] == new_data["text_content"]


def test_update_suggestion_successful_by_editor(client, registered_suggestion, suggestion_data):
    """Test updating a suggestion successfully by an editor."""
    suggestion_info, editor_data, _, _ = next(registered_suggestion(user_role=UserRolesEnum.editor.value))
    access_token = editor_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    new_data = next(suggestion_data(article_id=suggestion_info["article_id"]))
    new_data["id"] = suggestion_info["id"]
    response = client.patch(f"/suggestion/?{urlencode(new_data)}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.data == b""

    # Verify update
    get_response = client.get(f"/suggestion/?{urlencode({'id': suggestion_info['id']})}")
    assert get_response.status_code == HTTPStatus.OK
    updated_suggestion = get_response.json
    assert updated_suggestion["title"] == new_data["title"]
    assert updated_suggestion["text_content"] == new_data["text_content"]


def test_update_suggestion_unauthorized_no_token(client, registered_suggestion, suggestion_data):
    """Test updating a suggestion without authentication."""
    suggestion_info, _, _, _ = next(registered_suggestion())
    update_params = next(suggestion_data())
    update_params["id"] = suggestion_info["id"]
    response = client.patch(f"/suggestion/?{urlencode(update_params)}")
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_suggestion_forbidden_not_owner_or_editor(client, registered_suggestion, registered_user, suggestion_data):
    suggestion_info, _, _, _ = next(registered_suggestion(user_role="user"))  # Created by user1
    other_user_token = next(registered_user())["access_token"]
    update_params = next(suggestion_data())
    update_params["id"] = suggestion_info["id"]
    headers = {"Authorization": f"Bearer {other_user_token}"}
    response = client.patch(f"/suggestion/?{urlencode(update_params)}", headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED  # Should be unauthorized as not owner/editor


def test_update_suggestion_not_found(client, registered_user, suggestion_data):
    """Test updating a non-existent suggestion."""
    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    update_params = {"id": 999999, "title": "Non-existent Suggestion"}
    response = client.patch(f"/suggestion/?{urlencode(update_params)}", headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST  # Or NOT_FOUND/UNAUTHORIZED depending on backend


def test_update_suggestion_invalid_data_title_too_long(client, registered_suggestion, suggestion_data):
    """Test updating a suggestion with a title exceeding max length."""
    suggestion_info, user_data, _, _ = next(registered_suggestion())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    update_params = {"id": suggestion_info["id"], "title": "a" * 33}  # Too long
    response = client.patch(f"/suggestion/?{urlencode(update_params)}", headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_suggestion_no_payload(client, registered_suggestion):
    """Test updating a suggestion with an empty payload (only ID provided)."""
    suggestion_info, user_data, _ , _ = next(registered_suggestion())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    # Only ID provided, no update fields
    update_params = {"id": suggestion_info["id"]}
    response = client.patch(f"/suggestion/?{urlencode(update_params)}", headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


# DELETE /suggestion/
def test_delete_suggestion_successful_by_owner(client, registered_suggestion):
    """Test deleting a suggestion successfully by its owner."""
    suggestion_info, user_data, _, _ = next(registered_suggestion(user_role="user"))
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    delete_params = urlencode({"id": suggestion_info["id"]})
    response = client.delete(f"/suggestion/?{delete_params}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.data == b""

    # Verify deletion
    get_response = client.get(f"/suggestion/?{delete_params}")
    assert get_response.status_code == HTTPStatus.NO_CONTENT


def test_delete_suggestion_successful_by_editor(client, registered_suggestion):
    """Test deleting a suggestion successfully by an editor."""
    suggestion_info, editor_data, _, _ = next(registered_suggestion(user_role=UserRolesEnum.editor.value))
    access_token = editor_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    delete_params = urlencode({"id": suggestion_info["id"]})
    response = client.delete(f"/suggestion/?{delete_params}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.data == b""

    # Verify deletion
    get_response = client.get(f"/suggestion/?{delete_params}")
    assert get_response.status_code == HTTPStatus.NO_CONTENT


def test_delete_suggestion_unauthorized_no_token(client, registered_suggestion):
    """Test deleting a suggestion without authentication."""
    suggestion_info, _, _, _ = next(registered_suggestion())
    delete_params = urlencode({"id": suggestion_info["id"]})
    response = client.delete(f"/suggestion/?{delete_params}")  # No headers
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_suggestion_forbidden_not_owner_or_editor(client, registered_suggestion, registered_user):
    """Test deleting a suggestion when authenticated but not the owner or an editor."""
    suggestion_info, _, _, _ = next(registered_suggestion(user_role="user"))
    other_user_data = next(registered_user(role="user"))
    other_user_token = other_user_data["access_token"]
    headers = {"Authorization": f"Bearer {other_user_token}"}
    delete_params = urlencode({"id": suggestion_info["id"]})
    response = client.delete(f"/suggestion/?{delete_params}", headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_suggestion_not_found(client, registered_user):
    """Test deleting a non-existent suggestion."""
    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    delete_params = urlencode({"id": 999999})  # Non-existent ID
    response = client.delete(f"/suggestion/?{delete_params}", headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

