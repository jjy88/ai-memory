# api/admin_api.py
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from auth_utils import get_user_by_id, require_role
from schemas import UserUpdateSchema
from models import users_db, payments_db, uploads_db

ns = Namespace('admin', description='Admin operations')

# Models
user_model = ns.model('User', {
    'id': fields.String(description='User ID'),
    'email': fields.String(description='User email'),
    'role': fields.String(description='User role'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'is_active': fields.Boolean(description='Account status')
})

stats_model = ns.model('Stats', {
    'total_users': fields.Integer(description='Total number of users'),
    'total_payments': fields.Integer(description='Total number of payments'),
    'total_uploads': fields.Integer(description='Total number of uploads'),
    'active_users': fields.Integer(description='Number of active users')
})

user_update_model = ns.model('UserUpdate', {
    'role': fields.String(description='New user role', enum=['free', 'premium', 'admin']),
    'is_active': fields.Boolean(description='Account active status')
})


@ns.route('/stats')
class AdminStats(Resource):
    @ns.doc('get_stats', security='Bearer')
    @ns.marshal_with(stats_model)
    @jwt_required()
    @require_role('admin')
    def get(self):
        """Get system statistics (Admin only)"""
        total_users = len(users_db)
        total_payments = len(payments_db)
        total_uploads = len(uploads_db)
        active_users = sum(1 for u in users_db.values() if u.is_active)
        
        return {
            'total_users': total_users,
            'total_payments': total_payments,
            'total_uploads': total_uploads,
            'active_users': active_users
        }


@ns.route('/users')
class AdminUsers(Resource):
    @ns.doc('list_users', security='Bearer')
    @ns.marshal_list_with(user_model)
    @jwt_required()
    @require_role('admin')
    def get(self):
        """List all users (Admin only)"""
        return [user.to_dict() for user in users_db.values()]


@ns.route('/users/<string:user_id>')
@ns.param('user_id', 'The user identifier')
class AdminUser(Resource):
    @ns.doc('update_user', security='Bearer')
    @ns.expect(user_update_model)
    @ns.marshal_with(user_model)
    @jwt_required()
    @require_role('admin')
    def put(self, user_id):
        """Update user information (Admin only)"""
        user = users_db.get(user_id)
        if not user:
            ns.abort(404, 'User not found')
        
        schema = UserUpdateSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            ns.abort(400, f'Validation error: {err.messages}')
        
        # Update user
        if 'role' in data:
            user.role = data['role']
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        from datetime import datetime
        user.updated_at = datetime.utcnow()
        
        return user.to_dict()
    
    @ns.doc('delete_user', security='Bearer')
    @jwt_required()
    @require_role('admin')
    def delete(self, user_id):
        """Delete a user (Admin only)"""
        if user_id not in users_db:
            ns.abort(404, 'User not found')
        
        del users_db[user_id]
        return {'message': 'User deleted successfully'}, 204
