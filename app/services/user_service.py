from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional, List

from app.db.models.user import User
from app.schemas.user import UserUpdate, UserPasswordUpdate
from app.core.hashing import Hasher
from app.core.security import verify_password_strength


class UserService:
    """
    User service
    Handles user profile operations (CRUD)
    """
    
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
    
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """
        Get user by username
        
        Args:
            db: Database session
            username: Username
            
        Returns:
            User: User object
        """
        user = db.query(User).filter(User.username == username.lower()).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
    
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user by email (internal use)
        
        Args:
            db: Database session
            email: Email address
            
        Returns:
            User or None
        """
        return db.query(User).filter(User.email == email).first()
    
    
    @staticmethod
    def update_user_profile(db: Session, user_id: int, update_data: UserUpdate) -> User:
        """
        Update user profile
        
        Args:
            db: Database session
            user_id: User ID
            update_data: Fields to update (full_name, bio, avatar_url)
            
        Returns:
            User: Updated user object
        """
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields (only if provided)
        if update_data.full_name is not None:
            user.full_name = update_data.full_name
        
        if update_data.bio is not None:
            user.bio = update_data.bio
        
        if update_data.avatar_url is not None:
            user.avatar_url = update_data.avatar_url
        
        # Save changes
        db.commit()
        db.refresh(user)  # Get updated data
        
        return user
    
    
    @staticmethod
    def change_password(db: Session, user_id: int, password_data: UserPasswordUpdate) -> dict:
        """
        Change user password
        
        Args:
            db: Database session
            user_id: User ID
            password_data: Old and new password
            
        Returns:
            dict: Success message
        """
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify old password
        if not Hasher.verify_password(password_data.old_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is incorrect"
            )
        
        # Verify new password strength
        verify_password_strength(password_data.new_password)
        
        # Hash new password
        user.hashed_password = Hasher.get_password_hash(password_data.new_password)
        
        # Save changes
        db.commit()
        
        return {"message": "Password updated successfully"}
    
    
    @staticmethod
    def deactivate_user(db: Session, user_id: int) -> dict:
        """
        Deactivate user account
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            dict: Success message
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Deactivate account
        user.is_active = False
        
        db.commit()
        
        return {"message": "Account deactivated successfully"}
    
    
    @staticmethod
    def search_users(db: Session, query: str, limit: int = 20) -> List[User]:
        """
        Search users by username or full name
        
        Args:
            db: Database session
            query: Search query
            limit: Maximum results (default 20)
            
        Returns:
            List[User]: List of matching users
        """
        # Search in username and full_name
        users = db.query(User).filter(
            (User.username.ilike(f"%{query}%")) |  # ilike = case-insensitive LIKE
            (User.full_name.ilike(f"%{query}%"))
        ).filter(
            User.is_active == True  # Only active users
        ).limit(limit).all()
        
        return users
    
    
    @staticmethod
    def get_user_stats(db: Session, user_id: int) -> dict:
        """
        Get user statistics
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            dict: User stats (followers, following, posts)
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {
            "followers_count": user.followers_count,
            "following_count": user.following_count,
            "posts_count": user.posts_count
        }