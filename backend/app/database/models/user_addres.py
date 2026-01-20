from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from .base import Base


class UserAddress(Base):
    __tablename__ = "user_addresses"
    __table_args__ = (
        Index('idx_user_addresses_user_id', 'user_id'),
    )
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Адрес
    country = Column(String(100), default='Russia', nullable=False)
    region = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    street = Column(String(255), nullable=False)
    building = Column(String(50), nullable=False)
    apartment = Column(String(50), nullable=True)
    
    # Информация получателя
    recipient_name = Column(String(255), nullable=False)
    recipient_phone = Column(String(20), nullable=False)
    
    # Статусы
    is_default = Column(Boolean, default=False)
    is_billing = Column(Boolean, default=False)
    
    # Отношения
    user = relationship("User", back_populates="addresses")
    
    def __repr__(self):
        return f"<UserAddress(user_id={self.user_id}, city={self.city})>"
