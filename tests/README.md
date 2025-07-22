# Recipe Room Backend Tests

This directory contains all test files for the Recipe Room backend application.

## Test Files

### 📝 **Integration Tests (API Testing)**

#### `test_recipe_search.py`
- Tests the new recipe search endpoint (`GET /api/recipes/search`)
- **Features Tested:**
  - Search by title, description, and ingredients
  - Case-insensitive search functionality
  - Partial word matching
  - Error handling for invalid queries
  - Response structure validation
  - Includes group_id field in results

#### `test_groups.py`
- Comprehensive testing of group recipe sharing functionality
- **Features Tested:**
  - Recipe creation in groups with member validation
  - Group recipe retrieval with access control
  - Recipe updates and group transfers
  - Personal recipes (no group association)
  - Error handling for unauthorized access
  - Integration with existing group membership system

#### `test_groups_simple.py`
- Simple focused test for group recipe endpoint
- Quick validation of group recipe functionality

#### `test_image_upload.py`
- Tests image upload functionality for profiles and recipes
- **Features Tested:**
  - Profile image upload to Cloudinary
  - Recipe image upload to Cloudinary
  - Authentication and authorization for uploads
  - File validation and error handling
  - Cloudinary configuration validation

### 🏗️ **Unit Tests (Framework Placeholders)**

#### `test_auth.py`
- Authentication and authorization tests (placeholder)

#### `test_recipes.py`
- Recipe model and CRUD operation tests (placeholder)

#### `test_ratings.py`
- Rating system tests (placeholder)

#### `test_comments.py`
- Comment system tests (placeholder - not yet implemented)

## Running Tests

### Prerequisites
1. **Flask Application Running**: Make sure the Flask app is running on `http://127.0.0.1:5003`
   ```bash
   python run.py
   ```

2. **Database Setup**: Ensure database is migrated and has test data
   ```bash
   flask db upgrade
   ```

3. **Dependencies**: Make sure `requests` library is installed
   ```bash
   pip install requests
   ```

### Run Individual Tests
```bash
# From the main project directory
cd tests

# Run search endpoint tests
python test_recipe_search.py

# Run group functionality tests
python test_groups.py

# Run simple group test
python test_groups_simple.py
```

### Run All Tests
```bash
# From the main project directory
python run_tests.py
```

## Test Structure

### Integration Tests
These tests make actual HTTP requests to the running Flask application and test the complete API functionality including:
- Request/response handling
- Authentication and authorization
- Database operations
- Business logic validation
- Error handling

### Unit Tests (Future)
These will test individual components in isolation:
- Model methods
- Utility functions
- Schema validation
- Business logic functions

## Adding New Tests

1. **Create test file**: Add new test files in this directory following the naming convention `test_*.py`

2. **Integration tests**: For API endpoint testing, follow the pattern in existing files:
   - Use `requests` library for HTTP calls
   - Test both success and error cases
   - Validate response structure
   - Include authentication where required

3. **Unit tests**: For component testing, use Python's `unittest` or `pytest` framework

4. **Update test runner**: Add new test files to `run_tests.py` in the main directory

## Test Data

Tests use the existing data in the development database. Make sure you have:
- Test users created
- Sample recipes available
- Test groups and memberships set up

You can create test data by running the comprehensive tests once, as they set up their own test users and data.

## Notes

- Tests are designed to be **non-destructive** where possible
- Some tests create temporary data (users, groups, recipes) for testing
- Make sure to run tests against a development database, not production
- Tests assume the application is running on the default port (5003)

## Future Enhancements

- [ ] Add database cleanup after tests
- [ ] Add test configuration for different environments
- [ ] Add automated test data setup
- [ ] Add performance testing
- [ ] Add unit tests for models and utilities
- [ ] Add test coverage reporting
