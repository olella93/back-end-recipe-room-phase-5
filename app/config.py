import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.gotenv('SECRET_KEY', '2b2492e67a8f156fda78437999b439e0')
    SQLALCHEMY_DATABASE_URI = os.gotenv('DATABASE_URI', 'postgresql"//localhost/reciperoom')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-jwt-key")
    