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
        new_recipe = cls(**data)
        db.session.add(new_recipe)
        db.session.commit()
        return new_recipe

    @classmethod
    def get_by_id(cls, recipe_id):
        return cls.query.get(recipe_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
