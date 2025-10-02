# api/chat_api.py
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from auth_utils import get_user_by_id
from schemas import ChatMessageSchema

ns = Namespace('chat', description='Chat and AI interaction operations')

# Models
chat_request_model = ns.model('ChatRequest', {
    'message': fields.String(required=True, description='Chat message', example='Hello, how are you?'),
    'context_id': fields.String(description='Conversation context ID')
})

chat_response_model = ns.model('ChatResponse', {
    'reply': fields.String(description='AI response'),
    'context_id': fields.String(description='Conversation context ID')
})


@ns.route('/')
class Chat(Resource):
    @ns.doc('send_message')
    @ns.expect(chat_request_model)
    @ns.marshal_with(chat_response_model)
    @jwt_required()
    def post(self):
        """Send a chat message"""
        identity = get_jwt_identity()
        user = get_user_by_id(identity)
        
        if not user:
            ns.abort(404, 'User not found')
        
        schema = ChatMessageSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            ns.abort(400, f'Validation error: {err.messages}')
        
        message = data.get('message', '')
        context_id = data.get('context_id', '')
        
        # Simple echo response (replace with actual AI logic)
        reply = f"你好 {user.email}，欢迎来到 Obsi喵！你说的是：{message}"
        
        return {
            'reply': reply,
            'context_id': context_id or 'new-context'
        }
