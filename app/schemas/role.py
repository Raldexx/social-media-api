from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RoleBase(BaseModel):
    """Base role schema"""
    
    name: str = Field(..., min_length=2, max_length=50)  # Role name (e.g., "admin", "moderator")
    description: Optional[str] = Field(None, max_length=500)  # Role description


class RoleCreate(BaseModel):
    """Schema for creating new role"""
    
    name: str = Field(..., min_length=2, max_length=50)  # Unique role name
    description: Optional[str] = Field(None, max_length=500)  # What this role does
    
    # Permissions
    can_post: bool = True  # Can create posts
    can_comment: bool = True  # Can write comments
    can_like: bool = True  # Can like posts
    can_delete_own_posts: bool = True  # Can delete own posts
    can_delete_any_posts: bool = False  # Can delete anyone's posts (moderator)
    can_ban_users: bool = False  # Can ban users (admin)
    can_verify_users: bool = False  # Can verify users (admin)
    can_manage_roles: bool = False  # Can create/edit roles (super admin)
    
    # Limits
    max_posts_per_day: int = Field(default=100, ge=0)  # Daily post limit (ge = greater than or equal)
    max_followers: int = Field(default=10000, ge=0)  # Maximum followers allowed


class RoleUpdate(BaseModel):
    """Schema for updating role"""
    
    description: Optional[str] = Field(None, max_length=500)  # Update description
    
    # All permissions are optional (update only what you want)
    can_post: Optional[bool] = None
    can_comment: Optional[bool] = None
    can_like: Optional[bool] = None
    can_delete_own_posts: Optional[bool] = None
    can_delete_any_posts: Optional[bool] = None
    can_ban_users: Optional[bool] = None
    can_verify_users: Optional[bool] = None
    can_manage_roles: Optional[bool] = None
    
    # Optional limit updates
    max_posts_per_day: Optional[int] = Field(None, ge=0)
    max_followers: Optional[int] = Field(None, ge=0)


class RoleResponse(BaseModel):
    """Schema for role data in responses"""
    
    id: int  # Role ID
    name: str  # Role name
    description: Optional[str]  # Role description
    
    # Permissions
    can_post: bool
    can_comment: bool
    can_like: bool
    can_delete_own_posts: bool
    can_delete_any_posts: bool
    can_ban_users: bool
    can_verify_users: bool
    can_manage_roles: bool
    
    # Limits
    max_posts_per_day: int
    max_followers: int
    
    # Status
    is_active: bool  # Is this role active?
    
    # Timestamps
    created_at: datetime  # When role was created
    updated_at: datetime  # Last update time
    
    class Config:
        from_attributes = True  # Convert SQLAlchemy model to Pydantic


class RoleListItem(BaseModel):
    """Minimal role info for lists"""
    
    id: int  # Role ID
    name: str  # Role name
    description: Optional[str]  # Short description
    is_active: bool  # Active status
    
    class Config:
        from_attributes = True