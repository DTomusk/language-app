from backend.flashcards.application.repositories.flashcard_repository import FlashcardRepository


class AddSentenceToFlashcard:
    def __init__(self, flashcard_repository: FlashcardRepository):
        self.flashcard_repository = flashcard_repository

    def execute(self, user_id: str, flashcard_id: str, sentence: str):
        flashcard = self.flashcard_repository.get_flashcard(flashcard_id)
        if not flashcard or flashcard.user_id != user_id:
            raise ValueError("Flashcard not found.")
        flashcard.add_sentence(sentence)
        self.flashcard_repository.update_flashcard(flashcard)
