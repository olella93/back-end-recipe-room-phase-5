# app/tests/test_bookmarks.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "http://localhost:5003/api"

def test_bookmark_flow():
    user = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    requests.post(f"{BASE_URL}/auth/register", json=user)
    login = requests.post(f"{BASE_URL}/auth/login", json={"username": user["username"], "password": user["password"]})
    token = login.json()["token"]

    headers = {"Authorization": f"Bearer {token}"}

    recipe = {
        "title": "Test Bookmark Recipe",
        "description": "Just testing",
        "ingredients": "Stuff",
        "instructions": "Mix",
        "country": "Kenya",
        "serving_size": 2
    }
    res = requests.post(f"{BASE_URL}/recipes", headers=headers, json=recipe)
    recipe_id = res.json()["recipe_id"]

    res = requests.post(f"{BASE_URL}/bookmarks", headers=headers, json={"recipe_id": recipe_id})
    print("Bookmark:", res.status_code, res.json())

    res = requests.get(f"{BASE_URL}/bookmarks", headers=headers)
    print("Bookmarks:", res.status_code, res.json())

    bookmark_id = res.json()[0]["id"]
    res = requests.delete(f"{BASE_URL}/bookmarks/{bookmark_id}", headers=headers)
    print("Deleted:", res.status_code, res.json())

if __name__ == "__main__":
    test_bookmark_flow()
