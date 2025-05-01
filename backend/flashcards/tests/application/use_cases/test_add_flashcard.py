from unittest.mock import MagicMock
import pytest

from backend.flashcards.application.repositories.flashcard_repository import FlashcardRepository
from backend.flashcards.application.use_cases.add_flashcard import AddFlashcard
from backend.flashcards.domain.models import Flashcard, Lemma


@pytest.fixture
def mock_flashcard_repository() -> FlashcardRepository:
    """Fixture for a mocked FlashcardRepository."""
    mock_repo = MagicMock()
    mock_repo.flashcard_exists.return_value = None
    mock_repo.create_flashcard = MagicMock()
    return mock_repo

@pytest.fixture
def add_flashcard(mock_flashcard_repository) -> AddFlashcard:
    """Fixture for the AddFlashcard use case."""
    return AddFlashcard(flashcard_repository=mock_flashcard_repository)


def test_add_flashcard_success(add_flashcard, mock_flashcard_repository):
    # Arrange
    user_id = "user123"
    lemma = "test_word"

    # Act
    add_flashcard.execute(user_id=user_id, lemma=lemma)

    # Assert
    mock_flashcard_repository.flashcard_exists.assert_called_once_with(user_id, lemma=lemma)
    expected_flashcard = Flashcard(user_id=user_id, lemma=Lemma(lemma))
    actual_flashcard = mock_flashcard_repository.create_flashcard.call_args[0][0]
    assert actual_flashcard == expected_flashcard, f"Expected {expected_flashcard}, but got {actual_flashcard}"

def test_add_flashcard_existing_flashcard(add_flashcard, mock_flashcard_repository):
    # Arrange
    user_id = "user123"
    lemma = "test_word"
    mock_flashcard_repository.flashcard_exists.return_value = Flashcard(
        user_id=user_id, lemma=lemma
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Flashcard already exists."):
        add_flashcard.execute(user_id=user_id, lemma=lemma)

    mock_flashcard_repository.flashcard_exists.assert_called_once_with(user_id, lemma=lemma)
    mock_flashcard_repository.create_flashcard.assert_not_called()