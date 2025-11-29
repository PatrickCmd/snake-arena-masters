"""
Authentication router for user login, signup, and session management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.schemas import (
    AuthResponse,
    SignupRequest,
    Token,
    User,
)
from app.services.auth_service import auth_service
from app.utils.security import create_access_token, get_current_user_id

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    User login endpoint.

    Authenticate with email and password to receive a JWT token.
    """
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.id})
    return Token(access_token=access_token)


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest):
    """
    User registration endpoint.

    Create a new user account.
    """
    try:
        user = auth_service.create_user(
            email=request.email, username=request.username, password=request.password
        )
        return AuthResponse(success=True, user=user)
    except ValueError as e:
        return AuthResponse(success=False, error=str(e))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(current_user_id: str = Depends(get_current_user_id)):
    """
    User logout endpoint.

    End the current user session (client should discard the token).
    """
    # In a stateless JWT system, logout is handled client-side
    # This endpoint exists for API completeness
    return None


@router.get("/me", response_model=User)
async def get_current_user(current_user_id: str = Depends(get_current_user_id)):
    """
    Get current authenticated user information.
    """
    user = auth_service.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
