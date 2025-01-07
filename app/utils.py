from functools import wraps
from flask import Request, jsonify, redirect, render_template, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from app.admin.models import Admin
from app.player.models import Player
def hash_password(password):
    return generate_password_hash(password)

def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)

def process_request_data(request: Request):
    content_type = request.headers.get('Content-Type')
    if content_type is None:
        raise ValueError('content_type cannot be None')
    if 'application/json' in content_type:
        return request.json
    elif 'application/x-www-form-urlencoded' in content_type:
        return request.form
    else:
        return {}  # 或者抛出异常或者返回默认值，视情况而定
