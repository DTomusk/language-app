import pytest
from unittest.mock import MagicMock
from backend.user_management.application.use_cases.register_user import RegisterUser
from backend.user_management.domain.models import Email, User

@pytest.fixture
def mock_user_repository():
    """Fixture for a mocked UserRepository."""
    mock_repo = MagicMock()
    mock_repo.get_by_email.return_value = None
    mock_repo.save = MagicMock()
    return mock_repo

@pytest.fixture
def mock_hasher():
    """Fixture for a mocked Hasher."""
    mock_hasher = MagicMock()
    mock_hasher.hash.return_value = "hashed_password"
    return mock_hasher

@pytest.fixture
def register_user(mock_user_repository, mock_hasher):
    """Fixture for the RegisterUser use case."""
    return RegisterUser(user_repository=mock_user_repository, hasher=mock_hasher)

def test_register_user_success(register_user, mock_user_repository, mock_hasher):
    # Arrange
    email = "test@example.com"
    password = "securepassword"

    # Act
    user = register_user.execute(email=email, password=password)

    # Assert
    assert user.email.email == email, "User email should match the provided email"
    assert user.hashed_password is not None, "User hashed password should be set"
    mock_user_repository.get_by_email.assert_called_once_with(email)
    mock_user_repository.save.assert_called_once_with(user)
    mock_hasher.hash.assert_called_once_with(password)

def test_register_user_existing_email(register_user, mock_user_repository):
    # Arrange
    mock_user_repository.get_by_email.return_value = User(
        email=Email(email="test@example.com"), hashed_password="hashed_password"
    )
    email = "test@example.com"
    password = "securepassword"

    # Act & Assert
    with pytest.raises(ValueError, match="User already exists with this email."):
        register_user.execute(email=email, password=password)

    mock_user_repository.get_by_email.assert_called_once_with(email)
    mock_user_repository.save.assert_not_called()