from sqlalchemy import exists
from sqlalchemy.orm import Session, joinedload

from backend.flashcards.application.repositories.flashcard_repository import FlashcardRepository
from backend.flashcards.domain.models import Flashcard, Lemma, Sentence
from backend.flashcards.infrastructure.models import FlashcardModel


class SqliteFlashcardRepository(FlashcardRepository):
    def __init__(self, session: Session):
        self.session = session

    def flashcard_exists(self, user_id: str, lemma: str) -> bool:
        return self.session.query(
            exists().where(
                FlashcardModel.user_id == user_id,
                FlashcardModel.lemma == lemma
            )
        ).scalar()

    def get_flashcard(self, flashcard_id = str) -> Flashcard:
        result = (
            self.session.query(FlashcardModel)
            .options(joinedload(FlashcardModel.sentences))
            .filter_by(id=flashcard_id).first()
        )
        if result:
            return Flashcard(
                id=result.id,
                lemma=Lemma(result.lemma),
                user_id=result.user_id,
                sentences=[Sentence(sentence.text) for sentence in result.sentences],
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