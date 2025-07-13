from flask import g, jsonify
from .. import auth, db
from ..models import User


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        g.current_user = user
        return True
    return False


@auth.error_handler
def unauthorized():
    return jsonify({"error": "Unauthorized access"}), 401


def role_required(role):
    def wrapper(fn):
        def decorated(*args, **kwargs):
            if g.current_user.role != role:
                return jsonify({"error": "Permission denied"}), 403
            return fn(*args, **kwargs)

        decorated.__name__ = fn.__name__
        return decorated

    return wrapper
