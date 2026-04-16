from flask import render_template, request, redirect, url_for
from . import list_bp

@list_bp.route('/')
def index():
    """
    HTTP Method: GET
    顯示當前使用者的購買清單項目列表。
    Template: list/index.html
    """
    pass

@list_bp.route('/add/<int:recipe_id>', methods=['POST'])
def add_from_recipe(recipe_id):
    """
    HTTP Method: POST
    將指定食譜的所有食材，加總後寫入購物清單 (ShoppingListItem)。
    完成後重導向至 /list 或原食譜頁面。
    """
    pass

@list_bp.route('/item/<int:item_id>', methods=['POST'])
def update_item(item_id):
    """
    HTTP Method: POST
    更新購物項目的狀態 (例如：切換 is_bought 打勾/取消)。
    """
    pass

@list_bp.route('/item/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    """
    HTTP Method: POST
    將該食材項目從清單中刪除。
    """
    pass
