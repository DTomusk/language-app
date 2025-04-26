from fastapi import APIRouter, Depends

from backend.infrastructure.db.database import get_db
from backend.user_management.application.use_cases.register_user import RegisterUser
from backend.user_management.infrastructure.repositories.sqlite_user_repository import SqliteUserRepository
from backend.user_management.infrastructure.utilities.bcrypt_hasher import BCryptHasher


router = APIRouter()

def get_user_repository(db=Depends(get_db)):
    return SqliteUserRepository(session=db)

def get_bcrypt_hasher():
    return BCryptHasher()

def get_register_user_use_case(user_repo=Depends(get_user_repository), hasher=Depends(get_bcrypt_hasher)):
    return RegisterUser(user_repository=user_repo, hasher=hasher)

@router.post("/register")
async def register_user(email: str, password: str, register_user_use_case=Depends(get_register_user_use_case)):
    """Register a new user."""
    user = register_user_use_case.execute(email=email, password=password)
    return {"id": str(user.id), "email": user.email.email}