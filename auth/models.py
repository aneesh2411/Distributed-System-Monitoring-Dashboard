"""User model for authentication."""
from typing import Optional
from sqlalchemy import Column, String, Boolean
from passlib.hash import bcrypt
from models.base import Base

class User(Base):
    """User model for authentication."""
    
    __tablename__ = 'users'

    username = Column(String(50), primary_key=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    api_key = Column(String(255), unique=True, nullable=True)

    def set_password(self, password: str) -> None:
        """Hash and set the password."""
        self.password_hash = bcrypt.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify the password."""
        return bcrypt.verify(password, self.password_hash)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 