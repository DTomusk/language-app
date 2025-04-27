from backend.flashcards.application.repositories.flashcard_repository import FlashcardRepository
from backend.flashcards.domain.models import Flashcard, Lemma


class AddFlashcard:
    def __init__(self, flashcard_repository: FlashcardRepository):
        self.flashcard_repository = flashcard_repository

    def execute(self, user_id: str, lemma: str):
        # Check if the flashcard already exists
        existing_flashcard = self.flashcard_repository.get_flashcard(user_id, lemma=lemma)
        if existing_flashcard:
            raise ValueError("Flashcard already exists.")

        # Create a new flashcard
        flashcard = Flashcard(user_id=user_id, lemma=Lemma(lemma))
        self.flashcard_repository.create_flashcard(flashcard)
        