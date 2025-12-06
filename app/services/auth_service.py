from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.db.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.hashing import Hasher
from app.core.jwt import JWTHandler
from app.core.security import verify_password_strength


class AuthService:
    """
    Authentication service
    Handles user registration, login, and token operations
    """
    
    @staticmethod
    def register_user(db: Session, user_data: RegisterRequest) -> dict:
        """
        Register new user
        
        Args:
            db: Database session
            user_data: User registration data (username, email, password)
            
        Returns:
            dict: User info with tokens
        """
        # Check if username already exists
        existing_username = db.query(User).filter(User.username == user_data.username.lower()).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Check if email already exists
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Verify password strength (uppercase, lowercase, digit)
        verify_password_strength(user_data.password)
        
        # Hash password
        hashed_password = Hasher.get_password_hash(user_data.password)
        
        # Create new user
        new_user = User(
            username=user_data.username.lower(),  # Store username in lowercase
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            is_active=True,  # Active by default
            is_verified=False,  # Not verified initially
            is_superuser=False  # Not admin by default
        )
        
        # Save to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Get the ID and timestamps
        
        # Generate tokens (auto-login after registration)
        access_token = JWTHandler.create_access_token(
            data={"user_id": new_user.id, "email": new_user.email}
        )
        refresh_token = JWTHandler.create_refresh_token(
            data={"user_id": new_user.id, "email": new_user.email}
        )
        
        return {
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "full_name": new_user.full_name,
                "is_verified": new_user.is_verified
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    
    @staticmethod
    def login_user(db: Session, credentials: LoginRequest) -> dict:
        """
        Login user with email and password
        
        Args:
            db: Database session
            credentials: Login credentials (email, password)
            
        Returns:
            dict: User info with tokens
        """
        # Find user by email
        user = db.query(User).filter(User.email == credentials.email).first()
        
        # Check if user exists
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not Hasher.verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive. Contact support."
            )
        
        # Generate tokens
        access_token = JWTHandler.create_access_token(
            data={"user_id": user.id, "email": user.email}
        )
        refresh_token = JWTHandler.create_refresh_token(
            data={"user_id": user.id, "email": user.email}
        )
        
        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "avatar_url": user.avatar_url,
                "is_verified": user.is_verified,
                "followers_count": user.followers_count,
                "following_count": user.following_count,
                "posts_count": user.posts_count
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> dict:
        """
        Generate new access token using refresh token
        
        Args:
            db: Database session
            refresh_token: Valid refresh token
            
        Returns:
            dict: New access token
        """
        # Decode refresh token
        payload = JWTHandler.decode_token(refresh_token)
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
        # Get user_id from payload
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Check if user still exists and is active
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Generate new access token
        new_access_token = JWTHandler.create_access_token(
            data={"user_id": user.id, "email": user.email}
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """
        Get user by ID
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User: User object
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user