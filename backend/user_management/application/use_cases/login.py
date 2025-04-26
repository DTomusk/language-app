from backend.user_management.application.repositories.user_repository import UserRepository
from backend.user_management.application.utilities.hasher import Hasher
from backend.user_management.application.utilities.token_service import TokenService


class Login:
    def __init__(self, user_repository: UserRepository, hasher: Hasher, token_service: TokenService):
        self.user_repository = user_repository
        self.hasher = hasher
        self.token_service = token_service

    def execute(self, email: str, password: str) -> str:
        user = self.user_repository.get_by_email(email)
        if not user or not self.hasher.verify(password, user.hashed_password):
            raise ValueError("Invalid credentials.")
        
        token = self.token_service.create_token(data={"sub": user.id}, expires_minutes=30)
        return token
        
