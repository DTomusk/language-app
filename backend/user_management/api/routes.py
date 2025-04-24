from fastapi import APIRouter, Depends

from backend.infrastructure.db.database import SessionLocal
from backend.user_management.application.use_cases.register_user import RegisterUser
from backend.user_management.infrastructure.repositories.sqlite_user_repository import SqliteUserRepository
from backend.user_management.infrastructure.utilities.bcrypt_hasher import BCryptHasher


router = APIRouter()

# get new session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    # close session after the request is done
    finally:
        db.close()

def get_register_user_use_case(db=Depends(get_db)):
    hasher = BCryptHasher()
    user_repo = SqliteUserRepository(session=db)
    return RegisterUser(user_repository=user_repo, hasher=hasher)

@router.post("/register")
async def register_user(email: str, password: str, register_user_use_case=Depends(get_register_user_use_case)):
    """Register a new user."""
    user = register_user_use_case.execute(email=email, password=password)
    return {"id": str(user.id), "email": user.email.email}