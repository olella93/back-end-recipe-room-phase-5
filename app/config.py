import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '2b2492e67a8f156fda78437999b439e0')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://team_user:recipe123@localhost/recipe_room_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'
    