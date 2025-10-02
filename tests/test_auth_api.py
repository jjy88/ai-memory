# tests/test_auth_api.py
import pytest


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_register_user(client):
    """Test user registration"""
    data = {
        'email': 'newuser@example.com',
        'password': 'password123'
    }
    
    response = client.post('/api/v1/auth/register', json=data)
    assert response.status_code == 201
    
    response_data = response.get_json()
    assert 'access_token' in response_data
    assert 'refresh_token' in response_data
    assert response_data['user']['email'] == data['email']


def test_register_duplicate_user(client):
    """Test registering duplicate user fails"""
    data = {
        'email': 'duplicate@example.com',
        'password': 'password123'
    }
    
    # First registration should succeed
    response = client.post('/api/v1/auth/register', json=data)
    assert response.status_code == 201
    
    # Second registration should fail
    response = client.post('/api/v1/auth/register', json=data)
    assert response.status_code == 409


def test_login_user(client):
    """Test user login"""
    # First register
    register_data = {
        'email': 'login@example.com',
        'password': 'password123'
    }
    client.post('/api/v1/auth/register', json=register_data)
    
    # Then login
    login_data = {
        'email': 'login@example.com',
        'password': 'password123'
    }
    
    response = client.post('/api/v1/auth/login', json=login_data)
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'access_token' in data
    assert 'refresh_token' in data


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    data = {
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    }
    
    response = client.post('/api/v1/auth/login', json=data)
    assert response.status_code == 401


def test_get_current_user(client, auth_headers):
    """Test getting current user profile"""
    response = client.get('/api/v1/auth/me', headers=auth_headers)
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['email'] == 'test@example.com'
    assert data['role'] == 'free'


def test_get_current_user_unauthorized(client):
    """Test getting current user without auth"""
    response = client.get('/api/v1/auth/me')
    assert response.status_code == 401
