from abc import ABC, abstractmethod

class Hasher(ABC):
    """Abstract base class for hashing """
    
    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash a password."""
        pass

    @abstractmethod
    def verify(self, password: str, hashed_password: str) -> bool:
        """Verify a password against a hashed password."""
        pass