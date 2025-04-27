from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from backend.user_management.application.repositories.user_repository import UserRepository
from backend.user_management.application.use_cases.login import Login
from backend.user_management.application.utilities.hasher import Hasher
from backend.user_management.application.utilities.token_service import TokenService
from backend.user_management.domain.models import Email, User


@pytest.fixture
def mock_user_repository() -> UserRepository:
    """Fixture for a mocked UserRepository."""
    mock_repo = MagicMock()
    mock_repo.get_by_email.return_value = None
    mock_repo.save = MagicMock()
    return mock_repo

@pytest.fixture
def mock_hasher() -> Hasher:
    """Fixture for a mocked Hasher."""
    mock_hasher = MagicMock()
    mock_hasher.hash.return_value = "hashed_password"
    return mock_hasher

@pytest.fixture
def mock_token_service() -> TokenService:
    """Fixture for a mocked TokenService."""
    mock_token_service = MagicMock()
    mock_token_service.create_token.return_value = "mocked_token"
    return mock_token_service

@pytest.fixture
def login(mock_user_repository, mock_hasher, mock_token_service) -> Login:
    """Fixture for the Login use case."""
    return Login(user_repository=mock_user_repository, hasher=mock_hasher, token_service=mock_token_service)

def test_login_success(login, mock_user_repository, mock_hasher, mock_token_service):
    # Arrange
    mock_user_repository.get_by_email.return_value = User(
        id=uuid4(), email=Email(email="test@example.com"), hashed_password="hashed_password"
    )
    email = "test@example.com"
    password = "securepassword"

    # Act
    token = login.execute(email=email, password=password)

    # Assert
    assert token == "mocked_token", "Token should match the mocked token"
    mock_user_repository.get_by_email.assert_called_once_with(email)
    mock_hasher.verify.assert_called_once_with(password, "hashed_password")
    mock_token_service.create_token.assert_called_once_with(data={"sub": mock_user_repository.get_by_email.return_value.id}, expires_minutes=30)

def test_login_invalid_email(login):
    # Arrange
    email = "test@example.com"
    password = "securepassword"

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid credentials."):
        login.execute(email=email, password=password)

def test_login_invalid_password(login, mock_user_repository, mock_hasher):
    # Arrange
    mock_user_repository.get_by_email.return_value = User(
        id=uuid4(), email=Email(email="test@example.com"), hashed_password="hashed_password"
    )
    mock_hasher.verify.return_value = False
    email = "test@example.com"
    password = "securepassword"

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid credentials."):
        login.execute(email=email, password=password)