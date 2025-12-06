from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginRequest(BaseModel):
    """Schema for login request"""
    
    email: EmailStr  # User's email address
    password: str  # Plain text password


class LoginResponse(BaseModel):
    """Schema for login response"""
    
    access_token: str  # JWT token (30 min expiry)
    refresh_token: str  # Refresh token (7 days expiry)
    token_type: str = "bearer"  # Always "bearer" for JWT
    user: dict  # User info (id, username, email)


class RegisterRequest(BaseModel):
    """Schema for user registration"""
    
    username: str = Field(..., min_length=3, max_length=50)  # 3-50 chars
    email: EmailStr  # Valid email format required
    password: str = Field(..., min_length=8, max_length=100)  # Min 8 chars
    full_name: Optional[str] = Field(None, max_length=100)  # Optional field


class RegisterResponse(BaseModel):
    """Schema for registration response"""
    
    message: str  # Success message
    user: dict  # Created user info
    access_token: str  # Auto-login after registration
    refresh_token: str  # Refresh token
    token_type: str = "bearer"  # Token type


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""
    
    refresh_token: str  # Refresh token from login/register


class RefreshTokenResponse(BaseModel):
    """Schema for refresh token response"""
    
    access_token: str  # New access token
    token_type: str = "bearer"  # Token type


class TokenData(BaseModel):
    """Internal schema for decoded token data"""
    
    user_id: Optional[int] = None  # User ID from JWT payload
    email: Optional[str] = None  # User email from JWT payload