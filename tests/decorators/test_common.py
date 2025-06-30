import pytest
from pydantic.main import BaseModel
from pydantic.fields import Field
from typing import Optional
from pydantic import field_validator
from src.decorators.common import validate_model_params, validate_model_request
from werkzeug.exceptions import HTTPException
from http import HTTPStatus
from urllib.parse import urlencode


class MockModel(BaseModel):
    required_field: int = Field()
    optional_field: Optional[int] = None
    inline_validation_field: str = Field(max_length=4)
    validated_field: bool = Field()

    @field_validator("validated_field")
    def model_validate_field(cls, value):
        if not value:
            raise ValueError()
        return value


@pytest.mark.parametrize(
    "input_data",
    [
        {
            "required_field": 1,
            "optional_field": 1,
            "inline_validation_field": 'a'*3,
            "validated_field": True,
        },
        {
            "required_field": 1,
            "optional_field": None,
            "inline_validation_field": 'a'*3,
            "validated_field": True,
        }
    ]
)
def test_validate_model_request_successfull(app, input_data: dict):

    @validate_model_request(MockModel)
    def func(data: BaseModel):
        return data

    with app.test_request_context(
        '/test',
        method='GET',
        json=input_data
    ):
        result = func()
    assert result.model_dump(mode='dict') == input_data


@pytest.mark.parametrize(
    "input_data,  missing_args",
    [
        # Required field is missing
        (
            {
                "required_field": None,
                "inline_validation_field": 'a'*3,
                "validated_field": True,
            },
            [
                "required_field"
            ]
        ),
        # Inline validator field is invalid
        (
            {
                "required_field": 1,
                "inline_validation_field": 'a'*10,
                "validated_field": True,
            },
            [
                "inline_validation_field"
            ]
        ),
        # Explicit validator received an invalid data
        (
            {
                "required_field": 1,
                "inline_validation_field": 'a'*10,
                "validated_field": False,
            },
            [
                "validated_field"
            ]
        ),
        (
            {
                "required_field": None,
                "inline_validation_field": 'a'*10,
                "validated_field": False,
            },
            [
                "validated_field",
                "required_field",
                "inline_validation_field"
            ]
        )
    ]
)
def test_validate_model_request_fail(
        app,
        input_data: dict,
        missing_args
):
    @validate_model_request(MockModel)
    def func(data: BaseModel):
        return data

    with app.test_request_context(
        '/test',
        method='GET',
        json=input_data
    ):
        with pytest.raises(HTTPException) as http_exception:
            func()
            assert http_exception.code == HTTPStatus.BadRequest
            for arg in missing_args:
                assert http_exception.message.contain(arg)


@pytest.mark.parametrize(
    "input_data",
    [
        {
            "required_field": 1,
            "optional_field": 1,
            "inline_validation_field": 'a'*3,
            "validated_field": True,
        },
    ]
)
def test_validate_model_params_successfull(app, input_data: dict):

    @validate_model_params(MockModel)
    def func(data: BaseModel):
        return data
    input_data_url_string = urlencode(input_data)
    with app.test_request_context(
        f'/test?{input_data_url_string}',
        method='GET',
    ):
        result = func()
    assert result.model_dump(mode='dict') == input_data


@pytest.mark.parametrize(
    "input_data,  missing_args",
    [
        # Required field is missing
        (
            {
                "required_field": None,
                "inline_validation_field": 'a'*3,
                "validated_field": True,
            },
            [
                "required_field"
            ]
        ),
        # Inline validator field is invalid
        (
            {
                "required_field": 1,
                "inline_validation_field": 'a'*10,
                "validated_field": True,
            },
            [
                "inline_validation_field"
            ]
        ),
        # Explicit validator received an invalid data
        (
            {
                "required_field": 1,
                "inline_validation_field": 'a'*10,
                "validated_field": False,
            },
            [
                "validated_field"
            ]
        ),
        (
            {
                "required_field": None,
                "inline_validation_field": 'a'*10,
                "validated_field": False,
            },
            [
                "validated_field",
                "required_field",
                "inline_validation_field"
            ]
        )
    ]
)
def test_validate_model_params_fail(
        app,
        input_data: dict,
        missing_args
):
    @validate_model_params(MockModel)
    def func(data: BaseModel):
        return data
    input_data_url_string = urlencode(input_data)
    with app.test_request_context(
        f'/test?{input_data_url_string}',
        method='GET',
    ):
        with pytest.raises(HTTPException) as http_exception:
            func()
            assert http_exception.code == HTTPStatus.BadRequest
            for arg in missing_args:
                assert http_exception.message.contain(arg)
