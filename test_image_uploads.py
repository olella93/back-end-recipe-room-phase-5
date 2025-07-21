#!/usr/bin/env python3

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = "http://localhost:5001/api"
TEST_IMAGE_PATH = "test_image.jpeg" 

def register_test_user():
    """Register a test user"""
    url = f"{BASE_URL}/auth/register"
    data = {
        "username": "testuser_images",
        "email": "testuser_images@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(url, json=data)
    print(f"Registration: {response.status_code}")
    if response.status_code == 201:
        print("✅ User registered successfully")
        return True
    else:
        print(f"❌ Registration failed: {response.json()}")
        return False

def login_test_user():
    """Login and get JWT token"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "testuser_images",
        "password": "testpassword123"
    }
    
    response = requests.post(url, json=data)
    print(f"Login: {response.status_code}")
    if response.status_code == 200:
        token = response.json()["token"]
        print("✅ Login successful")
        return token
    else:
        print(f"❌ Login failed: {response.json()}")
        return None

def test_profile_image_upload(token):
    """Test profile image upload"""
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"❌ Test image not found: {TEST_IMAGE_PATH}")
        print("Please add a test image file (jpg/png) to the project root")
        return False
    
    url = f"{BASE_URL}/auth/upload-profile-image"
    headers = {"Authorization": f"Bearer {token}"}
    
    with open(TEST_IMAGE_PATH, 'rb') as image_file:
        files = {"image": image_file}
        response = requests.post(url, headers=headers, files=files)
    
    print(f"Profile image upload: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Profile image uploaded successfully")
        print(f"Image URL: {result['profile_image']}")
        return True
    else:
        print(f"❌ Profile image upload failed: {response.json()}")
        return False

def create_test_recipe(token):
    """Create a test recipe"""
    url = f"{BASE_URL}/recipes"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "title": "Test Recipe with Image",
        "description": "A test recipe to demonstrate image upload",
        "ingredients": "Test ingredient 1, Test ingredient 2",
        "instructions": "Mix ingredients and cook",
        "country": "Test Country",
        "serving_size": 4
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(f"Recipe creation: {response.status_code}")
    if response.status_code == 201:
        recipe_id = response.json()["recipe_id"]
        print(f"✅ Recipe created successfully, ID: {recipe_id}")
        return recipe_id
    else:
        print(f"❌ Recipe creation failed: {response.json()}")
        return None

def test_recipe_image_upload(token, recipe_id):
    """Test recipe image upload"""
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"❌ Test image not found: {TEST_IMAGE_PATH}")
        return False
    
    url = f"{BASE_URL}/recipes/{recipe_id}/upload-image"
    headers = {"Authorization": f"Bearer {token}"}
    
    with open(TEST_IMAGE_PATH, 'rb') as image_file:
        files = {"image": image_file}
        response = requests.post(url, headers=headers, files=files)
    
    print(f"Recipe image upload: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Recipe image uploaded successfully")
        print(f"Image URL: {result['image_url']}")
        return True
    else:
        print(f"❌ Recipe image upload failed: {response.json()}")
        return False

def main():
    """Main test function"""
    print("🧪 Starting Recipe Room Image Upload Tests")
    print("=" * 50)
    
    # Check if Cloudinary is configured
    if not all([
        os.getenv('CLOUDINARY_CLOUD_NAME'),
        os.getenv('CLOUDINARY_API_KEY'),
        os.getenv('CLOUDINARY_API_SECRET')
    ]):
        print("❌ Cloudinary credentials not found in environment")
        print("Please set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET")
        return
    
    print("✅ Cloudinary credentials found")
    
    # Register test user 
    register_test_user()
    
    # Login
    token = login_test_user()
    if not token:
        return
    
    # Test profile image upload
    print("\n📸 Testing profile image upload...")
    test_profile_image_upload(token)
    
    # Create test recipe
    print("\n🍳 Creating test recipe...")
    recipe_id = create_test_recipe(token)
    if not recipe_id:
        return
    
    # Test recipe image upload
    print("\n📸 Testing recipe image upload...")
    test_recipe_image_upload(token, recipe_id)
    
    print("\n🎉 Image upload tests completed!")
    print("\nNote: Check your Cloudinary dashboard to see the uploaded images")

if __name__ == "__main__":
    main()
