from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.auth import get_current_user
from backend.user_management.api.dependencies import get_login_use_case, get_register_user_use_case

router = APIRouter()

@router.post("/register")
async def register_user(email: str, password: str, register_user_use_case=Depends(get_register_user_use_case)):
    """Register a new user."""
    user = register_user_use_case.execute(email=email, password=password)
    return {"id": str(user.id), "email": user.email.email}

# TODO: renamed email to username, need to reconsider
@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm=Depends(), login_use_case=Depends(get_login_use_case)):
    """Login a user and return a JWT token."""
    username = form_data.username
    password = form_data.password
    token = login_use_case.execute(email=username, password=password)
    return {"access_token": token, "token_type": "Bearer"}

# This is a protected route that requires authentication.
# Currently just for testing
@router.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    """A protected route that requires authentication."""
    return {"message": "This is a protected route.", "user": current_user}