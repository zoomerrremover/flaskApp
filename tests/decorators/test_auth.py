from tests.helper_functions import generate_user_data
from src.decorators.auth import require_auth
from src.constants import UserRolesEnum
from src.exceptions import AuthenticationError, AuthorizationError
import pytest

MOCK_AUTH_HEADER = "HEADER"
MOCK_AUTH_PREFIX = "PREFIX"
MOCK_PARSED_TOKEN = "token"


def test_auth_sucessful(mocker, app):
    user = generate_user_data("user")
    desired_role = "user"
    MOCK_TOKEN = f"{MOCK_AUTH_PREFIX} {MOCK_PARSED_TOKEN}"
    MOCK_RETURNED_TOKEN = user
    mocked_auth_const = mocker.patch(
        "src.decorators.auth.AuthConstantsEnum",
        autospec=True
    )
    mocked_auth_const.AUTH_PREFIX = MOCK_AUTH_PREFIX
    mocked_auth_const.AUTH_HEADER = MOCK_AUTH_HEADER
    mocked_jwt_vert = mocker.patch(
        "src.decorators.auth.verify_jwt",
        return_value=MOCK_RETURNED_TOKEN
    )
    user_db_call = mocker.patch(
        "src.decorators.auth.User.get_by_id",
        return_value=MOCK_RETURNED_TOKEN
    )

    @require_auth(desired_role)
    def local_func():
        return 1

    with app.test_request_context(
        '/test',
        method='GET',
        headers={
            MOCK_AUTH_HEADER: MOCK_TOKEN
                 }
    ):
        result = local_func()
    assert result == 1
    mocked_jwt_vert.assert_called_once_with(MOCK_PARSED_TOKEN)
    user_db_call.assert_called_once_with(MOCK_RETURNED_TOKEN.id)


@pytest.mark.parametrize(
    "role,\
    role_required,\
    AUTH_HEADER,\
    AUTH_PREFIX,\
    user_exist,\
    exception",
    [
        # User is trying to do something that requires a admin role
        (
            UserRolesEnum.USER,
            UserRolesEnum.ADMIN,
            MOCK_AUTH_HEADER,
            MOCK_AUTH_PREFIX,
            True,
            AuthorizationError
        ),
        # The Auth header is missing.
        (
            UserRolesEnum.USER,
            UserRolesEnum.USER,
            "INVALIDHEADER",
            MOCK_AUTH_PREFIX,
            True,
            AuthenticationError
        ),
        # The Auth prefix is missing"
        (
            UserRolesEnum.USER,
            UserRolesEnum.USER,
            MOCK_AUTH_HEADER,
            None,
            True,
            AuthenticationError
        ),
        # The token is correct but the user is not found in db.
        (
            UserRolesEnum.USER,
            UserRolesEnum.USER,
            MOCK_AUTH_HEADER,
            MOCK_AUTH_PREFIX,
            False,
            AuthenticationError
        ),
    ]
)
def test_auth_fail(
        mocker,
        app,
        role: str,
        role_required: str,
        AUTH_HEADER: str,
        AUTH_PREFIX: str,
        user_exist: bool,
        exception
):
    user = generate_user_data(role)
    MOCK_TOKEN = f"{AUTH_PREFIX} {MOCK_PARSED_TOKEN}"
    MOCK_RETURNED_TOKEN = user
    mocked_auth_const = mocker.patch(
        "src.decorators.auth.AuthConstantsEnum",
        autospec=True
    )
    mocked_auth_const.AUTH_PREFIX = MOCK_AUTH_PREFIX
    mocked_auth_const.AUTH_HEADER = MOCK_AUTH_HEADER
    '''
    JWT token shoors exception when token does not match signature so there is
    no point to test it there.
    '''
    mocker.patch(
        "src.decorators.auth.verify_jwt",
        return_value=MOCK_RETURNED_TOKEN
    )
    mocker.patch(
        "src.decorators.auth.User.get_by_id",
        return_value=user if user_exist else None
    )

    @require_auth(role_required)
    def local_func():
        return 1

    with app.test_request_context(
        '/test',
        method='GET',
        headers={
            AUTH_HEADER: MOCK_TOKEN
                 }
    ):
        with pytest.raises(exception):
            local_func()
