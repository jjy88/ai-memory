# models.py
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
import uuid


@dataclass
class User:
    """User model"""
    id: str
    email: str
    password_hash: str
    role: str = 'free'  # free, premium, admin
    created_at: datetime = None
    updated_at: datetime = None
    is_active: bool = True
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }


@dataclass
class Payment:
    """Payment model"""
    order_id: str
    user_id: Optional[str]
    status: str  # pending, paid, failed
    created_time: datetime
    user_token: Optional[str] = None
    amount: float = 0.0
    
    def to_dict(self):
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'status': self.status,
            'created_time': self.created_time.isoformat() if self.created_time else None,
            'user_token': self.user_token,
            'amount': self.amount
        }


@dataclass
class UploadRecord:
    """Upload record model"""
    id: str
    user_id: str
    filename: str
    file_type: str
    page_count: int
    status: str  # processing, completed, failed
    created_at: datetime
    completed_at: Optional[datetime] = None
    download_url: Optional[str] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'file_type': self.file_type,
            'page_count': self.page_count,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'download_url': self.download_url
        }


# In-memory storage (replace with database in production)
users_db = {}
payments_db = {}
uploads_db = {}
