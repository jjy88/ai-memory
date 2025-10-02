# api/auth_api.py
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from marshmallow import ValidationError

from auth_utils import create_user, authenticate_user, generate_tokens, get_user_by_id
from schemas import UserRegistrationSchema, UserLoginSchema

ns = Namespace('auth', description='Authentication operations')

# Request models
register_model = ns.model('Register', {
    'email': fields.String(required=True, description='User email', example='user@example.com'),
    'password': fields.String(required=True, description='User password', example='password123')
})

login_model = ns.model('Login', {
    'email': fields.String(required=True, description='User email', example='user@example.com'),
    'password': fields.String(required=True, description='User password', example='password123')
})

# Response models
user_model = ns.model('User', {
    'id': fields.String(description='User ID'),
    'email': fields.String(description='User email'),
    'role': fields.String(description='User role'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'is_active': fields.Boolean(description='Account status')
})

token_response_model = ns.model('TokenResponse', {
    'access_token': fields.String(description='JWT access token'),
    'refresh_token': fields.String(description='JWT refresh token'),
    'user': fields.Nested(user_model)
})


@ns.route('/register')
class Register(Resource):
    @ns.doc('register_user', security=None)
    @ns.expect(register_model)
    @ns.marshal_with(token_response_model, code=201)
    @ns.response(400, 'Validation Error')
    @ns.response(409, 'User already exists')
    def post(self):
        """Register a new user"""
        schema = UserRegistrationSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            ns.abort(400, f'Validation error: {err.messages}')
        
        # Check if user exists
        from models import users_db
        for user in users_db.values():
            if user.email == data['email']:
                ns.abort(409, 'User with this email already exists')
        
        # Create user
        user = create_user(data['email'], data['password'])
        tokens = generate_tokens(user)
        
        return tokens, 201


@ns.route('/login')
class Login(Resource):
    @ns.doc('login_user', security=None)
    @ns.expect(login_model)
    @ns.marshal_with(token_response_model)
    @ns.response(401, 'Invalid credentials')
    def post(self):
        """Login with email and password"""
        schema = UserLoginSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            ns.abort(400, f'Validation error: {err.messages}')
        
        user = authenticate_user(data['email'], data['password'])
        if not user:
            ns.abort(401, 'Invalid email or password')
        
        tokens = generate_tokens(user)
        return tokens


@ns.route('/refresh')
class Refresh(Resource):
    @ns.doc('refresh_token')
    @jwt_required(refresh=True)
    def post(self):
        """Refresh access token"""
        identity = get_jwt_identity()
        user = get_user_by_id(identity)
        
        if not user:
            ns.abort(404, 'User not found')
        
        access_token = create_access_token(
            identity=user.id,
            additional_claims={'role': user.role, 'email': user.email}
        )
        
        return {'access_token': access_token}


@ns.route('/me')
class Me(Resource):
    @ns.doc('get_current_user')
    @ns.marshal_with(user_model)
    @jwt_required()
    def get(self):
        """Get current user profile"""
        identity = get_jwt_identity()
        user = get_user_by_id(identity)
        
        if not user:
            ns.abort(404, 'User not found')
        
        return user.to_dict()
