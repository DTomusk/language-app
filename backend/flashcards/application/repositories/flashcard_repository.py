from abc import ABC, abstractmethod

from backend.flashcards.domain.models import Flashcard


class FlashcardRepository(ABC):
    @abstractmethod
    def get_flashcard(self, user_id: str, lemma: str) -> Flashcard:
        """Get a flashcard by user ID and word."""
        pass

    @abstractmethod
    def create_flashcard(self, flashcard: Flashcard) -> None:
        """Create a new flashcard."""
        pass