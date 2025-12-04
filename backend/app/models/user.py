from sqlalchemy import Column, String, Boolean, DateTime, Index, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index('idx_users_email', 'email', unique=True),
        Index('idx_users_is_active', 'is_active'),
    )
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    
    is_active = Column(Boolean, default=False, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)
    
    email_verified_at = Column(DateTime, nullable=True)
    email_verification_token = Column(String(255), nullable=True)
    
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime, nullable=True)
    
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255), nullable=True)
    
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    preferred_language = Column(String(10), default='ru')
    
    last_login_at = Column(DateTime, nullable=True)
    last_login_ip = Column(String(45), nullable=True)
    
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    addresses = relationship("UserAddress", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, is_admin={self.is_admin})>"
