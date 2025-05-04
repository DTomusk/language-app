from unittest.mock import MagicMock
import pytest

from backend.flashcards.application.repositories.flashcard_repository import FlashcardRepository
from backend.flashcards.application.use_cases.add_sentence_to_flashcard import AddSentenceToFlashcard
from backend.flashcards.domain.models import Flashcard, Lemma, Sentence


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
    assert mock_flashcard_repository.update_flashcard.call_args[0][0].id == flashcard_id, "The flashcard ID does not match."
    assert mock_flashcard_repository.update_flashcard.call_args[0][0].user_id == user_id, "The user ID does not match."
    assert mock_flashcard_repository.update_flashcard.call_args[0][0].sentences[0].text == sentence, "The sentence was not added correctly."

def test_add_sentence_to_flashcard_flashcard_not_found(add_sentence_to_flashcard, mock_flashcard_repository):
    # Arrange
    user_id = "user123"
    flashcard_id = "flashcard123"
    sentence = "This is a test sentence."

    # Mock the flashcard retrieval to return None
    mock_flashcard_repository.get_flashcard.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match="Flashcard not found."):
        add_sentence_to_flashcard.execute(user_id=user_id, flashcard_id=flashcard_id, sentence=sentence)

    mock_flashcard_repository.get_flashcard.assert_called_once_with(flashcard_id)
    mock_flashcard_repository.update_flashcard.assert_not_called()

def test_add_sentence_to_flashcard_flashcard_belongs_to_another_user(add_sentence_to_flashcard, mock_flashcard_repository):
    # Arrange
    user_id = "user123"
    flashcard_id = "flashcard123"
    sentence = "This is a test sentence."

    # Mock the flashcard retrieval to return a flashcard with a different user ID
    mock_flashcard_repository.get_flashcard.return_value = Flashcard(
        id=flashcard_id, user_id="another_user", lemma=Lemma("test_word")
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Flashcard not found."):
        add_sentence_to_flashcard.execute(user_id=user_id, flashcard_id=flashcard_id, sentence=sentence)

    mock_flashcard_repository.get_flashcard.assert_called_once_with(flashcard_id)
    mock_flashcard_repository.update_flashcard.assert_not_called()

def test_add_sentence_to_flashcard_duplicate_sentence(add_sentence_to_flashcard, mock_flashcard_repository):
    # Arrange
    user_id = "user123"
    flashcard_id = "flashcard123"
    sentence = "This is a test sentence."

    # Mock the flashcard retrieval to return a flashcard with the same sentence
    mock_flashcard_repository.get_flashcard.return_value = Flashcard(
        id=flashcard_id, user_id=user_id, lemma=Lemma("test_word")
    )
    mock_flashcard_repository.get_flashcard.return_value.sentences.append(Sentence(sentence))

    # Act & Assert
    with pytest.raises(ValueError, match="Sentence already exists"):
        add_sentence_to_flashcard.execute(user_id=user_id, flashcard_id=flashcard_id, sentence=sentence)

    mock_flashcard_repository.get_flashcard.assert_called_once_with(flashcard_id)
    mock_flashcard_repository.update_flashcard.assert_not_called()