from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship

from app.db.base import BaseModel


class Role(BaseModel):
    """
    Role model - represents roles/permissions in the system
    Examples: admin, moderator, premium_user, verified_user
    """
    __tablename__ = "roles"
    
    # Role Info
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Permissions
    can_post = Column(Boolean, default=True, nullable=False)
    can_comment = Column(Boolean, default=True, nullable=False)
    can_like = Column(Boolean, default=True, nullable=False)
    can_delete_own_posts = Column(Boolean, default=True, nullable=False)
    can_delete_any_posts = Column(Boolean, default=False, nullable=False)
    can_ban_users = Column(Boolean, default=False, nullable=False)
    can_verify_users = Column(Boolean, default=False, nullable=False)
    can_manage_roles = Column(Boolean, default=False, nullable=False)
    
    # Limits
    max_posts_per_day = Column(Integer, default=100, nullable=False)
    max_followers = Column(Integer, default=10000, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships (will add after creating UserRole table)
    # users = relationship("UserRole", back_populates="role")
    
    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name})>"