from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


# Base schema with common fields
class UserBase(BaseModel):
    """
    Base user schema with common fields
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = Field(None, max_length=255)


# Schema for user creation (register)
class UserCreate(BaseModel):
    """
    Schema for creating new user (registration)
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: Optional[str] = Field(None, max_length=100)
    
    @validator('username')
    def username_alphanumeric(cls, v):
        """
        Username must be alphanumeric and underscore only
        """
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must contain only letters, numbers and underscore')
        return v.lower()
    
    @validator('password')
    def password_strength(cls, v):
        """
        Password must contain uppercase, lowercase and digit
        """
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        return v


# Schema for user update
class UserUpdate(BaseModel):
    """
    Schema for updating user profile
    All fields are optional
    """
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = Field(None, max_length=255)


# Schema for password update
class UserPasswordUpdate(BaseModel):
    """
    Schema for changing password
    """
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @validator('new_password')
    def password_strength(cls, v):
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        return v


# Schema for user response (what we return to client)
class UserResponse(BaseModel):
    """
    Schema for user data in responses
    Never includes password or sensitive data
    """
    id: int
    username: str
    email: str
    full_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    is_active: bool
    is_verified: bool
    is_superuser: bool
    followers_count: int
    following_count: int
    posts_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Allows SQLAlchemy model conversion


# Schema for public user profile (for other users to see)
class UserPublicProfile(BaseModel):
    """
    Public user profile (limited info for other users)
    """
    id: int
    username: str
    full_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    is_verified: bool
    followers_count: int
    following_count: int
    posts_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Schema for user list (minimal info)
class UserListItem(BaseModel):
    """
    Minimal user info for lists (followers, search results, etc.)
    """
    id: int
    username: str
    full_name: Optional[str]
    avatar_url: Optional[str]
    is_verified: bool
    
    class Config:
        from_attributes = True