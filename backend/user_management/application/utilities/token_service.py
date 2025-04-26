from abc import ABC, abstractmethod


class TokenService(ABC):
    @abstractmethod
    def create_token(self, data: dict, expires_minutes: int) -> str:
        """Create a token for the given user ID."""
        pass

    @abstractmethod
    def verify_token(self, token: str) -> dict:
        """Verify the given token and return the payload."""
        pass