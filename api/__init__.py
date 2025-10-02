# api/__init__.py
from flask import Blueprint
from flask_restx import Api

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Initialize Flask-RESTX API
api = Api(
    api_bp,
    title='AI Memory API',
    version='1.0',
    description='AI-powered document processing and memory management system',
    doc='/docs',
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
        }
    },
    security='Bearer'
)

# Import namespaces
from api.auth_api import ns as auth_ns
from api.upload_api import ns as upload_ns
from api.chat_api import ns as chat_ns
from api.admin_api import ns as admin_ns

# Add namespaces
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(upload_ns, path='/upload')
api.add_namespace(chat_ns, path='/chat')
api.add_namespace(admin_ns, path='/admin')
