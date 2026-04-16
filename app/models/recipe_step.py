from . import db

class RecipeStep(db.Model):
    __tablename__ = 'recipe_step'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text, nullable=False)

    @classmethod
    def create(cls, data):
        """新增一筆 RecipeStep 記錄"""
        try:
            new_item = cls(**data)
            db.session.add(new_item)
            db.session.commit()
            return new_item
        except Exception as e:
            db.session.rollback()
            print(f"Error creating RecipeStep: {e}")
            raise

    @classmethod
    def get_by_id(cls, item_id):
        """根據 ID 取得單筆記錄"""
        try:
            return cls.query.get(item_id)
        except Exception as e:
            print(f"Error getting RecipeStep by id: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all RecipeSteps: {e}")
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
            print(f"Error updating RecipeStep: {e}")
            return False

    def delete(self):
        """刪除目前的記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting RecipeStep: {e}")
            return False
