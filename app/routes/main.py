from flask import render_template, request, redirect, url_for
from . import main_bp

@main_bp.route('/')
def index():
    """
    HTTP Method: GET
    顯示系統首頁，包含最新與推薦的食譜列表。
    Template: main/index.html
    """
    pass

@main_bp.route('/search')
def search():
    """
    HTTP Method: GET
    接收 URL parameters (q 或 ingredients)，搜尋後回傳對應的食譜結果。
    Template: main/search.html
    """
    pass
