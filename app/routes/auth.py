from flask import render_template, request, redirect, url_for
from . import auth_bp

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    HTTP Method: GET, POST
    GET: 顯示註冊表單。 (Template: auth/register.html)
    POST: 接收註冊資料，建立使用者後重導向至登入頁面。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    HTTP Method: GET, POST
    GET: 顯示登入表單。 (Template: auth/login.html)
    POST: 驗證使用者帳密，成功後儲存 Session 並重導向至首頁。
    """
    pass

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    HTTP Method: POST
    清除使用者的 Session，登出後重導向至首頁。
    """
    pass
