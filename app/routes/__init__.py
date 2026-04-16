from flask import Blueprint

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')
list_bp = Blueprint('list', __name__, url_prefix='/list')

from . import main, auth, recipe, shopping_list
