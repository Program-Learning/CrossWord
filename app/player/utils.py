from functools import wraps
from flask import Request, jsonify, redirect, render_template, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from app.player.models import Player


def player_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # authentication
        if 'player_id' not in session:
            return jsonify({"code": 1, 'message': 'player_id not in session'}), 401

        player = Player.query.get(session['player_id'])
        if not player:
            return jsonify({"code": 1, 'message': 'player not found'}), 401

        # 如果验证通过，则执行原始函数
        return func(*args, **kwargs)

    return wrapper


def player_required_web(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'player_id' in session:
            if Player.query.get(session['player_id']):
                return func(*args, **kwargs)

        return redirect(url_for('player.login_player_web'))

    return wrapper
