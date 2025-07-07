from unittest.mock import Mock

from mock_alchemy.comparison import ExpressionMatcher

from src.db import Course
from tests.helper_functions import generate_course_data


def test_get_course_by_id(mock_db_session):
    expected_course = generate_course_data()
    expected_id = expected_course.id
    mock_query_result = Mock()
    mock_query_result.filter.return_value = mock_query_result
    mock_query_result.first.return_value = expected_course
    mock_db_session.query.return_value = mock_query_result
    course = Course.get_by_id(expected_id)
    assert course == expected_course
    mock_query_result.filter.assert_called_once_with(
        ExpressionMatcher(Course.id == expected_id)
    )
    mock_query_result.first.assert_called_once()


def test_create_course(mock_db_session, mocker):
    expected_return = generate_course_data()
    mock_update_vector = mocker.patch(
        "src.db.models.common.TextContentDbModelABC.update_search_vector",
        return_value=expected_return.as_dict(),
    )
    return_val = Course.create(**expected_return.as_dict())
    assert return_val.as_dict() == expected_return.as_dict()
    mock_db_session.add.assert_called_once_with(return_val)
    mock_update_vector.assert_called_once_with(**expected_return.as_dict())
    mock_db_session.commit.assert_called_once()


def test_update_course(mock_db_session, mocker):
    initial_course = generate_course_data()
    expected_return = 7
    expected_id = initial_course.id
    mock_query = Mock()
    mock_query.where.return_value = mock_query
    mock_query.update.return_value = expected_return
    mock_db_session.query.return_value = mock_query
    update_data = generate_course_data().as_dict()
    mock_update_vector = mocker.patch(
        "src.db.models.common.TextContentDbModelABC.update_search_vector",
        return_value=update_data,
    )
    actual_return = Course.update_by_id(expected_id, **update_data)
    assert actual_return == expected_return
    mock_query.update.assert_called_once_with(update_data)
    mock_update_vector.assert_called_once_with(**update_data)
    mock_query.where.assert_called_once_with(
        ExpressionMatcher(Course.id == expected_id)
    )
    mock_db_session.commit.assert_called_once()


def test_delete_course(mock_db_session):
    expected_return = 1
    expected_id = 1
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.delete.return_value = expected_return
    mock_db_session.query.return_value = mock_query
    actual_return = Course.delete_by_id(expected_id)
    assert actual_return == expected_return
    mock_query.filter.assert_called_once_with(
        ExpressionMatcher(Course.id == expected_id)
    )
    mock_db_session.commit.assert_called_once()


def test_search_course(mock_db_session, mocker):
    expected_courses = [generate_course_data() for _ in range(0, 7)]
    mock_query_result = Mock()
    mock_query_result.filter.return_value = mock_query_result
    mock_query_result.limit.return_value = mock_query_result
    mock_query_result.all.return_value = expected_courses
    mock_db_session.query.return_value = mock_query_result
    test_query = "test_query"
    test_limit = 7
    courses = Course.search(test_query, 7)
    assert courses == expected_courses
    mock_query_result.limit.assert_called_once_with(test_limit)
    mock_query_result.all.assert_called_once()


def test_get_course_by_category(mock_db_session):
    expected_courses = [generate_course_data() for _ in range(0, 7)]
    test_limit = 7
    expected_category = "test_category"
    mock_query_result = Mock()
    mock_query_result.filter.return_value = mock_query_result
    mock_query_result.limit.return_value = mock_query_result
    mock_query_result.all.return_value = expected_courses
    mock_db_session.query.return_value = mock_query_result
    course = Course.get_course_by_category(expected_category, test_limit)
    assert course == expected_courses
    mock_query_result.limit.assert_called_once_with(test_limit)
    mock_query_result.filter.assert_called_once_with(
        ExpressionMatcher(Course.category == expected_category)
    )
    mock_query_result.all.assert_called_once()
