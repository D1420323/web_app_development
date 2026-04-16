from flask import render_template, request, redirect, url_for
from . import main_bp

@main_bp.route('/')
def index():
    return "Main Index Placeholder. <a href='/recipes/'>Go to Recipes</a>"

@main_bp.route('/search')
def search():
    pass
