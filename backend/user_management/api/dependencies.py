from fastapi import Depends

from backend.infrastructure.db.database import get_db
from backend.user_management.application.use_cases.login import Login
from backend.user_management.application.use_cases.register_user import RegisterUser
from backend.user_management.infrastructure.repositories.sqlite_user_repository import SqliteUserRepository
from backend.user_management.infrastructure.utilities.bcrypt_hasher import BCryptHasher
from backend.user_management.infrastructure.utilities.jwt_token_service import JWTTokenService


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
