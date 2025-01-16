from app.admin.models import Admin
from app.admin.utils import admin_required, admin_required_web
from app.models import db, papers, poems, history_insert_records
from app.utils import process_request_data
from werkzeug.utils import secure_filename
import csv
import json
import os
from config import Config
from flask import (
    session,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    jsonify,
    Blueprint,
)
admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/login_admin', methods=['POST'])
def login_admin():
    # process data
    data = process_request_data(request)
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"code": 1, 'message': 'Missing username or password'}), 400
    admin = Admin.query.filter_by(username=username).first()
    if admin and admin.check_password(password):
        # Valid credentials, set session or token for authentication
        # Example of storing admin_id in session
        session['admin_id'] = admin.id
        session['username'] = admin.username
        return jsonify({"code": 0, 'message': 'Login successful', "data": {"id": session["admin_id"], "username": session["username"]
                                                                           }})
    else:
        return jsonify({"code": 1, 'message': 'Invalid username or password'})


@admin.route('/logout_admin', methods=['POST'])
@admin_required
def logout_admin():
    session.pop('username', None)
    session.pop('admin_id', None)
    response = jsonify({"code": 0, 'message': 'Logout successful'})
    response.delete_cookie('session', path='/')
    return response

# tested


@admin.route('/add_admin', methods=['POST'])
@admin_required
def add_admin():
    # process data
    data = process_request_data(request)
    if Admin.query.filter_by(username=data.get('username')).first():
        return jsonify({"code": 1, 'message': 'Username already exists'}), 400
    try:
        new_admin = Admin(**data)
    except:
        return jsonify({"code": 1, 'message': 'Invalid request'}), 400
    try:
        db.session.add(new_admin)
        db.session.commit()
    except:
        return jsonify({"code": 1, 'message': 'Error adding admin'}), 500
    return jsonify({"code": 0, 'message': 'Admin added successfully', "data": {"id": new_admin.id, "username": new_admin.username}})


@admin.route('/modify_admin', methods=['POST'])
@admin_required
def modify_admin():
    # process data
    data = process_request_data(request)
    id = data.pop('id')

    admin_to_modify = Admin.query.get(id)
    if not admin_to_modify:
        return jsonify({"code": 1, 'message': 'Admin not found'}), 404
    admin_to_modify.modify(**data)

    db.session.commit()
    return jsonify({"code": 0, 'message': 'Admin modified successfully', "data": admin_to_modify.to_dict()})


@admin.route('/query_admin', methods=['POST'])
@admin_required
def query_admin():

    data = process_request_data(request)
    try:
        admins_to_query = Admin.query.filter_by(**data).all()
    except:
        return jsonify({"code": 1, 'message': 'Invalid request'}), 400
    return jsonify({"code": 0, 'message': 'Admins queried successfully', "data": [admin.to_dict() for admin in admins_to_query]})


@admin.route('/delete_admin', methods=['POST'])
@admin_required
def delete_admin():

    data = process_request_data(request)
    id = data.pop('id')
    if not id:
        return jsonify({"code": 1, 'message': 'id not in data'}), 400

    admin_to_delete = Admin.query.get(id)
    if not admin_to_delete:
        return jsonify({"code": 1, 'message': 'Admin not found'}), 404

    db.session.delete(admin_to_delete)
    db.session.commit()
    return jsonify({"code": 0, 'message': 'Admin deleted successfully'}), 200

# 用于跳转的根路由
@admin.route('/')
@admin_required_web
def root_admin():
    return redirect(url_for('admin.dashboard_admin_web'))


# 使用ajax而不是原生表单提交
@admin.route('/dashboard_admin_web')
@admin_required_web
def dashboard_admin_web():
    return render_template('admin/dashboard_admin_web.html')


# 用于跳转的退出登陆路由
@admin.route('/logout_admin_web')
def logout_admin_web():
    session.pop('username', None)
    session.pop('admin_id', None)
    return redirect(url_for('admin.root_admin'))


@admin.route('/login_admin_web')
def login_admin_web():
    return render_template('admin/login_admin_web.html')

# 上传csv 从csv导入有效诗词，即题库
@admin.route("/upload_csv", methods=["GET", "POST"])
@admin_required_web
def upload_csv():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(
                os.path.join(Config.UPLOAD_FOLDER, filename)
            )  # 假设你有一个UPLOAD_FOLDER配置

            # 读取 CSV 文件并插入到数据库
            try:
                with open(
                    os.path.join(Config.UPLOAD_FOLDER, filename),
                    "r",
                    encoding="utf-8",
                ) as csvfile:
                    csvreader = csv.reader(csvfile)
                    for row in csvreader:
                        if row:  # 确保行不为空
                            poem_text = row[0].strip()  # 假设 CSV 文件只有一列
                            poem = poems(poem_text)
                            db.session.add(poem)

            except UnicodeDecodeError:
                with open(
                    os.path.join(Config.UPLOAD_FOLDER, filename),
                    "r",
                    encoding="cp936",
                ) as csvfile:
                    csvreader = csv.reader(csvfile)
                    for row in csvreader:
                        if row:  # 确保行不为空
                            # 替换空格
                            poem_text = row[0].strip()  # 假设 CSV 文件只有一列
                            poem = poems(poem_text)
                            db.session.add(poem)

            db.session.commit()
            flash("CSV file imported successfully!")
            return "上传成功"
        else:
            flash("Allowed file types is only csv")
            return redirect(request.url)
    else:
        return render_template("admin/upload_csv.html")  # 显示一个文件上传表单

# 检查文件扩展名是否允许
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# 你可以设置允许的扩展名
ALLOWED_EXTENSIONS = {"csv"}


# 数据库展示函数 调试用途
@admin.route("/show")
@admin_required_web
def show():
    return render_template(
        "admin/dev_show.html",
        papers=papers.query.all(),
        poems=poems.query.all(),
        historys=history_insert_records.query.all(),
    )


# 试卷添加函数 调试用途 测试了发现用不到但是还是先留着
@admin.route("/new_paper", methods=["GET", "POST"])
@admin_required_web
def new_paper():
    if request.method == "POST":
        if not request.form["paper"]:
            flash("Please enter all the fields", "error")
        else:
            paper = papers(request.form["paper"])
            print(paper)
            db.session.add(paper)
            db.session.commit()
            flash("Record was successfully added")
            return redirect(url_for("admin.show"))
    return render_template("admin/dev_new_paper.html")


# 单句诗词添加函数 调试用途
@admin.route("/new_poem", methods=["GET", "POST"])
@admin_required_web
def new_poem():
    if request.method == "POST":
        if not request.form["poem"]:
            flash("Please enter all the fields", "error")
        else:
            poem = poems(request.form["poem"])
            print(poem)
            db.session.add(poem)
            db.session.commit()
            flash("Record was successfully added")
            return redirect(url_for("admin.show"))
    return render_template("admin/dev_new_poem.html")
