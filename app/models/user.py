from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 關聯
    recipes = db.relationship('Recipe', backref='author', lazy=True, cascade="all, delete-orphan")
    shopping_list_items = db.relationship('ShoppingListItem', backref='user', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def create(cls, data):
        """新增一筆 User 記錄"""
        try:
            new_user = cls(**data)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            print(f"Error creating User: {e}")
            raise

    @classmethod
    def get_by_id(cls, user_id):
        """根據 ID 取得單筆記錄"""
        try:
            return cls.query.get(user_id)
        except Exception as e:
            print(f"Error getting User by id: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all Users: {e}")
            return []

    def update(self, data):
        """更新目前的記錄"""
        try:
            for key, value in data.items():
                setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating User: {e}")
            return False

    def delete(self):
        """刪除目前的記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting User: {e}")
            return False
