# tests/test_chat_api.py
import pytest


def test_chat_unauthorized(client):
    """Test chat without authentication"""
    data = {'message': 'Hello'}
    response = client.post('/api/v1/chat/', json=data)
    assert response.status_code == 401


def test_chat_success(client, auth_headers):
    """Test chat with authentication"""
    data = {'message': 'Hello, how are you?'}
    
    response = client.post('/api/v1/chat/', json=data, headers=auth_headers)
    assert response.status_code == 200
    
    response_data = response.get_json()
    assert 'reply' in response_data
    assert 'context_id' in response_data
    assert 'Hello, how are you?' in response_data['reply']


def test_chat_validation_error(client, auth_headers):
    """Test chat with invalid data"""
    data = {'message': ''}  # Empty message
    
    response = client.post('/api/v1/chat/', json=data, headers=auth_headers)
    assert response.status_code == 400
