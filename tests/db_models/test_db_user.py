from unittest.mock import Mock

from mock_alchemy.comparison import ExpressionMatcher

from src.db import User
from tests.helper_functions import generate_user_data


def test_get_user_by_id(mock_db_session):
    expected_user = generate_user_data("user")
    expected_id = expected_user.id
    mock_query_result = Mock()
    mock_query_result.filter.return_value = mock_query_result
    mock_query_result.first.return_value = expected_user
    mock_db_session.query.return_value = mock_query_result
    user = User.get_by_id(expected_id)
    assert user == expected_user
    mock_query_result.filter.assert_called_once_with(
        ExpressionMatcher(User.id == expected_id)
    )
    mock_query_result.first.assert_called_once()


def test_create_user(mock_db_session, mocker):
    expected_return = generate_user_data("user")
    mock_update_vector = mocker.patch(
        "src.db.models.user.User.update_search_vector",
        return_value=expected_return.as_dict(),
    )
    return_val = User.create(**expected_return.as_dict())
    assert return_val.as_dict() == expected_return.as_dict()
    mock_db_session.add.assert_called_once_with(return_val)
    mock_update_vector.assert_called_once_with(**expected_return.as_dict())
    mock_db_session.commit.assert_called_once()


def test_update_user(mock_db_session, mocker):
    initial_user = generate_user_data("user")
    expected_return = 7
    expected_id = initial_user.id
    mock_query = Mock()
    mock_query.where.return_value = mock_query
    mock_query.update.return_value = expected_return
    mock_db_session.query.return_value = mock_query
    update_data = generate_user_data("user").as_dict()
    mock_update_vector = mocker.patch(
        "src.db.models.user.User.update_search_vector",
        return_value=update_data,
    )
    actual_return = User.update_by_id(expected_id, **update_data)
    assert actual_return == expected_return
    mock_query.update.assert_called_once_with(update_data)
    mock_query.where.assert_called_once_with(ExpressionMatcher(User.id == expected_id))
    mock_db_session.commit.assert_called_once()
    mock_update_vector.assert_called_once_with(**update_data)


def test_delete_user(mock_db_session):
    expected_return = 1
    expected_id = 1
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.delete.return_value = expected_return
    mock_db_session.query.return_value = mock_query
    actual_return = User.delete_by_id(expected_id)
    assert actual_return == expected_return
    mock_query.filter.assert_called_once_with(ExpressionMatcher(User.id == expected_id))
    mock_db_session.commit.assert_called_once()


def test_search_user(mock_db_session, mocker):
    expected_users = [generate_user_data("user") for _ in range(0, 7)]
    mock_query_result = Mock()
    mock_query_result.filter.return_value = mock_query_result
    mock_query_result.limit.return_value = mock_query_result
    mock_query_result.all.return_value = expected_users
    mock_db_session.query.return_value = mock_query_result
    test_query = "test_query"
    test_limit = 7
    users = User.search(test_query, 7)
    assert users == expected_users
    mock_query_result.limit.assert_called_once_with(test_limit)
    mock_query_result.all.assert_called_once()


def test_get_user_by_name(mock_db_session):
    expected_user = generate_user_data("user")
    expected_name = expected_user.username
    mock_query_result = Mock()
    mock_query_result.filter.return_value = mock_query_result
    mock_query_result.first.return_value = expected_user
    mock_db_session.query.return_value = mock_query_result
    user = User.get_user_by_name(expected_name)
    assert user == expected_user
    mock_query_result.filter.assert_called_once_with(
        ExpressionMatcher(User.username == expected_name)
    )
    mock_query_result.first.assert_called_once()


def test_get_user_by_email(mock_db_session):
    expected_user = generate_user_data("user")
    expected_email = expected_user.email
    mock_query_result = Mock()
    mock_query_result.filter.return_value = mock_query_result
    mock_query_result.first.return_value = expected_user
    mock_db_session.query.return_value = mock_query_result
    user = User.get_user_by_email(expected_email)
    assert user == expected_user
    mock_query_result.filter.assert_called_once_with(
        ExpressionMatcher(User.email == expected_email)
    )
    mock_query_result.first.assert_called_once()
