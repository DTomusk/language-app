from backend.user_management.application.repositories.user_repository import UserRepository
from backend.user_management.application.utilities.hasher import Hasher
from backend.user_management.domain.models import Email, User


class RegisterUser:
    def __init__(self, user_repository: UserRepository, hasher: Hasher):
        self.user_repository = user_repository
        self.hasher = hasher

    def execute(self, email: str, password: str) -> User:
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("User already exists with this email.")
        email = Email(email=email)
        hashed_password = self.hasher.hash(password)
        user = User(email=email, hashed_password=hashed_password)
        self.user_repository.save(user)
        return user
