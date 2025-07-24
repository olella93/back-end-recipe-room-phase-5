from app.extensions import ma
from app.models.bookmark import Bookmark

class BookmarkSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Bookmark
        load_instance = True

    id = ma.auto_field()
    user_id = ma.auto_field()
    recipe_id = ma.auto_field()
