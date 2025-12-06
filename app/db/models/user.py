from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base import BaseModel


class User(BaseModel):
    """
    User model - represents users table in database
    """
    __tablename__ = "users"
    
    # Basic Info
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile Info
    full_name = Column(String(100), nullable=True)
    bio = Column(String(500), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # Counters (for performance, we cache these)
    followers_count = Column(Integer, default=0, nullable=False)
    following_count = Column(Integer, default=0, nullable=False)
    posts_count = Column(Integer, default=0, nullable=False)
    
    # Relationships (will be added when we create other models)
    # posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    # followers = relationship("Follow", foreign_keys="Follow.following_id", back_populates="following")
    # following = relationship("Follow", foreign_keys="Follow.follower_id", back_populates="follower")
    # likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    # comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"