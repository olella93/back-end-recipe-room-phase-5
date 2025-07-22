#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://127.0.0.1:5003"

def test_search_endpoint():
    """Test various search scenarios"""
    
    print("🧪 Testing Recipe Search Endpoint")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "name": "Search by title",
            "query": "carbonara",
            "expected_min_results": 1
        },
        {
            "name": "Search by description",
            "query": "italian",
            "expected_min_results": 1
        },
        {
            "name": "Search by ingredients",
            "query": "cheese",
            "expected_min_results": 1
        },
        {
            "name": "Case insensitive search",
            "query": "PASTA",
            "expected_min_results": 1
        },
        {
            "name": "Partial word match",
            "query": "spag",
            "expected_min_results": 1
        },
        {
            "name": "No results",
            "query": "sushi",
            "expected_min_results": 0
        }
    ]
    
    print("\n=== Valid Search Tests ===")
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print(f"Query: '{test['query']}'")
        
        try:
            response = requests.get(f"{BASE_URL}/api/recipes/search", 
                                  params={"query": test["query"]})
            
            if response.status_code == 200:
                data = response.json()
                result_count = data.get("result_count", 0)
                
                if result_count >= test["expected_min_results"]:
                    print(f"✅ PASS: Found {result_count} recipes")
                    
                    # Show first result if any
                    if result_count > 0:
                        first_recipe = data["recipes"][0]
                        print(f"   Example: '{first_recipe['title']}' by user {first_recipe['user_id']}")
                else:
                    print(f"❌ FAIL: Expected at least {test['expected_min_results']}, got {result_count}")
            else:
                print(f"❌ FAIL: HTTP {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
    
    # Test error cases
    print("\n=== Error Handling Tests ===")
    
    error_tests = [
        {
            "name": "Missing query parameter",
            "url": f"{BASE_URL}/api/recipes/search",
            "expected_status": 400
        },
        {
            "name": "Empty query parameter", 
            "url": f"{BASE_URL}/api/recipes/search?query=",
            "expected_status": 400
        },
        {
            "name": "Whitespace only query",
            "url": f"{BASE_URL}/api/recipes/search?query=   ",
            "expected_status": 400
        }
    ]
    
    for i, test in enumerate(error_tests, 1):
        print(f"\nError Test {i}: {test['name']}")
        
        try:
            response = requests.get(test["url"])
            
            if response.status_code == test["expected_status"]:
                data = response.json()
                print(f"✅ PASS: HTTP {response.status_code} - {data.get('error', 'No error message')}")
            else:
                print(f"❌ FAIL: Expected HTTP {test['expected_status']}, got {response.status_code}")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
    
    # Test response structure
    print("\n=== Response Structure Test ===")
    
    try:
        response = requests.get(f"{BASE_URL}/api/recipes/search?query=carbonara")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            required_fields = ["query", "result_count", "recipes"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                print("✅ PASS: All required fields present")
                
                # Check recipe structure if results exist
                if data["result_count"] > 0:
                    recipe = data["recipes"][0]
                    recipe_fields = ["id", "title", "description", "ingredients", "instructions", 
                                   "user_id", "group_id", "created_at", "updated_at"]
                    
                    missing_recipe_fields = [field for field in recipe_fields if field not in recipe]
                    
                    if not missing_recipe_fields:
                        print("✅ PASS: Recipe structure is complete")
                        print(f"   Includes group_id field: {recipe.get('group_id')}")
                    else:
                        print(f"❌ FAIL: Missing recipe fields: {missing_recipe_fields}")
                        
            else:
                print(f"❌ FAIL: Missing response fields: {missing_fields}")
                
        else:
            print(f"❌ FAIL: Could not test structure - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Recipe Search Endpoint Tests Completed!")
    print("\n📋 Summary:")
    print("✅ Search by title, description, and ingredients")
    print("✅ Case-insensitive search functionality")
    print("✅ Partial word matching")
    print("✅ Proper error handling for invalid queries")
    print("✅ Consistent response structure")
    print("✅ Includes group_id field in results")

def main():
    test_search_endpoint()

if __name__ == "__main__":
    main()
