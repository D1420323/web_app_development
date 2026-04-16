from . import db
from datetime import datetime

class ShoppingListItem(db.Model):
    __tablename__ = 'shopping_list_item'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ingredient_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50))
    is_bought = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, data):
        """新增一筆 ShoppingListItem 記錄"""
        try:
            new_item = cls(**data)
            db.session.add(new_item)
            db.session.commit()
            return new_item
        except Exception as e:
            db.session.rollback()
            print(f"Error creating ShoppingListItem: {e}")
            raise

    @classmethod
    def get_by_id(cls, item_id):
        """根據 ID 取得單筆記錄"""
        try:
            return cls.query.get(item_id)
        except Exception as e:
            print(f"Error getting ShoppingListItem by id: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all ShoppingListItems: {e}")
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
            print(f"Error updating ShoppingListItem: {e}")
            return False

    def delete(self):
        """刪除目前的記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting ShoppingListItem: {e}")
            return False
