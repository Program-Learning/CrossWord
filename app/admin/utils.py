# 定义 admin_required 装饰器  
from functools import wraps

from flask import jsonify, redirect, session, url_for

from app.admin.models import Admin


def admin_required(func):  
    @wraps(func)  
    def wrapper(*args, **kwargs):  
        # authentication
        if 'admin_id' not in session:  
            return jsonify({"code":1, 'message': 'admin_id not in session'}), 401  
  
        admin = Admin.query.get(session['admin_id'])  
        if not admin:  
            return jsonify({"code":1, 'message': 'Admin not found'}), 401  
  
        # 如果验证通过，则执行原始函数  
        return func(*args, **kwargs)  
  
    return wrapper  

def admin_required_web(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'admin_id' in session:
            if Admin.query.get(session['admin_id']):
                return func(*args, **kwargs)
            
        return redirect(url_for('admin.login_admin_web'))

    return wrapper

