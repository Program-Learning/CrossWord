from datetime import datetime
from functools import wraps
import json
import random
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


@player.route('/logout_player', methods=['POST', 'GET'])
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
    my_papers = papers.query.filter_by(playerID=session['player_id']).all()
    return render_template('player/dashboard_player_web.html', my_papers=my_papers)


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

@player.route('/list_paper')
@player_required
def list_paper():
    try:
        my_papers = papers.query.filter_by(playerID=session['player_id']).all()
    except:
        return jsonify({"code": 1, 'message': 'Invalid request'}), 400
    return jsonify({"code": 0, 'message': 'Papers queried successfully', "data": [paper.to_dict() for paper in my_papers]})


# 试卷生成函数(json)
@player.route("/genPaperJson")
def genPaperJson(width: int = 28, height: int = 21):
    init_poems = poems.query.all()
    selected_poem = random.choice(init_poems)

    # 初始化结果
    result = {
        "score": 0,
        "width": width,
        "height": height,
        "data": [["" for _ in range(width)] for _ in range(height)],
    }

    # 获取诗句文本并计算其长度
    poem_text = selected_poem.poem
    poem_length = len(poem_text)

    # 随机选择起始行和列（确保不会超出边界）
    directions = ["right", "down", "left", "up"]
    direction = random.choice(directions)
    start_row = random.randint(0, height - 1)
    start_col = random.randint(0, width - 1)

    current_row, current_col = start_row, start_col

    for char in poem_text:
        if direction == "right":
            if current_col < width:
                result["data"][current_row][current_col] = char
                current_col += 1
                if current_col >= width:
                    break
            else:
                break

        elif direction == "down":
            if current_row < height:
                result["data"][current_row][current_col] = char
                current_row += 1
                if current_row >= height:
                    break
            else:
                break

        elif direction == "left":
            if current_col >= 0:
                result["data"][current_row][current_col] = char
                current_col -= 1
                if current_col < 0:
                    break
            else:
                break

        elif direction == "up":
            if current_row >= 0:
                result["data"][current_row][current_col] = char
                current_row -= 1
                if current_row < 0:
                    break
            else:
                break

    return json.dumps(result)

@player.route('/create_game')
@player_required
def create_game():
    paper = papers(session.get('player_id'),genPaperJson(28, 21))
    db.session.add(paper)
    db.session.commit()
    return redirect(url_for('player.play', id=paper.id))

@player.route('/play/<int:id>')
@player_required
def play(id):
    try:
        paper = papers.query.get(id)
    except:
        return "错误"
    if paper.playerID != session.get('player_id'):
        return "无权限"
    return render_template('player/game.html', score=paper.score, PaperID=id, PaperJson=json.loads(paper.paper))


# 用户答题请求上传函数
@player.route("/submit/<int:paper_id>", methods=["POST"])
@player_required
def submit(paper_id):
    if request.method == "POST":
        # 检查请求头是否包含 application/json
        if (
            "Content-Type" in request.headers
            and request.headers["Content-Type"] == "application/json"
        ):
            # 解析 JSON 数据
            data = request.json
            # 这里可以处理 data 字典中的值
            # 例如，你可以从 data 中获取 poem, row, col, direction 等值
            poem = data.get("poem", "")
            paperID = paper_id
            paper = papers.query.get(paperID)
            if paper.playerID != session.get('player_id'):
                return "无权限"
            already_exist = history_insert_records.query.filter_by(
                history=poem, paperID=paperID
            ).first()
            if already_exist:
                return (
                    jsonify(
                        {
                            "status": "failed",
                            "message": "The poem you entered has already been filled in.",
                        }
                    ),
                    200,
                )
            row = data.get("row", "")
            col = data.get("col", "")
            direction = data.get("direction", "")

            # 在这里你可以进行其他业务逻辑处理，比如保存到数据库等
            if poem == "" or row == "" or col == "" or direction == "" or paperID == "":
                return jsonify({"status": "failed", "message": "param not enough"}), 200
            # 返回一个失败的 JSON 响应
            insert_status = json.loads(
                can_insert_json(poem, row, col, direction, paperID)
            )
            if insert_status["success"] == True:
                updatePaper(insert_status["paper"], paperID)
                history_insert_record = history_insert_records(paperID, poem)
                db.session.add(history_insert_record)
                db.session.commit()
                # 返回一个成功的 JSON 响应
                return (
                    jsonify(
                        {"status": "success", "message": "Data received successfully."}
                    ),
                    200,
                )
            return (
                jsonify(
                    {
                        "status": "failed",
                        "message": "insert failed:" + insert_status["message"],
                    }
                ),
                200,
            )
        else:
            # 如果请求头不是 application/json，则返回错误
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Invalid Content-Type, expected application/json",
                    }
                ),
                415,
            )
    else:
        # 如果请求方法不是 POST，则返回错误
        return (
            jsonify(
                {"status": "error", "message": "Invalid request method, expected POST"}
            ),
            405,
        )


# 检查诗词是否存在
def poem_exist(poem: str) -> bool:
    _poem = poems.query.filter_by(poem=poem).first()
    if _poem:
        return True
    return False


# 计算分数函数
def calc_score(dup):
    return 2**dup


# 检查插入是否合法
def _can_insert(
    poem: str, row: int, col: int, direction: str, paperID: int
) -> tuple[bool, any]:
    paper_entity = get_paper_by_id(paperID)
    paper = json.loads(paper_entity.paper)
    if not poem_exist(poem):
        return (False, "Poem does not exist")
        # return json.dumps({"success": False, "message": "Poem does not exist"})
    width = paper["width"]
    height = paper["height"]
    data = paper["data"]
    row -= 1
    col -= 1
    score = paper["score"]
    dup = 0

    # 检查方向（假设 "right" 代表横向，"down" 代表纵向）
    if direction not in ["right", "down", "left", "up"]:
        return (False, "Invalid direction")
        # return json.dumps({"success": False, "message": "Invalid direction"})

        # 检查位置是否在表格范围内
    if row < 0 or row >= height or col < 0 or col >= width:
        return (False, "Position out of bounds")
        # return json.dumps({"success": False, "message": "Position out of bounds"})

        # 根据方向检查是否有足够的空间插入诗词片段
    if direction == "right":
        if col + len(poem) > width:
            return (False, "Not enough space right")
            # return json.dumps({"success": False, "message": "Not enough space right"})
        for i, char in enumerate(poem):
            if data[row][col + i] != "":
                if data[row][col + i] != char:
                    return (False, "Conflict with existing content right")
                    # return json.dumps({"success": False, "message": "Conflict with existing content right"})
                dup += 1
                # 插入诗词片段
        for i, char in enumerate(poem):
            data[row][col + i] = char
    elif direction == "down":
        if row + len(poem) > height:
            return (False, "Not enough space down")
            # return json.dumps({"success": False, "message": "Not enough space down"})
        for i, char in enumerate(poem):
            if data[row + i][col] != "":
                if data[row + i][col] != char:
                    return (False, "Conflict with existing content down")
                    # return json.dumps({"success": False, "message": "Conflict with existing content down"})
                dup += 1
                # 插入诗词片段
        for i, char in enumerate(poem):
            data[row + i][col] = char
    elif direction == "left":
        if col - len(poem) + 1 < 0:
            return (False, "Not enough space left")
            # return json.dumps({"success": False, "message": "Not enough space left"})
        for i, char in enumerate(poem):  # 反向遍历字符串以从左边开始插入
            if data[row][col - i] != "":
                if data[row][col - i] != char:
                    return (False, "Conflict with existing content left")
                    # return json.dumps({"success": False, "message": "Conflict with existing content left"})
                dup += 1
                # 插入诗词片段
        for i, char in enumerate(poem):
            data[row][col - i] = char
    elif direction == "up":
        if row - len(poem) + 1 < 0:
            return (False, "Not enough space up")
            # return json.dumps({"success": False, "message": "Not enough space up"})
        for i, char in enumerate(poem):  # 反向遍历字符串以从上边开始插入
            if data[row - i][col] != "":
                if data[row - i][col] != char:
                    return (False, "Conflict with existing content up")
                    # return json.dumps({"success": False, "message": "Conflict with existing content up"})
                dup += 1
        # 插入诗词片段
        for i, char in enumerate(poem):
            data[row - i][col] = char

    paper["score"] += calc_score(dup)
    paper_entity.score += calc_score(dup)
    db.session.commit()
    # 返回更新后的JSON字符串
    return (True, paper)
    # return json.dumps({"success": True, "paper": paper})


def can_insert_json(poem, row, col, direction, paperID) -> str:
    can_insert, message = _can_insert(poem, row, col, direction, paperID)
    if can_insert:
        return json.dumps({"success": True, "paper": message})
    else:
        return json.dumps({"success": False, "message": message})


# 通过试卷id获取试卷函数
def get_paper_by_id(paperID):
    paper = papers.query.get(paperID)
    return paper


# 更新试卷函数
def updatePaper(paperStr: str, paperID):
    paper = papers.query.get(paperID)
    paper.paper = json.dumps(paperStr)
    db.session.commit()
