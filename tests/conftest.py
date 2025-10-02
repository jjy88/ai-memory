# tests/conftest.py
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    """Create application for testing"""
    # Set testing environment before importing
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['RATELIMIT_ENABLED'] = 'False'
    
    from main import app as flask_app
    from models import users_db, payments_db, uploads_db
    
    flask_app.config.update({
        'TESTING': True,
        'JWT_SECRET_KEY': 'test-secret',
        'SECRET_KEY': 'test-secret',
        'RATELIMIT_ENABLED': False,
        'RATELIMIT_STORAGE_URL': None
    })
    
    # Clear databases before each test
    users_db.clear()
    payments_db.clear()
    uploads_db.clear()
    
    yield flask_app
    
    # Clean up after test
    users_db.clear()
    payments_db.clear()
    uploads_db.clear()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def auth_headers(client, app):
    """Create authenticated user and return auth headers"""
    with app.app_context():
        # Register and login a test user
        register_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        
        response = client.post('/api/v1/auth/register', json=register_data)
        data = response.get_json()
        
        token = data.get('access_token')
        return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def admin_headers(client, app):
    """Create admin user and return auth headers"""
    with app.app_context():
        from auth_utils import create_user, generate_tokens
        
        # Create admin user
        admin = create_user('admin@example.com', 'admin123', role='admin')
        tokens = generate_tokens(admin)
        
        token = tokens.get('access_token')
        return {'Authorization': f'Bearer {token}'}
