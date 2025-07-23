# app/schemas/comment_schema.py

from app.extensions import ma
from app.models.comment import Comment
from marshmallow import fields

from app.schemas.user_schema import UserSchema
from app.schemas.recipe_schema import RecipeSchema

class CommentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Comment
        load_instance = True

    id = ma.auto_field()
    text = ma.auto_field()
    created_at = ma.auto_field()
    user_id = ma.auto_field()
    recipe_id = ma.auto_field()

    user = fields.Nested(UserSchema, only=['id', 'username'])
    recipe = fields.Nested(RecipeSchema, only=['id', 'title'])
