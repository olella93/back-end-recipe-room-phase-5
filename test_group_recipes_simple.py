#!/usr/bin/env python3

import requests
import json

BASE_URL = "http://127.0.0.1:5003"

def main():
    print("🧪 Testing Group Recipe Endpoint")
    
    # Login as existing user
    login_data = {"username": "chef_alice", "password": "password123"}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    
    if response.status_code != 200:
        print(f"Failed to login: {response.text}")
        return
    
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get user's groups
    response = requests.get(f"{BASE_URL}/api/my-groups", headers=headers)
    if response.status_code == 200:
        groups = response.json()
        print(f"Alice is in {len(groups)} groups:")
        for group in groups:
            print(f"  - Group {group['id']}: {group['name']}")
            
            # Try to get recipes for this group
            response = requests.get(f"{BASE_URL}/api/groups/{group['id']}/recipes", headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"    ✓ {data['recipe_count']} recipes in this group")
                for recipe in data['recipes']:
                    print(f"      - {recipe['title']} (by user {recipe['user_id']})")
            else:
                print(f"    ✗ Failed to get recipes: {response.text}")
    else:
        print(f"Failed to get user groups: {response.text}")

if __name__ == "__main__":
    main()
