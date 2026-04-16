from flask import Flask
from .models import db
from .routes import main_bp, auth_bp, recipe_bp, list_bp
import os

def create_app(test_config=None):
    # 建立並設定 Flask app
    app = Flask(__name__, instance_relative_config=True)
    
    # 基本設定
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI='sqlite:///database.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # 載入額外的設定（如果有的話）
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 確保 instance 目錄存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化 db
    db.init_app(app)
    
    # 如果有需要建立 table 可在此執行 (若不用 schema.sql)
    with app.app_context():
        db.create_all()

    # 註冊 Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(list_bp)

    return app
