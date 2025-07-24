#!/usr/bin/env python3

import requests
import json

# Configuration
BASE_URL = "http://localhost:5003/api"

def test_group_recipes_endpoint():
    """Test the group recipes endpoint specifically"""
    print("Testing Group Recipes Endpoint")
    print("=" * 40)
    
    # Register and login user
    register_data = {
        "username": "grouptest123",
        "email": "grouptest123@example.com", 
        "password": "password123"
    }
    
    # Try registration (ignore if exists)
    requests.post(f"{BASE_URL}/auth/register", json=register_data)
    
    # Login
    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "grouptest123",
        "password": "password123"
    })
    
    if login_response.status_code != 200:
        print("❌ Login failed")
        return
        
    token = login_response.json()["token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Create a group
    group_response = requests.post(f"{BASE_URL}/groups", headers=headers, json={
        "name": "Test Group for Recipes",
        "description": "Testing group recipes endpoint"
    })
    
    if group_response.status_code != 201:
        print(f"❌ Group creation failed: {group_response.json()}")
        return
        
    group_id = group_response.json()["group_id"]
    print(f"✅ Created group with ID: {group_id}")
    
    # Create a recipe in the group
    recipe_response = requests.post(f"{BASE_URL}/recipes", headers=headers, json={
        "title": "Group Recipe Test",
        "description": "Testing group recipe functionality",
        "ingredients": "Test ingredients",
        "instructions": "Test instructions",
        "country": "Test Country",
        "serving_size": 4,
        "group_id": group_id
    })
    
    if recipe_response.status_code != 201:
        print(f"❌ Recipe creation failed: {recipe_response.json()}")
        return
        
    recipe_id = recipe_response.json()["recipe_id"]
    print(f"✅ Created recipe with ID: {recipe_id}")
    
    # Test the group recipes endpoint
    print(f"\n🔍 Testing endpoint: /groups/{group_id}/recipes")
    group_recipes_response = requests.get(f"{BASE_URL}/groups/{group_id}/recipes", headers=headers)
    
    print(f"Status Code: {group_recipes_response.status_code}")
    
    if group_recipes_response.status_code == 200:
        data = group_recipes_response.json()
        print(f"✅ Successfully retrieved group recipes")
        print(f"Recipe count: {data.get('recipe_count', 'unknown')}")
        recipes = data.get('recipes', [])
        for recipe in recipes:
            print(f"  - {recipe.get('title', 'Unknown')} (ID: {recipe.get('id', 'unknown')})")
    else:
        print(f"❌ Failed to retrieve group recipes")
        print(f"Response: {group_recipes_response.text}")

if __name__ == "__main__":
    test_group_recipes_endpoint()
