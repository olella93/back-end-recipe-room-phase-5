#!/usr/bin/env python3

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = "http://localhost:5003/api"

def register_and_login_user(username, email, password):
    """Register and login a user, return JWT token"""
    # Try to register (might fail if user exists)
    register_url = f"{BASE_URL}/auth/register"
    register_data = {
        "username": username,
        "email": email,
        "password": password
    }
    requests.post(register_url, json=register_data) 
    
    # Login
    login_url = f"{BASE_URL}/auth/login"
    login_data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(login_url, json=login_data)
    if response.status_code == 200:
        return response.json()["token"]
    else:
        print(f"Login failed: {response.json()}")
        return None

def create_test_recipe(token, title="Test Recipe for Bookmarks"):
    """Create a test recipe and return recipe ID"""
    url = f"{BASE_URL}/recipes"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "title": title,
        "description": "A test recipe to demonstrate bookmark functionality",
        "ingredients": "Test ingredient 1, Test ingredient 2",
        "instructions": "Mix ingredients and cook",
        "country": "Test Country",
        "serving_size": 4
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        recipe_id = response.json()["recipe_id"]
        print(f"✓ Recipe '{title}' created successfully, ID: {recipe_id}")
        return recipe_id
    else:
        print(f"✗ Recipe creation failed: {response.json()}")
        return None

def test_create_bookmark(token, recipe_id):
    """Test creating a bookmark"""
    url = f"{BASE_URL}/bookmarks"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "recipe_id": recipe_id
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(f"Create bookmark: {response.status_code}")
    if response.status_code == 201:
        bookmark = response.json()
        print(f"✓ Bookmark created successfully, ID: {bookmark['id']}")
        print(f"  User ID: {bookmark['user_id']}")
        print(f"  Recipe ID: {bookmark['recipe_id']}")
        return bookmark['id']
    else:
        print(f"✗ Bookmark creation failed: {response.json()}")
        return None

def test_get_user_bookmarks(token):
    """Test getting user's bookmarks"""
    url = f"{BASE_URL}/bookmarks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Get user bookmarks: {response.status_code}")
    if response.status_code == 200:
        bookmarks = response.json()
        print(f"✓ Retrieved {len(bookmarks)} bookmarks")
        for i, bookmark in enumerate(bookmarks, 1):
            print(f"  Bookmark {i}: Recipe ID {bookmark['recipe_id']} (Bookmark ID: {bookmark['id']})")
        return bookmarks
    else:
        print(f"✗ Failed to get bookmarks: {response.json()}")
        return []

def test_delete_bookmark(token, bookmark_id):
    """Test deleting a bookmark"""
    url = f"{BASE_URL}/bookmarks/{bookmark_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.delete(url, headers=headers)
    print(f"Delete bookmark: {response.status_code}")
    if response.status_code == 200:
        print(f"✓ Bookmark deleted successfully")
        return True
    else:
        print(f"✗ Bookmark deletion failed: {response.json()}")
        return False

def test_duplicate_bookmark(token, recipe_id):
    """Test creating duplicate bookmark (should fail)"""
    url = f"{BASE_URL}/bookmarks"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "recipe_id": recipe_id
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(f"Duplicate bookmark attempt: {response.status_code}")
    if response.status_code == 400:
        print("✓ Duplicate bookmark correctly rejected")
        return True
    else:
        print(f"✗ Unexpected response: {response.status_code} - {response.json()}")
        return False

def test_bookmark_nonexistent_recipe(token):
    """Test bookmarking a non-existent recipe"""
    url = f"{BASE_URL}/bookmarks"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "recipe_id": 99999  # Non-existent recipe ID
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(f"Bookmark nonexistent recipe: {response.status_code}")
    if response.status_code == 404:
        print("✓ Nonexistent recipe correctly rejected")
        return True
    else:
        print(f"✗ Unexpected response: {response.status_code} - {response.json()}")
        return False

def test_unauthorized_bookmark_deletion(token1, token2, bookmark_id):
    """Test unauthorized bookmark deletion"""
    url = f"{BASE_URL}/bookmarks/{bookmark_id}"
    headers = {
        "Authorization": f"Bearer {token2}" 
    }
    
    response = requests.delete(url, headers=headers)
    print(f"Unauthorized delete attempt: {response.status_code}")
    if response.status_code == 403:
        print("✓ Unauthorized delete correctly blocked")
        return True
    else:
        print(f"✗ Unexpected response: {response.status_code} - {response.json()}")
        return False

def main():
    """Main test function"""
    print("Testing Recipe Room Bookmark Features")
    print("=" * 50)
    
    # Setup test users
    print("\n=== Setting up test users ===")
    token1 = register_and_login_user("bookmarkuser1", "bookmarkuser1@example.com", "password123")
    token2 = register_and_login_user("bookmarkuser2", "bookmarkuser2@example.com", "password123")
    
    if not token1 or not token2:
        print("Failed to setup test users")
        return
    
    print("✓ Test users created and logged in")
    
    # Create test recipes
    print("\n=== Creating test recipes ===")
    recipe_id1 = create_test_recipe(token1, "Amazing Pasta Recipe")
    recipe_id2 = create_test_recipe(token1, "Delicious Soup Recipe")
    recipe_id3 = create_test_recipe(token2, "Healthy Salad Recipe")
    
    if not all([recipe_id1, recipe_id2, recipe_id3]):
        print("Failed to create test recipes")
        return
    
    # Test bookmark creation
    print("\n=== Testing bookmark creation ===")
    bookmark_id1 = test_create_bookmark(token1, recipe_id1)  # User bookmarks own recipe
    bookmark_id2 = test_create_bookmark(token1, recipe_id3)  # User bookmarks another user's recipe
    bookmark_id3 = test_create_bookmark(token2, recipe_id1)  # Different user bookmarks recipe
    
    if not all([bookmark_id1, bookmark_id2, bookmark_id3]):
        print("Failed to create test bookmarks")
        return
    
    # Test getting user bookmarks
    print("\n=== Testing bookmark retrieval ===")
    print("User 1's bookmarks:")
    user1_bookmarks = test_get_user_bookmarks(token1)
    print("User 2's bookmarks:")
    user2_bookmarks = test_get_user_bookmarks(token2)
    
    # Test duplicate bookmark
    print("\n=== Testing duplicate bookmark prevention ===")
    test_duplicate_bookmark(token1, recipe_id1)
    
    # Test error cases
    print("\n=== Testing error cases ===")
    
    # Test bookmarking non-existent recipe
    print("Testing bookmark of nonexistent recipe...")
    test_bookmark_nonexistent_recipe(token1)
    
    # Test creating bookmark without recipe_id
    print("Testing bookmark creation without recipe_id...")
    url = f"{BASE_URL}/bookmarks"
    headers = {
        "Authorization": f"Bearer {token1}",
        "Content-Type": "application/json"
    }
    data = {}  # Missing recipe_id
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 400:
        print("✓ Missing recipe_id error handled correctly")
    else:
        print(f"✗ Unexpected response: {response.status_code} - {response.json()}")
    
    # Test unauthorized actions
    print("\n=== Testing unauthorized actions ===")
    test_unauthorized_bookmark_deletion(token1, token2, bookmark_id1)
    
    # Test bookmark deletion
    print("\n=== Testing bookmark deletion ===")
    test_delete_bookmark(token1, bookmark_id2)
    
    # Verify bookmarks after deletion
    print("\n=== Verifying bookmarks after deletion ===")
    print("User 1's bookmarks after deletion:")
    test_get_user_bookmarks(token1)
    
    print("\n" + "=" * 50)
    print("Bookmark feature testing completed!")
    print("\nFeatures tested:")
    print("✓ Bookmark creation with proper validation")
    print("✓ User bookmark retrieval")
    print("✓ Bookmark deletion by owner")
    print("✓ Duplicate bookmark prevention")
    print("✓ Authorization checks (users can only delete their own bookmarks)")
    print("✓ Error handling for invalid requests")
    print("✓ Cross-user recipe bookmarking")

if __name__ == "__main__":
    main()
