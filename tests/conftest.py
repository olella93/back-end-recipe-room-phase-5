import pytest
import requests

@pytest.fixture(scope='session')
def token():
    """Obtain a JWT token for test authentication."""
    register_url = 'http://localhost:5003/api/auth/register'
    login_url = 'http://localhost:5003/api/auth/login'
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }
    # Try to register the user and print response for debugging
    reg_response = requests.post(register_url, json=user_data)
    print('Register response:', reg_response.status_code, reg_response.text)
    # Log in to get token and print response for debugging
    login_payload = {
        'username': user_data['username'],
        'password': user_data['password']
    }
    response = requests.post(login_url, json=login_payload)
    print('Login response:', response.status_code, response.text)
    response.raise_for_status()
    return response.json().get('token')
