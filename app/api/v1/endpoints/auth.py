from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import (
    LoginRequest, 
    LoginResponse, 
    RegisterRequest, 
    RegisterResponse,
    RefreshTokenRequest,
    RefreshTokenResponse
)
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register new user
    
    - Creates new user account
    - Returns user info with access and refresh tokens
    - User is automatically logged in after registration
    """
    result = AuthService.register_user(db, user_data)
    
    return RegisterResponse(
        message="User registered successfully",
        user=result["user"],
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        token_type=result["token_type"]
    )


@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login user
    
    - Authenticates user with email and password
    - Returns access and refresh tokens
    - Access token expires in 30 minutes
    - Refresh token expires in 7 days
    """
    result = AuthService.login_user(db, credentials)
    
    return LoginResponse(
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        token_type=result["token_type"],
        user=result["user"]
    )


@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token
    
    - Generates new access token using refresh token
    - Use this when access token expires (after 30 minutes)
    - Refresh token is valid for 7 days
    """
    result = AuthService.refresh_access_token(db, token_data.refresh_token)
    
    return RefreshTokenResponse(
        access_token=result["access_token"],
        token_type=result["token_type"]
    )


@router.post("/logout")
def logout():
    """
    Logout user
    
    - In JWT-based auth, logout is handled on frontend
    - Frontend should delete stored tokens
    - This endpoint is here for consistency and future features
    """
    return {
        "message": "Logged out successfully. Please delete tokens from client."
    }