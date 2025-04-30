from http import HTTPStatus
from flask import request, Response, jsonify
from functools import wraps
from pydantic.main import BaseModel, ValidationError
from app.security.security import verify_jwt

def require_auth():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('JWT '):
                token = auth_header.split(' ')[1]
                user = verify_jwt(token)
                if user:
                    request.current_user = user
                    return f(*args,**kwargs)
                else:
                    return Response("Login required", status=HTTPStatus.FORBIDDEN)
            else:
                return Response("Login required", status=HTTPStatus.FORBIDDEN)
        return wrapper
    return decorator

def validate_request(model: type[BaseModel]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                data = model(**request.get_json())
                return f(data, *args, **kwargs)
            except ValidationError as e:
                return jsonify({"error": e.errors()}), HTTPStatus.BAD_REQUEST
        return wrapper
    return decorator

def validate_request_params(*expected_params):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            found_params = {}
            missing_params = []
            for param_name in expected_params:
                if param_name in request.args:
                    found_params[param_name] = request.args[param_name]
                else:
                    missing_params.append(param_name)
            if missing_params:
                missing_params_str = ", ".join(missing_params)
                error_message = f"Missing required parameters: {missing_params_str}"
                return Response(error_message, HTTPStatus.BAD_REQUEST)
            kwargs.update(found_params)
            return func(*args, **kwargs)
        return wrapper
    return decorator

