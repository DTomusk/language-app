from abc import ABC, abstractmethod
from typing import Optional

from backend.user_management.domain.models import User

class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        """Save a user."""
        pass