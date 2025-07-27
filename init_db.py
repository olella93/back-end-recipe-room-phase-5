#!/usr/bin/env python3
from app.main import create_app
from app.extensions import db

def init_db():
    """Initialize database tables"""
    app = create_app()
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
