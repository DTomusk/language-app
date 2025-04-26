from fastapi import APIRouter, Depends

from backend.infrastructure.db.database import get_db
from backend.user_management.application.use_cases.login import Login
from backend.user_management.application.use_cases.register_user import RegisterUser
from backend.user_management.infrastructure.repositories.sqlite_user_repository import SqliteUserRepository
from backend.user_management.infrastructure.utilities.bcrypt_hasher import BCryptHasher
from backend.user_management.infrastructure.utilities.jwt_token_service import JWTTokenService


router = APIRouter()

def get_user_repository(db=Depends(get_db)):
    return SqliteUserRepository(session=db)

def get_bcrypt_hasher():
    return BCryptHasher()

def get_token_service():
    return JWTTokenService()

def get_register_user_use_case(user_repo=Depends(get_user_repository), hasher=Depends(get_bcrypt_hasher)):
    return RegisterUser(user_repository=user_repo, hasher=hasher)

def get_login_use_case(user_repo=Depends(get_user_repository), hasher=Depends(get_bcrypt_hasher), token_service=Depends(get_token_service)):
    return Login(user_repository=user_repo, hasher=hasher, token_service=token_service)

@router.post("/register")
async def register_user(email: str, password: str, register_user_use_case=Depends(get_register_user_use_case)):
    """Register a new user."""
    user = register_user_use_case.execute(email=email, password=password)
    return {"id": str(user.id), "email": user.email.email}

@router.post("/login")
async def login_user(email: str, password: str, login_use_case=Depends(get_login_use_case)):
    """Login a user and return a JWT token."""
    token = login_use_case.execute(email=email, password=password)
    return {"token": token}