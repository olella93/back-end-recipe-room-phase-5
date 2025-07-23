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
    # Try to register (fail if user exists)
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

def create_test_recipe(token):
    """Create a test recipe and return recipe ID"""
    url = f"{BASE_URL}/recipes"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "title": "Test Recipe for Comments",
        "description": "A test recipe to demonstrate comment functionality",
        "ingredients": "Test ingredient 1, Test ingredient 2",
        "instructions": "Mix ingredients and cook",
        "country": "Test Country",
        "serving_size": 4
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        recipe_id = response.json()["recipe_id"]
        print(f"✓ Recipe created successfully, ID: {recipe_id}")
        return recipe_id
    else:
        print(f"✗ Recipe creation failed: {response.json()}")
        return None

def test_create_comment(token, recipe_id, comment_text):
    """Test creating a comment"""
    url = f"{BASE_URL}/comments/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "text": comment_text,
        "recipe_id": recipe_id
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(f"Create comment: {response.status_code}")
    if response.status_code == 201:
        comment = response.json()
        print(f"✓ Comment created successfully, ID: {comment['id']}")
        print(f"  Text: {comment['text']}")
        print(f"  User ID: {comment['user_id']}")
        print(f"  Recipe ID: {comment['recipe_id']}")
        return comment['id']
    else:
        print(f"✗ Comment creation failed: {response.json()}")
        return None

def test_get_comments_for_recipe(recipe_id):
    """Test getting all comments for a recipe"""
    url = f"{BASE_URL}/comments/{recipe_id}"
    
    response = requests.get(url)
    print(f"Get comments for recipe: {response.status_code}")
    if response.status_code == 200:
        comments = response.json()
        print(f"✓ Retrieved {len(comments)} comments for recipe {recipe_id}")
        for i, comment in enumerate(comments, 1):
            print(f"  Comment {i}: {comment['text'][:50]}..." if len(comment['text']) > 50 else f"  Comment {i}: {comment['text']}")
        return comments
    else:
        print(f"✗ Failed to get comments: {response.json()}")
        return []

def test_update_comment(token, comment_id, new_text):
    """Test updating a comment"""
    url = f"{BASE_URL}/comments/{comment_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "text": new_text
    }
    
    response = requests.put(url, headers=headers, json=data)
    print(f"Update comment: {response.status_code}")
    if response.status_code == 200:
        comment = response.json()
        print(f"✓ Comment updated successfully")
        print(f"  New text: {comment['text']}")
        return True
    else:
        print(f"✗ Comment update failed: {response.json()}")
        return False

def test_delete_comment(token, comment_id):
    """Test deleting a comment"""
    url = f"{BASE_URL}/comments/{comment_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.delete(url, headers=headers)
    print(f"Delete comment: {response.status_code}")
    if response.status_code == 200:
        print(f"✓ Comment deleted successfully")
        return True
    else:
        print(f"✗ Comment deletion failed: {response.json()}")
        return False

def test_unauthorized_actions(token1, token2, comment_id):
    """Test unauthorized comment actions"""
    print("\n=== Testing Unauthorized Actions ===")
    
    # Try to update another user's comment
    url = f"{BASE_URL}/comments/{comment_id}"
    headers = {
        "Authorization": f"Bearer {token2}",
        "Content-Type": "application/json"
    }
    data = {
        "text": "Trying to update someone else's comment"
    }
    
    response = requests.put(url, headers=headers, json=data)
    print(f"Unauthorized update attempt: {response.status_code}")
    if response.status_code == 403:
        print("✓ Unauthorized update correctly blocked")
    else:
        print(f"✗ Unexpected response: {response.json()}")
    
    # Try to delete another user's comment
    response = requests.delete(url, headers=headers)
    print(f"Unauthorized delete attempt: {response.status_code}")
    if response.status_code == 403:
        print("✓ Unauthorized delete correctly blocked")
    else:
        print(f"✗ Unexpected response: {response.json()}")

def main():
    """Main test function"""
    print("Testing Recipe Room Comment Features")
    print("=" * 50)
    
    # Setup test users
    print("\n=== Setting up test users ===")
    token1 = register_and_login_user("commentuser1", "commentuser1@example.com", "password123")
    token2 = register_and_login_user("commentuser2", "commentuser2@example.com", "password123")
    
    if not token1 or not token2:
        print("Failed to setup test users")
        return
    
    print("✓ Test users created and logged in")
    
    # Create test recipe
    print("\n=== Creating test recipe ===")
    recipe_id = create_test_recipe(token1)
    if not recipe_id:
        return
    
    # Test comment creation
    print("\n=== Testing comment creation ===")
    comment_id1 = test_create_comment(token1, recipe_id, "This recipe looks amazing! Can't wait to try it.")
    comment_id2 = test_create_comment(token2, recipe_id, "I made this yesterday and it was delicious!")
    comment_id3 = test_create_comment(token1, recipe_id, "Thanks for the feedback everyone!")
    
    if not all([comment_id1, comment_id2, comment_id3]):
        print("Failed to create test comments")
        return
    
    # Test getting comments for recipe
    print("\n=== Testing comment retrieval ===")
    comments = test_get_comments_for_recipe(recipe_id)
    
    # Test comment update
    print("\n=== Testing comment update ===")
    test_update_comment(token1, comment_id1, "This recipe looks absolutely amazing! Can't wait to try it tonight.")
    
    # Test unauthorized actions
    test_unauthorized_actions(token1, token2, comment_id1)
    
    # Test comment deletion
    print("\n=== Testing comment deletion ===")
    test_delete_comment(token1, comment_id3)
    
    # Verify comments after deletion
    print("\n=== Verifying comments after deletion ===")
    test_get_comments_for_recipe(recipe_id)
    
    print("\n=== Testing error cases ===")
    
    # Test creating comment without text
    print("Testing comment creation without text...")
    url = f"{BASE_URL}/comments/"
    headers = {
        "Authorization": f"Bearer {token1}",
        "Content-Type": "application/json"
    }
    data = {"recipe_id": recipe_id}  # Missing text
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 400:
        print("✓ Missing text error handled correctly")
    else:
        print(f"✗ Unexpected response: {response.status_code} - {response.json()}")
    
    # Test creating comment without recipe_id
    print("Testing comment creation without recipe_id...")
    data = {"text": "Some comment"}  # Missing recipe_id
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 400:
        print("✓ Missing recipe_id error handled correctly")
    else:
        print(f"✗ Unexpected response: {response.status_code} - {response.json()}")
    
    print("\n" + "=" * 50)
    print("Comment feature testing completed!")
    print("\nFeatures tested:")
    print("✓ Comment creation with proper validation")
    print("✓ Comment retrieval for recipes")
    print("✓ Comment updating by owner")
    print("✓ Comment deletion by owner")
    print("✓ Authorization checks (users can only edit/delete their own comments)")
    print("✓ Error handling for invalid requests")

if __name__ == "__main__":
    main()
