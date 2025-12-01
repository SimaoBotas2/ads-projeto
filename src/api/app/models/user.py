from sqlalchemy import Column, BigInteger, String, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class User(Base):
    __tablename__ = "_user_"
    
    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(512), nullable=False)
    name = Column(String(512))
    password = Column(String(512), nullable=False)
    email = Column(String(512), nullable=False)
    last_login = Column(Date)
    created_at = Column(Date, nullable=False, server_default=func.now())
    
    # Relationships
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint('username', 'email', name='_user_username_email_key'),
    )
