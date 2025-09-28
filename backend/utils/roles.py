from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User
from flask import abort


def roles_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception:
                # return plain payload and status rather than a Response object
                return {"message": "missing or invalid token"}, 401
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)
            if not user:
                return {"message": "user not found"}, 404
            if user.role not in allowed_roles:
                return {"message": "forbidden"}, 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
