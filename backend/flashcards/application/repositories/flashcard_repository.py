from abc import ABC, abstractmethod

from backend.flashcards.domain.models import Flashcard


class FlashcardRepository(ABC):
    @abstractmethod
    def flashcard_exists(self, user_id: str, lemma: str) -> bool:
        """Check if a flashcard exists for the given user and lemma."""
        pass

    @abstractmethod
    def get_flashcard(self, flashcard_id: str) -> Flashcard:
        """Get a flashcard by ID."""
        pass

    @abstractmethod
    def create_flashcard(self, flashcard: Flashcard) -> None:
        """Create a new flashcard."""
        pass