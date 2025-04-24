
from bcrypt import checkpw, gensalt, hashpw
from backend.user_management.application.utilities.hasher import Hasher


class BCryptHasher(Hasher):
    """Hasher using bcrypt."""

    def hash(self, password: str) -> str:
        """Hash a password."""

        # Generate a salt and hash the password
        salt = gensalt()
        hashed_password = hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    def verify(self, password: str, hashed_password: str) -> bool:
        """Verify a password against a hashed password."""
        return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))