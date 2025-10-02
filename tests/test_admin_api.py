# tests/test_admin_api.py
import pytest


def test_admin_stats_unauthorized(client):
    """Test admin stats without authentication"""
    response = client.get('/api/v1/admin/stats')
    assert response.status_code == 401


def test_admin_stats_non_admin(client, auth_headers):
    """Test admin stats with non-admin user"""
    response = client.get('/api/v1/admin/stats', headers=auth_headers)
    assert response.status_code == 403


def test_admin_stats_success(client, admin_headers):
    """Test admin stats with admin user"""
    response = client.get('/api/v1/admin/stats', headers=admin_headers)
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'total_users' in data
    assert 'total_payments' in data
    assert 'total_uploads' in data
    assert 'active_users' in data


def test_admin_list_users(client, admin_headers):
    """Test listing all users as admin"""
    response = client.get('/api/v1/admin/users', headers=admin_headers)
    assert response.status_code == 200
    
    data = response.get_json()
    assert isinstance(data, list)


def test_admin_update_user(client, admin_headers):
    """Test updating user as admin"""
    from auth_utils import create_user
    
    # Create a test user
    user = create_user('updateme@example.com', 'password123', role='free')
    
    # Update user role
    update_data = {
        'role': 'premium'
    }
    
    response = client.put(
        f'/api/v1/admin/users/{user.id}',
        json=update_data,
        headers=admin_headers
    )
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['role'] == 'premium'
