# auth_utils.py
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
from models import User, users_db


def create_user(email: str, password: str, role: str = 'free') -> User:
    """Create a new user"""
    user_id = str(uuid.uuid4())
    password_hash = generate_password_hash(password)
    
    user = User(
        id=user_id,
        email=email,
        password_hash=password_hash,
        role=role
    )
    
    users_db[user_id] = user
    return user


def authenticate_user(email: str, password: str) -> User:
    """Authenticate user and return user object if valid"""
    for user in users_db.values():
        if user.email == email and check_password_hash(user.password_hash, password):
            return user
    return None


def get_user_by_id(user_id: str) -> User:
    """Get user by ID"""
    return users_db.get(user_id)


def generate_tokens(user: User) -> dict:
    """Generate access and refresh tokens for user"""
    access_token = create_access_token(
        identity=user.id,
        additional_claims={'role': user.role, 'email': user.email}
    )
    refresh_token = create_refresh_token(identity=user.id)
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }


def require_role(required_role: str):
    """Decorator to check user role"""
    def decorator(fn):
        from functools import wraps
        from flask_jwt_extended import verify_jwt_in_request, get_jwt
        from flask import jsonify
        
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role', 'free')
            
            role_hierarchy = {'free': 0, 'premium': 1, 'admin': 2}
            
            if role_hierarchy.get(user_role, 0) < role_hierarchy.get(required_role, 0):
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator
