import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Secret keys
    SECRET_KEY = os.getenv('SECRET_KEY', '2b2492e67a8f156fda78437999b439e0')
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-jwt-key")

    # SQLAlchemy Database configuration
    SQLALCHEMY_DATABASE_URI = ('postgresql://citikom:newpassword@localhost:5432/recipe_room'

    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS
    CORS_HEADERS = 'Content-Type'

    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
