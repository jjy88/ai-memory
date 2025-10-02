# schemas.py
from marshmallow import Schema, fields, validate, validates, ValidationError


class UserRegistrationSchema(Schema):
    """Schema for user registration"""
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6, max=100))


class UserLoginSchema(Schema):
    """Schema for user login"""
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class TokenRefreshSchema(Schema):
    """Schema for token refresh"""
    refresh_token = fields.Str(required=True)


class UploadSchema(Schema):
    """Schema for file upload"""
    files = fields.List(fields.Raw(), required=True)


class ChatMessageSchema(Schema):
    """Schema for chat message"""
    message = fields.Str(required=True, validate=validate.Length(min=1, max=5000))
    context_id = fields.Str(required=False)


class PaymentSchema(Schema):
    """Schema for payment"""
    order_id = fields.Str(required=True)
    amount = fields.Float(required=False)


class UserUpdateSchema(Schema):
    """Schema for user update (admin)"""
    role = fields.Str(validate=validate.OneOf(['free', 'premium', 'admin']))
    is_active = fields.Bool()


# Response schemas
class UserResponseSchema(Schema):
    """Schema for user response"""
    id = fields.Str()
    email = fields.Email()
    role = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    is_active = fields.Bool()


class TokenResponseSchema(Schema):
    """Schema for token response"""
    access_token = fields.Str()
    refresh_token = fields.Str()
    user = fields.Nested(UserResponseSchema)


class UploadResponseSchema(Schema):
    """Schema for upload response"""
    message = fields.Str()
    page_count = fields.Int()
    price = fields.Float()
    download_url = fields.Str()
    upload_id = fields.Str()


class ErrorResponseSchema(Schema):
    """Schema for error response"""
    error = fields.Str()
    details = fields.Dict(required=False)
