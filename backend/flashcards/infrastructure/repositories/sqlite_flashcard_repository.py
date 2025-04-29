from sqlalchemy.orm import Session

from backend.flashcards.application.repositories.flashcard_repository import FlashcardRepository
from backend.flashcards.domain.models import Flashcard
from backend.flashcards.infrastructure.models import FlashcardModel


class SqliteFlashcardRepository(FlashcardRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_flashcard(self, user_id: str, lemma: str) -> Flashcard:
        """Get a flashcard by user ID and word."""
        result = self.session.query(FlashcardModel).filter_by(user_id=user_id, lemma=lemma).first()
        if result:
            return Flashcard(
                id=result.id,
                lemma=result.lemma,
                user_id=result.user_id,
            )
        return None

    def create_flashcard(self, flashcard: Flashcard) -> None:
        db_flashcard = FlashcardModel(
            id=str(flashcard.id),
            lemma=flashcard.lemma.text,
            user_id=flashcard.user_id,
        )
        self.session.add(db_flashcard)
        self.session.commit()