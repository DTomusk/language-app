from unittest.mock import MagicMock
import pytest

from backend.flashcards.application.repositories.flashcard_repository import FlashcardRepository
from backend.flashcards.application.use_cases.add_sentence_to_flashcard import AddSentenceToFlashcard
from backend.flashcards.domain.models import Flashcard, Lemma


@pytest.fixture
def mock_flashcard_repository() -> FlashcardRepository:
    """Fixture for a mocked FlashcardRepository."""
    mock_repo = MagicMock()
    mock_repo.flashcard_exists.return_value = None
    mock_repo.create_flashcard = MagicMock()
    return mock_repo

@pytest.fixture
def add_sentence_to_flashcard(mock_flashcard_repository) -> AddSentenceToFlashcard:
    """Fixture for the AddSentenceToFlashcard use case."""
    return AddSentenceToFlashcard(flashcard_repository=mock_flashcard_repository)

def test_add_sentence_to_flashcard_success(add_sentence_to_flashcard, mock_flashcard_repository):
    # Arrange
    user_id = "user123"
    flashcard_id = "flashcard123"
    sentence = "This is a test sentence."

    # Mock the flashcard retrieval
    mock_flashcard_repository.get_flashcard.return_value = Flashcard(
        id=flashcard_id, user_id=user_id, lemma=Lemma("test_word")
    )

    # Act
    add_sentence_to_flashcard.execute(user_id=user_id, flashcard_id=flashcard_id, sentence=sentence)

    # Assert
    mock_flashcard_repository.get_flashcard.assert_called_once_with(flashcard_id)
    mock_flashcard_repository.update_flashcard.assert_called_once()