from . import db
from datetime import datetime

class Recipe(db.Model):
    __tablename__ = 'recipe'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    image_path = db.Column(db.String(255))
    default_portions = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True, cascade="all, delete-orphan")
    steps = db.relationship('RecipeStep', backref='recipe', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def create(cls, data):
        """新增一筆 Recipe 記錄"""
        try:
            new_recipe = cls(**data)
            db.session.add(new_recipe)
            db.session.commit()
            return new_recipe
        except Exception as e:
            db.session.rollback()
            print(f"Error creating Recipe: {e}")
            raise

    @classmethod
    def get_by_id(cls, recipe_id):
        """根據 ID 取得單筆記錄"""
        try:
            return cls.query.get(recipe_id)
        except Exception as e:
            print(f"Error getting Recipe by id: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all Recipes: {e}")
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
            print(f"Error updating Recipe: {e}")
            return False

    def delete(self):
        """刪除目前的記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting Recipe: {e}")
            return False
