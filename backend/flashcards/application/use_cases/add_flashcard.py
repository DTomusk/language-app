from backend.flashcards.application.repositories.flashcard_repository import FlashcardRepository
from backend.flashcards.domain.models import Flashcard, Lemma


class AddFlashcard:
    def __init__(self, flashcard_repository: FlashcardRepository):
        self.flashcard_repository = flashcard_repository

    def execute(self, user_id: str, lemma: str):
        # Check if the flashcard already exists
        flashcard_exists = self.flashcard_repository.flashcard_exists(user_id, lemma=lemma)
        if flashcard_exists:
            raise ValueError("Flashcard already exists.")

        # Create a new flashcard
        flashcard = Flashcard(user_id=user_id, lemma=Lemma(lemma))
        self.flashcard_repository.create_flashcard(flashcard)
        