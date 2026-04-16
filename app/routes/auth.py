from flask import render_template, request, redirect, url_for, session, flash
from . import auth_bp
from ..models.user import User

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    user = User.query.first()
    if not user:
        user = User.create({'username': 'test', 'email': 'test@test.com', 'password_hash': 'xxx'})
    session['user_id'] = user.id
    return redirect(url_for('recipe.dashboard'))

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('main.index'))
