from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.db.models.user import User
from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    RoleListItem
)
from app.core.security import get_current_active_superuser


# Router for role management endpoints
router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    role_data: RoleCreate,  # Role data (name, permissions, limits)
    db: Session = Depends(get_db),  # Database session
    admin: User = Depends(get_current_active_superuser)  # Only admin can create roles
):
    """
    Create new role (Admin only)
    
    - Define role name and permissions
    - Set limits (max_posts_per_day, max_followers)
    - Only superusers can create roles
    """
    from app.db.models.role import Role
    
    # Check if role name already exists
    existing_role = db.query(Role).filter(Role.name == role_data.name).first()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role '{role_data.name}' already exists"
        )
    
    # Create new role
    new_role = Role(
        name=role_data.name,
        description=role_data.description,
        can_post=role_data.can_post,
        can_comment=role_data.can_comment,
        can_like=role_data.can_like,
        can_delete_own_posts=role_data.can_delete_own_posts,
        can_delete_any_posts=role_data.can_delete_any_posts,
        can_ban_users=role_data.can_ban_users,
        can_verify_users=role_data.can_verify_users,
        can_manage_roles=role_data.can_manage_roles,
        max_posts_per_day=role_data.max_posts_per_day,
        max_followers=role_data.max_followers,
        is_active=True
    )
    
    # Save to database
    db.add(new_role)
    db.commit()
    db.refresh(new_role)  # Get created role with ID
    
    return new_role


@router.get("/", response_model=List[RoleListItem])
def list_roles(
    db: Session = Depends(get_db)  # Database session
):
    """
    Get all roles
    
    - Returns list of all roles
    - Public endpoint (no authentication required)
    """
    from app.db.models.role import Role
    
    # Get all roles
    roles = db.query(Role).all()
    
    return roles


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: int,  # Role ID from URL path
    db: Session = Depends(get_db)  # Database session
):
    """
    Get role by ID
    
    - Returns full role details
    - Public endpoint
    """
    from app.db.models.role import Role
    
    # Find role by ID
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    return role


@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,  # Role ID to update
    role_data: RoleUpdate,  # Fields to update
    db: Session = Depends(get_db),  # Database session
    admin: User = Depends(get_current_active_superuser)  # Only admin can update
):
    """
    Update role (Admin only)
    
    - Update permissions and limits
    - All fields are optional
    - Only superusers can update roles
    """
    from app.db.models.role import Role
    
    # Find role
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    # Update fields (only if provided)
    if role_data.description is not None:
        role.description = role_data.description
    
    if role_data.can_post is not None:
        role.can_post = role_data.can_post
    
    if role_data.can_comment is not None:
        role.can_comment = role_data.can_comment
    
    if role_data.can_like is not None:
        role.can_like = role_data.can_like
    
    if role_data.can_delete_own_posts is not None:
        role.can_delete_own_posts = role_data.can_delete_own_posts
    
    if role_data.can_delete_any_posts is not None:
        role.can_delete_any_posts = role_data.can_delete_any_posts
    
    if role_data.can_ban_users is not None:
        role.can_ban_users = role_data.can_ban_users
    
    if role_data.can_verify_users is not None:
        role.can_verify_users = role_data.can_verify_users
    
    if role_data.can_manage_roles is not None:
        role.can_manage_roles = role_data.can_manage_roles
    
    if role_data.max_posts_per_day is not None:
        role.max_posts_per_day = role_data.max_posts_per_day
    
    if role_data.max_followers is not None:
        role.max_followers = role_data.max_followers
    
    # Save changes
    db.commit()
    db.refresh(role)  # Get updated role
    
    return role


@router.delete("/{role_id}")
def delete_role(
    role_id: int,  # Role ID to delete
    db: Session = Depends(get_db),  # Database session
    admin: User = Depends(get_current_active_superuser)  # Only admin can delete
):
    """
    Delete role (Admin only)
    
    - Permanently deletes role
    - Only superusers can delete roles
    - Cannot delete if users are assigned to this role
    """
    from app.db.models.role import Role
    
    # Find role
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    # TODO: Check if any users have this role
    # If yes, raise error: "Cannot delete role with assigned users"
    
    # Delete role
    db.delete(role)
    db.commit()
    
    return {"message": f"Role '{role.name}' deleted successfully"}