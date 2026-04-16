from flask import render_template, request, redirect, url_for
from . import recipe_bp

@recipe_bp.route('/')
def dashboard():
    """
    HTTP Method: GET
    顯示當前使用者的「個人食譜面板」，列出自己收藏/建立的食譜。
    Template: recipe/dashboard.html
    """
    pass

@recipe_bp.route('/<int:id>')
def detail(id):
    """
    HTTP Method: GET
    顯示單一食譜的詳細內容 (包含食材、步驟)。前端會處理份量動態換算。
    Template: recipe/detail.html
    """
    pass

@recipe_bp.route('/new', methods=['GET', 'POST'])
def new():
    """
    HTTP Method: GET, POST
    GET: 顯示新增食譜的表單。 (Template: recipe/new.html)
    POST: 接收表單資料，寫入相關資料表 (Recipe, Ingredient, RecipeStep) 後重導至該食譜詳情頁。
    """
    pass

@recipe_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    HTTP Method: GET, POST
    GET: 載入舊食譜資料顯示於編輯表單。 (Template: recipe/edit.html)
    POST: 接收更新的表單資料，更新資料表後重導至該食譜詳情頁。
    （需驗證是否為作者本人操作）
    """
    pass

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    HTTP Method: POST
    刪除指定 ID 的食譜，刪除後重導向至個人面板。
    （需驗證是否為作者本人操作）
    """
    pass
