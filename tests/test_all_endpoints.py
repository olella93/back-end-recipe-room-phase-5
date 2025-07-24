#!/usr/bin/env python3

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = "http://localhost:5003/api"

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("=== Testing Authentication Endpoints ===")
    
    # Test registration
    register_url = f"{BASE_URL}/auth/register"
    register_data = {
        "username": f"testuser_{os.urandom(4).hex()}",
        "email": f"test_{os.urandom(4).hex()}@example.com",
        "password": "password123"
    }
    
    response = requests.post(register_url, json=register_data)
    if response.status_code == 201:
        print("✓ User registration: PASS")
    else:
        print(f"✗ User registration: FAIL ({response.status_code})")
        return None
    
    # Test login
    login_url = f"{BASE_URL}/auth/login"
    login_data = {
        "username": register_data["username"],
        "password": register_data["password"]
    }
    
    response = requests.post(login_url, json=login_data)
    if response.status_code == 200:
        token = response.json()["token"]
        print("✓ User login: PASS")
        
        # Test profile
        profile_url = f"{BASE_URL}/auth/profile"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(profile_url, headers=headers)
        
        if response.status_code == 200:
            print("✓ Get profile: PASS")
        else:
            print(f"✗ Get profile: FAIL ({response.status_code})")
        
        return token
    else:
        print(f"✗ User login: FAIL ({response.status_code})")
        return None

def test_recipe_endpoints(token):
    """Test recipe CRUD endpoints"""
    print("\n=== Testing Recipe Endpoints ===")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test create recipe
    create_url = f"{BASE_URL}/recipes"
    recipe_data = {
        "title": f"Test Recipe {os.urandom(4).hex()}",
        "description": "A test recipe for endpoint verification",
        "ingredients": "Test ingredient 1, Test ingredient 2",
        "instructions": "Mix ingredients and cook",
        "country": "Test Country",
        "serving_size": 4
    }
    
    response = requests.post(create_url, headers=headers, json=recipe_data)
    if response.status_code == 201:
        recipe_id = response.json()["recipe_id"]
        print("✓ Create recipe: PASS")
        
        # Test get all recipes
        response = requests.get(f"{BASE_URL}/recipes")
        if response.status_code == 200:
            print("✓ Get all recipes: PASS")
        else:
            print(f"✗ Get all recipes: FAIL ({response.status_code})")
        
        # Test get single recipe
        response = requests.get(f"{BASE_URL}/recipes/{recipe_id}")
        if response.status_code == 200:
            print("✓ Get single recipe: PASS")
        else:
            print(f"✗ Get single recipe: FAIL ({response.status_code})")
        
        # Test update recipe
        update_data = {
            "title": f"Updated Test Recipe {os.urandom(4).hex()}",
            "description": "An updated test recipe"
        }
        response = requests.put(f"{BASE_URL}/recipes/{recipe_id}", headers=headers, json=update_data)
        if response.status_code == 200:
            print("✓ Update recipe: PASS")
        else:
            print(f"✗ Update recipe: FAIL ({response.status_code})")
        
        return recipe_id
    else:
        print(f"✗ Create recipe: FAIL ({response.status_code})")
        return None

def test_rating_endpoints(token, recipe_id):
    """Test rating endpoints"""
    print("\n=== Testing Rating Endpoints ===")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test create rating
    rating_data = {"value": 5}
    response = requests.post(f"{BASE_URL}/recipes/{recipe_id}/rate", headers=headers, json=rating_data)
    if response.status_code == 201:
        print("✓ Create rating: PASS")
    else:
        print(f"✗ Create rating: FAIL ({response.status_code})")

def test_group_endpoints(token):
    """Test group endpoints"""
    print("\n=== Testing Group Endpoints ===")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test create group
    group_data = {
        "name": f"Test Group {os.urandom(4).hex()}",
        "description": "A test group for endpoint verification"
    }
    
    response = requests.post(f"{BASE_URL}/groups", headers=headers, json=group_data)
    if response.status_code == 201:
        group_id = response.json()["group_id"]
        print("✓ Create group: PASS")
        
        # Test get all groups
        response = requests.get(f"{BASE_URL}/groups")
        if response.status_code == 200:
            print("✓ Get all groups: PASS")
        else:
            print(f"✗ Get all groups: FAIL ({response.status_code})")
        
        # Test get single group
        response = requests.get(f"{BASE_URL}/groups/{group_id}")
        if response.status_code == 200:
            print("✓ Get single group: PASS")
        else:
            print(f"✗ Get single group: FAIL ({response.status_code})")
        
        # Test get user's groups
        response = requests.get(f"{BASE_URL}/my-groups", headers=headers)
        if response.status_code == 200:
            print("✓ Get user groups: PASS")
        else:
            print(f"✗ Get user groups: FAIL ({response.status_code})")
        
        return group_id
    else:
        print(f"✗ Create group: FAIL ({response.status_code})")
        return None

def test_search_endpoint():
    """Test search endpoint"""
    print("\n=== Testing Search Endpoint ===")
    
    response = requests.get(f"{BASE_URL}/recipes/search?query=test")
    if response.status_code == 200:
        print("✓ Recipe search: PASS")
    else:
        print(f"✗ Recipe search: FAIL ({response.status_code})")

def main():
    """Main test function"""
    print("🧪 Recipe Room API Endpoint Verification")
    print("=" * 50)
    
    # Test authentication
    token = test_auth_endpoints()
    if not token:
        print("\n❌ Authentication failed - cannot continue with other tests")
        return
    
    # Test recipes
    recipe_id = test_recipe_endpoints(token)
    
    # Test ratings (if recipe was created)
    if recipe_id:
        test_rating_endpoints(token, recipe_id)
    
    # Test groups
    group_id = test_group_endpoints(token)
    
    # Test search
    test_search_endpoint()
    
    print("\n" + "=" * 50)
    print("✅ Endpoint verification completed!")

if __name__ == "__main__":
    main()
