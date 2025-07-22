#!/usr/bin/env python3
"""
Test Runner for Recipe Room Backend
Runs all test files in the tests directory
"""

import os
import sys
import subprocess

def run_tests():
    """Run all test files in the tests directory"""
    
    print("🧪 Recipe Room Backend Test Suite")
    print("=" * 50)
    
    tests_dir = "tests"
    test_files = [
        "test_recipe_search.py",
        "test_groups.py", 
        "test_groups_simple.py"
    ]
    
    print(f"\nFound {len(test_files)} test files:")
    for test_file in test_files:
        print(f"  - {test_file}")
    
    print("\n" + "=" * 50)
    
    # Run each test file
    for i, test_file in enumerate(test_files, 1):
        test_path = os.path.join(tests_dir, test_file)
        
        if not os.path.exists(test_path):
            print(f"\n❌ Test {i}: {test_file} - FILE NOT FOUND")
            continue
            
        print(f"\n🔄 Running Test {i}: {test_file}")
        print("-" * 30)
        
        try:
            # Run the test file
            result = subprocess.run([sys.executable, test_path], 
                                  capture_output=False, 
                                  text=True)
            
            if result.returncode == 0:
                print(f"\n✅ Test {i} PASSED: {test_file}")
            else:
                print(f"\n❌ Test {i} FAILED: {test_file} (exit code: {result.returncode})")
                
        except Exception as e:
            print(f"\n💥 Test {i} ERROR: {test_file} - {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 Test Suite Complete!")
    print("\nNote: Make sure the Flask application is running on http://127.0.0.1:5003")
    print("Run: python run.py")

if __name__ == "__main__":
    run_tests()
