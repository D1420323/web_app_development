from . import db

class RecipeStep(db.Model):
    __tablename__ = 'recipe_step'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text, nullable=False)

    @classmethod
    def create(cls, data):
        new_item = cls(**data)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    @classmethod
    def get_by_id(cls, item_id):
        return cls.query.get(item_id)

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
