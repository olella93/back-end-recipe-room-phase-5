from app.extensions import ma
from app.models.bookmark import Bookmark
from app.schemas.recipe_schema import RecipeSchema
from marshmallow import fields

class BookmarkSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Bookmark
        load_instance = True

    id = ma.auto_field()
    user_id = ma.auto_field()
    recipe_id = ma.auto_field()
    recipe = fields.Nested(RecipeSchema)