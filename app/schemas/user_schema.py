from app.extensions import ma
from app.models.user import User

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    profile_image = ma.auto_field()
    created_at = ma.auto_field()
