from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.db.models.user import User
from app.schemas.user import (
    UserResponse,
    UserPublicProfile,
    UserUpdate,
    UserPasswordUpdate,
    UserListItem
)
from app.services.user_service import UserService
from app.core.security import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's profile
    
    - Returns full profile info (including email)
    - Requires authentication (access token)
    """
    return current_user


@router.put("/me", response_model=UserResponse)
def update_my_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile
    
    - Update full_name, bio, avatar_url
    - All fields are optional
    - Only updates provided fields
    """
    updated_user = UserService.update_user_profile(
        db=db,
        user_id=current_user.id,
        update_data=update_data
    )
    
    return updated_user


@router.put("/me/password")
def change_my_password(
    password_data: UserPasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change current user's password
    
    - Requires old password for verification
    - New password must meet strength requirements
    """
    result = UserService.change_password(
        db=db,
        user_id=current_user.id,
        password_data=password_data
    )
    
    return result


@router.delete("/me")
def deactivate_my_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deactivate current user's account
    
    - Account will be deactivated (not deleted)
    - User cannot login after deactivation
    - Contact support to reactivate
    """
    result = UserService.deactivate_user(db=db, user_id=current_user.id)
    
    return result


@router.get("/me/stats")
def get_my_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's statistics
    
    - Returns followers, following, posts count
    """
    stats = UserService.get_user_stats(db=db, user_id=current_user.id)
    
    return stats


@router.get("/search", response_model=List[UserListItem])
def search_users(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Max results"),
    db: Session = Depends(get_db)
):
    """
    Search users by username or full name
    
    - Case-insensitive search
    - Returns max 100 results
    - Only returns active users
    """
    users = UserService.search_users(db=db, query=q, limit=limit)
    
    return users


@router.get("/{username}", response_model=UserPublicProfile)
def get_user_profile(
    username: str,
    db: Session = Depends(get_db)
):
    """
    Get user's public profile by username
    
    - Returns public info only (no email)
    - Anyone can view (no authentication required)
    """
    user = UserService.get_user_by_username(db=db, username=username)
    
    return user


@router.get("/{user_id}/stats")
def get_user_stats(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get user's statistics
    
    - Returns followers, following, posts count
    - Public endpoint (no authentication required)
    """
    stats = UserService.get_user_stats(db=db, user_id=user_id)
    
    return stats