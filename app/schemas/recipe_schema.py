from app.extensions import ma
from app.models.recipe import Recipe

class RecipeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Recipe
        load_instance = True

    id = ma.auto_field()
    title = ma.auto_field()
    description = ma.auto_field()
    ingredients = ma.auto_field()
    instructions = ma.auto_field()
    serving_size = ma.auto_field()
    image_url = ma.auto_field()
    country = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
    user_id = ma.auto_field()
    group_id = ma.auto_field()
