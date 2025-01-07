from datetime import datetime
from functools import wraps
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from app.models import db
from app.player.models import Player
from app.models import *
from app.player.utils import player_required, player_required_web
from app.utils import hash_password, process_request_data

player = Blueprint('player', __name__, template_folder='templates')


@player.route('/register_player', methods=['POST'])
def register_player():
    data = process_request_data(request)
    username = data.get('username')
    password = hash_password(data.get('password'))
    if username is None or password is None:
        return jsonify({"code": 1, 'message': 'Invalid request'})
    if Player.query.filter_by(username=username).first() is not None:
        return jsonify({"code": 1, 'message': 'username already exists'})
    try:
        new_player = Player(**data)
    except:
        return jsonify({"code": 1, 'message': 'Invalid request'}), 400
    db.session.add(new_player)
    db.session.commit()
    return jsonify({"code": 0, 'message': 'Player registered successfully'})


@player.route('/login_player', methods=['POST'])
def login_player():
    data = process_request_data(request)
    username = data.get('username')
    password = data.get('password')
    if username is None or password is None:
        return jsonify({"code": 1, 'message': 'Invalid request'})
    player = Player.query.filter_by(username=username).first()
    if player is None:
        return jsonify({"code": 1, 'message': 'Invalid username or password'})
    if not player.check_password(password):
        return jsonify({"code": 1, 'message': 'Invalid username or password'})

    session['username'] = username
    session['player_id'] = player.player_id
    return jsonify({"code": 0, 'message': 'Login successful'})


@player.route('/logout_player', methods=['POST'])
@player_required
def logout_player():
    session.pop('username', None)
    session.pop('player_id', None)
    return jsonify({"code": 0, 'message': 'Logout successful'})


@player.route('/modify_player_info', methods=['POST'])
@player_required
def modify_player_info():
    data = process_request_data(request)
    player_id = session.get('player_id')

    if not player_id:
        return jsonify({"code": 2, 'message': 'Player ID not found in session'})

    if not data:
        return jsonify({"code": 3, 'message': 'No data provided to update'})

    # 假设 'id' 字段不应该在请求数据中，因为它由 session 提供
    if "id" in data:
        data.pop('id')

    try:
        # 查找玩家记录
        player = Player.query.get(player_id)
        if not player:
            return jsonify({"code": 4, 'message': 'Player not found'})

        # 更新玩家信息
        for key, value in data.items():
            # 假设所有字段都存在于Player模型中，并且可以直接赋值
            setattr(player, key, value)

        # 提交数据库会话
        db.session.commit()

    except Exception as e:
        # 捕获所有异常，但通常最好捕获特定的异常类型
        db.session.rollback()  # 如果出现错误，回滚数据库会话
        return jsonify({"code": 1, 'message': 'Invalid request: ' + str(e)})

    return jsonify({"code": 0, 'message': 'Player info updated successfully'})


@player.route('/get_player_profile', methods=['GET'])
@player_required
def get_player_profile():
    player = Player.query.get(session['player_id'])
    if player is None:
        return jsonify({"code": 1, 'message': 'Invalid player ID'})

    return jsonify({"code": 0, "data": player.to_dict()})


# 用于跳转的根路由
@player.route('/')
@player_required_web
def root_player():
    return redirect(url_for('player.dashboard_player_web'))

@player.route('/dashboard_player_web')
@player_required_web
def dashboard_player_web():
    return render_template('player/dashboard_player_web.html')


# 用于跳转的退出登陆路由
@player.route('/logout_player_web')
@player_required_web
def logout_player_web():
    session.pop('username', None)
    session.pop('player_id', None)
    return redirect(url_for('player.root_player'))

# 注册界面
@player.route('/register_player_web')
def register_player_web():
    return render_template('player/register_player_web.html')


# 登陆界面
@player.route('/login_player_web')
def login_player_web():
    return render_template('player/login_player_web.html')
