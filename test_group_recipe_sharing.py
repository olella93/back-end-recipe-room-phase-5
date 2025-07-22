#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://127.0.0.1:5003"

def test_user_registration_and_login():
    """Register test users and return their tokens"""
    print("=== Setting up test users ===")
    
    # Register users
    users = [
        {"username": "chef_alice", "email": "alice@example.com", "password": "password123"},
        {"username": "chef_bob", "email": "bob@example.com", "password": "password123"},
        {"username": "chef_charlie", "email": "charlie@example.com", "password": "password123"}
    ]
    
    tokens = {}
    
    for user_data in users:
        # Register
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        if response.status_code not in [201, 400]:  # 400 might be "user already exists"
            print(f"Failed to register {user_data['username']}: Status {response.status_code}")
            print(f"Response: {response.text}")
            continue
            
        # Login
        login_data = {"username": user_data["username"], "password": user_data["password"]}
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        
        if response.status_code == 200:
            tokens[user_data["username"]] = response.json()["token"]
            print(f"✓ User {user_data['username']} ready")
        else:
            print(f"Failed to login {user_data['username']}: Status {response.status_code}")
            print(f"Response: {response.text}")
    
    return tokens

def test_group_creation(tokens):
    """Create test groups and return group IDs"""
    print("\n=== Creating test groups ===")
    
    alice_token = tokens["chef_alice"]
    headers = {"Authorization": f"Bearer {alice_token}"}
    
    groups = [
        {"name": "Italian Cuisine Lovers", "description": "Share your favorite Italian recipes"},
        {"name": "Vegan Recipes", "description": "Plant-based cooking community"}
    ]
    
    group_ids = []
    
    for group_data in groups:
        response = requests.post(f"{BASE_URL}/api/groups", json=group_data, headers=headers)
        if response.status_code == 201:
            group_id = response.json()["group"]["id"]
            group_ids.append(group_id)
            print(f"✓ Created group '{group_data['name']}' with ID {group_id}")
        else:
            print(f"Failed to create group: {response.text}")
    
    return group_ids

def test_group_membership(tokens, group_ids):
    """Add users to groups"""
    print("\n=== Setting up group memberships ===")
    
    if len(group_ids) < 2:
        print("Need at least 2 groups for testing")
        return
    
    # Add Bob to Italian Cuisine group
    bob_token = tokens["chef_bob"]
    headers = {"Authorization": f"Bearer {bob_token}"}
    
    response = requests.post(f"{BASE_URL}/api/groups/{group_ids[0]}/join", headers=headers)
    if response.status_code == 200:
        print(f"✓ Bob joined Italian Cuisine group")
    else:
        print(f"Failed to add Bob to group: {response.text}")
    
    # Add Charlie to Vegan Recipes group
    charlie_token = tokens["chef_charlie"]
    headers = {"Authorization": f"Bearer {charlie_token}"}
    
    response = requests.post(f"{BASE_URL}/api/groups/{group_ids[1]}/join", headers=headers)
    if response.status_code == 200:
        print(f"✓ Charlie joined Vegan Recipes group")
    else:
        print(f"Failed to add Charlie to group: {response.text}")

def test_recipe_creation_with_groups(tokens, group_ids):
    """Test creating recipes with and without group association"""
    print("\n=== Testing recipe creation with groups ===")
    
    alice_token = tokens["chef_alice"]
    bob_token = tokens["chef_bob"]
    charlie_token = tokens["chef_charlie"]
    
    # Test 1: Alice creates a recipe in Italian Cuisine group (she's the owner)
    print("\nTest 1: Owner creates recipe in their group")
    headers = {"Authorization": f"Bearer {alice_token}"}
    recipe_data = {
        "title": "Authentic Carbonara",
        "description": "Traditional Roman pasta dish",
        "ingredients": "Spaghetti, eggs, pecorino cheese, guanciale, black pepper",
        "instructions": "1. Cook pasta 2. Prepare sauce 3. Combine",
        "country": "Italy",
        "serving_size": 4,
        "group_id": group_ids[0]  # Italian Cuisine group
    }
    
    response = requests.post(f"{BASE_URL}/api/recipes", json=recipe_data, headers=headers)
    if response.status_code == 201:
        alice_recipe_id = response.json()["recipe_id"]
        print(f"✓ Alice created recipe in Italian group (ID: {alice_recipe_id})")
    else:
        print(f"✗ Failed: {response.text}")
    
    # Test 2: Bob creates a recipe in Italian Cuisine group (he's a member)
    print("\nTest 2: Member creates recipe in group")
    headers = {"Authorization": f"Bearer {bob_token}"}
    recipe_data = {
        "title": "Margherita Pizza",
        "description": "Classic Neapolitan pizza",
        "ingredients": "Pizza dough, tomatoes, mozzarella, basil",
        "instructions": "1. Prepare dough 2. Add toppings 3. Bake",
        "country": "Italy",
        "serving_size": 2,
        "group_id": group_ids[0]  # Italian Cuisine group
    }
    
    response = requests.post(f"{BASE_URL}/api/recipes", json=recipe_data, headers=headers)
    if response.status_code == 201:
        bob_recipe_id = response.json()["recipe_id"]
        print(f"✓ Bob created recipe in Italian group (ID: {bob_recipe_id})")
    else:
        print(f"✗ Failed: {response.text}")
    
    # Test 3: Charlie tries to create recipe in Italian group (not a member) - should fail
    print("\nTest 3: Non-member tries to create recipe in group (should fail)")
    headers = {"Authorization": f"Bearer {charlie_token}"}
    recipe_data = {
        "title": "Fake Italian Recipe",
        "description": "This should fail",
        "ingredients": "Test ingredients",
        "instructions": "Test instructions",
        "group_id": group_ids[0]  # Italian Cuisine group
    }
    
    response = requests.post(f"{BASE_URL}/api/recipes", json=recipe_data, headers=headers)
    if response.status_code == 403:
        print(f"✓ Charlie correctly denied access to Italian group")
    else:
        print(f"✗ Unexpected result: {response.status_code} - {response.text}")
    
    # Test 4: Charlie creates recipe in Vegan group (he's a member)
    print("\nTest 4: Member creates recipe in their group")
    recipe_data = {
        "title": "Quinoa Buddha Bowl",
        "description": "Healthy vegan bowl",
        "ingredients": "Quinoa, kale, chickpeas, tahini",
        "instructions": "1. Cook quinoa 2. Prepare veggies 3. Assemble",
        "serving_size": 1,
        "group_id": group_ids[1]  # Vegan Recipes group
    }
    
    response = requests.post(f"{BASE_URL}/api/recipes", json=recipe_data, headers=headers)
    if response.status_code == 201:
        charlie_recipe_id = response.json()["recipe_id"]
        print(f"✓ Charlie created recipe in Vegan group (ID: {charlie_recipe_id})")
    else:
        print(f"✗ Failed: {response.text}")
    
    # Test 5: Create recipe without group (personal recipe)
    print("\nTest 5: Create personal recipe (no group)")
    recipe_data = {
        "title": "Personal Secret Recipe",
        "description": "My personal favorite",
        "ingredients": "Secret ingredients",
        "instructions": "Secret method"
    }
    
    response = requests.post(f"{BASE_URL}/api/recipes", json=recipe_data, headers=headers)
    if response.status_code == 201:
        personal_recipe_id = response.json()["recipe_id"]
        print(f"✓ Charlie created personal recipe (ID: {personal_recipe_id})")
    else:
        print(f"✗ Failed: {response.text}")
    
    return {
        "alice_recipe_id": alice_recipe_id if 'alice_recipe_id' in locals() else None,
        "bob_recipe_id": bob_recipe_id if 'bob_recipe_id' in locals() else None,
        "charlie_recipe_id": charlie_recipe_id if 'charlie_recipe_id' in locals() else None,
        "personal_recipe_id": personal_recipe_id if 'personal_recipe_id' in locals() else None
    }

def test_group_recipe_retrieval(tokens, group_ids):
    """Test retrieving recipes by group"""
    print("\n=== Testing group recipe retrieval ===")
    
    alice_token = tokens["chef_alice"]
    bob_token = tokens["chef_bob"]
    charlie_token = tokens["chef_charlie"]
    
    # Test 1: Alice gets Italian group recipes (she's owner)
    print("\nTest 1: Group owner retrieves group recipes")
    headers = {"Authorization": f"Bearer {alice_token}"}
    response = requests.get(f"{BASE_URL}/api/groups/{group_ids[0]}/api/recipes", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Alice retrieved {data['recipe_count']} recipes from Italian group")
        for recipe in data['recipes']:
            print(f"   - {recipe['title']} (by user {recipe['user_id']})")
    else:
        print(f"✗ Failed: {response.text}")
    
    # Test 2: Bob gets Italian group recipes (he's member)
    print("\nTest 2: Group member retrieves group recipes")
    headers = {"Authorization": f"Bearer {bob_token}"}
    response = requests.get(f"{BASE_URL}/api/groups/{group_ids[0]}/api/recipes", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Bob retrieved {data['recipe_count']} recipes from Italian group")
    else:
        print(f"✗ Failed: {response.text}")
    
    # Test 3: Charlie tries to get Italian group recipes (not a member) - should fail
    print("\nTest 3: Non-member tries to retrieve group recipes (should fail)")
    headers = {"Authorization": f"Bearer {charlie_token}"}
    response = requests.get(f"{BASE_URL}/api/groups/{group_ids[0]}/api/recipes", headers=headers)
    
    if response.status_code == 403:
        print(f"✓ Charlie correctly denied access to Italian group recipes")
    else:
        print(f"✗ Unexpected result: {response.status_code} - {response.text}")
    
    # Test 4: Charlie gets Vegan group recipes (he's member)
    print("\nTest 4: Member retrieves their group recipes")
    response = requests.get(f"{BASE_URL}/api/groups/{group_ids[1]}/api/recipes", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Charlie retrieved {data['recipe_count']} recipes from Vegan group")
        for recipe in data['recipes']:
            print(f"   - {recipe['title']} (by user {recipe['user_id']})")
    else:
        print(f"✗ Failed: {response.text}")

def test_recipe_updates_with_groups(tokens, group_ids, recipe_ids):
    """Test updating recipes with group changes"""
    print("\n=== Testing recipe updates with group changes ===")
    
    alice_token = tokens["chef_alice"]
    bob_token = tokens["chef_bob"]
    
    if not recipe_ids.get("alice_recipe_id"):
        print("No Alice recipe to test with")
        return
    
    # Test 1: Alice moves her recipe from Italian group to Vegan group
    # First, Alice needs to join the Vegan group
    print("\nTest 1: Moving recipe between groups")
    headers = {"Authorization": f"Bearer {alice_token}"}
    
    # Join Vegan group
    response = requests.post(f"{BASE_URL}/api/groups/{group_ids[1]}/join", headers=headers)
    if response.status_code == 200:
        print(f"✓ Alice joined Vegan group")
    
    # Move recipe to Vegan group
    update_data = {"group_id": group_ids[1]}
    response = requests.put(f"{BASE_URL}/api/recipes/{recipe_ids['alice_recipe_id']}", 
                          json=update_data, headers=headers)
    
    if response.status_code == 200:
        print(f"✓ Alice moved recipe to Vegan group")
    else:
        print(f"✗ Failed to move recipe: {response.text}")
    
    # Test 2: Alice removes recipe from group (makes it personal)
    print("\nTest 2: Removing recipe from group")
    update_data = {"group_id": None}
    response = requests.put(f"{BASE_URL}/api/recipes/{recipe_ids['alice_recipe_id']}", 
                          json=update_data, headers=headers)
    
    if response.status_code == 200:
        print(f"✓ Alice made recipe personal (removed from group)")
    else:
        print(f"✗ Failed to remove from group: {response.text}")
    
    # Test 3: Alice tries to move recipe to group she's not member of - should fail
    print("\nTest 3: Trying to move recipe to non-member group (should fail)")
    # Leave Vegan group first
    response = requests.delete(f"{BASE_URL}/api/groups/{group_ids[1]}/leave", headers=headers)
    
    # Try to move recipe to Vegan group (not a member anymore)
    update_data = {"group_id": group_ids[1]}
    response = requests.put(f"{BASE_URL}/api/recipes/{recipe_ids['alice_recipe_id']}", 
                          json=update_data, headers=headers)
    
    if response.status_code == 403:
        print(f"✓ Alice correctly denied moving recipe to non-member group")
    else:
        print(f"✗ Unexpected result: {response.status_code} - {response.text}")

def test_recipe_visibility(tokens, group_ids):
    """Test recipe visibility in general listings"""
    print("\n=== Testing recipe visibility ===")
    
    alice_token = tokens["chef_alice"]
    
    # Get all recipes and check group_id field
    print("\nTesting general recipe listing includes group_id")
    headers = {"Authorization": f"Bearer {alice_token}"}
    response = requests.get(f"{BASE_URL}/api/recipes", headers=headers)
    
    if response.status_code == 200:
        recipes = response.json()
        print(f"✓ Retrieved {len(recipes)} recipes")
        
        group_recipes = [r for r in recipes if r.get('group_id')]
        personal_recipes = [r for r in recipes if not r.get('group_id')]
        
        print(f"   - {len(group_recipes)} group recipes")
        print(f"   - {len(personal_recipes)} personal recipes")
        
        # Show some examples
        for recipe in recipes[:3]:
            group_info = f"(Group {recipe['group_id']})" if recipe.get('group_id') else "(Personal)"
            print(f"   - {recipe['title']} {group_info}")
    else:
        print(f"✗ Failed to get recipes: {response.text}")

def main():
    """Run all tests"""
    print("🧪 Testing Group Recipe Sharing Functionality")
    print("=" * 50)
    
    try:
        # Setup
        tokens = test_user_registration_and_login()
        if len(tokens) < 3:
            print("❌ Failed to set up required test users")
            return
        
        group_ids = test_group_creation(tokens)
        if len(group_ids) < 2:
            print("❌ Failed to create required test groups")
            return
        
        test_group_membership(tokens, group_ids)
        
        # Main tests
        recipe_ids = test_recipe_creation_with_groups(tokens, group_ids)
        test_group_recipe_retrieval(tokens, group_ids)
        test_recipe_updates_with_groups(tokens, group_ids, recipe_ids)
        test_recipe_visibility(tokens, group_ids)
        
        print("\n" + "=" * 50)
        print("🎉 Group Recipe Sharing Tests Completed!")
        print("\nKey features tested:")
        print("✓ Creating recipes in groups (with member validation)")
        print("✓ Retrieving recipes by group (with access control)")
        print("✓ Moving recipes between groups")
        print("✓ Removing recipes from groups")
        print("✓ group_id field in general recipe listings")
        print("✓ Proper error handling for unauthorized access")
        
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
