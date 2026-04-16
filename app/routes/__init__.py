from flask import Blueprint

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')
list_bp = Blueprint('list', __name__, url_prefix='/list')

# TODO: 這裡之後可在 application factory (create_app) 中註冊這些 Blueprint
